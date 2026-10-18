import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

def is_sample_walk_paper(paper_title: str) -> bool:
    t = (paper_title or "").lower()
    return "postprandial glycemic excursions and 10-minute post-meal walking in south asian adults with prediabetes" in t

def _build_dynamic_paper_storyboard(
    visual_style: str,
    language: str,
    claims: Optional[List[Dict[str, Any]]],
    paper_title: str,
    voice_name: str,
    visual_theme: str = "warm_editorial"
) -> Dict[str, Any]:
    clm_ids = [c.get("claim_id", f"CLM-{i+1:03d}") for i, c in enumerate(claims)] if claims else ["CLM-001", "CLM-002", "CLM-003"]
    primary_clm = clm_ids[0] if clm_ids else "CLM-001"
    c1_obj = claims[0] if claims else {}
    c2_obj = claims[1] if claims and len(claims) > 1 else c1_obj
    c3_obj = claims[2] if claims and len(claims) > 2 else c1_obj

    c1 = c1_obj.get("claim_text") or f"Clinical evidence demonstrates significant metabolic benefits in {paper_title[:50]}."
    c2 = c2_obj.get("claim_text") or "Targeted lifestyle interventions optimize metabolic regulation and insulin sensitivity."
    c3 = c3_obj.get("claim_text") or "Daily adherence and timing are essential for sustained metabolic vitality."
    sample_size = c1_obj.get("sample_size") or "Clinical Cohort"
    short_title = paper_title[:55]

    if visual_style == "inside_your_body":
        scenes = [
            {
                "scene_number": 1,
                "duration_seconds": 10.0,
                "visual_cue": "Red blood cell character smiling in flowing arterial bloodstream delivering oxygen molecules",
                "on_screen_text": "Finding 1: Circulation & Uptake",
                "narration": f"Finding one: Clinical research on {short_title[:35]} demonstrates that: {c1}",
                "subtitle_text": f"Finding 1: {c1[:60]}...",
                "visual_style": "inside_your_body",
                "visual_theme": visual_theme,
                "animation_action": "inside_your_body",
                "organ_character": "red_blood_cell",
                "character_name": "Red Blood Cell",
                "claim_ids": [primary_clm]
            },
            {
                "scene_number": 2,
                "duration_seconds": 10.5,
                "visual_cue": "Expressive Brain character firing gentle synaptic sparks in glowing violet neural space",
                "on_screen_text": "Finding 2: Neural Signalling",
                "narration": f"Finding two: Metabolic cellular pathways respond directly: {c2}",
                "subtitle_text": f"Finding 2: {c2[:60]}...",
                "visual_style": "inside_your_body",
                "visual_theme": visual_theme,
                "animation_action": "inside_your_body",
                "organ_character": "brain",
                "character_name": "Brain",
                "claim_ids": [clm_ids[1] if len(clm_ids) > 1 else primary_clm]
            },
            {
                "scene_number": 3,
                "duration_seconds": 10.0,
                "visual_cue": "Curved Stomach character regulating smooth gastric emptying and digestive rhythm",
                "on_screen_text": "Finding 3: Organ Protection",
                "narration": f"Finding three: Targeted lifestyle components support long-term organ protection: {c3}",
                "subtitle_text": f"Finding 3: {c3[:60]}...",
                "visual_style": "inside_your_body",
                "visual_theme": visual_theme,
                "animation_action": "inside_your_body",
                "organ_character": "stomach",
                "character_name": "Stomach",
                "claim_ids": [clm_ids[2] if len(clm_ids) > 2 else primary_clm]
            }
        ]
        target_dur = 30
        reel_title = f"Inside Your Body: {short_title}"
        hook = f"Take a look inside your biology: What does new research reveal about {short_title}?"
        takeaway = "Targeted metabolic habits directly support vital cellular and digestive health."

    elif visual_style == "everyday_human":
        scenes = [
            {
                "scene_number": 1,
                "duration_seconds": 5.5,
                "visual_cue": "Relatable urban dining table with family finishing meal",
                "on_screen_text": f"Clinical Routine: {short_title[:35]}...",
                "narration": f"How do clinical findings translate into real-life habits? Here is what research shows about {short_title}.",
                "subtitle_text": f"Real-life routine: {short_title[:45]}...",
                "visual_style": "everyday_human",
                "visual_theme": visual_theme,
                "animation_action": "everyday_human",
                "scene_role": "dining_table",
                "character_name": None,
                "claim_ids": [primary_clm]
            },
            {
                "scene_number": 2,
                "duration_seconds": 6.5,
                "visual_cue": "Smartwatch on wrist lighting up with health notification",
                "on_screen_text": f"Evidence Cohort: {sample_size}",
                "narration": f"Evaluating clinical data across {sample_size}: {c1}",
                "subtitle_text": f"{c1[:60]}...",
                "visual_style": "everyday_human",
                "visual_theme": visual_theme,
                "animation_action": "everyday_human",
                "scene_role": "smartwatch_alert",
                "character_name": None,
                "claim_ids": [primary_clm]
            },
            {
                "scene_number": 3,
                "duration_seconds": 6.5,
                "visual_cue": "Person walking smoothly on apartment terrace under sunset sky",
                "on_screen_text": "Actionable Daily Habit",
                "narration": f"Putting science into practice: {c2}",
                "subtitle_text": f"{c2[:60]}...",
                "visual_style": "everyday_human",
                "visual_theme": visual_theme,
                "animation_action": "everyday_human",
                "scene_role": "terrace_walk",
                "character_name": None,
                "claim_ids": [clm_ids[1] if len(clm_ids) > 1 else primary_clm]
            },
            {
                "scene_number": 4,
                "duration_seconds": 6.0,
                "visual_cue": "Wall clock showing optimal timing window",
                "on_screen_text": "Consistency Window",
                "narration": f"Adherence and timing are the key differentiators: {c3}",
                "subtitle_text": f"{c3[:60]}...",
                "visual_style": "everyday_human",
                "visual_theme": visual_theme,
                "animation_action": "everyday_human",
                "scene_role": "timing_clock",
                "character_name": None,
                "claim_ids": [clm_ids[2] if len(clm_ids) > 2 else primary_clm]
            },
            {
                "scene_number": 5,
                "duration_seconds": 5.5,
                "visual_cue": "Happy relaxed human drinking water on balcony with Steer badge",
                "on_screen_text": "Steer Doctor Takeaway",
                "narration": "Steer clinical translation: Build sustainable micro-habits that protect your metabolic vitality every day.",
                "subtitle_text": "Steer Doctor Takeaway: Evidence-backed micro-habits.",
                "visual_style": "everyday_human",
                "visual_theme": visual_theme,
                "animation_action": "everyday_human",
                "scene_role": "doctor_takeaway",
                "character_name": None,
                "claim_ids": clm_ids
            }
        ]
        target_dur = 30
        reel_title = f"Everyday Habits: {short_title}"
        hook = f"Looking for practical metabolic habits? Here is what new clinical research reveals about {short_title}."
        takeaway = "Consistent daily lifestyle habits produce measurable, long-term metabolic health gains."

    elif visual_style == "animated_explainer":
        scenes = [
            {
                "scene_number": 1,
                "duration_seconds": 5.5,
                "visual_cue": "Animated continuous glucose sensor with radiating wireless signal waves and study parameters",
                "on_screen_text": f"Clinical Analysis ({sample_size})",
                "narration": f"What does clinical research show about {short_title}? Let's examine the scientific data.",
                "subtitle_text": f"Clinical analysis across {sample_size}.",
                "visual_style": "animated_explainer",
                "visual_theme": visual_theme,
                "animation_action": "animated_explainer",
                "scene_role": "cgm_intro",
                "character_name": None,
                "claim_ids": [primary_clm]
            },
            {
                "scene_number": 2,
                "duration_seconds": 6.5,
                "visual_cue": "Dynamic 24fps kinetic curve comparing measured metabolic outcomes",
                "on_screen_text": c1[:38] + "...",
                "narration": f"Primary outcome data demonstrated that: {c1}",
                "subtitle_text": f"{c1[:60]}...",
                "visual_style": "animated_explainer",
                "visual_theme": visual_theme,
                "animation_action": "animated_explainer",
                "scene_role": "curve_comparison",
                "character_name": None,
                "claim_ids": [primary_clm]
            },
            {
                "scene_number": 3,
                "duration_seconds": 6.5,
                "visual_cue": "Biochemical transport diagram showing physiological pathway gates",
                "on_screen_text": "Intervention Pathway",
                "narration": f"Biological analysis confirms the underlying pathway: {c2}",
                "subtitle_text": f"{c2[:60]}...",
                "visual_style": "animated_explainer",
                "visual_theme": visual_theme,
                "animation_action": "animated_explainer",
                "scene_role": "glut4_mechanism",
                "character_name": None,
                "claim_ids": [clm_ids[1] if len(clm_ids) > 1 else primary_clm]
            },
            {
                "scene_number": 4,
                "duration_seconds": 6.0,
                "visual_cue": "Comparative timeline illustrating clinical nuance across conditions",
                "on_screen_text": "Evidence Scope & Nuance",
                "narration": f"Investigators noted essential clinical nuances: {c3}",
                "subtitle_text": f"{c3[:60]}...",
                "visual_style": "animated_explainer",
                "visual_theme": visual_theme,
                "animation_action": "animated_explainer",
                "scene_role": "timing_window",
                "character_name": None,
                "claim_ids": [clm_ids[2] if len(clm_ids) > 2 else primary_clm]
            },
            {
                "scene_number": 5,
                "duration_seconds": 5.5,
                "visual_cue": "Steer clinical takeaway badge with green verified shield and citation card",
                "on_screen_text": "Steer Clinical Standard",
                "narration": f"Steer clinical translation: Verified against peer-reviewed publication: {short_title}.",
                "subtitle_text": "Steer Clinical Translation: Verified Research.",
                "visual_style": "animated_explainer",
                "visual_theme": visual_theme,
                "animation_action": "animated_explainer",
                "scene_role": "steer_takeaway",
                "character_name": None,
                "claim_ids": clm_ids
            }
        ]
        target_dur = 30
        reel_title = f"Animated Explainer: {short_title}"
        hook = f"What does continuous data analysis show about {short_title}? Explore the evidence."
        takeaway = "Evidence-based metabolic interventions create verifiable physiological improvements."

    elif visual_style == "professional":
        scenes = [
            {
                "scene_number": 1,
                "duration_seconds": 6.0,
                "visual_cue": f"Clinical study protocol card displaying {sample_size} cohort",
                "on_screen_text": f"Clinical Protocol ({sample_size})",
                "narration": f"In this investigation with {sample_size}, clinical researchers examined: {short_title}.",
                "subtitle_text": f"Investigation: {sample_size}.",
                "visual_style": "professional",
                "visual_theme": visual_theme,
                "animation_action": "professional",
                "character_name": None,
                "claim_ids": [primary_clm]
            },
            {
                "scene_number": 2,
                "duration_seconds": 6.5,
                "visual_cue": "Continuous trajectory chart with error bars showing statistical findings",
                "on_screen_text": c1[:38] + "...",
                "narration": f"The primary endpoint analysis demonstrated that: {c1}",
                "subtitle_text": f"{c1[:60]}...",
                "visual_style": "professional",
                "visual_theme": visual_theme,
                "animation_action": "professional",
                "character_name": None,
                "claim_ids": [primary_clm]
            },
            {
                "scene_number": 3,
                "duration_seconds": 6.5,
                "visual_cue": "Biochemical pathway diagram highlighting cellular metabolic transport",
                "on_screen_text": "Biochemical Pathway",
                "narration": f"Mechanistic analysis indicates: {c2}",
                "subtitle_text": f"{c2[:60]}...",
                "visual_style": "professional",
                "visual_theme": visual_theme,
                "animation_action": "professional",
                "character_name": None,
                "claim_ids": [clm_ids[1] if len(clm_ids) > 1 else primary_clm]
            },
            {
                "scene_number": 4,
                "duration_seconds": 6.5,
                "visual_cue": "Chrono-kinetic timeline comparing study conditions",
                "on_screen_text": "Clinical Scope & Nuance",
                "narration": f"Protocol analysis highlights key caveats: {c3}",
                "subtitle_text": f"{c3[:60]}...",
                "visual_style": "professional",
                "visual_theme": visual_theme,
                "animation_action": "professional",
                "character_name": None,
                "claim_ids": [clm_ids[2] if len(clm_ids) > 2 else primary_clm]
            },
            {
                "scene_number": 5,
                "duration_seconds": 6.5,
                "visual_cue": "Clinical translation summary with Steer Medical Review Gate verification status",
                "on_screen_text": "Medical Review Gate Translation",
                "narration": f"Steer medical translation: Grounding patient guidance in peer-reviewed evidence from: {short_title}.",
                "subtitle_text": f"Steer Clinical Translation: {short_title[:40]}...",
                "visual_style": "professional",
                "visual_theme": visual_theme,
                "animation_action": "professional",
                "character_name": None,
                "claim_ids": clm_ids
            }
        ]
        target_dur = 32
        reel_title = f"Clinical Evidence: {short_title}"
        hook = f"Peer-reviewed evidence on {short_title}."
        takeaway = "Clinical evidence provides actionable insight for personalized metabolic protection."

    else:  # talking_characters
        scenes = [
            {
                "scene_number": 1,
                "duration_seconds": 5.5,
                "visual_cue": "3D Glossy Apple character introducing itself with sunny sparkles",
                "on_screen_text": f"Research: {short_title[:35]}...",
                "narration": f"Hey! Did you know what clinical research reveals about {short_title}? Let's look at the science!",
                "subtitle_text": f"Research on: {short_title[:45]}...",
                "visual_style": "talking_characters",
                "visual_theme": visual_theme,
                "animation_action": "talking_character",
                "character_name": "Dr. Amla",
                "claim_ids": [primary_clm]
            },
            {
                "scene_number": 2,
                "duration_seconds": 6.5,
                "visual_cue": "Apple chatting with cute pink Gut character about research findings",
                "on_screen_text": f"Cohort Data: {sample_size}",
                "narration": f"Researchers evaluated evidence across {sample_size}. Here is what they discovered: {c1}",
                "subtitle_text": f"{c1[:60]}...",
                "visual_style": "talking_characters",
                "visual_theme": visual_theme,
                "animation_action": "talking_character",
                "character_name": "Dr. Amla",
                "claim_ids": [primary_clm]
            },
            {
                "scene_number": 3,
                "duration_seconds": 6.5,
                "visual_cue": "Cute Gut character surrounded by friendly dancing microbiome bacteria",
                "on_screen_text": "Metabolic Mechanism!",
                "narration": f"How does the body respond? Clinical analysis shows: {c2}",
                "subtitle_text": f"{c2[:60]}...",
                "visual_style": "talking_characters",
                "visual_theme": visual_theme,
                "animation_action": "talking_character",
                "character_name": "Dr. Amla",
                "claim_ids": [clm_ids[1] if len(clm_ids) > 1 else primary_clm]
            },
            {
                "scene_number": 4,
                "duration_seconds": 6.0,
                "visual_cue": "Relatable cartoon girl with salad bowl asking interactive question",
                "on_screen_text": "Everyday Application",
                "narration": f"Making it practical: {c3}",
                "subtitle_text": f"{c3[:60]}...",
                "visual_style": "talking_characters",
                "visual_theme": visual_theme,
                "animation_action": "talking_character",
                "character_name": None,
                "claim_ids": [clm_ids[2] if len(clm_ids) > 2 else primary_clm]
            },
            {
                "scene_number": 5,
                "duration_seconds": 5.5,
                "visual_cue": "Group celebration outro with Steer Metabolic Club handoff badge",
                "on_screen_text": "Explore on Steer  ➔",
                "narration": "Steer doctor takeaway: Anchor your routine in real science. Save this reel and explore more on Steer!",
                "subtitle_text": "Steer Doctor Takeaway: Real Science • Real Health.",
                "visual_style": "talking_characters",
                "visual_theme": visual_theme,
                "animation_action": "talking_character",
                "character_name": "Dr. Amla",
                "claim_ids": clm_ids
            }
        ]
        target_dur = 30
        reel_title = f"The Science of {short_title}"
        hook = f"Hey! What does new medical research say about {short_title}?"
        takeaway = "Evidence-based daily habits protect your long-term metabolic health."

    if language == "hi":
        hook = f"क्लीनिकल रिसर्च ब्रीफिंग: {short_title[:45]}. जानिए अध्ययन में क्या पाया गया।"
        takeaway = "प्रमाण-आधारित आदतें आपके लंबे समय के मेटाबॉलिक स्वास्थ्य की रक्षा करती हैं।"
        for s in scenes:
            s_num = s["scene_number"]
            if s_num == 1:
                s["narration"] = f"क्लीनिकल रिसर्च ब्रीफिंग: {short_title[:45]}. आइए देखते हैं कि अध्ययन में क्या पाया गया।"
                s["subtitle_text"] = f"क्लीनिकल रिसर्च: {short_title[:40]}..."
            elif s_num == 2:
                s["narration"] = f"अध्ययन का दायरा: {sample_size}। शोधकर्ताओं ने पाया कि: {c1[:80]}"
                s["subtitle_text"] = f"{c1[:60]}..."
            elif s_num == 3:
                s["narration"] = f"शरीर की कार्यप्रणाली: {c2[:80]}"
                s["subtitle_text"] = f"{c2[:60]}..."
            elif s_num == 4:
                s["narration"] = f"दैनिक जीवन में उपयोग: {c3[:80]}"
                s["subtitle_text"] = f"{c3[:60]}..."
            elif s_num == 5:
                s["narration"] = "डॉक्टर की सलाह: विज्ञान-समर्थित आदतों को अपनाएं। Steer पर और जानें।"
                s["subtitle_text"] = "डॉक्टर की सलाह: विज्ञान-समर्थित आदतें अपनाएं।"
    elif language == "te":
        hook = f"క్లినికల్ రీసెర్చ్: {short_title[:45]}. కొత్త అధ్యయనంలో ఏం తేలింది?"
        takeaway = "శాస్త్రీయ ఆధారిత అలవాట్లు మీ మెటబాలిక్ ఆరోగ్యాన్ని కాపాడతాయి."
        for s in scenes:
            s_num = s["scene_number"]
            if s_num == 1:
                s["narration"] = f"క్లినికల్ రీసెర్చ్: {short_title[:45]}. కొత్త అధ్యయనంలో ఏం తేలిందో చూద్దాం."
                s["subtitle_text"] = f"క్లినికల్ రీసెర్చ్: {short_title[:40]}..."
            elif s_num == 2:
                s["narration"] = f"అధ్యయనం పరిధి: {sample_size}. పరిశోధకులు గుర్తించిన అంశం: {c1[:80]}"
                s["subtitle_text"] = f"{c1[:60]}..."
            elif s_num == 3:
                s["narration"] = f"శరీరంలో మార్పులు: {c2[:80]}"
                s["subtitle_text"] = f"{c2[:60]}..."
            elif s_num == 4:
                s["narration"] = f"రోజువారీ ఆచరణ: {c3[:80]}"
                s["subtitle_text"] = f"{c3[:60]}..."
            elif s_num == 5:
                s["narration"] = "డాక్టర్ సలహా: సైన్స్ ఆధారిత అలవాట్లను పాటించండి. Steer లో మరిన్ని వివరాలు."
                s["subtitle_text"] = "డాక్టర్ సలహా: సైన్స్ ఆధారిత అలవాట్లు."
    elif language == "ta":
        hook = f"மருத்துவ ஆய்வு: {short_title[:45]}. புதிய கண்டுபிடிப்பு என்ன?"
        takeaway = "அறிவியல் பூர்வமான பழக்கங்கள் உங்கள் வளர்சிதை மாற்ற ஆரோக்கியத்தை பாதுகாக்கும்."
        for s in scenes:
            s_num = s["scene_number"]
            if s_num == 1:
                s["narration"] = f"மருத்துவ ஆய்வு: {short_title[:45]}. புதிய ஆய்வு முடிவுகளை பார்ப்போம்."
                s["subtitle_text"] = f"மருத்துவ ஆய்வு: {short_title[:40]}..."
            elif s_num == 2:
                s["narration"] = f"ஆய்வு விவரம்: {sample_size}. முக்கிய முடிவு: {c1[:80]}"
                s["subtitle_text"] = f"{c1[:60]}..."
            elif s_num == 3:
                s["narration"] = f"உடலியல் செயல்பாடு: {c2[:80]}"
                s["subtitle_text"] = f"{c2[:60]}..."
            elif s_num == 4:
                s["narration"] = f"தினசரி பழக்கம்: {c3[:80]}"
                s["subtitle_text"] = f"{c3[:60]}..."
            elif s_num == 5:
                s["narration"] = "மருத்துவர் பரிந்துரை: அறிவியல் பூர்வமான பழக்கங்களை பின்பற்றுங்கள். Steer-ல் அறியுங்கள்."
                s["subtitle_text"] = "மருத்துவர் பரிந்துரை: அறிவியல் பழக்கங்கள்."
    elif language == "kn":
        hook = f"ವೈದ್ಯಕೀಯ ಸಂಶೋಧನೆ: {short_title[:45]}. ಹೊಸ ಅಧ್ಯಯನ ಏನು ಹೇಳುತ್ತದೆ?"
        takeaway = "ವಿಜ್ಞಾನ ಆಧಾರಿತ ಸಣ್ಣ ಅಭ್ಯಾಸಗಳು ನಿಮ್ಮ ಮೆಟಬಾಲಿಕ್ ಆರೋಗ್ಯ ಕಾಪಾಡುತ್ತವೆ."
        for s in scenes:
            s_num = s["scene_number"]
            if s_num == 1:
                s["narration"] = f"ವೈದ್ಯಕೀಯ ಸಂಶೋಧನೆ: {short_title[:45]}. ಹೊಸ ಅಧ್ಯಯನದ ವಿವರ ತಿಳಿಯೋಣ."
                s["subtitle_text"] = f"ವೈದ್ಯಕೀಯ ಸಂಶೋಧನೆ: {short_title[:40]}..."
            elif s_num == 2:
                s["narration"] = f"ಅಧ್ಯಯನದ ವ್ಯಾಪ್ತಿ: {sample_size}. ಪ್ರಮುಖ ಅಂಶ: {c1[:80]}"
                s["subtitle_text"] = f"{c1[:60]}..."
            elif s_num == 3:
                s["narration"] = f"ದೇಹದ ಪ್ರಕ್ರಿಯೆ: {c2[:80]}"
                s["subtitle_text"] = f"{c2[:60]}..."
            elif s_num == 4:
                s["narration"] = f"ದೈನಂದಿನ ಬಳಕೆ: {c3[:80]}"
                s["subtitle_text"] = f"{c3[:60]}..."
            elif s_num == 5:
                s["narration"] = "ವೈದ್ಯರ ಸಲಹೆ: ವಿಜ್ಞಾನ ಆಧಾರಿತ ಅಭ್ಯಾಸಗಳನ್ನು ರೂಢಿಸಿಕೊಳ್ಳಿ. Steer ನಲ್ಲಿ ಇನ್ನಷ್ಟು ತಿಳಿಯಿರಿ."
                s["subtitle_text"] = "ವೈದ್ಯರ ಸಲಹೆ: ವಿಜ್ಞಾನ ಆಧಾರಿತ ಅಭ್ಯಾಸ."
    elif language == "ml":
        hook = f"ക്ലിനിക്കൽ പഠനം: {short_title[:45]}. പുതിയ കണ്ടെത്തലുകൾ എന്തൊക്കെ?"
        takeaway = "ശാസ്ത്രീയമായ നല്ല ശീലങ്ങൾ മെറ്റബോളിക് ആരോഗ്യം സംരക്ഷിക്കുന്നു."
        for s in scenes:
            s_num = s["scene_number"]
            if s_num == 1:
                s["narration"] = f"ക്ലിനിക്കൽ പഠനം: {short_title[:45]}. പുതിയ കണ്ടെത്തലുകൾ പരിശോധിക്കാം."
                s["subtitle_text"] = f"ക്ലിനിക്കൽ പഠനം: {short_title[:40]}..."
            elif s_num == 2:
                s["narration"] = f"പഠന വ്യാപ്തി: {sample_size}. പ്രധാന കണ്ടെത്തൽ: {c1[:80]}"
                s["subtitle_text"] = f"{c1[:60]}..."
            elif s_num == 3:
                s["narration"] = f"ശരീരത്തിലെ മാറ്റങ്ങൾ: {c2[:80]}"
                s["subtitle_text"] = f"{c2[:60]}..."
            elif s_num == 4:
                s["narration"] = f"ദൈനംദിന ശീലങ്ങൾ: {c3[:80]}"
                s["subtitle_text"] = f"{c3[:60]}..."
            elif s_num == 5:
                s["narration"] = "ഡോക്ടറുടെ നിർദ്ദേശം: ശാസ്ത്രീയ ശീലങ്ങൾ പിന്തുടരൂ. Steer-ൽ കൂടുതൽ അറിയൂ."
                s["subtitle_text"] = "ഡോക്ടറുടെ നിർദ്ദേശം: ശാസ്ത്രീയ ശീലങ്ങൾ."

    return {
        "reel_title": reel_title,
        "hook": hook,
        "target_duration_seconds": target_dur,
        "mode": "professional" if visual_style == "professional" else "everyday",
        "visual_style": visual_style,
        "visual_theme": visual_theme,
        "language": language,
        "voice_name": voice_name,
        "scenes": scenes,
        "practical_takeaway": takeaway,
        "caption": f"Doctor-Led Research Briefing: {paper_title}\n\nKey Finding: {c1}\n\nClinical Mechanism: {c2}\n\nSteer Takeaway: {takeaway}\n\nSource: {short_title} 🩺✨",
        "hashtags": ["#MetabolicHealth", "#ClinicalEvidence", "#SteerHealth", "#DoctorLed"],
        "claim_ids": clm_ids,
        "source_citation": f"Evidence: {short_title}"
    }

