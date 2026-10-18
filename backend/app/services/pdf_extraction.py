import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import pymupdf  # PyMuPDF

logger = logging.getLogger(__name__)

class PDFExtractionService:
    @staticmethod
    def extract_pdf(file_path: Path) -> Dict[str, Any]:
        """
        Extracts structured text, page numbers, sections, and metadata from a PDF.
        Handles large documents safely, detects scanned or empty documents,
        and accurately extracts title, authors, journal, study type, and page count.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found at: {file_path}")

        try:
            doc = pymupdf.open(str(file_path))
        except Exception as e:
            raise ValueError(f"Corrupted or invalid PDF file: {str(e)}")

        if doc.is_encrypted:
            raise PermissionError("This PDF file is password protected or encrypted. Please provide an unencrypted PDF.")

        page_count = len(doc)
        if page_count == 0:
            raise ValueError("The uploaded PDF contains 0 pages.")

        # Safe extraction limit for very large documents (e.g. 500+ page books/guidelines)
        MAX_PAGES_TO_EXTRACT = 50
        pages_to_process = min(page_count, MAX_PAGES_TO_EXTRACT)

        pages_data: List[Dict[str, Any]] = []
        total_text_length = 0
        all_text = ""

        # Metadata from PDF properties
        doc_meta = doc.metadata or {}
        raw_pdf_title = doc_meta.get("title", "").strip() or None
        raw_pdf_author = doc_meta.get("author", "").strip() or None

        # Check if metadata title looks like an artifact/filename
        clean_meta_title = None
        if raw_pdf_title:
            lower_t = raw_pdf_title.lower()
            if not (lower_t.endswith(".pdf") or "untitled" in lower_t or "microsoft word" in lower_t or "article" == lower_t):
                clean_meta_title = raw_pdf_title

        # Page-by-page extraction
        for page_idx in range(pages_to_process):
            page = doc[page_idx]
            page_num = page_idx + 1
            page_text = page.get_text("text").strip()
            # De-hyphenate line-broken words (e.g. inter-\nvention -> intervention)
            page_text = re.sub(r"(\w+)-\s*\n\s*(\w+)", r"\1\2", page_text)
            total_text_length += len(page_text)
            all_text += f"\n--- [Page {page_num}] ---\n" + page_text

            # Extract text blocks
            blocks = page.get_text("blocks")
            detected_sections = []

            for b in blocks:
                block_text = b[4].strip()
                if re.match(r"^(Abstract|Introduction|Methods|Methodology|Results|Discussion|Conclusion|Limitations|References)\b", block_text, re.IGNORECASE):
                    detected_sections.append(block_text.split("\n")[0])

            pages_data.append({
                "page_number": page_num,
                "text": page_text,
                "detected_sections": detected_sections,
                "char_count": len(page_text)
            })

        doc.close()

        # Check for scanned PDF with zero or negligible text
        if total_text_length < 150 and page_count > 0:
            raise ValueError(
                "This PDF appears to be a scanned image or empty with no embedded digital text. "
                "Steer Studio requires digital scientific text for evidence extraction."
            )

        first_page_text = pages_data[0]["text"] if pages_data else ""
        first_page_lines = [l.strip() for l in first_page_text.split("\n") if l.strip()]

        # DOI match
        doi_match = re.search(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", all_text)
        
        # Year match
        year_match = re.search(r"\b(19\d\d|20[0-2]\d)\b", first_page_text)

        # Journal detection
        detected_journal = None
        journal_patterns = [
            (r"PLOS\s*ONE", "PLOS ONE"),
            (r"European\s+Journal\s+of\s+Applied\s+Physiology", "European Journal of Applied Physiology"),
            (r"Indian\s+Journal\s+of\s+Clinical\s+Metabolic\s+Medicine", "Indian Journal of Clinical Metabolic Medicine"),
            (r"Diabetes\s+Care", "Diabetes Care"),
            (r"The\s+Lancet", "The Lancet"),
            (r"BMJ\s+Open", "BMJ Open"),
            (r"Frontiers\s+in\s+Endocrinology", "Frontiers in Endocrinology"),
            (r"Cell\s+Metabolism", "Cell Metabolism"),
            (r"Nature\s+Metabolism", "Nature Metabolism"),
            (r"Journal\s+of\s+[A-Za-z\s]+", None)
        ]
        for pat, jname in journal_patterns:
            m = re.search(pat, all_text[:5000], re.IGNORECASE)
            if m:
                detected_journal = jname or m.group(0).strip()
                break

        # Study type detection
        detected_study_type = "Clinical Investigation"
        study_patterns = [
            (r"systematic\s+review(\s+and\s+meta-analysis)?", "Systematic Review"),
            (r"meta-analysis", "Meta-Analysis"),
            (r"randomized\s+crossover(\s+clinical)?\s+trial", "Randomized Crossover Clinical Trial"),
            (r"crossover\s+(design|trial|study)", "Randomized Crossover Trial"),
            (r"randomized\s+controlled\s+trial", "Randomized Controlled Trial"),
            (r"prospective\s+cohort\s+study", "Prospective Cohort Study"),
            (r"cross-sectional\s+study", "Cross-Sectional Study"),
            (r"observational\s+study", "Observational Cohort Study")
        ]
        for pat, stype in study_patterns:
            if re.search(pat, all_text[:8000], re.IGNORECASE):
                detected_study_type = stype
                break

        # Abstract extraction
        abstract = ""
        # Look for Abstract and stop at Introduction, Keywords, Author Summary, or Page break
        abs_match = re.search(r"Abstract[:\s\n]+(.*?)(?=\n\s*(?:(?:1[\.\s]+)?Introduction\b|Key\s*words\b|Keywords\b|Author\s+[Ss]ummary\b|\n--- \[Page [3-9]\d*\]|\n\n\n\n+))", all_text, re.DOTALL | re.IGNORECASE)
        if abs_match:
            abstract = abs_match.group(1).strip()
            # Clean up extra spaces
            abstract = re.sub(r"[ \t]+", " ", abstract)
            if len(abstract) > 3000:
                abstract = abstract[:3000] + "..."
        elif "abstract" in all_text.lower():
            fb_match = re.search(r"Abstract[:\s\n]+(.*?)(?=\n--- \[Page|\Z)", all_text, re.DOTALL | re.IGNORECASE)
            if fb_match:
                candidate = fb_match.group(1).strip()
                abstract = candidate[:2500].strip()

        # Title Extraction
        title = clean_meta_title
        if not title:
            # Look for title on page 1 before Abstract or Authors
            candidate_lines = []
            for line in first_page_lines:
                clean_l = line.strip()
                # Skip journal metadata headers, DOI lines, or license lines
                if re.match(r"^(CLINICAL|RESEARCH|ORIGINAL|REVIEW|OPEN ACCESS|http|doi:|vol|pp\.)", clean_l, re.IGNORECASE):
                    continue
                if "doi:" in clean_l.lower() or "journal of" in clean_l.lower() or "issn" in clean_l.lower():
                    continue
                if re.match(r"^(Authors|Author|Affiliations|Abstract|Introduction|Keywords|Background)\b", clean_l, re.IGNORECASE):
                    break
                if len(clean_l) > 10:
                    candidate_lines.append(clean_l)
                    if len(candidate_lines) >= 3:
                        break

            if candidate_lines:
                title = " ".join(candidate_lines[:2]).strip()
            else:
                title = file_path.stem.replace("_", " ").replace("-", " ").title()

        # Clean title of odd punctuation or excess spaces
        title = re.sub(r"\s+", " ", title).strip()

        # Authors Extraction
        authors = []
        if raw_pdf_author and len(raw_pdf_author) > 3 and not raw_pdf_author.lower().endswith(".pdf"):
            authors = [raw_pdf_author]
        else:
            # Search for author line after title before abstract
            in_authors = False
            for line in first_page_lines:
                clean_l = line.strip()
                if re.match(r"^Authors?:", clean_l, re.IGNORECASE):
                    in_authors = True
                    continue
                if in_authors:
                    if re.match(r"^(Affiliations|Abstract|Background|Keywords)", clean_l, re.IGNORECASE):
                        break
                    # Clean out degree markers or footnote symbols
                    cleaned_author = re.sub(r"[\*\d]+", "", clean_l).strip()
                    if cleaned_author and len(cleaned_author) > 3:
                        authors.append(cleaned_author)
                elif ("@" in clean_l or "1*" in clean_l) and len(authors) == 0:
                    authors = [re.sub(r"[\d\*]+", "", clean_l).strip()]


        return {
            "title": title,
            "authors": authors,
            "year": int(year_match.group(1)) if year_match else None,
            "doi": doi_match.group(0) if doi_match else None,
            "journal": detected_journal or "Peer-Reviewed Scientific Journal",
            "study_type": detected_study_type,
            "abstract": abstract if abstract else None,
            "page_count": page_count,
            "pages_analyzed": len(pages_data),
            "pages": pages_data,
            "full_text": all_text
        }