def get_professional_reel_storyboard(
    claims: Optional[List[Dict[str, Any]]],
    paper_title: str,
    voice_name: str,
    visual_theme: str = "warm_editorial"
) -> Dict[str, Any]:
    if not is_sample_walk_paper(paper_title):
        return _build_dynamic_paper_storyboard("professional", "en", claims, paper_title, voice_name, visual_theme)

    clm_ids = [c.get("claim_id", f"CLM-{i+1:03d}") for i, c in enumerate(claims)] if claims else ["CLM-001", "CLM-002", "CLM-003"]
    primary_clm = clm_ids[0] if clm_ids else "CLM-001"
    c2 = clm_ids[1] if len(clm_ids) > 1 else primary_clm
    c3 = clm_ids[2] if len(clm_ids) > 2 else primary_clm


    return {
        "reel_title": "Clinical Evidence: Postprandial Ambulation & Glycemic Response",
        "hook": "Randomized crossover evidence on postprandial glucose excursion kinetics.",
        "target_duration_seconds": 32,
        "mode": "professional",
        "visual_style": "professional",
        "visual_theme": visual_theme,
        "language": "en",
        "voice_name": voice_name,
        "practical_takeaway": "Light ambulation within 30 minutes of meal intake optimizes non-insulin glucose disposal.",
        "caption": "Scientific Briefing: A randomized crossover trial (n=48) demonstrated that 10 minutes of post-meal ambulation blunts peak glucose excursion by 34% (p < 0.01). Non-insulin-mediated GLUT4 translocation in contracting skeletal muscle clears systemic glucose without placing pancreatic demand.",
        "hashtags": ["#Endocrinology", "#MetabolicMedicine", "#ClinicalTrial", "#RandomizedTrial", "#GLUT4"],
        "claim_ids": clm_ids,
        "source_citation": f"Crossover Clinical Trial ({paper_title[:45]})",
        "scenes": [
            {
                "scene_number": 1,
                "duration_seconds": 6.0,
                "visual_cue": "Clinical study protocol card displaying Randomized Crossover Trial, n=48 South Asian cohort",
                "on_screen_text": "Randomized Crossover Trial (n=48)",
                "narration": "In this randomized crossover investigation with forty-eight South Asian adults, researchers assessed the acute postprandial glycemic impact of immediate post-meal ambulation.",
                "subtitle_text": "Randomized Crossover Trial: Postprandial Glycemia (n=48)",
                "visual_style": "professional",
                "visual_theme": visual_theme,
                "animation_action": "professional",
                "character_name": None,
                "claim_ids": [primary_clm]
            },
            {
                "scene_number": 2,
                "duration_seconds": 6.5,
                "visual_cue": "Continuous glucose monitoring excursion chart with error bars showing 34% reduction (p < 0.01)",
                "on_screen_text": "34% Reduction in Peak Excursion",
                "narration": "Ten minutes of light walking initiated within fifteen to thirty minutes post-ingestion resulted in a thirty-four percent reduction in peak glucose excursion compared with sedentary rest.",
                "subtitle_text": "10-min light walking blunted peak excursion by 34% (p < 0.01).",
                "visual_style": "professional",
                "visual_theme": visual_theme,
                "animation_action": "professional",
                "character_name": None,
                "claim_ids": [primary_clm]
            },
            {
                "scene_number": 3,
                "duration_seconds": 6.5,
                "visual_cue": "Biochemical pathway diagram highlighting non-insulin-mediated GLUT4 translocation into skeletal muscle",
                "on_screen_text": "Non-Insulin GLUT4 Translocation",
                "narration": "Mechanistic analyses indicate skeletal muscle contractions stimulate GLUT-4 translocation independent of the insulin-signaling cascade, mitigating pancreatic beta-cell strain.",
                "subtitle_text": "Skeletal contractions trigger GLUT4 translocation independently of insulin.",
                "visual_style": "professional",
                "visual_theme": visual_theme,
                "animation_action": "professional",
                "character_name": None,
                "claim_ids": [c2]
            },
            {
                "scene_number": 4,
                "duration_seconds": 6.5,
                "visual_cue": "Chrono-kinetic timeline comparing immediate 15-30 min ambulation vs 60-min delayed exercise",
                "on_screen_text": "Kinetic Window: 30 vs 60 Mins",
                "narration": "Crucially, delaying ambulation to sixty minutes postprandially diminished the attenuation to just nine percent, underscoring the critical kinetic window.",
                "subtitle_text": "Delaying to 60 mins attenuated glycemic benefit from 34% to 9%.",
                "visual_style": "professional",
                "visual_theme": visual_theme,
                "animation_action": "professional",
                "character_name": None,
                "claim_ids": [c3]
            },
            {
                "scene_number": 5,
                "duration_seconds": 6.5,
                "visual_cue": "Clinical translation summary with Steer Medical Review Gate verification status",
                "on_screen_text": "Clinical Translation & Evidence Gate",
                "narration": "Clinical recommendation: light ambulation within thirty minutes of carbohydrate intake. Note that individual glycemic variance depends on baseline insulin sensitivity.",
                "subtitle_text": "Steer Clinical Translation: Light ambulation within 30 mins of meals.",
                "visual_style": "professional",
                "visual_theme": visual_theme,
                "animation_action": "professional",
                "character_name": None,
                "claim_ids": clm_ids
            }
        ]
    }


def get_inside_your_body_storyboard(
    language: str,
    claims: Optional[List[Dict[str, Any]]],
    paper_title: str,
    voice_name: str,
    visual_theme: str = "warm_editorial"
) -> Dict[str, Any]:
    if not is_sample_walk_paper(paper_title):
        return _build_dynamic_paper_storyboard("inside_your_body", language, claims, paper_title, voice_name, visual_theme)

    clm_ids = [c.get("claim_id", f"CLM-{i+1:03d}") for i, c in enumerate(claims)] if claims else ["CLM-001", "CLM-002", "CLM-003"]
    num_findings = min(3, max(1, len(claims))) if claims else 3

    scripts = {
        "en": {
            "title": "Inside Your Body: What Post-Meal Pacing Does To Your Biology",
            "hook": "Take a look inside your bloodstream, brain, and stomach when you walk after eating.",
            "takeaway": "Light post-meal movement optimizes circulation, brain satiety signals, and gastric digestion.",
            "caption": "Inside your body after meals: clinical research demonstrates 3 distinct physiological benefits from 10 minutes of gentle walking. Swipe to explore the biology! 🔬🫀",
            "findings": [
                {
                    "organ": "red_blood_cell",
                    "on_screen": "Finding 1: Bloodstream & Oxygen Flow",
                    "visual_cue": "Red blood cell character smiling in flowing arterial bloodstream delivering oxygen molecules",
                    "narration": "Finding one: post-meal walking stimulates arterial blood circulation, delivering fresh oxygen and clearing excess glucose thirty-four percent faster.",
                    "subtitle": "Finding 1: Circulation clears excess glucose 34% faster.",
                    "duration": 11.0,
                    "claim_idx": 0
                },
                {
                    "organ": "brain",
                    "on_screen": "Finding 2: Brain Signalling & Appetite",
                    "visual_cue": "Expressive Brain character firing gentle synaptic sparks in glowing violet neural space",
                    "narration": "Finding two: light ambulation sends stabilizing satiety signals to your brain's hypothalamus, curbing sudden cravings and energy crashes.",
                    "subtitle": "Finding 2: Movement stabilizes hypothalamic satiety signals.",
                    "duration": 11.5,
                    "claim_idx": 1
                },
                {
                    "organ": "stomach",
                    "on_screen": "Finding 3: Gastric Emptying & Digestion",
                    "visual_cue": "Curved Stomach character regulating smooth gastric emptying and digestive rhythm",
                    "narration": "Finding three: gentle pacing modulates gastric emptying rate, allowing steady carbohydrate absorption instead of a violent blood sugar spike.",
                    "subtitle": "Finding 3: Steady gastric digestion prevents sudden sugar spikes.",
                    "duration": 11.0,
                    "claim_idx": 2
                }
            ]
        },
        "hi": {
            "title": "शरीर के अंदर: खाने के बाद टहलने का जैविक असर",
            "hook": "देखिए खाने के बाद टहलने से आपके खून, दिमाग और पेट में क्या असर होता है।",
            "takeaway": "हल्का टहलना ब्लड सर्कुलेशन, मस्तिष्क संकेत और पाचन को तुरंत संतुलित करता है।",
            "caption": "खाने के बाद शरीर के अंदर क्या होता है? क्लिनिकल रिसर्च में तीन बड़े जैविक फायदे साबित हुए हैं। 🔬🫀",
            "findings": [
                {
                    "organ": "red_blood_cell",
                    "on_screen": "निष्कर्ष 1: ब्लड सर्कुलेशन और ऑक्सीजन",
                    "visual_cue": "धमनियों में तैरता मुस्कुराता रेड ब्लड सेल ऑक्सीजन के अणु पहुंचाते हुए",
                    "narration": "निष्कर्ष एक: खाने के बाद टहलने से ब्लड सर्कुलेशन तेज़ होता है और ग्लूकोज चौंतीस प्रतिशत तेज़ी से साफ़ होता है।",
                    "subtitle": "निष्कर्ष 1: ब्लड सर्कुलेशन से 34% तेज़ी से ग्लूकोज साफ़ होता है।",
                    "duration": 11.0,
                    "claim_idx": 0
                },
                {
                    "organ": "brain",
                    "on_screen": "निष्कर्ष 2: मस्तिष्क संकेत और भूख नियंत्रण",
                    "visual_cue": "बैंगनी न्यूरल स्पेस में चमकते सिग्नलों के साथ मस्तिष्क कैरेक्टर",
                    "narration": "निष्कर्ष दो: हल्की चाल मस्तिष्क को तृप्ति के शांत संकेत भेजती है, जिससे बेवजह की क्रेविंग्स और सुस्ती रुकती है।",
                    "subtitle": "निष्कर्ष 2: मस्तिष्क को तृप्ति के संकेत मिलते हैं और क्रेविंग्स रुकती हैं।",
                    "duration": 11.5,
                    "claim_idx": 1
                },
                {
                    "organ": "stomach",
                    "on_screen": "निष्कर्ष 3: पाचन क्रिया और पेट",
                    "visual_cue": "पेट का कैरेक्टर पाचन की गति को संतुलित करते हुए",
                    "narration": "निष्कर्ष तीन: हल्का टहलना पेट में गैस्ट्रिक पाचन को स्थिर करता है, जिससे शुगर का अचानक स्पाइक नहीं होता।",
                    "subtitle": "निष्कर्ष 3: पाचन संतुलित रहता है और शुगर स्पाइक नहीं होता।",
                    "duration": 11.0,
                    "claim_idx": 2
                }
            ]
        },
        "te": {
            "title": "శరీరం లోపల: తిన్న తర్వాత నడవడం వల్ల కలిగే అద్భుతాలు",
            "hook": "భోజనం తర్వాత నడిస్తే రక్తప్రసరణ, మెదడు మరియు పొట్టలో ఏం జరుగుతుందో చూడండి.",
            "takeaway": "చిన్న నడక రక్త ప్రసరణను, ఆకలి సంకేతాలను మరియు జీర్ణక్రియను మెరుగుపరుస్తుంది.",
            "caption": "తిన్న తర్వాత శరీరం లోపల జరిగే 3 ముఖ్యమైన శాస్త్రీయ నిజాలు! 🔬🫀",
            "findings": [
                {
                    "organ": "red_blood_cell",
                    "on_screen": "ఫలితం 1: రక్త ప్రసరణ మరియు ఆక్సిజన్",
                    "visual_cue": "రక్తనాళంలో ఆక్సిజన్ అణువులను మోసుకెళ్తున్న రెడ్ బ్లడ్ సెల్ క్యారెక్టర్",
                    "narration": "ఫలితం ఒకటి: తిన్న తర్వాత నడవడం వల్ల రక్త ప్రసరణ మెరుగై, గ్లూకోజ్ ముప్పై నాలుగు శాతం వేగంగా తగ్గుతుంది.",
                    "subtitle": "ఫలితం 1: రక్త ప్రసరణ ద్వారా 34% వేగంగా గ్లూకోజ్ తగ్గుతుంది.",
                    "duration": 11.0,
                    "claim_idx": 0
                },
                {
                    "organ": "brain",
                    "on_screen": "ఫలితం 2: మెదడు సంకేతాలు & ఆకలి నియంత్రణ",
                    "visual_cue": "విద్యుత్ మెరుపులతో శాంతంగా ఉండే మెదడు క్యారెక్టర్",
                    "narration": "ఫలితం రెండు: తిన్న తర్వాత నడక మెదడుకు సంతృప్తి సంకేతాలను పంపి, అనవసరమైన ఆకలిని నివారిస్తుంది.",
                    "subtitle": "ఫలితం 2: మెదడుకు సంతృప్తి సంకేతాలు చేరి ఆకలి నియంత్రణలో ఉంటుంది.",
                    "duration": 11.5,
                    "claim_idx": 1
                },
                {
                    "organ": "stomach",
                    "on_screen": "ఫలితం 3: జీర్ణవ్యవస్థ మరియు పొట్ట",
                    "visual_cue": "ఆహార జీర్ణక్రియను క్రమబద్ధీకరించే పొట్ట క్యారెక్టర్",
                    "narration": "ఫలితం మూడు: చిన్న నడక పొట్టలో జీర్ణక్రియను సమతుల్యం చేసి, షుగర్ ఒక్కసారిగా పెరగకుండా కాపాడుతుంది.",
                    "subtitle": "ఫలితం 3: జీర్ణక్రియ సక్రమంగా జరిగి షుగర్ స్పైక్ ఆగుతుంది.",
                    "duration": 11.0,
                    "claim_idx": 2
                }
            ]
        },
        "ta": {
            "title": "உடலின் உள்ளே: சாப்பிட்ட பின் நடப்பதன் அறிவியல் பலன்கள்",
            "hook": "சாப்பிட்ட பின் நடக்கும்போது ரத்த ஓட்டம், மூளை மற்றும் வயிற்றில் என்ன நடக்கிறது என்று பாருங்கள்.",
            "takeaway": "லேசான நடை ரத்த ஓட்டம், பசி கட்டுப்பாடு மற்றும் செரிமானத்தை சீராக்குகிறது.",
            "caption": "சாப்பிட்ட பின் உடலுக்குள் நிகழும் 3 முக்கிய அறிவியல் உண்மைகள்! 🔬🫀",
            "findings": [
                {
                    "organ": "red_blood_cell",
                    "on_screen": "முடிவு 1: ரத்த ஓட்டம் மற்றும் ஆக்சிஜன்",
                    "visual_cue": "ரத்த ஓட்டத்தில் ஆக்சிஜன் மூலக்கூறுகளை சுமந்து செல்லும் சிவப்பு ரத்த அணு",
                    "narration": "முடிவு ஒன்று: சாப்பிட்ட பின் நடப்பது ரத்த ஓட்டத்தை சீராக்கி, சர்க்கரையை முப்பத்து நான்கு சதவீதம் வேகமாக குறைக்கிறது.",
                    "subtitle": "முடிவு 1: ரத்த ஓட்டம் சீராகி 34% வேகமாக சர்க்கரை குறைகிறது.",
                    "duration": 11.0,
                    "claim_idx": 0
                },
                {
                    "organ": "brain",
                    "on_screen": "முடிவு 2: மூளை சமிக்ஞைகள் & பசி கட்டுப்பாடு",
                    "visual_cue": "மின்னல் சமிக்ஞைகளுடன் பசியை ஒழுங்குபடுத்தும் மூளை கேரக்டர்",
                    "narration": "முடிவு இரண்டு: உணவு உண்ட பின் லேசான நடை மூளைக்கு நிறைவான உணர்வை தந்து, தேவையற்ற பசியை தடுக்கிறது.",
                    "subtitle": "முடிவு 2: மூளைக்கு திருப்தி சமிக்ஞை சென்று பசி கட்டுக்குள் இருக்கும்.",
                    "duration": 11.5,
                    "claim_idx": 1
                },
                {
                    "organ": "stomach",
                    "on_screen": "முடிவு 3: செரிமான மண்டலம் & வயிறு",
                    "visual_cue": "செரிமானத்தை மென்மையாக ஒழுங்குபடுத்தும் வயிறு கேரக்டர்",
                    "narration": "முடிவு மூன்று: லேசாக நடப்பது வயிற்றின் செரிமானத்தை சமன் செய்து, திடீர் சர்க்கரை உயர்வை தணிக்கிறது.",
                    "subtitle": "முடிவு 3: செரிமானம் சீராகி திடீர் சர்க்கரை உயர்வு குறைகிறது.",
                    "duration": 11.0,
                    "claim_idx": 2
                }
            ]
        },
        "kn": {
            "title": "ದೇಹದ ಒಳಗೆ: ಊಟದ ನಂತರದ ನಡಿಗೆಯ ಜೈವಿಕ ಪರಿಣಾಮ",
            "hook": "ಊಟದ ನಂತರ ನಡೆದಾಗ ರಕ್ತ ಪರಿಚಲನೆ, ಮೆದುಳು ಮತ್ತು ಹೊಟ್ಟೆಯಲ್ಲಿ ಏನು ಬದಲಾಗುತ್ತದೆ ನೋಡಿ.",
            "takeaway": "ಶಾಂತ ನಡಿಗೆಯು ರಕ್ತ ಸಂಚಾರ, ಹಸಿವಿನ ನಿಯಂತ್ರಣ ಮತ್ತು ಜೀರ್ಣಕ್ರಿಯೆಯನ್ನು ಸುಧಾರಿಸುತ್ತದೆ.",
            "caption": "ಊಟದ ನಂತರ ದೇಹದೊಳಗಿನ 3 ಪ್ರಮುಖ ಜೈವಿಕ ಸಂಶೋಧನೆಗಳು! 🔬🫀",
            "findings": [
                {
                    "organ": "red_blood_cell",
                    "on_screen": "ಸಂಶೋಧನೆ 1: ರಕ್ತ ಪರಿಚಲನೆ ಮತ್ತು ಆಕ್ಸಿಜನ್",
                    "visual_cue": "ರಕ್ತನಾಳದಲ್ಲಿ ಆಕ್ಸಿಜನ್ ಕಣಗಳನ್ನು ಸಾಗಿಸುವ ಕೆಂಪು ರಕ್ತ ಕಣದ ಪಾತ್ರ",
                    "narration": "ಸಂಶೋಧನೆ ಒಂದು: ಊಟದ ನಂತರ ನಡೆಯುವುದರಿಂದ ರಕ್ತ ಪರಿಚಲನೆ ಸುಧಾರಿಸಿ, ಸಕ್ಕರೆಯ ಮಟ್ಟ ಮೂವತ್ನಾಲ್ಕು ಪ್ರತಿಶತ ವೇಗವಾಗಿ ಕಡಿಮೆಯಾಗುತ್ತದೆ.",
                    "subtitle": "ಸಂಶೋಧನೆ 1: ರಕ್ತ ಪರಿಚಲನೆಯಿಂದ 34% ವೇಗವಾಗಿ ಸಕ್ಕರೆ ಕಡಿಮೆಯಾಗುತ್ತದೆ.",
                    "duration": 11.0,
                    "claim_idx": 0
                },
                {
                    "organ": "brain",
                    "on_screen": "ಸಂಶೋಧನೆ 2: ಮೆದುಳಿನ ಸಂಕೇತಗಳು ಮತ್ತು ಹಸಿವಿನ ನಿಯಂತ್ರಣ",
                    "visual_cue": "ನರಮಂಡಲದಲ್ಲಿ ಪ್ರಶಾಂತವಾಗಿ ಹೊಳೆಯುವ ಮೆದುಳಿನ ಪಾತ್ರ",
                    "narration": "ಸಂಶೋಧನೆ ಎರಡು: ಊಟದ ನಂತರದ ವಾಕಿಂಗ್ ಮೆದುಳಿಗೆ ತೃಪ್ತಿಯ ಸಂದೇಶ ಕಳುಹಿಸಿ, ಅತಿಯಾದ ಹಸಿವನ್ನು ನಿಯಂತ್ರಿಸುತ್ತದೆ.",
                    "subtitle": "ಸಂಶೋಧನೆ 2: ಮೆದುಳಿಗೆ ತೃಪ್ತಿಯ ಸಂಕೇತ ತಲುಪಿ ಹಸಿವು ನಿಯಂತ್ರಣಗೊಳ್ಳುತ್ತದೆ.",
                    "duration": 11.5,
                    "claim_idx": 1
                },
                {
                    "organ": "stomach",
                    "on_screen": "ಸಂಶೋಧನೆ 3: ಜೀರ್ಣಕ್ರಿಯೆ ಮತ್ತು ಹೊಟ್ಟೆ",
                    "visual_cue": "ಜೀರ್ಣಕ್ರಿಯೆಯನ್ನು ಸರಾಗವಾಗಿ ನಿಯಂತ್ರಿಸುವ ಹೊಟ್ಟೆಯ ಪಾತ್ರ",
                    "narration": "ಸಂಶೋಧನೆ ಮೂರು: ಶಾಂತ ನಡಿಗೆಯು ಜೀರ್ಣಕ್ರಿಯೆಯನ್ನು ಸರಾಗಗೊಳಿಸಿ, ತೀವ್ರ ರಕ್ತದ ಸಕ್ಕರೆ ಹೆಚ್ಚಳವನ್ನು ತಡೆಯುತ್ತದೆ.",
                    "subtitle": "ಸಂಶೋಧನೆ 3: ಜೀರ್ಣಕ್ರಿಯೆ ಸರಾಗವಾಗಿ ಸಕ್ಕರೆ ಸ್ಪೈಕ್ ನಿಯಂತ್ರಣವಾಗುತ್ತದೆ.",
                    "duration": 11.0,
                    "claim_idx": 2
                }
            ]
        },
        "ml": {
            "title": "ശരീരത്തിനുള്ളിൽ: ഭക്ഷണത്തിന് ശേഷമുള്ള നടത്തത്തിന്റെ മാജിക്",
            "hook": "ഭക്ഷണത്തിന് ശേഷം നടക്കുമ്പോൾ രക്തചംക്രമണം, തലച്ചോറ്, ആമാശയം എന്നിവയിൽ എന്ത് സംഭവിക്കുന്നു എന്ന് കാണൂ.",
            "takeaway": "ലഘുവായ നടത്തം രക്തചംക്രമണം, വിശപ്പ് നിയന്ത്രണം, ദഹനം എന്നിവ സുഗമമാക്കുന്നു.",
            "caption": "ഭക്ഷണത്തിന് ശേഷം ശരീരത്തിനുള്ളിൽ സംഭവിക്കുന്ന 3 കണ്ടെത്തലുകൾ! 🔬🫀",
            "findings": [
                {
                    "organ": "red_blood_cell",
                    "on_screen": "കണ്ടെത്തൽ 1: രക്തചംക്രമണവും ഓക്സിജനും",
                    "visual_cue": "രക്തക്കുഴലിലൂടെ ഓക്സിജൻ കണികകൾ എത്തിക്കുന്ന ചുവന്ന രക്താണു കഥാപാത്രം",
                    "narration": "കണ്ടെത്തൽ ഒന്ന്: ഭക്ഷണത്തിന് ശേഷമുള്ള നടത്തം രക്തചംക്രമണം വർദ്ധിപ്പിച്ച് പഞ്ചസാര മുപ്പത്തിനാല് ശതമാനം വേഗത്തിൽ കുറയ്ക്കുന്നു.",
                    "subtitle": "കണ്ടെത്തൽ 1: രക്തചംക്രമണം വഴി 34% വേഗത്തിൽ പഞ്ചസാര കുറയുന്നു.",
                    "duration": 11.0,
                    "claim_idx": 0
                },
                {
                    "organ": "brain",
                    "on_screen": "കണ്ടെത്തൽ 2: തലച്ചോറിലെ സന്ദേശങ്ങളും വിശപ്പും",
                    "visual_cue": "ന്യൂറോണുകളിൽ മിന്നുന്ന സന്ദേശങ്ങളോടെ വിശപ്പ് നിയന്ത്രിക്കുന്ന തലച്ചോറ് കഥാപാത്രം",
                    "narration": "കണ്ടെത്തൽ രണ്ട്: ഭക്ഷണത്തിന് ശേഷമുള്ള നടത്തം തലച്ചോറിലേക്ക് സംതൃപ്തി സന്ദേശങ്ങൾ എത്തിച്ച് അനാവശ്യ വിശപ്പ് തടയുന്നു.",
                    "subtitle": "കണ്ടെത്തൽ 2: തലച്ചോറിലേക്ക് തൃപ്തി സന്ദേശങ്ങൾ എത്തി വിശപ്പ് നിയന്ത്രിക്കുന്നു.",
                    "duration": 11.5,
                    "claim_idx": 1
                },
                {
                    "organ": "stomach",
                    "on_screen": "കണ്ടെത്തൽ 3: ദഹനവ്യവസ്ഥയും ആമാശയവും",
                    "visual_cue": "ഭക്ഷണ ദഹനം ശാന്തമായി ക്രമീകരിക്കുന്ന ആമാശയം കഥാപാത്രം",
                    "narration": "കണ്ടെത്തൽ മൂന്ന്: ലളിതമായ നടത്തം ആമാശയത്തിലെ ദഹനം സുഗമമാക്കി പെട്ടെന്നുള്ള ഷുഗർ സ്പൈക്ക് തടയുന്നു.",
                    "subtitle": "കണ്ടെത്തൽ 3: ദഹനം സുഗമമാക്കി പെട്ടെന്നുള്ള ഷുഗർ സ്പൈക്ക് തടയുന്നു.",
                    "duration": 11.0,
                    "claim_idx": 2
                }
            ]
        }
    }

    b_lang = scripts.get(language, scripts["en"])
    selected = b_lang["findings"][:num_findings]

    scenes = []
    total_dur = 0.0
    for idx, f in enumerate(selected):
        c_id = clm_ids[min(f["claim_idx"], len(clm_ids) - 1)]
        total_dur += f["duration"]
        scenes.append({
            "scene_number": idx + 1,
            "duration_seconds": f["duration"],
            "visual_cue": f["visual_cue"],
            "on_screen_text": f["on_screen"],
            "narration": f["narration"],
            "subtitle_text": f["subtitle"],
            "visual_style": "inside_your_body",
            "visual_theme": visual_theme,
            "animation_action": "inside_your_body",
            "organ_character": f["organ"],
            "character_name": f["organ"].replace("_", " ").title(),
            "claim_ids": [c_id]
        })

    return {
        "reel_title": b_lang["title"],
        "hook": b_lang["hook"],
        "target_duration_seconds": int(total_dur),
        "mode": "everyday",
        "visual_style": "inside_your_body",
        "visual_theme": visual_theme,
        "language": language,
        "voice_name": voice_name,
        "scenes": scenes,
        "practical_takeaway": b_lang["takeaway"],
        "caption": b_lang["caption"],
        "hashtags": ["#InsideYourBody", "#MetabolicBiology", "#SteerHealth", "#Physiology", "#CellularHealth"],
        "claim_ids": clm_ids[:num_findings],
        "source_citation": f"Evidence: {paper_title[:45]} (n=48)"
    }


def get_everyday_reel_storyboard(
    language: str,
    claims: Optional[List[Dict[str, Any]]],
    paper_title: str,
    voice_name: str,
    visual_theme: str = "warm_editorial"
) -> Dict[str, Any]:
    if not is_sample_walk_paper(paper_title):
        return _build_dynamic_paper_storyboard("talking_characters", language, claims, paper_title, voice_name, visual_theme)

    clm_ids = [c.get("claim_id", f"CLM-{i+1:03d}") for i, c in enumerate(claims)] if claims else ["CLM-001", "CLM-002", "CLM-003"]
    primary_clm = clm_ids[0] if clm_ids else "CLM-001"
    c2 = clm_ids[1] if len(clm_ids) > 1 else primary_clm
    c3 = clm_ids[2] if len(clm_ids) > 2 else primary_clm

    scripts = {
        "en": {
            "title": "The 10-Minute Post-Dinner Habit That Beats Blood Sugar Spikes",
            "hook": "Hey! I'm an apple. What happens inside you right after food?",
            "takeaway": "Consistent everyday micro-habits protect your long-term metabolic vitality.",
            "caption": "Your grandparents called it 'Shatapadi' (100 steps after food). Modern endocrinology just proved them right! A 10-minute stroll right after meals cuts the sugar spike by 34%. Try it tonight! 🚶‍♂️✨",
            "scenes": [
                {
                    "on_screen": "Hey! I'm an apple...",
                    "narration": "Hey! I'm an apple. What happens inside you right after eating?",
                    "subtitle": "Hey! I'm an apple. What happens inside you after eating?",
                    "visual_cue": "3D Glossy Apple character introducing itself with sunny sparkles",
                    "duration": 4.0
                },
                {
                    "on_screen": "Keep your gut active!",
                    "narration": "Walking lightly after meals keeps your digestion active and happy!",
                    "subtitle": "Light walking keeps your digestion active and happy!",
                    "visual_cue": "Apple chatting with cute pink Gut character about post-meal digestion",
                    "duration": 4.5
                },
                {
                    "on_screen": "Cut sugar spike by 34%!",
                    "narration": "Clinical study shows a 10-minute walk cuts glucose spikes by 34%!",
                    "subtitle": "A 10-minute walk cuts glucose spikes by 34%!",
                    "visual_cue": "Cute Gut character surrounded by friendly dancing microbiome bacteria",
                    "duration": 5.0
                },
                {
                    "on_screen": "Which foods help your gut?",
                    "narration": "Quick quiz! What feeds your gut bacteria? Fruits, veggies, or grains?",
                    "subtitle": "What feeds gut bacteria? Fruits, veggies, or grains?",
                    "visual_cue": "Relatable cartoon girl with salad bowl asking interactive gut health question",
                    "duration": 5.0
                },
                {
                    "on_screen": "Good choice! All of them!",
                    "narration": "All of them! They feed good microbes and stabilize glucose.",
                    "subtitle": "All of them! They feed good microbes and stabilize glucose.",
                    "visual_cue": "Glowing green checkmark celebration with Apple and Gut cheering side by side",
                    "duration": 4.5
                },
                {
                    "on_screen": "Muscles soak up sugar!",
                    "narration": "Working leg muscles absorb glucose directly without insulin stress.",
                    "subtitle": "Leg muscles absorb glucose directly without insulin stress.",
                    "visual_cue": "Cartoon girl enjoying fresh smoothie with thumbs up habit reminder",
                    "duration": 5.0
                },
                {
                    "on_screen": "Explore on Steer  ➔",
                    "narration": "Take 100 steps tonight! Explore more on Steer.",
                    "subtitle": "Take 100 steps tonight! Explore more on Steer.",
                    "visual_cue": "Group celebration outro with Steer Metabolic Club handoff badge",
                    "duration": 4.0
                }
            ]
        },
        "hi": {
            "title": "डिनर के बाद 10 मिनट की वॉक: शुगर स्पाइक रोकने का आसान तरीका",
            "hook": "अरे! मैं सेब हूँ। क्या आपको पता है खाने के बाद शरीर में क्या होता है?",
            "takeaway": "डिनर के बाद सिर्फ 10 मिनट आराम से टहलिए और अपनी शुगर को सामान्य रखिए।",
            "caption": "हमारे बड़े इसे 'शतपदी' कहते थे—खाने के बाद 100 कदम! रिसर्च बताती है कि खाने के 30 मिनट के अंदर 10 मिनट टहलने से शुगर स्पाइक 34% तक कम होता है। आज रात ज़रूर ट्राय करें! 🩺✨",
            "scenes": [
                {
                    "on_screen": "अरे! मैं सेब हूँ...",
                    "narration": "अरे! मैं सेब हूँ। क्या आपको पता है खाने के बाद क्या होता है?",
                    "subtitle": "अरे! मैं सेब हूँ। क्या आपको पता है खाने के बाद क्या होता है?",
                    "visual_cue": "मुस्कुराता 3D सेब कैरेक्टर चमकते स्पार्कल्स के साथ",
                    "duration": 4.0
                },
                {
                    "on_screen": "पाचन तंत्र को एक्टिव रखिए!",
                    "narration": "खाने के बाद हल्का टहलने से पाचन तंत्र एक्टिव और खुश रहता है!",
                    "subtitle": "हल्का टहलने से पाचन तंत्र एक्टिव और खुश रहता है!",
                    "visual_cue": "सेब और गट कैरेक्टर आपस में बातचीत करते हुए",
                    "duration": 4.5
                },
                {
                    "on_screen": "शुगर स्पाइक 34% घटाइए!",
                    "narration": "रिसर्च में साबित हुआ: 10 मिनट टहलने से शुगर स्पाइक 34% घटता है!",
                    "subtitle": "10 मिनट टहलने से शुगर स्पाइक 34% घटता है!",
                    "visual_cue": "गट कैरेक्टर के आसपास दोस्ताना माइक्रोब्स नाचते हुए",
                    "duration": 5.0
                },
                {
                    "on_screen": "पेट के लिए क्या बेहतर है?",
                    "narration": "क्विज टाइम! अच्छे बैक्टीरिया के लिए क्या बेहतर है? फल या सब्जियां?",
                    "subtitle": "अच्छे बैक्टीरिया के लिए क्या बेहतर है? फल या सब्जियां?",
                    "visual_cue": "सलाद बाउल के साथ कार्टून गर्ल सवाल पूछते हुए",
                    "duration": 5.0
                },
                {
                    "on_screen": "शाबाश! दोनों!",
                    "narration": "दोनों! ये माइक्रोबायोम को पोषण देकर शुगर स्थिर रखते हैं।",
                    "subtitle": "दोनों! ये माइक्रोबायोम को पोषण देकर शुगर स्थिर रखते हैं।",
                    "visual_cue": "हरे चेकमार्क के साथ सेब और गट दोनों जश्न मनाते हुए",
                    "duration": 4.5
                },
                {
                    "on_screen": "मांसपेशियां शुगर सोखती हैं!",
                    "narration": "पैरों की मांसपेशियां बिना पैंक्रियास पर दबाव डाले शुगर सोखती हैं।",
                    "subtitle": "पैरों की मांसपेशियां सीधे ब्लड से शुगर सोखती हैं।",
                    "visual_cue": "स्मूदी पीते हुए थम्स-अप देती कार्टून लड़की",
                    "duration": 5.0
                },
                {
                    "on_screen": "Steer पर और जानिए  ➔",
                    "narration": "आज रात 100 कदम चलिए! Steer पर और हेल्थ टिप्स देखिए।",
                    "subtitle": "आज रात 100 कदम चलिए! Steer पर और टिप्स देखिए।",
                    "visual_cue": "Steer हेल्थ क्लब बैज के साथ ग्रुप आउट्रो",
                    "duration": 4.0
                }
            ]
        },
        "te": {
            "title": "డిన్నర్ తర్వాత 10 నిమిషాల నడక: బ్లడ్ షుగర్ కంట్రోల్ సీక్రెట్",
            "hook": "హేయ్! నేను ఆపిల్. తిన్న వెంటనే శరీరంలో ఏం జరుగుతుందో తెలుసా?",
            "takeaway": "భోజనం తర్వాత 10 నిమిషాలు నడిస్తే రోజంతా గ్లూకోజ్ నియంత్రణలో ఉంటుంది.",
            "caption": "మన పెద్దలు చెప్పిన 'శతపది'ని సైన్స్ కూడా నిరూపించింది! భోజనం తర్వాత 10 నిమిషాలు నడిస్తే షుగర్ స్పైక్ 34% తగ్గుతుంది. ఈ రాత్రే ప్రారంభించండి! 🚶‍♂️🌿",
            "scenes": [
                {
                    "on_screen": "హేయ్! నేను ఆపిల్...",
                    "narration": "హేయ్! నేను ఆపిల్. తిన్న వెంటనే శరీరంలో ఏం జరుగుతుందో తెలుసా?",
                    "subtitle": "హేయ్! నేను ఆపిల్. తిన్న వెంటనే ఏం జరుగుతుందో తెలుసా?",
                    "visual_cue": "మెరిసే ఆపిల్ క్యారెక్టర్ నవ్వుతూ పరిచయం చేసుకుంటోంది",
                    "duration": 4.0
                },
                {
                    "on_screen": "జీర్ణక్రియ చురుగ్గా ఉంటుంది!",
                    "narration": "భోజనం తర్వాత చిన్న నడక జీర్ణవ్యవస్థను చురుగ్గా ఉంచుతుంది!",
                    "subtitle": "చిన్న నడక జీర్ణవ్యవస్థను చురుగ్గా ఉంచుతుంది!",
                    "visual_cue": "ఆపిల్ మరియు గట్ క్యారెక్టర్ సంభాషణ",
                    "duration": 4.5
                },
                {
                    "on_screen": "షుగర్ స్పైక్ 34% తగ్గుతుంది!",
                    "narration": "10 నిమిషాల నడకతో బ్లడ్ షుగర్ స్పైక్ 34% తగ్గుతుందని తేలింది!",
                    "subtitle": "10 నిమిషాల నడకతో షుగర్ స్పైక్ 34% తగ్గుతుంది!",
                    "visual_cue": "మంచి మైక్రోబ్స్‌తో కలిసి సంతోషంగా ఉన్న గట్ క్యారెక్టర్",
                    "duration": 5.0
                },
                {
                    "on_screen": "కడుపుకి ఏది మేలు చేస్తుంది?",
                    "narration": "చిన్న క్విజ్! మంచి బ్యాక్టీరియాకు ఏది మంచిది? పండ్లా లేక కూరగాయలా?",
                    "subtitle": "మంచి బ్యాక్టీరియాకు ఏది మంచిది? పండ్లా కూరగాయలా?",
                    "visual_cue": "సలాడ్ బౌల్‌తో ప్రశ్నిస్తున్న కార్టూన్ అమ్మాయి",
                    "duration": 5.0
                },
                {
                    "on_screen": "సరైన సమాధానం! రెండూ!",
                    "narration": "రెండూ! ఇవి మైక్రోబయోమ్‌కు మేలు చేసి షుగర్‌ను కంట్రోల్ చేస్తాయి.",
                    "subtitle": "రెండూ! ఇవి మైక్రోబయోమ్‌కు మేలు చేసి షుగర్‌ను ఆపుతాయి.",
                    "visual_cue": "గ్రీన్ టిక్‌తో ఆపిల్ మరియు గట్ సంబరాలు",
                    "duration": 4.5
                },
                {
                    "on_screen": "కండరాలు గ్లూకోజ్‌ను పీల్చుకుంటాయి!",
                    "narration": "కాళ్ల కండరాలు ఇన్సులిన్ శ్రమ లేకుండానే గ్లూకోజ్‌ను గ్రహిస్తాయి.",
                    "subtitle": "కాళ్ల కండరాలు నేరుగా గ్లూకోజ్‌ను గ్రహిస్తాయి.",
                    "visual_cue": "స్మూతీ తాగుతూ థంబ్స్-అప్ చూపుతున్న అమ్మాయి",
                    "duration": 5.0
                },
                {
                    "on_screen": "Steer లో మరింత తెలుసుకోండి  ➔",
                    "narration": "ఈ రాత్రే 100 అడుగులు వేయండి! Steer లో మరిన్ని చూడండి.",
                    "subtitle": "రాత్రి 100 అడుగులు వేయండి! Steer లో మరిన్ని చూడండి.",
                    "visual_cue": "Steer క్లబ్ బ్యాడ్జ్‌తో గ్రూప్ ముగింపు",
                    "duration": 4.0
                }
            ]
        },
        "ta": {
            "title": "சாப்பிட்ட பிறகு 10 நிமிடம் நடை: சர்க்கரை அளவைக் கட்டுப்படுத்தும் வழி",
            "hook": "ஹேய்! நான் ஆப்பிள். சாப்பிட்ட உடனே உடம்பில் என்ன நடக்குதுன்னு தெரியுமா?",
            "takeaway": "சாப்பிட்ட உடனே 10 நிமிடம் மெதுவாக நடந்தால் ரத்த சர்க்கரை கட்டுக்குள் இருக்கும்.",
            "caption": "நமது முன்னோர்கள் சொன்ன 'சதபரி' முறையை மருத்துவம் நிரூபித்துள்ளது! சாப்பிட்ட 30 நிமிடத்திற்குள் 10 நிமிடம் நடந்தால் சர்க்கரை உயர்வு 34% குறையும். இன்றே தொடங்குங்கள்! 🩺✨",
            "scenes": [
                {
                    "on_screen": "ஹேய்! நான் ஆப்பிள்...",
                    "narration": "ஹேய்! நான் ஆப்பிள். சாப்பிட்ட உடனே என்ன நடக்குதுன்னு தெரியுமா?",
                    "subtitle": "ஹேய்! நான் ஆப்பிள். சாப்பிட்ட உடனே என்ன நடக்குதுன்னு தெரியுமா?",
                    "visual_cue": "ஒளிரும் 3D ஆப்பிள் கேரக்டர் அறிமுகம்",
                    "duration": 4.0
                },
                {
                    "on_screen": "செரிமானத்தை சுறுசுறுப்பாக்குங்கள்!",
                    "narration": "சாப்பிட்ட பின் லேசாக நடப்பது செரிமானத்தை சுறுசுறுப்பாக்கும்!",
                    "subtitle": "லேசான நடை செரிமானத்தை சுறுசுறுப்பாக்கும்!",
                    "visual_cue": "ஆப்பிள் மற்றும் குடல் கேரக்டர் உரையாடல்",
                    "duration": 4.5
                },
                {
                    "on_screen": "சர்க்கரை உயர்வு 34% குறையும்!",
                    "narration": "10 நிமிடம் நடந்தால் ரத்த சர்க்கரை உயர்வு 34% குறைகிறது!",
                    "subtitle": "10 நிமிடம் நடந்தால் சர்க்கரை உயர்வு 34% குறைகிறது!",
                    "visual_cue": "நல்ல நுண்ணுயிரிகளுடன் நடனமாடும் குடல் கேரக்டர்",
                    "duration": 5.0
                },
                {
                    "on_screen": "வயிற்றுக்கு எது நல்லது?",
                    "narration": "சின்ன வினாடி வினா! நல்ல பாக்டீரியாவுக்கு எது நல்லது? பழங்களா காய்கறிகளா?",
                    "subtitle": "நல்ல பாக்டீரியாவுக்கு எது நல்லது? பழங்களா காய்கறிகளா?",
                    "visual_cue": "சாலட் கிண்ணத்துடன் கேள்வி கேட்கும் கார்ட்டூன் பெண்",
                    "duration": 5.0
                },
                {
                    "on_screen": "சிறப்பான தேர்வு! இரண்டுமே!",
                    "narration": "இரண்டுமே! இவை நுண்ணுயிரிகளுக்கு உணவளித்து சர்க்கரையை சீராக்கும்.",
                    "subtitle": "இரண்டுமே! நுண்ணுயிரிகளுக்கு உணவளித்து சர்க்கரையை சீராக்கும்.",
                    "visual_cue": "பச்சை டிக் குறியுடன் ஆப்பிள் மற்றும் குடல் மகிழ்ச்சி",
                    "duration": 4.5
                },
                {
                    "on_screen": "தசைகள் சர்க்கரையை உறிஞ்சும்!",
                    "narration": "கால்களின் தசைகள் கணைய சுமையின்றி சர்க்கரையை நேரடியாக உறிஞ்சும்.",
                    "subtitle": "கால்களின் தசைகள் சர்க்கரையை நேரடியாக உறிஞ்சும்.",
                    "visual_cue": "ஸ்மூத்தி குடித்து தம்ப்ஸ்-அப் காட்டும் பெண்",
                    "duration": 5.0
                },
                {
                    "on_screen": "Steer-ல் மேலும் அறிய  ➔",
                    "narration": "இன்றே 100 அடிகள் நடங்கள்! Steer-ல் மேலும் பல குறிப்புகளை அறியுங்கள்.",
                    "subtitle": "இன்று 100 அடிகள் நடங்கள்! Steer-ல் அறியுங்கள்.",
                    "visual_cue": "Steer பேட்ஜுடன் குழு இறுதி காட்சி",
                    "duration": 4.0
                }
            ]
        },
        "kn": {
            "title": "ಊಟದ ನಂತರ 10 ನಿಮಿಷ ವಾಕಿಂಗ್: ಬ್ಲಡ್ ಶುಗರ್ ನಿಯಂತ್ರಿಸುವ ಸೂತ್ರ",
            "hook": "ಹೇ! ನಾನು ಸೇಬು. ಊಟವಾದ ತಕ್ಷಣ ನಮ್ಮ ದೇಹದಲ್ಲಿ ಏನಾಗುತ್ತದೆ ಗೊತ್ತಾ?",
            "takeaway": "ಊಟದ ನಂತರ 10 ನಿಮಿಷ ಶಾಂತವಾಗಿ ನಡೆದರೆ ಗ್ಲೂಕೋಸ್ ಸ್ಪೈಕ್ ನಿಯಂತ್ರಣದಲ್ಲಿರುತ್ತದೆ.",
            "caption": "ನಮ್ಮ ಹಿರಿಯರ ಶತಪದಿ ಸಂಪ್ರದಾಯವನ್ನು ವಿಜ್ಞಾನ ಸಾಬೀತುಪಡಿಸಿದೆ! ಊಟವಾದ ತಕ್ಷಣ 10 ನಿಮಿಷ ನಡೆದರೆ ಶುಗರ್ ಸ್ಪೈಕ್ 34% ಕಡಿಮೆಯಾಗುತ್ತದೆ. ಇಂದೇ ಟ್ರೈ ಮಾಡಿ! 🚶‍♂️🌿",
            "scenes": [
                {
                    "on_screen": "ಹೇ! ನಾನು ಸೇಬು...",
                    "narration": "ಹೇ! ನಾನು ಸೇಬು. ಊಟವಾದ ತಕ್ಷಣ ದೇಹದಲ್ಲಿ ಏನಾಗುತ್ತದೆ ಗೊತ್ತಾ?",
                    "subtitle": "ಹೇ! ನಾನು ಸೇಬು. ಊಟವಾದ ತಕ್ಷಣ ಏನಾಗುತ್ತದೆ ಗೊತ್ತಾ?",
                    "visual_cue": "ಹೊಳೆಯುವ 3D ಸೇಬಿನ ಪಾತ್ರ ಪರಿಚಯ",
                    "duration": 4.0
                },
                {
                    "on_screen": "ಜೀರ್ಣಕ್ರಿಯೆ ಚುರುಕಾಗಿರಿಸಿಕೊಳ್ಳಿ!",
                    "narration": "ಊಟದ ನಂತರ ಸ್ವಲ್ಪ ನಡೆದರೆ ಜೀರ್ಣಕ್ರಿಯೆ ಚುರುಕಾಗಿರುತ್ತದೆ!",
                    "subtitle": "ಸ್ವಲ್ಪ ನಡಿಗೆ ಜೀರ್ಣಕ್ರಿಯೆಯನ್ನು ಚುರುಕಾಗಿರಿಸುತ್ತದೆ!",
                    "visual_cue": "ಸೇಬು ಮತ್ತು ಕರುಳಿನ ಪಾತ್ರಗಳ ಮಾತುಕತೆ",
                    "duration": 4.5
                },
                {
                    "on_screen": "ಸಕ್ಕರೆ ಸ್ಪೈಕ್ 34% ಕಡಿಮೆ!",
                    "narration": "10 ನಿಮಿಷ ವಾಕಿಂಗ್ ಮಾಡುವುದರಿಂದ ಸಕ್ಕರೆ ಸ್ಪೈಕ್ 34% ಕಡಿಮೆಯಾಗುತ್ತದೆ!",
                    "subtitle": "10 ನಿಮಿಷ ನಡೆದರೆ ಸಕ್ಕರೆ ಸ್ಪೈಕ್ 34% ಕಡಿಮೆಯಾಗುತ್ತದೆ!",
                    "visual_cue": "ಒಳ್ಳೆಯ ಸೂಕ್ಷ್ಮಜೀವಿಗಳೊಂದಿಗೆ ನಲಿಯುವ ಕರುಳಿನ ಪಾತ್ರ",
                    "duration": 5.0
                },
                {
                    "on_screen": "ಹೊಟ್ಟೆಗೆ ಯಾವುದು ಉತ್ತಮ?",
                    "narration": "ಸಣ್ಣ ಕ್ವಿಜ್! ಒಳ್ಳೆಯ ಬ್ಯಾಕ್ಟೀರಿಯಾಗಳಿಗೆ ಯಾವುದು ಉತ್ತಮ? ಹಣ್ಣುಗಳಾ ತರಕಾರಿಗಳಾ?",
                    "subtitle": "ಒಳ್ಳೆಯ ಬ್ಯಾಕ್ಟೀರಿಯಾಗಳಿಗೆ ಯಾವುದು ಉತ್ತಮ? ಹಣ್ಣುಗಳಾ ತರಕಾರಿಗಳಾ?",
                    "visual_cue": "ಸಲಾಡ್ ಬಟ್ಟಲಿನೊಂದಿಗೆ ಪ್ರಶ್ನಿಸುವ ಕಾರ್ಟೂನ್ ಹುಡುಗಿ",
                    "duration": 5.0
                },
                {
                    "on_screen": "ಉತ್ತಮ ಆಯ್ಕೆ! ಎರಡೂ!",
                    "narration": "ಎರಡೂ! ಇವು ಮೈಕ್ರೋಬಯೋಮ್‌ಗೆ ಶಕ್ತಿ ನೀಡಿ ಸಕ್ಕರೆಯನ್ನು ನಿಯಂತ್ರಿಸುತ್ತವೆ.",
                    "subtitle": "ಎರಡೂ! ಇವು ಮೈಕ್ರೋಬಯೋಮ್‌ಗೆ ಶಕ್ತಿ ನೀಡಿ ಸಕ್ಕರೆ ನಿಯಂತ್ರಿಸುತ್ತವೆ.",
                    "visual_cue": "ಹಸಿರು ಚಿಹ್ನೆಯೊಂದಿಗೆ ಸೇಬು ಮತ್ತು ಕರುಳಿನ ಸಂಭ್ರಮ",
                    "duration": 4.5
                },
                {
                    "on_screen": "ಸ್ನಾಯುಗಳು ಸಕ್ಕರೆ ಹೀರಿಕೊಳ್ಳುತ್ತವೆ!",
                    "narration": "ಸ್ನಾಯುಗಳು ಪ್ಯಾಂಕ್ರಿಯಾಸ್ ಶ್ರಮವಿಲ್ಲದೆ ಸಕ್ಕರೆಯನ್ನು ನೇರವಾಗಿ ಹೀರಿಕೊಳ್ಳುತ್ತವೆ.",
                    "subtitle": "ಸ್ನಾಯುಗಳು ಸಕ್ಕರೆಯನ್ನು ನೇರವಾಗಿ ಹೀರಿಕೊಳ್ಳುತ್ತವೆ.",
                    "visual_cue": "ಸ್ಮೂಥಿ ಕುಡಿಯುತ್ತಾ ಹೆಬ್ಬೆರಳು ತೋರಿಸುವ ಹುಡುಗಿ",
                    "duration": 5.0
                },
                {
                    "on_screen": "Steer ನಲ್ಲಿ ಇನ್ನಷ್ಟು ತಿಳಿಯಿರಿ  ➔",
                    "narration": "ಇಂದೇ 100 ಹೆಜ್ಜೆ ಹಾಕಿ! Steer ನಲ್ಲಿ ಇನ್ನಷ್ಟು ತಿಳಿಯಿರಿ.",
                    "subtitle": "ಇಂದೇ 100 ಹೆಜ್ಜೆ ಹಾಕಿ! Steer ನಲ್ಲಿ ತಿಳಿಯಿರಿ.",
                    "visual_cue": "Steer ಬ್ಯಾಡ್ಜ್‌ನೊಂದಿಗೆ ಗ್ರೂಪ್ ಔಟ್ರೋ",
                    "duration": 4.0
                }
            ]
        },
        "ml": {
            "title": "അത്താഴത്തിന് ശേഷം 10 മിനിറ്റ് നടത്തം: ഷുഗർ സ്പൈക്ക് തടയാൻ എളുപ്പവഴി",
            "hook": "ഹേയ്! ഞാൻ ആപ്പിൾ. ഭക്ഷണത്തിന് ശേഷം ശരീരത്തിൽ എന്ത് സംഭവിക്കുന്നു എന്ന് അറിയാമോ?",
            "takeaway": "ഭക്ഷണത്തിന് ശേഷം 10 മിനിറ്റ് നടന്നാൽ രക്തത്തിലെ പഞ്ചസാരയുടെ അളവ് നിയന്ത്രിക്കാം.",
            "caption": "നമ്മുടെ പൂർവ്വികർ പറഞ്ഞ 'ശതപദി' ആധുനിക വൈദ്യശാസ്ത്രം ശരിവെച്ചിരിക്കുന്നു! ഭക്ഷണത്തിന് ശേഷം 10 മിനിറ്റ് നടന്നാൽ ഷുഗർ സ്പൈക്ക് 34% കുറയും. ഇന്നുതന്നെ തുടങ്ങൂ! 🩺✨",
            "scenes": [
                {
                    "on_screen": "ഹേയ്! ഞാൻ ആപ്പിൾ...",
                    "narration": "ഹേയ്! ഞാൻ ആപ്പിൾ. ഭക്ഷണത്തിന് ശേഷം എന്ത് സംഭവിക്കുന്നു എന്ന് അറിയാമോ?",
                    "subtitle": "ഹേയ്! ഞാൻ ആപ്പിൾ. ഭക്ഷണത്തിന് ശേഷം എന്ത് സംഭവിക്കുന്നു എന്ന് അറിയാമോ?",
                    "visual_cue": "തിളങ്ങുന്ന 3D ആപ്പിൾ കഥാപാത്രത്തിന്റെ ആമുഖം",
                    "duration": 4.0
                },
                {
                    "on_screen": "ദഹനം സജീവമാക്കൂ!",
                    "narration": "ഭക്ഷണത്തിന് ശേഷമുള്ള ലഘുവായ നടത്തം ദഹനത്തെ സജീവമാക്കുന്നു!",
                    "subtitle": "ലഘുവായ നടത്തം ദഹനവ്യവസ്ഥയെ സജീവമാക്കുന്നു!",
                    "visual_cue": "ആപ്പിളും കുടലും തമ്മിലുള്ള സംഭാഷണം",
                    "duration": 4.5
                },
                {
                    "on_screen": "ഷുഗർ സ്പൈക്ക് 34% കുറയ്ക്കൂ!",
                    "narration": "10 മിനിറ്റ് നടന്നാൽ ഗ്ലൂക്കോസ് സ്പൈക്ക് 34% കുറയുമെന്ന് പഠനം!",
                    "subtitle": "10 മിനിറ്റ് നടന്നാൽ ഗ്ലൂക്കോസ് സ്പൈക്ക് 34% കുറയും!",
                    "visual_cue": "നല്ല സൂക്ഷ്മാണുക്കളോടൊപ്പം നൃത്തം ചെയ്യുന്ന കുടൽ കഥാപാത്രം",
                    "duration": 5.0
                },
                {
                    "on_screen": "വയറിന് ഏറ്റവും നല്ലത് ഏതാണ്?",
                    "narration": "ക്വിസ് ടൈം! നല്ല ബാക്ടീരിയകൾക്ക് നല്ലത് ഏതാണ്? പഴങ്ങളോ പച്ചക്കറികളോ?",
                    "subtitle": "നല്ല ബാക്ടീരിയകൾക്ക് നല്ലത് ഏതാണ്? പഴങ്ങളോ പച്ചക്കറികളോ?",
                    "visual_cue": "സാലഡ് ബൗളുമായി ചോദ്യം ചോദിക്കുന്ന കാർട്ടൂൺ പെൺകുട്ടി",
                    "duration": 5.0
                },
                {
                    "on_screen": "മികച്ച തിരഞ്ഞെടുപ്പ്! രണ്ടും!",
                    "narration": "രണ്ടും! ഇവ മൈക്രോബയോമിന് കരുത്തേകി പഞ്ചസാര ക്രമീകരിക്കുന്നു.",
                    "subtitle": "രണ്ടും! ഇവ മൈക്രോബയോമിന് കരുത്തേകി പഞ്ചസാര ക്രമീകരിക്കുന്നു.",
                    "visual_cue": "പച്ച ടിക്കോടെ ആപ്പിളും കുടലും ആഘോഷിക്കുന്നു",
                    "duration": 4.5
                },
                {
                    "on_screen": "പേശികൾ പഞ്ചസാര ആഗിരണം ചെയ്യുന്നു!",
                    "narration": "കാലിലെ പേശികൾ ഇൻസുലിൻ ആവശ്യമില്ലാതെ പഞ്ചസാര നേരിട്ട് ആഗിരണം ചെയ്യുന്നു.",
                    "subtitle": "പേശികൾ പഞ്ചസാര നേരിട്ട് ആഗിരണം ചെയ്യുന്നു.",
                    "visual_cue": "സ്മൂത്തി കുടിച്ച് തമ്പ്സ്-അപ്പ് കാട്ടുന്ന പെൺകുട്ടി",
                    "duration": 5.0
                },
                {
                    "on_screen": "Steer-ൽ കൂടുതൽ അറിയൂ  ➔",
                    "narration": "ഇന്ന് 100 ചുവടുകൾ വെക്കൂ! Steer-ൽ കൂടുതൽ അറിയൂ.",
                    "subtitle": "ഇന്ന് 100 ചുവടുകൾ വെക്കൂ! Steer-ൽ കൂടുതൽ അറിയൂ.",
                    "visual_cue": "Steer ക്ലബ് ബാഡ്ജോടെ ഗ്രൂപ്പ് ഔട്രോ",
                    "duration": 4.0
                }
            ]
        }
    }

    lang_data = scripts.get(language, scripts["en"])

    scenes_list = []
    total_time = 0.0
    for idx, item in enumerate(lang_data["scenes"]):
        dur = item.get("duration", 5.5)
        total_time += dur
        scenes_list.append({
            "scene_number": idx + 1,
            "duration_seconds": dur,
            "visual_cue": item["visual_cue"],
            "on_screen_text": item["on_screen"],
            "narration": item["narration"],
            "subtitle_text": item["subtitle"],
            "visual_style": "talking_characters",
            "visual_theme": visual_theme,
            "animation_action": "talking_character" if idx in [0, 1, 2, 4, 6] else "everyday",
            "character_name": "Dr. Amla" if idx in [0, 1, 4] else None,
            "claim_ids": [primary_clm] if idx < 3 else ([c2] if idx < 5 else clm_ids)
        })

    return {
        "reel_title": lang_data["title"],
        "hook": lang_data["hook"],
        "target_duration_seconds": int(total_time),
        "mode": "everyday",
        "visual_style": "talking_characters",
        "visual_theme": visual_theme,
        "language": language,
        "voice_name": voice_name,
        "scenes": scenes_list,
        "practical_takeaway": lang_data["takeaway"],
        "caption": lang_data["caption"],
        "hashtags": ["#MetabolicHealth", "#SteerHealth", "#Shatapadi", "#BloodSugar", "#HealthHabits"],
        "claim_ids": clm_ids,
        "source_citation": f"Source: {paper_title[:45]} (n=48)"
    }

get_talking_characters_storyboard = get_everyday_reel_storyboard


def get_everyday_human_storyboard(
    language: str,
    claims: Optional[List[Dict[str, Any]]],
    paper_title: str,
    voice_name: str,
    visual_theme: str = "warm_editorial"
) -> Dict[str, Any]:
    if not is_sample_walk_paper(paper_title):
        return _build_dynamic_paper_storyboard("everyday_human", language, claims, paper_title, voice_name, visual_theme)

    clm_ids = [c.get("claim_id", f"CLM-{i+1:03d}") for i, c in enumerate(claims)] if claims else ["CLM-001", "CLM-002", "CLM-003"]
    primary_clm = clm_ids[0] if clm_ids else "CLM-001"
    c2 = clm_ids[1] if len(clm_ids) > 1 else primary_clm
    c3 = clm_ids[2] if len(clm_ids) > 2 else primary_clm

    scripts = {
        "en": {
            "title": "Everyday Human: The Real-Life 10-Minute Post-Dinner Routine",
            "hook": "Just finished dinner? Don't sink into the couch yet—here is your 15-minute window.",
            "takeaway": "Take a 10-minute relaxed stroll on the terrace or balcony right after meals to blunt glucose spikes.",
            "caption": "Real-life metabolic routine: Stepping away from the dining table for a gentle 10-minute walk cuts glucose spikes by 34%. Make Shatapadi your evening habit! 🚶‍♂️🌇",
            "scenes": [
                {
                    "scene_role": "dinner_table",
                    "on_screen": "Dinner Finished... Couch or Walk?",
                    "narration": "Just finished a comforting dinner? Sitting straight on the couch lets glucose surge rapidly into your bloodstream.",
                    "subtitle": "Just finished dinner? Couch inertia spikes blood sugar.",
                    "visual_cue": "Warm dining table with evening dinner plate, dal-chawal, and an animated dilemma indicator",
                    "duration": 5.0
                },
                {
                    "scene_role": "smartwatch",
                    "on_screen": "Smartwatch Alert: 15m Window",
                    "narration": "Your smartwatch buzzes: the golden fifteen to thirty minute metabolic window is open right now.",
                    "subtitle": "Smartwatch reminder: The 15-30 min golden window is open.",
                    "visual_cue": "Sleek smartwatch on wrist vibrating with gentle pulse waves showing 15-min post-meal alert",
                    "duration": 5.0
                },
                {
                    "scene_role": "terrace_walk",
                    "on_screen": "Terrace Walk: 75 Steps / Min",
                    "narration": "Step out onto the terrace or balcony. Just ten minutes of relaxed, conversational pacing is all it takes.",
                    "subtitle": "A gentle 10-minute stroll on the terrace at 75 steps/min.",
                    "visual_cue": "Peaceful evening terrace walk under twilight stars with smooth walking strides and railing",
                    "duration": 5.5
                },
                {
                    "scene_role": "clock_timing",
                    "on_screen": "Timing Matters: 3x More Effective",
                    "narration": "Timing is critical: walking within thirty minutes gives triple the glycemic benefit compared to waiting an hour.",
                    "subtitle": "Walking within 30 mins is 3x more effective than waiting 60 mins.",
                    "visual_cue": "Ticking clock comparing immediate 30-min window versus delayed 60-min movement",
                    "duration": 5.0
                },
                {
                    "scene_role": "habit_success",
                    "on_screen": "Spike Flattened By 34%!",
                    "narration": "Clinical trials confirm a 34% drop in peak glucose elevation. Practice traditional Shatapadi tonight with Steer!",
                    "subtitle": "Clinical evidence: Peak glucose spike reduced by 34%.",
                    "visual_cue": "Glowing green checkmark celebration with CGM spike flattened card and Steer lifestyle badge",
                    "duration": 4.5
                }
            ]
        },
        "hi": {
            "title": "एवरीडे रूटीन: डिनर के बाद 10 मिनट की आसान आदत",
            "hook": "डिनर खत्म हुआ? सोफे पर मत बैठिए—यह 15 मिनट का सबसे अहम समय है।",
            "takeaway": "खाने के तुरंत बाद बालकनी या छत पर 10 मिनट टहलने से शुगर स्पाइक 34% घटती है।",
            "caption": "रोज़मर्रा की सेहत: डिनर के बाद सीधे सोफे पर बैठने के बजाय 10 मिनट टहलिए और शुगर स्पाइक 34% कम कीजिए। शतपदी अपनाएं! 🚶‍♂️🩺",
            "scenes": [
                {
                    "scene_role": "dinner_table",
                    "on_screen": "खाना खत्म... सोफा या वॉक?",
                    "narration": "अभी-अभी स्वादिष्ट डिनर किया है? सीधे सोफे पर बैठ जाने से ब्लड शुगर तेजी से बढ़ सकती है।",
                    "subtitle": "डिनर के बाद सोफे पर बैठना शुगर बढ़ाता है।",
                    "visual_cue": "डाइनिंग टेबल पर दाल-चावल की थाली और वॉक का विकल्प",
                    "duration": 5.0
                },
                {
                    "scene_role": "smartwatch",
                    "on_screen": "स्मार्टवॉच अलर्ट: 15 मिनट विंडो",
                    "narration": "स्मार्टवॉच का अलर्ट: खाने के बाद 15 से 30 मिनट का सबसे अहम समय शुरू हो चुका है!",
                    "subtitle": "स्मार्टवॉच अलर्ट: 15-30 मिनट का समय शुरू!",
                    "visual_cue": "कलाई पर स्मार्टवॉच वाइब्रेट करते हुए 15 मिनट का अलर्ट दिखाते हुए",
                    "duration": 5.0
                },
                {
                    "scene_role": "terrace_walk",
                    "on_screen": "छत पर 10 मिनट की चहलकदमी",
                    "narration": "छत या बालकनी पर टहलें। सिर्फ 10 मिनट आराम से चलना ही आपके ग्लूकोज को काबू में रखता है।",
                    "subtitle": "बालकनी या छत पर 10 मिनट आराम से टहलें।",
                    "visual_cue": "तारों भरी रात में छत पर टहलता हुआ व्यक्ति",
                    "duration": 5.5
                },
                {
                    "scene_role": "clock_timing",
                    "on_screen": "समय का महत्व: 3 गुना असरदार",
                    "narration": "सही समय ज़रूरी है: 30 मिनट के अंदर टहलना, एक घंटे बाद चलने से 3 गुना ज़्यादा असरदार है।",
                    "subtitle": "30 मिनट के अंदर चलना 3 गुना ज़्यादा फायदेमंद है।",
                    "visual_cue": "घड़ी का कांटा घूमते हुए समय का अंतर समझाते हुए",
                    "duration": 5.0
                },
                {
                    "scene_role": "habit_success",
                    "on_screen": "शुगर स्पाइक 34% कम!",
                    "narration": "रिसर्च में साबित हुआ: 34% शुगर स्पाइक कम होती है। आज रात शतपदी अपनाएं Steer के साथ!",
                    "subtitle": "क्लिनिकल रिसर्च: शुगर स्पाइक 34% तक कम!",
                    "visual_cue": "हरा टिक मार्क और CGM चार्ट पर 34% गिरावट का कार्ड",
                    "duration": 4.5
                }
            ]
        },
        "te": {
            "title": "రోజువారీ అలవాటు: రాత్రి భోజనం తర్వాత 10 నిమిషాల నడక",
            "hook": "భోజనం ముగిసిందా? వెంటనే సోఫాలో వాలకండి—ఈ 15 నిమిషాలు చాలా కీలకం.",
            "takeaway": "భోజనం తర్వాత బాల్కనీలో 10 నిమిషాలు నడిస్తే బ్లడ్ షుగర్ 34% తగ్గుతుంది.",
            "caption": "మన పెద్దల శతపది నిరూపించబడింది! భోజనం తర్వాత 10 నిమిషాల నడకతో షుగర్ స్పైక్ 34% తగ్గుతుంది. ఈ రాత్రే మొదలుపెట్టండి! 🚶‍♂️🌿",
            "scenes": [
                {
                    "scene_role": "dinner_table",
                    "on_screen": "భోజనం ముగిసింది... సోఫానా లేక నడకా?",
                    "narration": "రుచికరమైన భోజనం పూర్తి చేశారా? వెంటనే సోఫాలో కూర్చుంటే బ్లడ్ షుగర్ వేగంగా పెరుగుతుంది.",
                    "subtitle": "భోజనం తర్వాత వెంటనే కూర్చుంటే షుగర్ పెరుగుతుంది.",
                    "visual_cue": "డైనింగ్ టేబుల్ వద్ద రాత్రి భోజనం ప్లేట్ మరియు నడక ఆలోచన",
                    "duration": 5.0
                },
                {
                    "scene_role": "smartwatch",
                    "on_screen": "స్మార్ట్‌వాచ్ అలర్ట్: 15 నిమిషాల సమయం",
                    "narration": "స్మార్ట్‌వాచ్ అలర్ట్: భోజనం తర్వాత 15 నుండి 30 నిమిషాల ముఖ్యమైన సమయం మొదలైంది!",
                    "subtitle": "స్మార్ట్‌వాచ్ అలర్ట్: 15-30 నిమిషాల సమయం మొదలైంది!",
                    "visual_cue": "చేతి వాచ్ వైబ్రేట్ అవుతూ నడక సమయాన్ని సూచించడం",
                    "duration": 5.0
                },
                {
                    "scene_role": "terrace_walk",
                    "on_screen": "టెర్రస్‌పై 10 నిమిషాల ప్రశాంత నడక",
                    "narration": "బాల్కనీ లేదా టెర్రస్‌పై నడవండి. కేవలం 10 నిమిషాల సులువైన నడక చాలు.",
                    "subtitle": "బాల్కనీలో 10 నిమిషాలు ప్రశాంతంగా నడవండి.",
                    "visual_cue": "ఆకాశం కింద టెర్రస్‌పై నడుస్తున్న దృశ్యం",
                    "duration": 5.5
                },
                {
                    "scene_role": "clock_timing",
                    "on_screen": "సమయం ముఖ్యం: 3 రెట్లు ఎక్కువ మేలు",
                    "narration": "సమయం ముఖ్యం: గంట తర్వాత కంటే 30 నిమిషాలలోపు నడవడం 3 రెట్లు ఎక్కువ మేలు చేస్తుంది.",
                    "subtitle": "30 నిమిషాల లోపు నడవడం 3 రెట్లు ఎక్కువ మేలు.",
                    "visual_cue": "గడియారంలో సమయ వ్యత్యాసాన్ని చూపే గ్రాఫిక్స్",
                    "duration": 5.0
                },
                {
                    "scene_role": "habit_success",
                    "on_screen": "షుగర్ స్పైక్ 34% తగ్గింది!",
                    "narration": "క్లినికల్ రీసెర్చ్ ప్రకారం షుగర్ స్పైక్ 34% తగ్గుతుంది. ఈ రాత్రే శతపది ప్రారంభించండి!",
                    "subtitle": "రీసెర్చ్ నిరూపణ: షుగర్ స్పైక్ 34% తగ్గింది!",
                    "visual_cue": "గ్రీన్ టిక్ మార్క్ మరియు 34% తగ్గుదల చూపే కార్డ్",
                    "duration": 4.5
                }
            ]
        },
        "ta": {
            "title": "தினசரி பழக்கம்: இரவு உணவுக்குப் பின் 10 நிமிட நடைப்பயிற்சி",
            "hook": "சாப்பிட்டு முடித்தீர்களா? உடனே சோபாவில் அமராதீர்கள்—இந்த 15 நிமிடம் மிக முக்கியம்.",
            "takeaway": "சாப்பிட்ட உடனே 10 நிமிடம் மெதுவாக நடந்தால் ரத்த சர்க்கரை உயர்வு 34% குறையும்.",
            "caption": "சாப்பிட்ட 30 நிமிடத்திற்குள் 10 நிமிடம் மெதுவாக நடந்தால் ரத்த சர்க்கரை உயர்வு 34% குறையும். சதபரி பழக்கத்தை இன்றே தொடங்குங்கள்! 🩺✨",
            "scenes": [
                {
                    "scene_role": "dinner_table",
                    "on_screen": "உணவு முடிந்தது... சோபாவா அல்லது நடையா?",
                    "narration": "சுவையான உணவை முடித்துவிட்டீர்களா? உடனே சோபாவில் அமர்ந்தால் ரத்த சர்க்கரை வேகமாக உயரும்.",
                    "subtitle": "சாப்பிட்டவுடன் சோபாவில் அமர்வது சர்க்கரையை உயர்த்தும்.",
                    "visual_cue": "இரவு உணவு தட்டு மற்றும் நடப்பதா அமர்வதா என்ற தேர்வு",
                    "duration": 5.0
                },
                {
                    "scene_role": "smartwatch",
                    "on_screen": "ஸ்மார்ட்வாட்ச் நினைவூட்டல்: 15 நிமிட நேரம்",
                    "narration": "ஸ்மார்ட்வாட்ச் நினைவூட்டல்: சாப்பிட்ட 15 முதல் 30 நிமிட முக்கிய நேரம் துவங்கிவிட்டது!",
                    "subtitle": "ஸ்மார்ட்வாட்ச் நினைவூட்டல்: 15-30 நிமிட நேரம் துவங்கியது!",
                    "visual_cue": "ஸ்மார்ட்வாட்ச் அதிர்வுடன் நடப்பதற்கான அழைப்பு விடுத்தல்",
                    "duration": 5.0
                },
                {
                    "scene_role": "terrace_walk",
                    "on_screen": "மாடியில் 10 நிமிட நடைப்பயிற்சி",
                    "narration": "மாடி அல்லது பால்கனியில் 10 நிமிடம் மிதமான வேகத்தில் நடங்கள்.",
                    "subtitle": "மாடியில் 10 நிமிடம் மெதுவாக நடங்கள்.",
                    "visual_cue": "இரவு வானத்தின் கீழ் மாடியில் அமைதியாக நடக்கும் காட்சி",
                    "duration": 5.5
                },
                {
                    "scene_role": "clock_timing",
                    "on_screen": "நேரத்தின் முக்கியத்துவம்: 3 மடங்கு பலன்",
                    "narration": "சரியான நேரம் முக்கியம்: ஒரு மணி நேரம் கழித்து நடப்பதை விட 30 நிமிடத்தில் நடப்பது 3 மடங்கு பலன் தரும்.",
                    "subtitle": "30 நிமிடத்தில் நடப்பது 3 மடங்கு அதிக பலன் தரும்.",
                    "visual_cue": "கடிகார முள் சுழன்று நேரத்தின் முக்கியத்துவத்தை விளக்குதல்",
                    "duration": 5.0
                },
                {
                    "scene_role": "habit_success",
                    "on_screen": "சர்க்கரை உயர்வு 34% குறைந்தது!",
                    "narration": "ஆய்வுப்படி சர்க்கரை உயர்வு 34% குறைகிறது. இன்றே சதபரி பழக்கத்தை Steer உடன் துவங்குங்கள்!",
                    "subtitle": "மருத்துவ உண்மை: சர்க்கரை உயர்வு 34% குறைகிறது!",
                    "visual_cue": "வெற்றி காட்டும் பச்சை டிக் மற்றும் 34% குறைவு அட்டை",
                    "duration": 4.5
                }
            ]
        },
        "kn": {
            "title": "ದೈನಂದಿನ ಅಭ್ಯಾಸ: ಊಟದ ನಂತರ 10 ನಿಮಿಷ ವಾಕಿಂಗ್",
            "hook": "ಊಟ ಮುಗಿಸಿದಿರಾ? ತಕ್ಷಣ ಸೋಫಾದಲ್ಲಿ ಕುಳಿತುಕೊಳ್ಳಬೇಡಿ—ಈ 15 ನಿಮಿಷ ಬಹುಮುಖ್ಯ.",
            "takeaway": "ಊಟವಾದ ತಕ್ಷಣ 10 ನಿಮಿಷ ಆರಾಮವಾಗಿ ಹೆಜ್ಜೆ ಹಾಕಿದರೆ ಶುಗರ್ ಸ್ಪೈಕ್ 34% ಕಡಿಮೆಯಾಗುತ್ತದೆ.",
            "caption": "ನಮ್ಮ ಹಿರಿಯರ ಶತಪದಿ ಸಾಬೀತಾಗಿದೆ! ಊಟದ ನಂತರ 10 ನಿಮಿಷ ಹೆಜ್ಜೆ ಹಾಕಿದರೆ ಶುಗರ್ ಸ್ಪೈಕ್ 34% ಕಡಿಮೆಯಾಗುತ್ತದೆ. ಇಂದೇ ರೂಢಿಸಿಕೊಳ್ಳಿ! 🚶‍♂️🌿",
            "scenes": [
                {
                    "scene_role": "dinner_table",
                    "on_screen": "ಊಟ ಮುಗಿಯಿತು... ಸೋಫಾ ಅಥವಾ ವಾಕ್?",
                    "narration": "ರುಚಿಯಾದ ಊಟ ಮುಗಿಸಿದಿರಾ? ತಕ್ಷಣ ಸೋಫಾದಲ್ಲಿ ಕುಳಿತರೆ ರಕ್ತದಲ್ಲಿ ಸಕ್ಕರೆ ವೇಗವಾಗಿ ಹೆಚ್ಚುತ್ತದೆ.",
                    "subtitle": "ಊಟದ ನಂತರ ತಕ್ಷಣ ಕುಳಿತರೆ ಸಕ್ಕರೆ ಮಟ್ಟ ಹೆಚ್ಚುತ್ತದೆ.",
                    "visual_cue": "ಊಟದ ತಟ್ಟೆ ಮತ್ತು ನಡಿಗೆಯ ಆಯ್ಕೆ ತೋರಿಸುವ ದೃಶ್ಯ",
                    "duration": 5.0
                },
                {
                    "scene_role": "smartwatch",
                    "on_screen": "ಸ್ಮಾರ್ಟ್‌ವಾಚ್ ಎಚ್ಚರಿಕೆ: 15 ನಿಮಿಷದ ಅವಕಾಶ",
                    "narration": "ಸ್ಮಾರ್ಟ್‌ವಾಚ್ ಎಚ್ಚರಿಕೆ: ಊಟದ ನಂತರದ 15 ರಿಂದ 30 ನಿಮಿಷಗಳ ಸುವರ್ಣಾವಕಾಶ ಶುರುವಾಗಿದೆ!",
                    "subtitle": "ಸ್ಮಾರ್ಟ್‌ವಾಚ್ ಎಚ್ಚರಿಕೆ: 15-30 ನಿಮಿಷದ ಗೋಲ್ಡನ್ ವಿಂಡೋ!",
                    "visual_cue": "ಕೈಗಡಿಯಾರ ವೈಬ್ರೇಟ್ ಆಗುತ್ತಾ ನಡಿಗೆಯ ಸೂಚನೆ ನೀಡುವುದು",
                    "duration": 5.0
                },
                {
                    "scene_role": "terrace_walk",
                    "on_screen": "ತಾರಸಿಯ ಮೇಲೆ 10 ನಿಮಿಷ ಹೆಜ್ಜೆ ಹಾಕಿ",
                    "narration": "ಬಾಲ್ಕನಿ ಅಥವಾ ತಾರಸಿಯಲ್ಲಿ ಕೇವಲ 10 ನಿಮಿಷ ಆರಾಮವಾಗಿ ಹೆಜ್ಜೆ ಹಾಕಿ.",
                    "subtitle": "ತಾರಸಿಯ ಮೇಲೆ 10 ನಿಮಿಷ ಆರಾಮವಾಗಿ ಹೆಜ್ಜೆ ಹಾಕಿ.",
                    "visual_cue": "ರಾತ್ರಿಯ ತಂಪಿನಲ್ಲಿ ತಾರಸಿಯ ಮೇಲೆ ವಾಕಿಂಗ್ ಮಾಡುವ ದೃಶ್ಯ",
                    "duration": 5.5
                },
                {
                    "scene_role": "clock_timing",
                    "on_screen": "ಸಮಯ ಮುಖ್ಯ: 3 ಪಟ್ಟು ಹೆಚ್ಚು ಲಾಭ",
                    "narration": "ಸಮಯ ಮುಖ್ಯ: ಒಂದು ಗಂಟೆ ನಂತರಕ್ಕಿಂತ 30 ನಿಮಿಷದೊಳಗೆ ಹೆಜ್ಜೆ ಹಾಕುವುದು 3 ಪಟ್ಟು ಹೆಚ್ಚು ಪರಿಣಾಮಕಾರಿ.",
                    "subtitle": "30 ನಿಮಿಷದೊಳಗೆ ನಡೆಯುವುದು 3 ಪಟ್ಟು ಹೆಚ್ಚು ಲಾಭದಾಯಕ.",
                    "visual_cue": "ಗಡಿಯಾರದ ಮುಳ್ಳು ತಿರುಗುತ್ತಾ ಸಮಯದ ಮಹತ್ವ ತಿಳಿಸುವುದು",
                    "duration": 5.0
                },
                {
                    "scene_role": "habit_success",
                    "on_screen": "ಶುಗರ್ ಸ್ಪೈಕ್ 34% ಕಡಿಮೆ!",
                    "narration": "ಕ್ಲಿನಿಕಲ್ ಟ್ರಯಲ್‌ನಲ್ಲಿ ಶುಗರ್ ಸ್ಪೈಕ್ 34% ಕಡಿಮೆಯಾಗಿದೆ. ಇಂದೇ ಶತಪದಿ ರೂಢಿಸಿಕೊಳ್ಳಿ!",
                    "subtitle": "ಸಂಶೋಧನೆ ಸಾಬೀತು: ಶುಗರ್ ಸ್ಪೈಕ್ 34% ಕಡಿಮೆ!",
                    "visual_cue": "ಹಸಿರು ಟಿಕ್ ಮಾರ್ಕ್ ಮತ್ತು 34% ಇಳಿಕೆ ಕಾರ್ಡ್",
                    "duration": 4.5
                }
            ]
        },
        "ml": {
            "title": "ദൈനംദിന ശീലം: ഭക്ഷണത്തിന് ശേഷം 10 മിനിറ്റ് നടത്തം",
            "hook": "ഭക്ഷണം കഴിച്ചു കഴിഞ്ഞോ? ഉടൻ സോഫയിൽ വിശ്രമിക്കരുത്—ഈ 15 മിനിറ്റ് നിർണായകമാണ്.",
            "takeaway": "ഭക്ഷണത്തിന് ശേഷം ബാൽക്കണിയിൽ 10 മിനിറ്റ് നടന്നാൽ ഗ്ലൂക്കോസ് സ്പൈക്ക് 34% കുറയും.",
            "caption": "ഭക്ഷണത്തിന് ശേഷം 10 മിനിറ്റ് സാവധാനം നടന്നാൽ ഷുഗർ സ്പൈക്ക് 34% കുറയും. ശതപദി ഇന്നുതന്നെ ശീലമാക്കൂ! 🩺✨",
            "scenes": [
                {
                    "scene_role": "dinner_table",
                    "on_screen": "ഭക്ഷണം കഴിഞ്ഞു... സോഫയോ അതോ നടപ്പേോ?",
                    "narration": "രുചികരമായ ഭക്ഷണം കഴിച്ചു കഴിഞ്ഞോ? ഉടൻ സോഫയിൽ വിശ്രമിച്ചാൽ രക്തത്തിലെ പഞ്ചസార പെട്ടെന്ന് കൂടും.",
                    "subtitle": "ഭക്ഷണത്തിന് ശേഷം ഇരിക്കുന്നത് പഞ്ചസാര കൂട്ടും.",
                    "visual_cue": "ഡൈനിംഗ് ടേബിളിൽ ഭക്ഷണ പ്ലേറ്റും നടക്കാനുള്ള ചോയ്‌സും",
                    "duration": 5.0
                },
                {
                    "scene_role": "smartwatch",
                    "on_screen": "സ്മാർട്ട് വാച്ച് അലേർട്ട്: 15 മിനിറ്റ് സമയം",
                    "narration": "സ്മാർട്ട് വാച്ച് അലേർട്ട്: ഭക്ഷണത്തിന് ശേഷമുള്ള 15 മുതൽ 30 മിനിറ്റ് നിർണായക സമയം തുടങ്ങി!",
                    "subtitle": "സ്മാർട്ട് വാച്ച് അലേർട്ട്: 15-30 മിനിറ്റ് സമയം തുടങ്ങി!",
                    "visual_cue": "സ്മാർട്ട് വാച്ച് വൈബ്രേറ്റ് ചെയ്തു നടക്കാൻ ഓർമ്മിപ്പിക്കുന്നു",
                    "duration": 5.0
                },
                {
                    "scene_role": "terrace_walk",
                    "on_screen": "ടെറസിൽ 10 മിനിറ്റ് ശാന്തമായ നടത്തം",
                    "narration": "ബാൽക്കണിയിലോ ടെറസിലോ 10 മിനിറ്റ് ശാന്തമായി നടക്കാം.",
                    "subtitle": "ടെറസിലോ ബാൽക്കണിയിലോ 10 മിനിറ്റ് നടക്കുക.",
                    "visual_cue": "നക്ഷത്രങ്ങൾ നിറഞ്ഞ ആകാശത്തിന് കീഴെ ടെറസിൽ നടക്കുന്ന വ്യക്തി",
                    "duration": 5.5
                },
                {
                    "scene_role": "clock_timing",
                    "on_screen": "സമയം പ്രധാനം: 3 ഇരട്ടി ഫലം",
                    "narration": "സമയം പ്രധാനം: ഒരു മണിക്കൂർ കഴിഞ്ഞതിനേക്കാൾ 30 മിനിറ്റിനുള്ളിൽ നടക്കുന്നത് 3 ഇരട്ടി ഫലപ്രദമാണ്.",
                    "subtitle": "30 മിനിറ്റിനുള്ളിൽ നടക്കുന്നത് 3 ഇരട്ടി ഫലം നൽകും.",
                    "visual_cue": "ക്ലോക്കിൽ സമയം കാണിച്ച് പ്രാധാന്യം വ്യക്തമാക്കുന്നു",
                    "duration": 5.0
                },
                {
                    "scene_role": "habit_success",
                    "on_screen": "ഗ്ലൂക്കോസ് സ്പൈക്ക് 34% കുറഞ്ഞു!",
                    "narration": "ഗ്ലൂക്കോസ് സ്പൈക്ക് 34% കുറയുമെന്ന് തെളിഞ്ഞു. ഇന്ന് രാത്രി ശതപദി തുടങ്ങൂ!",
                    "subtitle": "ക്ലിനിക്കൽ പരീക്ഷണം: ഷുഗർ സ്പൈക്ക് 34% കുറഞ്ഞു!",
                    "visual_cue": "പച്ച ടിക് മാർക്കും 34% കുറവ് കാണിക്കുന്ന കാർഡും",
                    "duration": 4.5
                }
            ]
        }
    }

    lang_data = scripts.get(language, scripts["en"])
    scenes_list = []
    total_time = 0.0

    for idx, item in enumerate(lang_data["scenes"]):
        dur = item.get("duration", 5.0)
        total_time += dur
        scenes_list.append({
            "scene_number": idx + 1,
            "duration_seconds": dur,
            "visual_cue": item["visual_cue"],
            "on_screen_text": item["on_screen"],
            "narration": item["narration"],
            "subtitle_text": item["subtitle"],
            "visual_style": "everyday_human",
            "visual_theme": visual_theme,
            "animation_action": "everyday_human",
            "scene_role": item.get("scene_role", "terrace_walk"),
            "character_name": None,
            "claim_ids": [primary_clm] if idx in [1, 4] else ([c2] if idx == 2 else [c3])
        })

    return {
        "reel_title": lang_data["title"],
        "hook": lang_data["hook"],
        "target_duration_seconds": int(total_time),
        "mode": "everyday",
        "visual_style": "everyday_human",
        "visual_theme": visual_theme,
        "language": language,
        "voice_name": voice_name,
        "scenes": scenes_list,
        "practical_takeaway": lang_data["takeaway"],
        "caption": lang_data["caption"],
        "hashtags": ["#EverydayHabits", "#SteerHealth", "#Shatapadi", "#BloodSugarControl", "#LifestyleMedicine"],
        "claim_ids": clm_ids,
        "source_citation": f"Crossover Clinical Trial: {paper_title[:45]} (n=48)"
    }


def get_animated_explainer_storyboard(
    language: str,
    claims: Optional[List[Dict[str, Any]]],
    paper_title: str,
    voice_name: str,
    visual_theme: str = "warm_editorial"
) -> Dict[str, Any]:
    if not is_sample_walk_paper(paper_title):
        return _build_dynamic_paper_storyboard("animated_explainer", language, claims, paper_title, voice_name, visual_theme)

    clm_ids = [c.get("claim_id", f"CLM-{i+1:03d}") for i, c in enumerate(claims)] if claims else ["CLM-001", "CLM-002", "CLM-003"]
    primary_clm = clm_ids[0] if clm_ids else "CLM-001"
    c2 = clm_ids[1] if len(clm_ids) > 1 else primary_clm
    c3 = clm_ids[2] if len(clm_ids) > 2 else primary_clm

    scripts = {
        "en": {
            "title": "Animated Explainer: Continuous Glucose Kinetics & Muscle Clearance",
            "hook": "What does a continuous glucose monitor reveal 45 minutes after eating?",
            "takeaway": "Light ambulation within 30 minutes lowers peak glucose elevation by 34% via insulin-independent GLUT4 transport.",
            "caption": "Animated science briefing: Continuous glucose monitoring reveals a 34% drop in peak glycemic elevation from a simple 10-minute walk. Explore the GLUT4 kinetics! 📊🩺",
            "scenes": [
                {
                    "scene_role": "cgm_intro",
                    "on_screen": "Continuous Glucose Monitoring (n=48)",
                    "narration": "What does continuous glucose monitoring reveal right after a carbohydrate-rich Indian meal?",
                    "subtitle": "Continuous glucose monitoring reveals postprandial kinetics.",
                    "visual_cue": "Animated continuous glucose sensor with radiating wireless signal waves and study parameters",
                    "duration": 5.0
                },
                {
                    "scene_role": "curve_comparison",
                    "on_screen": "166 mg/dL vs 146 mg/dL Peak",
                    "narration": "Sedentary rest drives a sharp spike to 166 mg/dL. A 10-minute walk flattens peak elevation to 146 mg/dL.",
                    "subtitle": "Sedentary rest peaks at 166 mg/dL; 10-min walk blunts to 146 mg/dL.",
                    "visual_cue": "Dynamic 24fps kinetic CGM curve comparing red sedentary spike against green walking curve",
                    "duration": 5.5
                },
                {
                    "scene_role": "glut4_mechanism",
                    "on_screen": "Non-Insulin GLUT4 Clearance",
                    "narration": "How does it work? Contracting quadriceps and soleus activate non-insulin GLUT4 transport channels directly.",
                    "subtitle": "Contracting leg muscles open GLUT4 channels without insulin strain.",
                    "visual_cue": "Biochemical muscle membrane diagram showing AMPK activation and opening GLUT4 glucose gates",
                    "duration": 5.0
                },
                {
                    "scene_role": "timing_window",
                    "on_screen": "Window: 15m (34%) vs 60m (9%)",
                    "narration": "Chronobiology matters: walking at 15 minutes yields a 34% drop, but waiting 60 minutes drops only 9%.",
                    "subtitle": "Immediate walk gives 34% reduction; waiting 60 mins yields only 9%.",
                    "visual_cue": "Comparative chronobiology bar chart contrasting the 15-min and 60-min intervention arms",
                    "duration": 5.0
                },
                {
                    "scene_role": "summary_stat",
                    "on_screen": "-34% Peak Glucose Elevation",
                    "narration": "Conclusion: 34% peak reduction confirmed in 48 participants. Adopt evidence-based Shatapadi with Steer.",
                    "subtitle": "34% peak glucose reduction verified (p < 0.001, n=48).",
                    "visual_cue": "Large pulsing -34% reduction badge with clinical evidence link and Shatapadi recommendation",
                    "duration": 4.5
                }
            ]
        },
        "hi": {
            "title": "एनिमेटेड एक्सप्लेनर: ग्लूकोज काइनेटिक्स और मसल क्लीयरेंस",
            "hook": "खाने के 45 मिनट बाद कंटीन्यूअस ग्लूकोज मॉनिटर क्या दिखाता है?",
            "takeaway": "खाने के 30 मिनट के भीतर 10 मिनट टहलने से बिना इंसुलिन के GLUT4 के जरिए शुगर स्पाइक 34% कम होता है।",
            "caption": "एनिमेटेड साइंस ब्रीफिंग: CGM डेटा दिखाता है कि 10 मिनट टहलने से पीक ग्लूकोज 34% घटता है। GLUT4 मैकेनिज्म समझिए! 📊🩺",
            "scenes": [
                {
                    "scene_role": "cgm_intro",
                    "on_screen": "कंटीन्यूअस ग्लूकोज मॉनिटरिंग (n=48)",
                    "narration": "भारतीय भोजन के बाद कंटीन्यूअस ग्लूकोज मॉनिटर शरीर के बारे में क्या दिखाता है?",
                    "subtitle": "CGM सेंसर खाने के बाद का ग्लूकोज डेटा दिखाता है।",
                    "visual_cue": "सेंसर और वायरलेस सिग्नल तरंगों के साथ रिसर्च अध्ययन का कार्ड",
                    "duration": 5.0
                },
                {
                    "scene_role": "curve_comparison",
                    "on_screen": "166 mg/dL बनाम 146 mg/dL",
                    "narration": "सोफे पर बैठे रहने से शुगर 166 mg/dL तक उछलती है, जबकि 10 मिनट टहलने से यह 146 mg/dL पर रुक जाती है।",
                    "subtitle": "बैठे रहने पर 166 mg/dL, 10 मिनट चलने पर 146 mg/dL।",
                    "visual_cue": "लाल और हरी कर्व के साथ 24fps एनिमेटेड CGM ग्राफ",
                    "duration": 5.5
                },
                {
                    "scene_role": "glut4_mechanism",
                    "on_screen": "बिना इंसुलिन GLUT4 क्लीयरेंस",
                    "narration": "यह कैसे काम करता है? पैरों की मांसपेशियों का संकुचन बिना इंसुलिन के GLUT4 चैनल्स खोल देता है।",
                    "subtitle": "मांसपेशियों का चलना GLUT4 गेट्स खोलता है।",
                    "visual_cue": "मांसपेशी झिल्ली और GLUT4 ट्रांसपोर्टर गेट्स खुलते हुए",
                    "duration": 5.0
                },
                {
                    "scene_role": "timing_window",
                    "on_screen": "समय: 15 मिनट (34%) बनाम 60 मिनट (9%)",
                    "narration": "समय का गणित: 15 मिनट में टहलने से 34% गिरावट मिलती है, पर 60 मिनट रुकने पर सिर्फ 9% फायदा होता है।",
                    "subtitle": "15 मिनट में 34% कमी, 60 मिनट रुकने पर सिर्फ 9%।",
                    "visual_cue": "समय के अंतर का तुलनात्मक बार चार्ट",
                    "duration": 5.0
                },
                {
                    "scene_role": "summary_stat",
                    "on_screen": "पीक ग्लूकोज स्पाइक -34% कम",
                    "narration": "निष्कर्ष: 48 प्रतिभागियों में 34% स्पाइक कम होना साबित हुआ। Steer के साथ वैज्ञानिक शतपदी अपनाएं।",
                    "subtitle": "34% पीक ग्लूकोज कमी क्लिनिकली प्रमाणित (p < 0.001)।",
                    "visual_cue": "चमकता हुआ -34% बैज और शतपदी क्लिनिकल निष्कर्ष",
                    "duration": 4.5
                }
            ]
        },
        "te": {
            "title": "యానిమేటెడ్ ఎక్స్‌ప్లేనర్: గ్లూకోజ్ కైనటిక్స్ & కండరాల పనితీరు",
            "hook": "భోజనం తర్వాత 45 నిమిషాలకు CGM ఏం చూపిస్తుంది?",
            "takeaway": "భోజనం తర్వాత 10 నిమిషాలు నడిస్తే GLUT4 ద్వారా ఇన్సులిన్ లేకుండానే షుగర్ 34% తగ్గుతుంది.",
            "caption": "సైంటిఫిక్ బ్రీఫింగ్: 10 నిమిషాల నడకతో గ్లూకోజ్ స్పైక్ 34% తగ్గుతుందని CGM డేటా నిర్ధారించింది! 📊🩺",
            "scenes": [
                {
                    "scene_role": "cgm_intro",
                    "on_screen": "కంటిన్యూయస్ గ్లూకోజ్ మానిటరింగ్ (n=48)",
                    "narration": "భోజనం తర్వాత కంటిన్యూయస్ గ్లూకోజ్ మానిటర్ మన రక్తంలో ఏం జరుగుతుందో చూపిస్తుంది?",
                    "subtitle": "CGM సెన్సార్ రక్తంలో గ్లూకోజ్ ప్రవాహాన్ని చూపిస్తుంది.",
                    "visual_cue": "వైర్‌లెస్ సిగ్నల్ తరంగాలతో CGM సెన్సార్ పరిశోధన వివరాలు",
                    "duration": 5.0
                },
                {
                    "scene_role": "curve_comparison",
                    "on_screen": "166 mg/dL vs 146 mg/dL గరిష్ట స్థాయి",
                    "narration": "కదలకుండా కూర్చుంటే షుగర్ 166 mg/dL కు ఎగబాకుతుంది, 10 నిమిషాలు నడిస్తే 146 mg/dL వద్ద ఆగుతుంది.",
                    "subtitle": "కూర్చుంటే 166 mg/dL, నడిస్తే 146 mg/dL వద్ద నియంత్రణ.",
                    "visual_cue": "ఎరుపు మరియు ఆకుపచ్చ గ్రాఫ్‌లతో 24fps యానిమేటెడ్ CGM చార్ట్",
                    "duration": 5.5
                },
                {
                    "scene_role": "glut4_mechanism",
                    "on_screen": "ఇన్సులిన్ లేని GLUT4 క్లియరెన్స్",
                    "narration": "ఇది ఎలా పనిచేస్తుంది? కాళ్ల కండరాల కదలిక ఇన్సులిన్ అవసరం లేకుండానే నేరుగా GLUT4 ద్వారా గ్లూకోజ్‌ను పీల్చుకుంటుంది.",
                    "subtitle": "కండరాల కదలికతో GLUT4 మార్గాలు నేరుగా తెరుచుకుంటాయి.",
                    "visual_cue": "కండరాల పొరపై GLUT4 గ్లూకోజ్ ద్వారాలు తెరుచుకునే యానిమేషన్",
                    "duration": 5.0
                },
                {
                    "scene_role": "timing_window",
                    "on_screen": "సమయం: 15ని (34%) vs 60ని (9%)",
                    "narration": "సమయ ప్రాముఖ్యత: 15 నిమిషాల్లో నడిస్తే 34% తగ్గుదల, కానీ 60 నిమిషాలు ఆగితే కేవలం 9% మాత్రమే ఫలితం.",
                    "subtitle": "15 నిమిషాల్లో నడిస్తే 34%, 60 నిమిషాలు ఆగితే 9% మాత్రమే.",
                    "visual_cue": "సమయ వ్యత్యాసాన్ని చూపించే బార్ చార్ట్",
                    "duration": 5.0
                },
                {
                    "scene_role": "summary_stat",
                    "on_screen": "షుగర్ స్పైక్ -34% తగ్గింది",
                    "narration": "ముగింపు: 48 మందిలో 34% తగ్గుదల నిర్ధారించబడింది. Steer తో సైంటిఫిక్ శతపది అనుసరించండి.",
                    "subtitle": "34% తగ్గుదల శాస్త్రీయంగా రుజువైంది (p < 0.001).",
                    "visual_cue": "వెలుగుతున్న -34% బ్యాడ్జ్ మరియు శతపది సిఫార్సు",
                    "duration": 4.5
                }
            ]
        },
        "ta": {
            "title": "அனிமேஷன் விளக்கம்: குளுக்கோஸ் இயக்கம் மற்றும் தசை உறிஞ்சுதல்",
            "hook": "உணவுக்குப் பின் 45 நிமிடங்களில் தொடர் குளுக்கோஸ் மானிட்டர் என்ன காட்டுகிறது?",
            "takeaway": "உணவுக்குப் பின் 10 நிமிட நடைப்பயிற்சி இன்சுலின் இன்றி GLUT4 வழியே சர்க்கரை உயர்வை 34% குறைக்கிறது.",
            "caption": "அறிவியல் விளக்கம்: 10 நிமிட நடைப்பயிற்சி சர்க்கரை உயர்வை 34% குறைக்கிறது என்பதை CGM நிரூபிக்கிறது! 📊🩺",
            "scenes": [
                {
                    "scene_role": "cgm_intro",
                    "on_screen": "தொடர் குளுக்கோஸ் கண்காணிப்பு (n=48)",
                    "narration": "உணவுக்குப் பின் தொடர் குளுக்கோஸ் மானிட்டர் ரத்தத்தில் என்ன காட்டுகிறது?",
                    "subtitle": "CGM சென்சார் ரத்த சர்க்கரை அளவை காட்டுகிறது.",
                    "visual_cue": "வயர்லெஸ் அலைகளுடன் கூடிய CGM சென்சார் மற்றும் ஆய்வு தரவு",
                    "duration": 5.0
                },
                {
                    "scene_role": "curve_comparison",
                    "on_screen": "166 mg/dL vs 146 mg/dL உச்சம்",
                    "narration": "அமர்ந்திருந்தால் சர்க்கரை 166 mg/dL வரை எகிறும், 10 நிமிடம் நடந்தால் 146 mg/dL ஆக மட்டுப்படும்.",
                    "subtitle": "அமர்ந்தால் 166 mg/dL; நடந்தால் 146 mg/dL ஆக குறையும்.",
                    "visual_cue": "சிகப்பு மற்றும் பச்சை கோடுகளுடன் 24fps அனிமேஷன் CGM வரைபடம்",
                    "duration": 5.5
                },
                {
                    "scene_role": "glut4_mechanism",
                    "on_screen": "இன்சுலின் அற்ற GLUT4 உறிஞ்சுதல்",
                    "narration": "இது எவ்வாறு செயல்படுகிறது? கால்களின் தசை இயக்கம் இன்சுலின் துணையின்றி GLUT4 வழியே சர்க்கரையை உறிஞ்சுகிறது.",
                    "subtitle": "தசை அசைவு இன்சுலின் இன்றி GLUT4 வழிகளை திறக்கிறது.",
                    "visual_cue": "தசை சவ்வில் GLUT4 கதவுகள் திறந்து சர்க்கரையை உறிஞ்சும் காட்சி",
                    "duration": 5.0
                },
                {
                    "scene_role": "timing_window",
                    "on_screen": "நேரம்: 15நி (34%) vs 60நி (9%)",
                    "narration": "நேரத்தின் முக்கியத்துவம்: 15 நிமிடத்தில் நடந்தால் 34% குறையும், ஆனால் 60 நிமிடம் தாமதித்தால் 9% மட்டுமே பயன்.",
                    "subtitle": "15 நிமிடத்தில் நடந்தால் 34%, 60 நிமிடம் கழித்தால் 9% மட்டுமே.",
                    "visual_cue": "நேர வேறுபாட்டை காட்டும் ஒப்பீட்டு வரைபடம்",
                    "duration": 5.0
                },
                {
                    "scene_role": "summary_stat",
                    "on_screen": "சர்க்கரை உயர்வு -34% குறைவு",
                    "narration": "முடிவு: 48 பேரில் 34% சர்க்கரை உயர்வு குறைவது உறுதியானது. Steer உடன் அறிவியல் சதபரியை பின்பற்றுங்கள்.",
                    "subtitle": "34% குறைவு மருத்துவ ரீதியாக நிரூபிக்கப்பட்டது (p < 0.001).",
                    "visual_cue": "ஒளிரும் -34% பேட்ஜ் மற்றும் சதபரி பரிந்துரை",
                    "duration": 4.5
                }
            ]
        },
        "kn": {
            "title": "ಅನಿಮೇಟೆಡ್ ವಿವರಣೆ: ಗ್ಲೂಕೋಸ್ ಕೈನೆಟಿಕ್ಸ್ ಮತ್ತು ಸ್ನಾಯು ಹೀರುವಿಕೆ",
            "hook": "ಊಟದ 45 ನಿಮಿಷಗಳ ನಂತರ ಕಂಟಿನ್ಯೂಯಸ್ ಗ್ಲೂಕೋಸ್ ಮಾನಿಟರ್ ಏನು ಹೇಳುತ್ತದೆ?",
            "takeaway": "ಊಟದ ನಂತರ 10 ನಿಮಿಷ ನಡೆದರೆ ಇನ್ಸುಲಿನ್ ಇಲ್ಲದೆಯೇ GLUT4 ಮೂಲಕ ಸಕ್ಕರೆ ಸ್ಪೈಕ್ 34% ಕಡಿಮೆಯಾಗುತ್ತದೆ.",
            "caption": "ವೈಜ್ಞಾನಿಕ ವಿವರಣೆ: 10 ನಿಮಿಷ ವಾಕಿಂಗ್ ಮಾಡುವುದರಿಂದ ಗ್ಲೂಕೋಸ್ ಸ್ಪೈಕ್ 34% ತಗ್ಗುತ್ತದೆ ಎಂದು CGM ಸಾಬೀತುಪಡಿಸಿದೆ! 📊🩺",
            "scenes": [
                {
                    "scene_role": "cgm_intro",
                    "on_screen": "ಕಂಟಿನ್ಯೂಯಸ್ ಗ್ಲೂಕೋಸ್ ಮಾನಿಟರಿಂಗ್ (n=48)",
                    "narration": "ಊಟದ ನಂತರ ಕಂಟಿನ್ಯೂಯಸ್ ಗ್ಲೂಕೋಸ್ ಮಾನಿಟರ್ ನಮ್ಮ ದೇಹದ ಬಗ್ಗೆ ಏನು ಹೇಳುತ್ತದೆ?",
                    "subtitle": "CGM ಸೆನ್ಸರ್ ರಕ್ತದಲ್ಲಿನ ಸಕ್ಕರೆ ಬದಲಾವಣೆ ತೋರಿಸುತ್ತದೆ.",
                    "visual_cue": "ವೈರ್‌ಲೆಸ್ ತರಂಗಗಳೊಂದಿಗೆ CGM ಸೆನ್ಸರ್ ಮತ್ತು ಸಂಶೋಧನಾ ಮಾಹಿತಿ",
                    "duration": 5.0
                },
                {
                    "scene_role": "curve_comparison",
                    "on_screen": "166 mg/dL vs 146 mg/dL ಗರಿಷ್ಠ",
                    "narration": "ಕೂತೇ ಇದ್ದರೆ ಸಕ್ಕರೆ 166 mg/dL ವರೆಗೆ ಏರುತ್ತದೆ, 10 ನಿಮಿಷ ನಡೆದರೆ 146 mg/dL ಗೆ ನಿಯಂತ್ರಣವಾಗುತ್ತದೆ.",
                    "subtitle": "ಕೂತಿದ್ದರೆ 166 mg/dL, 10 ನಿಮಿಷ ನಡೆದರೆ 146 mg/dL.",
                    "visual_cue": "ಕೆಂಪು ಮತ್ತು ಹಸಿರು ರೇಖೆಗಳೊಂದಿಗೆ 24fps ಅನಿಮೇಟೆಡ್ CGM ಚಾರ್ಟ್",
                    "duration": 5.5
                },
                {
                    "scene_role": "glut4_mechanism",
                    "on_screen": "ಇನ್ಸುಲಿನ್ ರಹಿತ GLUT4 ಹೀರುವಿಕೆ",
                    "narration": "ಇದು ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ? ಕಾಲುಗಳ ಸ್ನಾಯು ಸಂಕೋಚನವು ಇನ್ಸುಲಿನ್ ಇಲ್ಲದೆಯೇ GLUT4 ಚಾನೆಲ್‌ಗಳನ್ನು ತೆರೆಯುತ್ತದೆ.",
                    "subtitle": "ಸ್ನಾಯು ಚಲನೆಯು GLUT4 ಗೇಟ್‌ಗಳನ್ನು ತೆರೆಯುತ್ತದೆ.",
                    "visual_cue": "ಸ್ನಾಯು ಪೊರೆಯಲ್ಲಿ GLUT4 ಸಕ್ಕರೆ ದ್ವಾರಗಳು ತೆರೆದುಕೊಳ್ಳುವ ದೃಶ್ಯ",
                    "duration": 5.0
                },
                {
                    "scene_role": "timing_window",
                    "on_screen": "ಸಮಯ: 15ನಿ (34%) vs 60ನಿ (9%)",
                    "narration": "ಸಮಯದ ಲೆಕ್ಕಾಚಾರ: 15 ನಿಮಿಷದಲ್ಲಿ ನಡೆದರೆ 34% ಇಳಿಕೆ, ಆದರೆ 60 ನಿಮಿಷ ತಡಮಾಡಿದರೆ ಕೇವಲ 9% ಲಾಭ.",
                    "subtitle": "15 ನಿಮಿಷದಲ್ಲಿ ನಡೆದರೆ 34%, 60 ನಿಮಿಷ ತಡಮಾಡಿದರೆ 9% ಮಾತ್ರ.",
                    "visual_cue": "ಸಮಯದ ವ್ಯತ್ಯಾಸ ತೋರಿಸುವ ಬಾರ್ ಚಾರ್ಟ್",
                    "duration": 5.0
                },
                {
                    "scene_role": "summary_stat",
                    "on_screen": "ಸಕ್ಕರೆ ಸ್ಪೈಕ್ -34% ಕಡಿಮೆ",
                    "narration": "ತೀರ್ಮಾನ: 48 ಜನರಲ್ಲಿ 34% ಸಕ್ಕರೆ ಏರಿಕೆ ತಗ್ಗಿದೆ. Steer ಜೊತೆ ವೈಜ್ಞಾನಿಕ ಶತಪದಿ ರೂಢಿಸಿಕೊಳ್ಳಿ.",
                    "subtitle": "34% ಇಳಿಕೆ ಸಾಬೀತಾಗಿದೆ (p < 0.001, n=48).",
                    "visual_cue": "ಹೊಳೆಯುವ -34% ಬ್ಯಾಡ್ಜ್ ಮತ್ತು ಶತಪದಿ ಶಿಫಾರಸು",
                    "duration": 4.5
                }
            ]
        },
        "ml": {
            "title": "ആനിമേറ്റഡ് വിവരണം: ഗ്ലൂക്കോസ് ചലനവും പേശി ആഗിരണവും",
            "hook": "ഭക്ഷണത്തിന് 45 മിനിറ്റിന് ശേഷം കണ്ടിന്യൂവസ് ഗ്ലൂക്കോസ് മോണിറ്റർ എന്ത് കാണിക്കുന്നു?",
            "takeaway": "ഭക്ഷണത്തിന് ശേഷം 10 മിനിറ്റ് നടന്നാൽ ഇൻസുലിൻ ഇല്ലാതെ തന്നെ GLUT4 വഴി ഗ്ലൂക്കോസ് സ്പൈക്ക് 34% കുറയും.",
            "caption": "ശാസ്ത്രീയ വിവരണം: 10 മിനിറ്റ് നടന്നാൽ ഗ്ലൂക്കോസ് സ്പൈക്ക് 34% കുറയുമെന്ന് CGM തെളിയിക്കുന്നു! 📊🩺",
            "scenes": [
                {
                    "scene_role": "cgm_intro",
                    "on_screen": "കണ്ടിന്യൂവസ് ഗ്ലൂക്കോസ് മോണിറ്ററിംഗ് (n=48)",
                    "narration": "ഭക്ഷണത്തിന് ശേഷം കണ്ടിന്യൂവസ് ഗ്ലൂക്കോസ് മോണിറ്റർ കാണിക്കുന്നത് എന്താണ്?",
                    "subtitle": "CGM സെൻസർ ഭക്ഷണത്തിന് ശേഷമുള്ള ഗ്ലൂക്കോസ് കാണിക്കുന്നു.",
                    "visual_cue": "വയർലെസ് തരംഗങ്ങളോടെ CGM സെൻസറും റിസർച്ച് കാർഡും",
                    "duration": 5.0
                },
                {
                    "scene_role": "curve_comparison",
                    "on_screen": "166 mg/dL vs 146 mg/dL",
                    "narration": "ഇരുന്നാൽ പഞ്ചസാര 166 mg/dL ആയി കുതിച്ചുയരും, 10 മിനിറ്റ് നടന്നാൽ 146 mg/dL ആയി കുറയും.",
                    "subtitle": "ഇരുന്നാൽ 166 mg/dL; നടന്നാൽ 146 mg/dL ആയി കുറയും.",
                    "visual_cue": "ചുവപ്പും പച്ചയും വരകളോടെ 24fps ആനിമേറ്റഡ് CGM ഗ്രാഫ്",
                    "duration": 5.5
                },
                {
                    "scene_role": "glut4_mechanism",
                    "on_screen": "ഇൻസുലിൻ ഇല്ലാതെ GLUT4 ആഗിരണം",
                    "narration": "ഇത് എങ്ങനെ പ്രവർത്തിക്കുന്നു? പേശികളുടെ ചലനം ഇൻസുലിൻ ഇല്ലാതെ തന്നെ GLUT4 വഴി ഗ്ലൂക്കോസ് നേരിട്ട് ആഗിരണം ചെയ്യുന്നു.",
                    "subtitle": "പേശി ചലനം GLUT4 വാതിലുകൾ തുറക്കുന്നു.",
                    "visual_cue": "പേശി കോശങ്ങളിൽ GLUT4 ചാനലുകൾ തുറക്കുന്ന ആനിമേഷൻ",
                    "duration": 5.0
                },
                {
                    "scene_role": "timing_window",
                    "on_screen": "സമയം: 15മി (34%) vs 60മി (9%)",
                    "narration": "സമയത്തിന്റെ പ്രാധാന്യം: 15 മിനിറ്റിൽ നടന്നാൽ 34% കുറയും, എന്നാൽ 60 മിനിറ്റ് വൈകിയാൽ 9% മാത്രം ഫലം.",
                    "subtitle": "15 മിനിറ്റിൽ 34% കുറവ്, 60 മിനിറ്റിൽ 9% മാത്രം.",
                    "visual_cue": "സമയ വ്യത്യാസം കാണിക്കുന്ന ബാർ ചാർട്ട്",
                    "duration": 5.0
                },
                {
                    "scene_role": "summary_stat",
                    "on_screen": "ഗ്ലൂക്കോസ് സ്പൈക്ക് -34% കുറവ്",
                    "narration": "ഉപസംഹാരം: 48 പേരിൽ 34% സ്പൈക്ക് കുറയുമെന്ന് തെളിഞ്ഞു. Steer-നൊപ്പം ശാസ്ത്രീയ ശതപദി ശീലമാക്കൂ.",
                    "subtitle": "34% കുറവ് തെളിയിക്കപ്പെട്ടു (p < 0.001, n=48).",
                    "visual_cue": "തിളങ്ങുന്ന -34% ബാഡ്ജും ശതപദി നിർദ്ദേശവും",
                    "duration": 4.5
                }
            ]
        }
    }

    lang_data = scripts.get(language, scripts["en"])
    scenes_list = []
    total_time = 0.0

    for idx, item in enumerate(lang_data["scenes"]):
        dur = item.get("duration", 5.0)
        total_time += dur
        scenes_list.append({
            "scene_number": idx + 1,
            "duration_seconds": dur,
            "visual_cue": item["visual_cue"],
            "on_screen_text": item["on_screen"],
            "narration": item["narration"],
            "subtitle_text": item["subtitle"],
            "visual_style": "animated_explainer",
            "visual_theme": visual_theme,
            "animation_action": "animated_explainer",
            "scene_role": item.get("scene_role", "curve_comparison"),
            "character_name": None,
            "claim_ids": [primary_clm] if idx in [1, 4] else ([c2] if idx == 2 else [c3])
        })

    return {
        "reel_title": lang_data["title"],
        "hook": lang_data["hook"],
        "target_duration_seconds": int(total_time),
        "mode": "everyday",
        "visual_style": "animated_explainer",
        "visual_theme": visual_theme,
        "language": language,
        "voice_name": voice_name,
        "scenes": scenes_list,
        "practical_takeaway": lang_data["takeaway"],
        "caption": lang_data["caption"],
        "hashtags": ["#AnimatedExplainer", "#MetabolicScience", "#CGMData", "#GLUT4", "#SteerHealth"],
        "claim_ids": clm_ids,
        "source_citation": f"Evidence: {paper_title[:45]} (n=48 Crossover Trial)"
    }

