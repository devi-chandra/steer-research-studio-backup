import math
import os
import random
from pathlib import Path
from typing import Dict, Any, List, Optional
from PIL import Image, ImageDraw, ImageFont

class AnimationEngine:
    def __init__(self, width: int = 720, height: int = 1280, fps: int = 24):
        self.width = width
        self.height = height
        self.fps = fps

        # Steer Brand Palette
        self.c_cream = (245, 235, 223)
        self.c_rust = (192, 78, 42)
        self.c_maroon = (102, 20, 20)
        self.c_ink = (53, 29, 29)
        self.c_clay = (181, 135, 119)
        self.c_blush = (230, 203, 189)
        self.c_soft_paper = (248, 242, 235)
        self.c_white = (255, 255, 255)
        self.c_green = (46, 125, 50)
        self.c_light_green = (232, 245, 233)

        # Regional font support for Indian scripts
        self.font_path = "C:/Windows/Fonts/Nirmala.ttc"
        if not Path(self.font_path).exists():
            self.font_path = "arial.ttf"

    def _get_font(self, size: int) -> ImageFont.ImageFont:
        try:
            return ImageFont.truetype(self.font_path, size)
        except Exception:
            return ImageFont.load_default()

    def _wrap_text(self, text: str, font: ImageFont.ImageFont, max_width: int, draw: ImageDraw.ImageDraw) -> List[str]:
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_w = bbox[2] - bbox[0]
            if line_w <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        if current_line:
            lines.append(" ".join(current_line))
        return lines

    def get_theme(self, theme_name: Optional[str]) -> Dict[str, Any]:
        themes = {
            "steer_brand": {
                "name": "steer_brand",
                "bg": (245, 235, 223),          # cream
                "card_bg": (248, 242, 235),     # soft paper
                "card_border": (230, 203, 189), # blush
                "accent_primary": (192, 78, 42),# rust
                "accent_secondary": (102, 20, 20),# maroon
                "text_primary": (53, 29, 29),   # ink
                "text_muted": (181, 135, 119),  # clay
                "badge_bg": (230, 203, 189),
                "badge_text": (102, 20, 20),
                "sub_bg": (53, 29, 29),
                "sub_text": (255, 255, 255),
                "progress_active": (192, 78, 42),
                "progress_bg": (230, 203, 189),
            },
            "warm_editorial": {
                "name": "warm_editorial",
                "bg": (250, 245, 238),          # warm linen
                "card_bg": (255, 253, 249),     # warm offwhite
                "card_border": (226, 215, 200), # gentle ochre
                "accent_primary": (200, 90, 50),# terracotta
                "accent_secondary": (120, 53, 15),# rich amber
                "text_primary": (44, 30, 24),   # espresso
                "text_muted": (140, 115, 95),   # warm taupe
                "badge_bg": (242, 230, 214),
                "badge_text": (120, 53, 15),
                "sub_bg": (44, 30, 24),
                "sub_text": (255, 253, 249),
                "progress_active": (200, 90, 50),
                "progress_bg": (226, 215, 200),
            },
            "colourful_cartoon": {
                "name": "colourful_cartoon",
                "bg": (255, 247, 204),          # sunny yellow cream
                "card_bg": (255, 255, 255),     # pure white
                "card_border": (99, 102, 241),  # vibrant indigo
                "accent_primary": (249, 115, 22),# punchy orange
                "accent_secondary": (79, 70, 229),# electric indigo
                "text_primary": (30, 27, 75),   # deep indigo ink
                "text_muted": (107, 114, 128),
                "badge_bg": (224, 231, 255),
                "badge_text": (67, 56, 202),
                "sub_bg": (30, 27, 75),
                "sub_text": (255, 255, 255),
                "progress_active": (249, 115, 22),
                "progress_bg": (224, 231, 255),
            },
            "playful_pastel": {
                "name": "playful_pastel",
                "bg": (245, 240, 255),          # soft lavender
                "card_bg": (255, 255, 255),     # pure white
                "card_border": (216, 205, 252), # lilac border
                "accent_primary": (147, 51, 234),# vibrant violet
                "accent_secondary": (236, 72, 153),# vibrant pink
                "text_primary": (30, 41, 59),   # slate dark
                "text_muted": (100, 116, 139),
                "badge_bg": (243, 232, 255),
                "badge_text": (126, 34, 206),
                "sub_bg": (30, 41, 59),
                "sub_text": (255, 255, 255),
                "progress_active": (147, 51, 234),
                "progress_bg": (233, 213, 255),
            },
            "cinematic": {
                "name": "cinematic",
                "bg": (15, 23, 42),              # dark slate 900
                "card_bg": (30, 41, 59),         # slate 800
                "card_border": (51, 65, 85),     # slate 700
                "accent_primary": (6, 182, 212), # neon cyan
                "accent_secondary": (245, 158, 11),# bright amber
                "text_primary": (248, 250, 252), # clean crisp white
                "text_muted": (148, 163, 184),   # slate 400
                "badge_bg": (51, 65, 85),
                "badge_text": (6, 182, 212),
                "sub_bg": (2, 6, 23),
                "sub_text": (248, 250, 252),
                "progress_active": (6, 182, 212),
                "progress_bg": (51, 65, 85),
            },
            "clean_infographic": {
                "name": "clean_infographic",
                "bg": (240, 249, 255),          # clean sky tint
                "card_bg": (255, 255, 255),     # pure white
                "card_border": (186, 230, 253), # light blue
                "accent_primary": (2, 132, 199),# clinical cobalt
                "accent_secondary": (13, 148, 136),# teal
                "text_primary": (15, 23, 42),   # navy
                "text_muted": (71, 85, 105),
                "badge_bg": (224, 242, 254),
                "badge_text": (3, 105, 161),
                "sub_bg": (15, 23, 42),
                "sub_text": (255, 255, 255),
                "progress_active": (2, 132, 199),
                "progress_bg": (224, 242, 254),
            },
            "inside_anatomy": {
                "name": "inside_anatomy",
                "bg": (255, 247, 237),          # warm peach
                "card_bg": (255, 255, 255),
                "card_border": (254, 215, 170),
                "accent_primary": (234, 88, 12),# organ orange
                "accent_secondary": (225, 29, 72),# muscle red
                "text_primary": (30, 20, 25),
                "text_muted": (154, 52, 18),
                "badge_bg": (254, 237, 213),
                "badge_text": (194, 65, 12),
                "sub_bg": (30, 20, 25),
                "sub_text": (255, 255, 255),
                "progress_active": (234, 88, 12),
            }
        }
        if not theme_name:
            return themes["warm_editorial"]
        if theme_name == "pastel_educational":
            return themes["playful_pastel"]
        if theme_name not in themes:
            raise ValueError(
                f"Unsupported visual theme '{theme_name}'. "
                f"Available themes: {list(themes.keys()) + ['pastel_educational']}"
            )
        return themes[theme_name]


    def render_scene_frames(
        self,
        scene: Dict[str, Any],
        scene_idx: int,
        total_scenes: int,
        duration_seconds: float,
        out_dir: Path
    ) -> List[Path]:
        """
        Renders an authentic multi-frame animation sequence (at 24 fps)
        based on the selected visual style and animation action.
        """
        out_dir.mkdir(parents=True, exist_ok=True)
        total_frames = max(24, int(duration_seconds * self.fps))
        frame_paths: List[Path] = []

        visual_style = scene.get("visual_style", "talking_characters")
        theme_name = scene.get("visual_theme") or "warm_editorial"
        palette = self.get_theme(theme_name)
        self.current_palette = palette

        on_screen_text = scene.get("on_screen_text", "Metabolic Science")
        subtitle_text = scene.get("subtitle_text") or scene.get("narration", "")

        for frame_num in range(total_frames):
            p = frame_num / total_frames  # progress 0.0 to 1.0
            im = Image.new("RGB", (self.width, self.height), palette["bg"])
            draw = ImageDraw.Draw(im)

            # Outer card border
            draw.rounded_rectangle(
                [24, 48, self.width - 24, self.height - 48],
                radius=32,
                fill=palette["card_bg"],
                outline=palette["card_border"],
                width=3
            )

            # Top progress segmented indicator
            self._draw_progress_bar(draw, p, scene_idx, total_scenes, palette)

            # Top badge & mode
            self._draw_header(draw, visual_style, scene_idx, total_scenes, palette)

            # On-screen headline
            self._draw_headline(draw, on_screen_text, palette)

            # Dispatch central animated subject according to visual style
            if visual_style in ["talking_characters", "characters", "everyday"]:
                self._draw_everyday_reel_scene(draw, frame_num, total_frames, p, scene, scene_idx, total_scenes)
            elif visual_style == "inside_your_body":
                self._draw_inside_body_scene(draw, frame_num, total_frames, p, scene, scene_idx, total_scenes)
            elif visual_style == "everyday_human":
                self._draw_everyday_human(draw, frame_num, total_frames, p, scene, scene_idx, palette)
            elif visual_style == "animated_explainer":
                self._draw_animated_explainer(draw, frame_num, total_frames, p, scene, scene_idx, palette)
            else:  # professional
                self._draw_professional_mode(draw, frame_num, total_frames, p, scene)

            # Bottom synchronized subtitle box
            self._draw_subtitle_box(draw, subtitle_text, p, palette)

            frame_file = out_dir / f"frame_{frame_num:04d}.png"
            im.save(str(frame_file), "PNG")
            frame_paths.append(frame_file)

        return frame_paths

    # -------------------------------------------------------------
    # Common UI Elements
    # -------------------------------------------------------------
    def _draw_progress_bar(self, draw: ImageDraw.ImageDraw, p: float, scene_idx: int, total_scenes: int, palette: Optional[Dict[str, Any]] = None):
        pal = palette or getattr(self, "current_palette", None) or self.get_theme("warm_editorial")
        bar_y = 75
        margin = 48
        bar_w = (self.width - (margin * 2) - ((total_scenes - 1) * 8)) // total_scenes
        for s in range(total_scenes):
            sx = margin + s * (bar_w + 8)
            ex = sx + bar_w
            if s < scene_idx:
                fill = pal["progress_active"]
            elif s == scene_idx:
                draw.rounded_rectangle([sx, bar_y, ex, bar_y + 6], radius=3, fill=pal["progress_bg"])
                fill_w = int(bar_w * p)
                if fill_w > 0:
                    draw.rounded_rectangle([sx, bar_y, sx + fill_w, bar_y + 6], radius=3, fill=pal["progress_active"])
                continue
            else:
                fill = pal["progress_bg"]
            draw.rounded_rectangle([sx, bar_y, ex, bar_y + 6], radius=3, fill=fill)

    def _draw_header(self, draw: ImageDraw.ImageDraw, visual_style: str, scene_idx: int, total_scenes: int, palette: Optional[Dict[str, Any]] = None):
        pal = palette or getattr(self, "current_palette", None) or self.get_theme("warm_editorial")
        font_badge = self._get_font(18)
        font_part = self._get_font(18)

        style_labels = {
            "talking_characters": "STEER EVERYDAY • ANIMATED REEL",
            "characters": "STEER EVERYDAY • ANIMATED REEL",
            "everyday": "STEER EVERYDAY • ANIMATED REEL",
            "inside_your_body": "STEER BIOLOGY • INSIDE YOUR BODY",
            "everyday_human": "STEER LIFESTYLE • DAILY HABIT",
            "animated_explainer": "STEER METABOLICS • ANIMATED EXPLAINER",
            "professional": "STEER CLINICAL • EVIDENCE BRIEFING"
        }
        badge_text = style_labels.get(visual_style, "STEER HEALTH REEL")

        draw.rounded_rectangle([48, 102, 430, 138], radius=18, fill=pal["badge_bg"])
        draw.text((64, 110), badge_text, font=font_badge, fill=pal["badge_text"])
        draw.text((self.width - 150, 110), f"PART {scene_idx + 1:02d}/{total_scenes:02d}", font=font_part, fill=pal["text_muted"])

    def _draw_headline(self, draw: ImageDraw.ImageDraw, text: str, palette: Optional[Dict[str, Any]] = None):
        pal = palette or getattr(self, "current_palette", None) or self.get_theme("warm_editorial")
        font = self._get_font(32)
        lines = self._wrap_text(text, font, self.width - 96, draw)
        cur_y = 155
        for line in lines[:2]:
            draw.text((48, cur_y), line, font=font, fill=pal["text_primary"])
            cur_y += 38

    def _draw_subtitle_box(self, draw: ImageDraw.ImageDraw, text: str, progress: float, palette: Optional[Dict[str, Any]] = None):
        pal = palette or getattr(self, "current_palette", None) or self.get_theme("warm_editorial")
        box_top = self.height - 210
        box_bottom = self.height - 90
        draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=20, fill=pal["sub_bg"])

        font_sub = self._get_font(25)
        lines = self._wrap_text(text, font_sub, self.width - 130, draw)
        
        start_y = box_top + 22 if len(lines) == 1 else box_top + 14
        for l in lines[:2]:
            bbox = draw.textbbox((0, 0), l, font=font_sub)
            lw = bbox[2] - bbox[0]
            draw.text(((self.width - lw) // 2, start_y), l, font=font_sub, fill=pal["sub_text"])
            start_y += 34

    # -------------------------------------------------------------
    # CHARACTER COMPONENT: 3D Glossy Apple Fruit Character
    # -------------------------------------------------------------
    def _draw_apple_character(
        self,
        draw: ImageDraw.ImageDraw,
        cx: int,
        cy: int,
        r: int,
        frame: int,
        mouth_mode: str = "talking",
        gesture: str = "wave"
    ):
        bob = int(8 * math.sin(2 * math.pi * frame / 18))
        cy = cy + bob

        # Soft ambient glow behind apple
        glow_r = r + 25
        for gr in range(glow_r, r, -5):
            alpha_glow = (255, 230, 215)
            draw.ellipse([cx - gr, cy - gr, cx + gr, cy + gr], fill=alpha_glow)

        # Apple Body with 3D spherical shading
        # 1. Dark crimson base
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(185, 28, 28), outline=(153, 27, 27), width=4)
        # 2. Main glossy red highlight zone
        draw.ellipse([cx - r + 8, cy - r + 10, cx + r - 12, cy + r - 12], fill=(225, 29, 42))
        # 3. Soft upper-left specular curve
        draw.arc([cx - r + 20, cy - r + 20, cx - 15, cy - 10], start=160, end=290, fill=(254, 202, 202), width=10)
        draw.ellipse([cx - r + 38, cy - r + 38, cx - r + 56, cy - r + 56], fill=(255, 255, 255))

        # Green leaf and stem with natural sway
        sway = int(6 * math.sin(2 * math.pi * frame / 16))
        draw.line([cx, cy - r + 10, cx + sway, cy - r - 35], fill=(92, 64, 51), width=6)
        leaf_pts = [
            (cx + sway, cy - r - 25),
            (cx + 35 + sway, cy - r - 55),
            (cx + 70 + sway, cy - r - 35),
            (cx + 35 + sway, cy - r - 18)
        ]
        draw.polygon(leaf_pts, fill=(74, 222, 128), outline=(22, 163, 74))
        draw.line([cx + sway, cy - r - 25, cx + 50 + sway, cy - r - 35], fill=(22, 163, 74), width=2)

        # Rosy Cheeks
        draw.ellipse([cx - int(r*0.65), cy + 20, cx - int(r*0.35), cy + 46], fill=(254, 150, 150))
        draw.ellipse([cx + int(r*0.35), cy + 20, cx + int(r*0.65), cy + 46], fill=(254, 150, 150))

        # Big Expressive Eyes with Anime Specular Twinkle
        blink = (frame % 40) in [0, 1, 2]
        eye_y = cy - 22
        left_eye_x = cx - int(r * 0.42)
        right_eye_x = cx + int(r * 0.42)
        eye_w = 22
        eye_h = 32

        if blink:
            draw.line([left_eye_x - 18, eye_y, left_eye_x + 18, eye_y], fill=self.c_ink, width=6)
            draw.line([right_eye_x - 18, eye_y, right_eye_x + 18, eye_y], fill=self.c_ink, width=6)
        else:
            # Sclera / eye background
            draw.ellipse([left_eye_x - eye_w, eye_y - eye_h, left_eye_x + eye_w, eye_y + eye_h], fill=(255, 255, 255), outline=self.c_ink, width=3)
            draw.ellipse([right_eye_x - eye_w, eye_y - eye_h, right_eye_x + eye_w, eye_y + eye_h], fill=(255, 255, 255), outline=self.c_ink, width=3)
            # Dark iris
            draw.ellipse([left_eye_x - eye_w + 4, eye_y - eye_h + 4, left_eye_x + eye_w - 2, eye_y + eye_h - 2], fill=(30, 20, 25))
            draw.ellipse([right_eye_x - eye_w + 2, eye_y - eye_h + 4, right_eye_x + eye_w - 4, eye_y + eye_h - 2], fill=(30, 20, 25))
            # Primary white catchlight
            draw.ellipse([left_eye_x - 12, eye_y - 20, left_eye_x + 4, eye_y - 4], fill=(255, 255, 255))
            draw.ellipse([right_eye_x - 6, eye_y - 20, right_eye_x + 10, eye_y - 4], fill=(255, 255, 255))
            # Secondary twinkle catchlight
            draw.ellipse([left_eye_x + 2, eye_y + 8, left_eye_x + 10, eye_y + 16], fill=(255, 255, 255))
            draw.ellipse([right_eye_x + 6, eye_y + 8, right_eye_x + 14, eye_y + 16], fill=(255, 255, 255))

        # Eyebrows
        eb_y = eye_y - eye_h - 10
        draw.arc([left_eye_x - 22, eb_y, left_eye_x + 22, eb_y + 18], start=195, end=345, fill=self.c_ink, width=4)
        draw.arc([right_eye_x - 22, eb_y, right_eye_x + 22, eb_y + 18], start=195, end=345, fill=self.c_ink, width=4)

        # Mouth with phoneme animation or smile
        mouth_y = cy + 42
        if mouth_mode == "smile":
            draw.arc([cx - 35, mouth_y - 15, cx + 35, mouth_y + 25], start=20, end=160, fill=self.c_ink, width=6)
            draw.polygon([(cx - 25, mouth_y), (cx + 25, mouth_y), (cx, mouth_y + 26)], fill=(225, 29, 72))
        else:
            phoneme = (frame // 3) % 4
            if phoneme == 0:
                draw.arc([cx - 30, mouth_y - 12, cx + 30, mouth_y + 20], start=20, end=160, fill=self.c_ink, width=6)
            elif phoneme == 1:
                # Open talking mouth with teeth and tongue
                draw.ellipse([cx - 26, mouth_y - 12, cx + 26, mouth_y + 24], fill=(136, 19, 55), outline=self.c_ink, width=3)
                draw.ellipse([cx - 16, mouth_y + 6, cx + 16, mouth_y + 22], fill=(251, 113, 133))
                draw.line([cx - 16, mouth_y - 4, cx + 16, mouth_y - 4], fill=(255, 255, 255), width=4)
            elif phoneme == 2:
                draw.ellipse([cx - 32, mouth_y - 16, cx + 32, mouth_y + 30], fill=(136, 19, 55), outline=self.c_ink, width=3)
                draw.ellipse([cx - 20, mouth_y + 10, cx + 20, mouth_y + 28], fill=(251, 113, 133))
            else:
                draw.ellipse([cx - 18, mouth_y - 8, cx + 18, mouth_y + 18], fill=(136, 19, 55), outline=self.c_ink, width=3)

        # Gesturing Arms/Hands
        if gesture == "cheer":
            # Both hands raised in celebration!
            draw.line([cx - r + 15, cy + 15, cx - r - 35, cy - 45], fill=(225, 29, 42), width=10)
            draw.ellipse([cx - r - 48, cy - 60, cx - r - 22, cy - 34], fill=(254, 150, 150))
            draw.line([cx + r - 15, cy + 15, cx + r + 35, cy - 45], fill=(225, 29, 42), width=10)
            draw.ellipse([cx + r + 22, cy - 60, cx + r + 48, cy - 34], fill=(254, 150, 150))
        elif gesture == "point_right":
            # Arm pointing towards the gut character on the right
            arm_reach = int(10 * math.sin(frame * 0.4))
            draw.line([cx + r - 20, cy + 20, cx + r + 50 + arm_reach, cy + 10], fill=(225, 29, 42), width=10)
            draw.ellipse([cx + r + 45 + arm_reach, cy - 2, cx + r + 75 + arm_reach, cy + 22], fill=(254, 150, 150))
        else:
            # Waving right hand
            wave = int(14 * math.sin(2 * math.pi * frame / 14))
            draw.line([cx + r - 15, cy + 20, cx + r + 40, cy - 10 + wave], fill=(225, 29, 42), width=10)
            draw.ellipse([cx + r + 30, cy - 25 + wave, cx + r + 56, cy + 2 + wave], fill=(254, 150, 150))

    # -------------------------------------------------------------
    # CHARACTER COMPONENT: Cute Pink Intestine / Gut Character
    # -------------------------------------------------------------
    def _draw_gut_character(
        self,
        draw: ImageDraw.ImageDraw,
        cx: int,
        cy: int,
        frame: int,
        mouth_mode: str = "talking",
        cheer: bool = False
    ):
        bob = int(6 * math.sin(2 * math.pi * frame / 20 + 1.0))
        cy = cy + bob

        # Intestinal Loops (layered curvy pink segments)
        gut_pink = (255, 175, 189)
        gut_outline = (225, 112, 134)
        
        # Upper lobes
        draw.ellipse([cx - 85, cy - 70, cx - 15, cy - 10], fill=gut_pink, outline=gut_outline, width=5)
        draw.ellipse([cx - 20, cy - 80, cx + 55, cy - 18], fill=gut_pink, outline=gut_outline, width=5)
        draw.ellipse([cx + 25, cy - 65, cx + 90, cy - 8], fill=gut_pink, outline=gut_outline, width=5)
        
        # Lower lobes
        draw.ellipse([cx - 95, cy - 15, cx - 15, cy + 55], fill=gut_pink, outline=gut_outline, width=5)
        draw.ellipse([cx - 30, cy - 5, cx + 45, cy + 65], fill=gut_pink, outline=gut_outline, width=5)
        draw.ellipse([cx + 25, cy - 10, cx + 95, cy + 60], fill=gut_pink, outline=gut_outline, width=5)
        
        # Smooth central belly merge
        draw.rounded_rectangle([cx - 65, cy - 45, cx + 65, cy + 45], radius=25, fill=gut_pink)

        # Rosy Cheeks
        draw.ellipse([cx - 62, cy + 6, cx - 36, cy + 28], fill=(255, 130, 155))
        draw.ellipse([cx + 36, cy + 6, cx + 62, cy + 28], fill=(255, 130, 155))

        # Cute Large Anime Eyes
        blink = (frame % 38) in [0, 1, 2]
        eye_y = cy - 18
        if blink:
            draw.line([cx - 45, eye_y, cx - 15, eye_y], fill=self.c_ink, width=5)
            draw.line([cx + 15, eye_y, cx + 45, eye_y], fill=self.c_ink, width=5)
        else:
            # Left & Right eyes
            draw.ellipse([cx - 46, eye_y - 20, cx - 14, eye_y + 18], fill=(30, 20, 25))
            draw.ellipse([cx + 14, eye_y - 20, cx + 46, eye_y + 18], fill=(30, 20, 25))
            # Catchlights
            draw.ellipse([cx - 42, eye_y - 16, cx - 26, eye_y - 4], fill=(255, 255, 255))
            draw.ellipse([cx + 18, eye_y - 16, cx + 34, eye_y - 4], fill=(255, 255, 255))
            draw.ellipse([cx - 26, eye_y + 6, cx - 20, eye_y + 12], fill=(255, 255, 255))
            draw.ellipse([cx + 34, eye_y + 6, cx + 40, eye_y + 12], fill=(255, 255, 255))

        # Smiling / Talking Mouth
        mouth_y = cy + 24
        if mouth_mode == "smile" or cheer:
            draw.arc([cx - 26, mouth_y - 10, cx + 26, mouth_y + 22], start=20, end=160, fill=self.c_ink, width=5)
            draw.polygon([(cx - 18, mouth_y), (cx + 18, mouth_y), (cx, mouth_y + 20)], fill=(225, 29, 72))
        else:
            phoneme = (frame // 4) % 3
            if phoneme == 0:
                draw.arc([cx - 22, mouth_y - 8, cx + 22, mouth_y + 16], start=20, end=160, fill=self.c_ink, width=5)
            elif phoneme == 1:
                draw.ellipse([cx - 18, mouth_y - 8, cx + 18, mouth_y + 18], fill=(136, 19, 55), outline=self.c_ink, width=3)
                draw.ellipse([cx - 10, mouth_y + 5, cx + 10, mouth_y + 16], fill=(251, 113, 133))
            else:
                draw.ellipse([cx - 14, mouth_y - 6, cx + 14, mouth_y + 14], fill=(136, 19, 55), outline=self.c_ink, width=3)

        # Arms
        if cheer:
            draw.line([cx - 75, cy - 10, cx - 110, cy - 65], fill=gut_pink, width=9)
            draw.ellipse([cx - 122, cy - 78, cx - 98, cy - 54], fill=(255, 140, 160))
            draw.line([cx + 75, cy - 10, cx + 110, cy - 65], fill=gut_pink, width=9)
            draw.ellipse([cx + 98, cy - 78, cx + 122, cy - 54], fill=(255, 140, 160))
        else:
            # Gentle hand wave
            wave = int(10 * math.sin(frame * 0.35))
            draw.line([cx - 75, cy + 10, cx - 105, cy + wave], fill=gut_pink, width=9)
            draw.ellipse([cx - 116, cy - 10 + wave, cx - 94, cy + 12 + wave], fill=(255, 140, 160))
            draw.line([cx + 75, cy + 10, cx + 105, cy + 25], fill=gut_pink, width=9)
            draw.ellipse([cx + 94, cy + 15, cx + 116, cy + 37], fill=(255, 140, 160))

    # -------------------------------------------------------------
    # CHARACTER COMPONENT: Friendly Colorful Microbiome Bacteria
    # -------------------------------------------------------------
    def _draw_microbe(self, draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int, color_base: tuple, frame: int, seed: int):
        wiggle = int(5 * math.sin(frame * 0.3 + seed))
        cy = cy + wiggle
        
        # Round friendly microbe cell
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color_base, outline=(255, 255, 255), width=2)
        # Cute little eyes
        draw.ellipse([cx - 7, cy - 4, cx - 2, cy + 3], fill=(30, 20, 25))
        draw.ellipse([cx + 2, cy - 4, cx + 7, cy + 3], fill=(30, 20, 25))
        draw.ellipse([cx - 6, cy - 3, cx - 4, cy - 1], fill=(255, 255, 255))
        draw.ellipse([cx + 3, cy - 3, cx + 5, cy - 1], fill=(255, 255, 255))
        # Happy smile
        draw.arc([cx - 6, cy + 2, cx + 6, cy + 9], start=20, end=160, fill=(30, 20, 25), width=2)
        # Little sensory nubs / tentacles
        for a in range(0, 360, 60):
            rad = math.radians(a + frame * 4)
            nx = cx + int((r + 4) * math.cos(rad))
            ny = cy + int((r + 4) * math.sin(rad))
            draw.ellipse([nx - 2, ny - 2, nx + 2, ny + 2], fill=color_base)

    # -------------------------------------------------------------
    # CHARACTER COMPONENT: Relatable Human Girl Cartoon
    # -------------------------------------------------------------
    def _draw_human_girl(
        self,
        draw: ImageDraw.ImageDraw,
        cx: int,
        cy: int,
        frame: int,
        action: str = "salad"
    ):
        bob = int(4 * math.sin(frame * 0.25))
        cy = cy + bob

        skin_color = (255, 219, 186)
        skin_shadow = (235, 185, 150)
        hair_color = (45, 25, 20)

        # Hair Bun on top
        draw.ellipse([cx - 26, cy - 135, cx + 26, cy - 85], fill=hair_color)

        # Head / Face
        draw.ellipse([cx - 55, cy - 100, cx + 55, cy + 10], fill=skin_color)
        
        # Hair front strands framing face
        draw.ellipse([cx - 60, cy - 110, cx - 20, cy - 50], fill=hair_color)
        draw.ellipse([cx + 20, cy - 110, cx + 60, cy - 50], fill=hair_color)
        draw.ellipse([cx - 45, cy - 115, cx + 45, cy - 80], fill=hair_color)

        # Rosy Cheeks
        draw.ellipse([cx - 45, cy - 32, cx - 22, cy - 14], fill=(255, 160, 160))
        draw.ellipse([cx + 22, cy - 32, cx + 45, cy - 14], fill=(255, 160, 160))

        # Expressive Eyes & Smile
        eye_y = cy - 45
        draw.ellipse([cx - 36, eye_y - 12, cx - 18, eye_y + 10], fill=hair_color)
        draw.ellipse([cx + 18, eye_y - 12, cx + 36, eye_y + 10], fill=hair_color)
        draw.ellipse([cx - 32, eye_y - 10, cx - 24, eye_y - 2], fill=(255, 255, 255))
        draw.ellipse([cx + 22, eye_y - 10, cx + 30, eye_y - 2], fill=(255, 255, 255))

        # Smile
        draw.arc([cx - 20, cy - 15, cx + 20, cy + 6], start=20, end=160, fill=(180, 40, 40), width=4)

        # Torso / Blue Casual Shirt
        shirt_color = (79, 142, 198)
        draw.rounded_rectangle([cx - 55, cy + 15, cx + 55, cy + 180], radius=16, fill=shirt_color)
        # Shirt Collar
        draw.polygon([(cx - 20, cy + 15), (cx + 20, cy + 15), (cx, cy + 45)], fill=skin_color)

        # Action: Holding Salad Bowl or Drinking Smoothie
        if action == "salad":
            # Arms holding a colorful salad bowl
            draw.line([cx - 45, cy + 40, cx - 30, cy + 100], fill=shirt_color, width=16)
            draw.line([cx + 45, cy + 40, cx + 30, cy + 100], fill=shirt_color, width=16)
            # Salad Bowl (white porcelain)
            bowl_y = cy + 90
            draw.arc([cx - 70, bowl_y - 20, cx + 70, bowl_y + 60], start=0, end=180, fill=(240, 240, 245), width=8)
            draw.ellipse([cx - 68, bowl_y - 15, cx + 68, bowl_y + 15], fill=(255, 255, 255), outline=(200, 200, 210), width=2)
            # Salad Contents: Greens, cherry tomatoes, seeds
            draw.ellipse([cx - 45, bowl_y - 12, cx - 15, bowl_y + 8], fill=(74, 222, 128))
            draw.ellipse([cx + 10, bowl_y - 10, cx + 45, bowl_y + 10], fill=(34, 197, 94))
            draw.ellipse([cx - 10, bowl_y - 14, cx + 18, bowl_y + 6], fill=(239, 68, 68))  # tomato
            draw.ellipse([cx + 25, bowl_y - 8, cx + 38, bowl_y + 4], fill=(239, 68, 68))
        elif action == "smoothie":
            # Arm holding smoothie glass with straw & other hand giving thumbs up!
            # Left arm holding glass
            draw.line([cx - 45, cy + 40, cx - 25, cy + 95], fill=shirt_color, width=16)
            glass_x = cx - 25
            glass_y = cy + 85
            # Smoothie Glass with orange/green nutritious glow
            draw.rounded_rectangle([glass_x - 18, glass_y, glass_x + 18, glass_y + 60], radius=6, fill=(251, 146, 60), outline=(255, 255, 255), width=2)
            # Straw extending up to girl's smile
            draw.line([glass_x + 5, glass_y + 10, cx - 5, cy + 5], fill=(254, 202, 202), width=5)
            # Right Arm giving Thumbs-Up!
            draw.line([cx + 45, cy + 40, cx + 85, cy + 65], fill=shirt_color, width=16)
            thumb_x = cx + 90
            thumb_y = cy + 60
            draw.ellipse([thumb_x - 10, thumb_y - 10, thumb_x + 12, thumb_y + 12], fill=skin_color)
            draw.line([thumb_x - 2, thumb_y + 5, thumb_x - 2, thumb_y - 16], fill=skin_shadow, width=7)

    # -------------------------------------------------------------
    # 1. EVERYDAY MODE SCENE RENDERER (7 Distinct Storyboard Scenes)
    # -------------------------------------------------------------
    def _draw_everyday_reel_scene(
        self,
        draw: ImageDraw.ImageDraw,
        frame: int,
        total_frames: int,
        p: float,
        scene: Dict[str, Any],
        scene_idx: int,
        total_scenes: int
    ):
        # Determine narrative scene role (7 scenes or modulo)
        scene_role = scene_idx % 7

        if scene_role == 0:
            # ---------------------------------------------------------
            # Scene 1 (0-3s): Hook (Curiosity) - "Hey! I'm not just a fruit..."
            # ---------------------------------------------------------
            cx = self.width // 2
            cy = 580

            # Golden glowing sunburst / kitchen background sparkles
            for sp_idx in range(12):
                ang = math.radians(sp_idx * 30 + frame * 2)
                dist = 260 + int(30 * math.sin(frame * 0.2 + sp_idx))
                sx = cx + int(dist * math.cos(ang))
                sy = cy + int(dist * math.sin(ang))
                draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 215, 0))

            # Central 3D Apple character
            self._draw_apple_character(draw, cx, cy, 155, frame, mouth_mode="talking", gesture="wave")

            # Speech bubble
            bubble_top = 280
            draw.rounded_rectangle([80, bubble_top, self.width - 80, bubble_top + 95], radius=20, fill=self.c_white, outline=self.c_blush, width=3)
            # Speech arrow
            draw.polygon([(cx - 15, bubble_top + 95), (cx + 15, bubble_top + 95), (cx, bubble_top + 115)], fill=self.c_white)
            font_hook = self._get_font(28)
            hook_text = scene.get("on_screen_text") or "Hey! I'm not just a fruit..."
            lines = self._wrap_text(hook_text, font_hook, self.width - 190, draw)
            by = bubble_top + 22
            for l in lines[:2]:
                bbox = draw.textbbox((0, 0), l, font=font_hook)
                lw = bbox[2] - bbox[0]
                draw.text(((self.width - lw) // 2, by), l, font=font_hook, fill=self.c_rust)
                by += 34

        elif scene_role == 1:
            # ---------------------------------------------------------
            # Scene 2 (3-8s): Character Interaction - Apple & Gut Talking
            # ---------------------------------------------------------
            apple_x = 220
            apple_y = 590
            gut_x = self.width - 210
            gut_y = 590

            # Apple on left pointing right
            self._draw_apple_character(draw, apple_x, apple_y, 115, frame, mouth_mode="talking", gesture="point_right")
            # Cute Gut on right listening and smiling
            self._draw_gut_character(draw, gut_x, gut_y, frame, mouth_mode="smile")

            # Dialogue Speech Bubble between characters
            bubble_top = 310
            draw.rounded_rectangle([70, bubble_top, self.width - 70, bubble_top + 105], radius=22, fill=self.c_white, outline=self.c_rust, width=3)
            draw.polygon([(apple_x + 60, bubble_top + 105), (apple_x + 90, bubble_top + 105), (apple_x + 75, bubble_top + 125)], fill=self.c_white)

            font_b = self._get_font(26)
            tip_text = scene.get("on_screen_text") or "I help your gut stay healthy!"
            lines = self._wrap_text(f"“{tip_text}”", font_b, self.width - 180, draw)
            by = bubble_top + 24
            for l in lines[:2]:
                bbox = draw.textbbox((0, 0), l, font=font_b)
                lw = bbox[2] - bbox[0]
                draw.text(((self.width - lw) // 2, by), l, font=font_b, fill=self.c_maroon)
                by += 34

        elif scene_role == 2:
            # ---------------------------------------------------------
            # Scene 3 (8-15s): Animated Explanation - Gut & Microbes
            # ---------------------------------------------------------
            gut_x = self.width // 2
            gut_y = 600

            # Floating friendly microbiome bacteria around Gut
            microbe_colors = [(56, 189, 248), (168, 85, 247), (250, 204, 21), (244, 114, 182), (74, 222, 128)]
            microbe_coords = [
                (140, 440, 32),
                (self.width - 140, 450, 30),
                (120, 720, 28),
                (self.width - 130, 710, 34),
                (self.width // 2, 380, 26)
            ]
            for m_idx, (mx, my, mr) in enumerate(microbe_coords):
                self._draw_microbe(draw, mx, my, mr, microbe_colors[m_idx % len(microbe_colors)], frame, m_idx * 17)

            # Central Gut Character talking
            self._draw_gut_character(draw, gut_x, gut_y, frame, mouth_mode="talking")

            # Explanation Callout Box
            callout_top = 280
            draw.rounded_rectangle([70, callout_top, self.width - 70, callout_top + 80], radius=18, fill=self.c_white, outline=self.c_blush, width=2)
            font_exp = self._get_font(24)
            exp_text = scene.get("on_screen_text") or "I feed the good bacteria in your gut!"
            bbox = draw.textbbox((0, 0), exp_text, font=font_exp)
            lw = bbox[2] - bbox[0]
            draw.text(((self.width - lw) // 2, callout_top + 24), exp_text, font=font_exp, fill=self.c_rust)

        elif scene_role == 3:
            # ---------------------------------------------------------
            # Scene 4 (15-25s): Interactive Question - Girl & Food Quiz
            # ---------------------------------------------------------
            girl_x = 230
            girl_y = 590
            self._draw_human_girl(draw, girl_x, girl_y, frame, action="salad")

            # Quiz Checklist on Right
            quiz_x = 420
            quiz_y_start = 450
            checklist_items = ["Fruits", "Vegetables", "Whole Grains"]
            
            # Question banner
            draw.rounded_rectangle([70, 280, self.width - 70, 360], radius=18, fill=self.c_white, outline=self.c_rust, width=3)
            font_q = self._get_font(26)
            q_text = "Which foods help your gut?"
            bbox = draw.textbbox((0, 0), q_text, font=font_q)
            lw = bbox[2] - bbox[0]
            draw.text(((self.width - lw) // 2, 305), q_text, font=font_q, fill=self.c_ink)

            font_chk = self._get_font(22)
            for idx, item in enumerate(checklist_items):
                item_y = quiz_y_start + idx * 75
                draw.rounded_rectangle([quiz_x, item_y, self.width - 60, item_y + 60], radius=14, fill=self.c_white, outline=self.c_clay, width=2)
                # Green checkmark circle
                draw.ellipse([quiz_x + 14, item_y + 14, quiz_x + 46, item_y + 46], fill=self.c_green)
                draw.text((quiz_x + 22, item_y + 16), "✔", font=self._get_font(20), fill=self.c_white)
                draw.text((quiz_x + 60, item_y + 18), item, font=font_chk, fill=self.c_ink)

        elif scene_role == 4:
            # ---------------------------------------------------------
            # Scene 5 (25-35s): Positive Feedback - "Good choice!" Celebration
            # ---------------------------------------------------------
            apple_x = 240
            apple_y = 660
            gut_x = self.width - 230
            gut_y = 660

            # Radiating gold sunburst
            cx = self.width // 2
            cy = 380
            for r_idx in range(16):
                ang = math.radians(r_idx * 22.5 + frame * 3)
                rx = cx + int(150 * math.cos(ang))
                ry = cy + int(150 * math.sin(ang))
                draw.line([cx, cy, rx, ry], fill=(254, 240, 138), width=3)

            # Big glowing green checkmark badge
            badge_r = 75
            pulse = int(5 * math.sin(frame * 0.4))
            draw.ellipse([cx - badge_r - pulse, cy - badge_r - pulse, cx + badge_r + pulse, cy + badge_r + pulse], fill=self.c_green, outline=(255, 255, 255), width=6)
            draw.text((cx - 36, cy - 50), "✔", font=self._get_font(72), fill=self.c_white)

            font_good = self._get_font(34)
            draw.text((cx - 95, cy + 90), "Good choice!", font=font_good, fill=self.c_green)

            # Apple & Gut cheering side by side below!
            self._draw_apple_character(draw, apple_x, apple_y, 110, frame, mouth_mode="smile", gesture="cheer")
            self._draw_gut_character(draw, gut_x, gut_y, frame, mouth_mode="smile", cheer=True)

        elif scene_role == 5:
            # ---------------------------------------------------------
            # Scene 6 (35-42s): Key Takeaway - Girl Drinking Smoothie & Thumbs Up
            # ---------------------------------------------------------
            girl_x = self.width // 2
            girl_y = 570
            self._draw_human_girl(draw, girl_x, girl_y, frame, action="smoothie")

            # Habit Takeaway Banner
            banner_top = 280
            draw.rounded_rectangle([60, banner_top, self.width - 60, banner_top + 110], radius=22, fill=self.c_white, outline=self.c_rust, width=3)
            font_tw = self._get_font(30)
            font_sub = self._get_font(20)
            draw.text((85, banner_top + 18), "Small habits • Big difference!", font=font_tw, fill=self.c_rust)
            
            takeaway_sub = scene.get("on_screen_text") or "Consistent micro-habits protect metabolic health."
            lines = self._wrap_text(takeaway_sub, font_sub, self.width - 150, draw)
            by = banner_top + 58
            for l in lines[:2]:
                draw.text((85, by), l, font=font_sub, fill=self.c_ink)
                by += 26

        else:
            # ---------------------------------------------------------
            # Scene 7 (42-45s): Handoff / CTA - Group Outro & Steer Handoff
            # ---------------------------------------------------------
            # Group: Girl in center, Apple on left, Gut on right
            self._draw_human_girl(draw, self.width // 2, 590, frame, action="salad")
            self._draw_apple_character(draw, 140, 680, 85, frame, mouth_mode="smile", gesture="cheer")
            self._draw_gut_character(draw, self.width - 140, 680, frame, mouth_mode="smile", cheer=True)

            # Outro Steer Button
            cta_top = 280
            draw.rounded_rectangle([60, cta_top, self.width - 60, cta_top + 130], radius=24, fill=self.c_white, outline=self.c_blush, width=3)
            font_cta_lbl = self._get_font(22)
            draw.text((85, cta_top + 20), "Want to know more science-backed tips?", font=font_cta_lbl, fill=self.c_ink)

            # CTA Pill Button
            btn_top = cta_top + 60
            draw.rounded_rectangle([85, btn_top, self.width - 85, btn_top + 50], radius=25, fill=self.c_rust)
            font_btn = self._get_font(22)
            btn_txt = "Explore on Steer  ➔"
            bbox = draw.textbbox((0, 0), btn_txt, font=font_btn)
            bw = bbox[2] - bbox[0]
            draw.text(((self.width - bw) // 2, btn_top + 12), btn_txt, font=font_btn, fill=self.c_white)

    # -------------------------------------------------------------
    # 2. INSIDE YOUR BODY SCENE RENDERER (Finding-Driven Biological Scenes)
    # -------------------------------------------------------------
    def _draw_inside_body_scene(
        self,
        draw: ImageDraw.ImageDraw,
        frame: int,
        total_frames: int,
        p: float,
        scene: Dict[str, Any],
        scene_idx: int,
        total_scenes: int
    ):
        organ = scene.get("organ_character")
        if not organ:
            # Alternate through finding archetypes based on scene index
            archetypes = ["red_blood_cell", "brain", "stomach"]
            organ = archetypes[scene_idx % len(archetypes)]

        if organ == "red_blood_cell" or scene_idx == 0:
            # ---------------------------------------------------------
            # Scene 1: Blood Circulation - Red Blood Cell Character
            # ---------------------------------------------------------
            # Undulating arterial bloodstream container
            box_top = 240
            box_bottom = 980
            draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=28, fill=(254, 242, 242), outline=(239, 68, 68), width=3)
            
            draw.text((75, box_top + 22), "BLOODSTREAM & OXYGEN TRANSPORT", font=self._get_font(22), fill=(185, 28, 28))

            # Flowing vessel waves
            for w_idx in range(6):
                wy = box_top + 80 + w_idx * 110
                curve = int(12 * math.sin(frame * 0.2 + w_idx))
                draw.arc([40, wy + curve, self.width - 40, wy + 70 + curve], start=0, end=180, fill=(254, 202, 202), width=3)

            # Drifting small red blood cells in background
            for s_idx in range(8):
                sx = (s_idx * 100 + frame * 6) % (self.width - 120) + 60
                sy = box_top + 100 + (s_idx * 45) % 450
                draw.ellipse([sx - 16, sy - 10, sx + 16, sy + 10], fill=(220, 38, 38))

            # Floating cyan oxygen molecules (O2)
            for o_idx in range(5):
                ox = (o_idx * 140 - frame * 4) % (self.width - 140) + 70
                oy = box_top + 160 + (o_idx * 65) % 400
                draw.ellipse([ox - 16, oy - 16, ox + 16, oy + 16], fill=(56, 189, 248), outline=(255, 255, 255), width=2)
                draw.text((ox - 10, oy - 10), "O₂", font=self._get_font(16), fill=self.c_white)

            # Central Cute Red Blood Cell Character!
            rbc_cx = self.width // 2
            rbc_cy = 580 + int(8 * math.sin(frame * 0.3))
            rbc_r = 135

            # 3D glossy red biconcave body
            draw.ellipse([rbc_cx - rbc_r, rbc_cy - rbc_r, rbc_cx + rbc_r, rbc_cy + rbc_r], fill=(220, 38, 38), outline=(185, 28, 28), width=5)
            # Inner biconcave depression
            draw.ellipse([rbc_cx - 75, rbc_cy - 75, rbc_cx + 75, rbc_cy + 75], fill=(185, 28, 28))
            draw.ellipse([rbc_cx - 55, rbc_cy - 55, rbc_cx + 55, rbc_cy + 55], fill=(239, 68, 68))
            draw.ellipse([rbc_cx - 95, rbc_cy - 95, rbc_cx - 45, rbc_cy - 45], fill=(254, 202, 202))

            # Big shiny eyes
            blink = (frame % 36) in [0, 1, 2]
            eye_y = rbc_cy - 15
            if blink:
                draw.line([rbc_cx - 55, eye_y, rbc_cx - 15, eye_y], fill=(30, 20, 25), width=5)
                draw.line([rbc_cx + 15, eye_y, rbc_cx + 55, eye_y], fill=(30, 20, 25), width=5)
            else:
                draw.ellipse([rbc_cx - 55, eye_y - 20, rbc_cx - 20, eye_y + 18], fill=(30, 20, 25))
                draw.ellipse([rbc_cx + 20, eye_y - 20, rbc_cx + 55, eye_y + 18], fill=(30, 20, 25))
                draw.ellipse([rbc_cx - 50, eye_y - 16, rbc_cx - 34, eye_y - 2], fill=(255, 255, 255))
                draw.ellipse([rbc_cx + 26, eye_y - 16, rbc_cx + 42, eye_y - 2], fill=(255, 255, 255))

            # Happy open mouth
            draw.arc([rbc_cx - 28, rbc_cy + 15, rbc_cx + 28, rbc_cy + 45], start=20, end=160, fill=(30, 20, 25), width=5)
            draw.polygon([(rbc_cx - 18, rbc_cy + 25), (rbc_cx + 18, rbc_cy + 25), (rbc_cx, rbc_cy + 42)], fill=(255, 255, 255))

            # Waving hands holding oxygen molecule
            draw.line([rbc_cx - rbc_r + 15, rbc_cy + 10, rbc_cx - rbc_r - 35, rbc_cy - 20], fill=(220, 38, 38), width=10)
            draw.line([rbc_cx + rbc_r - 15, rbc_cy + 10, rbc_cx + rbc_r + 35, rbc_cy - 20], fill=(220, 38, 38), width=10)

            # Speech bubble
            sp_top = rbc_cy + rbc_r + 25
            draw.rounded_rectangle([75, sp_top, self.width - 75, sp_top + 90], radius=18, fill=self.c_white, outline=(239, 68, 68), width=2)
            font_sp = self._get_font(24)
            sp_txt = "“I carry oxygen to your muscles!”"
            bbox = draw.textbbox((0, 0), sp_txt, font=font_sp)
            bw = bbox[2] - bbox[0]
            draw.text(((self.width - bw) // 2, sp_top + 28), sp_txt, font=font_sp, fill=(185, 28, 28))

        elif organ == "brain" or scene_idx == 1:
            # ---------------------------------------------------------
            # Scene 2: Brain Signalling - Pink Brain Character & Synapses
            # ---------------------------------------------------------
            box_top = 240
            box_bottom = 980
            draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=28, fill=(245, 243, 255), outline=(139, 92, 246), width=3)
            draw.text((75, box_top + 22), "NEURAL CIRCUITS & SATIETY SIGNALLING", font=self._get_font(22), fill=(109, 40, 217))

            # Branching electrical neural network in background
            cx = self.width // 2
            cy = 580
            for syn_idx in range(12):
                ang = math.radians(syn_idx * 30 + frame * 2)
                sx1 = cx + int(140 * math.cos(ang))
                sy1 = cy + int(140 * math.sin(ang))
                sx2 = cx + int(240 * math.cos(ang + 0.3))
                sy2 = cy + int(240 * math.sin(ang + 0.3))
                draw.line([sx1, sy1, sx2, sy2], fill=(196, 181, 253), width=2)
                # Golden sparking synaptic pulse
                if (frame + syn_idx * 3) % 8 < 4:
                    draw.ellipse([sx2 - 6, sy2 - 6, sx2 + 6, sy2 + 6], fill=(250, 204, 21))

            # Central 3D Pink Brain Character!
            brain_r = 145
            brain_bob = int(6 * math.sin(frame * 0.25))
            b_cy = cy + brain_bob

            # Left & Right hemispheres
            brain_pink = (244, 114, 182)
            draw.ellipse([cx - brain_r, b_cy - int(brain_r*0.75), cx - 10, b_cy + int(brain_r*0.75)], fill=brain_pink, outline=(219, 39, 119), width=5)
            draw.ellipse([cx + 10, b_cy - int(brain_r*0.75), cx + brain_r, b_cy + int(brain_r*0.75)], fill=brain_pink, outline=(219, 39, 119), width=5)

            # Cerebral Folds / Grooves
            draw.arc([cx - 100, b_cy - 60, cx - 40, b_cy], start=30, end=200, fill=(219, 39, 119), width=4)
            draw.arc([cx - 80, b_cy - 10, cx - 20, b_cy + 50], start=10, end=180, fill=(219, 39, 119), width=4)
            draw.arc([cx + 40, b_cy - 60, cx + 100, b_cy], start=340, end=150, fill=(219, 39, 119), width=4)
            draw.arc([cx + 20, b_cy - 10, cx + 80, b_cy + 50], start=0, end=170, fill=(219, 39, 119), width=4)

            # Sparkling Eyes
            eye_y = b_cy + 5
            draw.ellipse([cx - 50, eye_y - 18, cx - 18, eye_y + 16], fill=(30, 20, 25))
            draw.ellipse([cx + 18, eye_y - 18, cx + 50, eye_y + 16], fill=(30, 20, 25))
            draw.ellipse([cx - 45, eye_y - 14, cx - 32, eye_y - 2], fill=(255, 255, 255))
            draw.ellipse([cx + 24, eye_y - 14, cx + 36, eye_y - 2], fill=(255, 255, 255))

            # Rosy cheeks
            draw.ellipse([cx - 68, eye_y + 8, cx - 46, eye_y + 24], fill=(251, 113, 133))
            draw.ellipse([cx + 46, eye_y + 8, cx + 68, eye_y + 24], fill=(251, 113, 133))

            # Happy mouth
            draw.arc([cx - 24, b_cy + 30, cx + 24, b_cy + 55], start=20, end=160, fill=(30, 20, 25), width=5)

            # Speech bubble
            sp_top = b_cy + brain_r - 10
            draw.rounded_rectangle([75, sp_top, self.width - 75, sp_top + 90], radius=18, fill=self.c_white, outline=(139, 92, 246), width=2)
            font_sp = self._get_font(24)
            sp_txt = "“I help you feel full for longer!”"
            bbox = draw.textbbox((0, 0), sp_txt, font=font_sp)
            bw = bbox[2] - bbox[0]
            draw.text(((self.width - bw) // 2, sp_top + 28), sp_txt, font=font_sp, fill=(109, 40, 217))

        elif organ == "stomach" or scene_idx == 2:
            # ---------------------------------------------------------
            # Scene 3: Stomach Function - Curved Stomach Character & Digestion
            # ---------------------------------------------------------
            box_top = 240
            box_bottom = 980
            draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=28, fill=(255, 247, 237), outline=(249, 115, 22), width=3)
            draw.text((75, box_top + 22), "GASTRIC EMPTYING & NUTRIENT ABSORPTION", font=self._get_font(22), fill=(194, 65, 12))

            # Floating food particles (apple bits, broccoli, grains)
            for f_idx in range(6):
                fx = 120 + (f_idx * 90 + frame * 3) % (self.width - 240)
                fy = box_top + 120 + (f_idx * 55) % 400
                if f_idx % 2 == 0:
                    draw.ellipse([fx - 14, fy - 14, fx + 14, fy + 14], fill=(74, 222, 128))  # broccoli green
                else:
                    draw.polygon([(fx, fy - 12), (fx + 12, fy + 8), (fx - 12, fy + 8)], fill=(239, 68, 68))  # apple wedge

            # Central Cute Curved Stomach Organ Character!
            stomach_cx = self.width // 2
            stomach_cy = 580 + int(6 * math.sin(frame * 0.28))

            stomach_orange = (251, 146, 60)
            # J-shaped curved stomach body
            draw.ellipse([stomach_cx - 130, stomach_cy - 120, stomach_cx + 10, stomach_cy + 100], fill=stomach_orange, outline=(234, 88, 12), width=5)
            draw.ellipse([stomach_cx - 60, stomach_cy + 10, stomach_cx + 120, stomach_cy + 110], fill=stomach_orange, outline=(234, 88, 12), width=5)
            # Upper esophagus entrance
            draw.rounded_rectangle([stomach_cx - 45, stomach_cy - 140, stomach_cx - 10, stomach_cy - 90], radius=10, fill=stomach_orange, outline=(234, 88, 12), width=3)

            # Big friendly eyes
            eye_y = stomach_cy - 15
            draw.ellipse([stomach_cx - 75, eye_y - 18, stomach_cx - 42, eye_y + 16], fill=(30, 20, 25))
            draw.ellipse([stomach_cx - 18, eye_y - 18, stomach_cx + 15, eye_y + 16], fill=(30, 20, 25))
            draw.ellipse([stomach_cx - 70, eye_y - 14, stomach_cx - 58, eye_y - 2], fill=(255, 255, 255))
            draw.ellipse([stomach_cx - 12, eye_y - 14, stomach_cx, eye_y - 2], fill=(255, 255, 255))

            # Cheeks
            draw.ellipse([stomach_cx - 95, eye_y + 8, stomach_cx - 72, eye_y + 24], fill=(254, 202, 202))
            draw.ellipse([stomach_cx + 18, eye_y + 8, stomach_cx + 40, eye_y + 24], fill=(254, 202, 202))

            # Smiling mouth
            draw.arc([stomach_cx - 50, stomach_cy + 25, stomach_cx, stomach_cy + 52], start=20, end=160, fill=(30, 20, 25), width=5)

            # Speech bubble
            sp_top = stomach_cy + 130
            draw.rounded_rectangle([75, sp_top, self.width - 75, sp_top + 90], radius=18, fill=self.c_white, outline=(249, 115, 22), width=2)
            font_sp = self._get_font(24)
            sp_txt = "“I slow down food digestion!”"
            bbox = draw.textbbox((0, 0), sp_txt, font=font_sp)
            bw = bbox[2] - bbox[0]
            draw.text(((self.width - bw) // 2, sp_top + 28), sp_txt, font=font_sp, fill=(194, 65, 12))

        elif organ == "muscle_glut4" or scene_idx == 3:
            # ---------------------------------------------------------
            # Scene 4: Skeletal Muscle & GLUT4 Translocation
            # ---------------------------------------------------------
            box_top = 240
            box_bottom = 980
            draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=28, fill=(240, 253, 244), outline=(34, 197, 94), width=3)
            draw.text((75, box_top + 22), "SKELETAL MUSCLE & NON-INSULIN GLUT4", font=self._get_font(22), fill=(22, 101, 52))

            # Muscle Fiber bands
            for fib_i in range(5):
                fy = box_top + 90 + fib_i * 90
                draw.rounded_rectangle([70, fy, self.width - 70, fy + 70], radius=14, fill=(220, 252, 231), outline=(134, 239, 172), width=2)
                for st_x in range(90, self.width - 80, 25):
                    draw.line([st_x, fy + 8, st_x, fy + 62], fill=(74, 222, 128), width=2)

            # GLUT4 Character (Friendly Green Transporter)
            g_cx = self.width // 2
            g_cy = 580 + int(6 * math.sin(frame * 0.25))
            draw.rounded_rectangle([g_cx - 100, g_cy - 70, g_cx + 100, g_cy + 70], radius=24, fill=(34, 197, 94), outline=(21, 128, 61), width=4)
            # Eyes & Smile
            draw.ellipse([g_cx - 45, g_cy - 20, g_cx - 15, g_cy + 15], fill=(30, 20, 25))
            draw.ellipse([g_cx + 15, g_cy - 20, g_cx + 45, g_cy + 15], fill=(30, 20, 25))
            draw.ellipse([g_cx - 40, g_cy - 16, g_cx - 25, g_cy - 4], fill=(255, 255, 255))
            draw.ellipse([g_cx + 20, g_cy - 16, g_cx + 35, g_cy - 4], fill=(255, 255, 255))
            draw.arc([g_cx - 25, g_cy + 15, g_cx + 25, g_cy + 42], start=20, end=160, fill=(30, 20, 25), width=4)

            # Speech Bubble
            sp_top = g_cy + 100
            draw.rounded_rectangle([75, sp_top, self.width - 75, sp_top + 90], radius=18, fill=self.c_white, outline=(34, 197, 94), width=2)
            font_sp = self._get_font(24)
            sp_txt = "“I clear sugar directly into muscles!”"
            bbox = draw.textbbox((0, 0), sp_txt, font=font_sp)
            bw = bbox[2] - bbox[0]
            draw.text(((self.width - bw) // 2, sp_top + 28), sp_txt, font=font_sp, fill=(22, 101, 52))

        else:
            # ---------------------------------------------------------
            # Scene 5: Whole Body Harmony & Pancreas Protection
            # ---------------------------------------------------------
            box_top = 240
            box_bottom = 980
            draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=28, fill=(255, 251, 235), outline=(245, 158, 11), width=3)
            draw.text((75, box_top + 22), "WHOLE BODY METABOLIC STABILIZATION", font=self._get_font(22), fill=(180, 83, 9))

            # Resting Pancreas Character (Gentle Gold/Yellow)
            p_cx = self.width // 2
            p_cy = 540 + int(5 * math.sin(frame * 0.2))
            draw.ellipse([p_cx - 120, p_cy - 70, p_cx + 120, p_cy + 70], fill=(253, 224, 71), outline=(217, 119, 6), width=4)
            # Sleepy calm eyes (resting from insulin surge)
            draw.arc([p_cx - 65, p_cy - 15, p_cx - 25, p_cy + 15], start=200, end=340, fill=(30, 20, 25), width=4)
            draw.arc([p_cx + 25, p_cy - 15, p_cx + 65, p_cy + 15], start=200, end=340, fill=(30, 20, 25), width=4)
            draw.arc([p_cx - 20, p_cy + 10, p_cx + 20, p_cy + 35], start=20, end=160, fill=(30, 20, 25), width=4)

            # Achievement Stamp
            stamp_top = p_cy + 110
            draw.rounded_rectangle([75, stamp_top, self.width - 75, box_bottom - 30], radius=20, fill=(254, 243, 199), outline=(217, 119, 6), width=3)
            draw.text((95, stamp_top + 20), "-34% POSTPRANDIAL SPIKE", font=self._get_font(32), fill=(180, 83, 9))
            draw.text((95, stamp_top + 65), "Pancreatic beta cells spared from acute glycemic stress.", font=self._get_font(18), fill=(120, 53, 15))
            draw.text((95, stamp_top + 95), "Confirmed via Continuous Glucose Monitoring (n=48).", font=self._get_font(18), fill=(120, 53, 15))

    # -------------------------------------------------------------
    # -------------------------------------------------------------
    # 3. Everyday Human Scenario Animation (5 Distinct Storyboard Scenes)
    # -------------------------------------------------------------
    def _draw_everyday_human(
        self,
        draw: ImageDraw.ImageDraw,
        frame: int,
        total_frames: int,
        p: float,
        scene: Dict[str, Any],
        scene_idx: int = 0,
        palette: Optional[Dict[str, Any]] = None
    ):
        pal = palette or getattr(self, "current_palette", None) or self.get_theme("warm_editorial")
        role = scene.get("scene_role") or ["dinner_table", "smartwatch", "terrace_walk", "clock_timing", "habit_success"][scene_idx % 5]
        box_top = 260
        box_bottom = 980

        if role == "dinner_table" or (isinstance(role, str) and "dinner" in role.lower()) or scene_idx == 0:
            # SCENE 1: Cozy Indian Evening Dinner Setting
            draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=24, fill=pal["card_bg"], outline=pal["card_border"], width=3)
            # Window with night sky / crescent moon
            win_top = box_top + 25
            draw.rounded_rectangle([80, win_top, self.width - 80, win_top + 220], radius=16, fill=(24, 32, 54), outline=pal["card_border"], width=2)
            # Stars & Crescent Moon
            draw.ellipse([self.width - 150, win_top + 30, self.width - 100, win_top + 80], fill=(254, 240, 138))
            draw.ellipse([self.width - 138, win_top + 25, self.width - 90, win_top + 75], fill=(24, 32, 54))
            for st_i in range(12):
                st_x = 110 + (st_i * 45) % (self.width - 250)
                st_y = win_top + 40 + (st_i * 35) % 120
                tw = int(180 + 75 * math.sin(frame * 0.3 + st_i))
                draw.ellipse([st_x - 2, st_y - 2, st_x + 2, st_y + 2], fill=(tw, tw, 220))
            
            # Dining Table
            tbl_top = win_top + 240
            draw.rounded_rectangle([70, tbl_top, self.width - 70, box_bottom - 40], radius=20, fill=(180, 115, 75), outline=(130, 80, 50), width=3)
            # Table Cloth
            draw.rounded_rectangle([90, tbl_top + 15, self.width - 90, box_bottom - 60], radius=14, fill=(245, 235, 220))

            # Steel Thali
            thali_cx = self.width // 2
            thali_cy = tbl_top + 180
            draw.ellipse([thali_cx - 150, thali_cy - 120, thali_cx + 150, thali_cy + 120], fill=(215, 220, 228), outline=(170, 175, 185), width=5)
            # Rotis
            draw.ellipse([thali_cx - 100, thali_cy - 70, thali_cx - 20, thali_cy + 10], fill=(245, 215, 160), outline=(210, 175, 120), width=3)
            draw.ellipse([thali_cx - 70, thali_cy - 90, thali_cx + 10, thali_cy - 10], fill=(240, 210, 150), outline=(210, 175, 120), width=3)
            # Bowl of Dal (yellow)
            draw.ellipse([thali_cx + 25, thali_cy - 85, thali_cx + 115, thali_cy - 5], fill=(245, 190, 50), outline=(180, 130, 30), width=4)
            # Steaming Vegetable Curry
            draw.ellipse([thali_cx + 10, thali_cy + 10, thali_cx + 105, thali_cy + 85], fill=(185, 75, 45), outline=(140, 50, 30), width=4)

            # Rising Steam Animation
            for sm_i in range(3):
                sm_x = thali_cx + 60 + sm_i * 25
                sm_y = thali_cy - 90 - (frame * 3 + sm_i * 20) % 70
                drift = int(8 * math.sin(frame * 0.2 + sm_i))
                draw.arc([sm_x + drift - 15, sm_y - 20, sm_x + drift + 15, sm_y + 20], start=30, end=150, fill=(240, 240, 240), width=3)

            # Floating Tag
            draw.rounded_rectangle([100, box_bottom - 120, self.width - 100, box_bottom - 60], radius=16, fill=pal["badge_bg"], outline=pal["card_border"], width=2)
            draw.text((120, box_bottom - 104), "🍽  Evening Meal Finished (8:30 PM)", font=self._get_font(22), fill=pal["badge_text"])

        elif role == "smartwatch" or (isinstance(role, str) and "watch" in role.lower()) or scene_idx == 1:
            # SCENE 2: High-Tech Smartwatch / Countdown
            draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=24, fill=pal["card_bg"], outline=pal["card_border"], width=3)
            
            # Watch body (circular sleek bezel)
            w_cx = self.width // 2
            w_cy = box_top + 310
            # Wrist strap
            draw.rounded_rectangle([w_cx - 75, box_top + 30, w_cx + 75, box_bottom - 30], radius=24, fill=(40, 44, 52), outline=(60, 65, 75), width=3)
            # Watch dial
            draw.ellipse([w_cx - 190, w_cy - 190, w_cx + 190, w_cy + 190], fill=(15, 23, 42), outline=(100, 116, 139), width=8)
            draw.ellipse([w_cx - 170, w_cy - 170, w_cx + 170, w_cy + 170], fill=(15, 23, 42), outline=(30, 41, 59), width=4)

            # Glowing Activity Ring
            prog_angle = int(360 * min(1.0, p * 1.2))
            draw.arc([w_cx - 150, w_cy - 150, w_cx + 150, w_cy + 150], start=270, end=270 + prog_angle, fill=pal["accent_primary"], width=12)

            # Pulse Icon
            draw.text((w_cx - 85, w_cy - 110), "♥ 84 BPM", font=self._get_font(24), fill=(244, 63, 94))
            draw.text((w_cx - 110, w_cy - 40), "15 MIN", font=self._get_font(60), fill=(255, 255, 255))
            draw.text((w_cx - 105, w_cy + 35), "CLINICAL TIMER", font=self._get_font(24), fill=pal["accent_primary"])

            # Prompt Card below
            call_top = w_cy + 220
            draw.rounded_rectangle([75, call_top, self.width - 75, box_bottom - 40], radius=18, fill=pal["badge_bg"], outline=pal["card_border"], width=2)
            draw.text((95, call_top + 18), "WINDOW CLOSING: 15–30m POST-MEAL", font=self._get_font(20), fill=pal["badge_text"])
            draw.text((95, call_top + 48), "Step outside now to intercept the glucose spike!", font=self._get_font(18), fill=pal["text_primary"])

        elif role == "terrace_walk" or (isinstance(role, str) and "walk" in role.lower()) or scene_idx == 2:
            # SCENE 3: Peaceful Animated Terrace Walk
            draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=24, fill=(245, 240, 235), outline=pal["card_border"], width=2)
            # Night Terrace Sky
            draw.rounded_rectangle([60, box_top + 16, self.width - 60, box_top + 340], radius=18, fill=(30, 40, 60))
            for s_idx in range(16):
                sx = 80 + (s_idx * 42) % (self.width - 160)
                sy = box_top + 35 + (s_idx * 28) % 180
                brightness = int(180 + 75 * math.sin(frame * 0.3 + s_idx))
                draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(brightness, brightness, 220))

            railing_y = box_top + 280
            draw.line([60, railing_y, self.width - 60, railing_y], fill=(180, 190, 205), width=5)
            for rx in range(80, self.width - 60, 45):
                draw.line([rx, railing_y, rx, box_top + 340], fill=(140, 150, 165), width=3)

            # Walking Character Animation
            stride_phase = math.sin(2 * math.pi * frame / 14)
            step_x = int(140 + (self.width - 280) * ((frame % 60) / 60))
            char_y = box_top + 175

            draw.ellipse([step_x - 22, char_y - 65, step_x + 22, char_y - 21], fill=(235, 185, 155))
            draw.arc([step_x - 10, char_y - 42, step_x + 10, char_y - 30], start=20, end=160, fill=(30, 20, 25), width=3)
            draw.ellipse([step_x - 24, char_y - 70, step_x + 24, char_y - 48], fill=(40, 30, 30))
            draw.rounded_rectangle([step_x - 18, char_y - 20, step_x + 18, char_y + 35], radius=8, fill=pal["accent_primary"])

            arm_swing = int(16 * stride_phase)
            draw.line([step_x - 10, char_y - 10, step_x - 24 + arm_swing, char_y + 15], fill=(235, 185, 155), width=6)
            draw.line([step_x + 10, char_y - 10, step_x + 24 - arm_swing, char_y + 15], fill=(235, 185, 155), width=6)

            leg_stride = int(22 * stride_phase)
            draw.line([step_x - 8, char_y + 35, step_x - 8 + leg_stride, char_y + 85], fill=(53, 29, 29), width=7)
            draw.line([step_x + 8, char_y + 35, step_x + 8 - leg_stride, char_y + 85], fill=(53, 29, 29), width=7)

            # Pace & Habit Status
            clock_box_top = box_top + 370
            draw.rounded_rectangle([60, clock_box_top, self.width - 60, clock_box_top + 130], radius=18, fill=pal["card_bg"], outline=pal["card_border"], width=2)
            walk_banner = (scene.get("on_screen_text") or "ACTIONABLE LIFESTYLE HABIT").upper()
            if len(walk_banner) > 34:
                walk_banner = walk_banner[:32] + "..."
            draw.text((90, clock_box_top + 25), walk_banner, font=self._get_font(22), fill=pal["accent_primary"])
            sub_desc = scene.get("subtitle_text") or "Conversational pace • Sustainable lifestyle habit"
            if len(sub_desc) > 46:
                sub_desc = sub_desc[:43] + "..."
            draw.text((90, clock_box_top + 65), sub_desc, font=self._get_font(18), fill=pal["text_primary"])

            cgm_top = clock_box_top + 155
            draw.rounded_rectangle([60, cgm_top, self.width - 60, box_bottom - 20], radius=18, fill=(240, 253, 244), outline=(134, 239, 172), width=2)
            draw.text((85, cgm_top + 22), "MUSCLE CONTRACTION ACTIVE", font=self._get_font(18), fill=(22, 101, 52))
            draw.text((85, cgm_top + 52), "GLUT4 Non-Insulin Glucose Clearance ➔", font=self._get_font(22), fill=pal["accent_primary"])

        elif role == "clock_timing" or (isinstance(role, str) and "timing" in role.lower()) or scene_idx == 3:
            # SCENE 4: Dual Timing Comparison
            draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=24, fill=pal["card_bg"], outline=pal["card_border"], width=3)
            draw.text((75, box_top + 22), "TIMING IS EVERYTHING: 15 MIN VS 60 MIN", font=self._get_font(22), fill=pal["accent_secondary"])

            # Left Card: Immediate 15-30m Walk
            c1_top = box_top + 70
            draw.rounded_rectangle([70, c1_top, self.width - 70, c1_top + 260], radius=20, fill=(240, 253, 244), outline=(74, 222, 128), width=3)
            draw.text((95, c1_top + 20), "✔ WALK WITHIN 15–30 MIN", font=self._get_font(24), fill=(22, 101, 52))
            draw.text((95, c1_top + 60), "-34% PEAK SPIKE", font=self._get_font(52), fill=pal["accent_primary"])
            draw.text((95, c1_top + 130), "Intercepts glucose influx before peak absorption.", font=self._get_font(20), fill=(22, 101, 52))
            draw.text((95, c1_top + 165), "Delta elevation: 38.4 ± 6.2 mg/dL (p < 0.001)", font=self._get_font(18), fill=(22, 101, 52))

            # Right Card: Delayed 60m Walk
            c2_top = c1_top + 285
            draw.rounded_rectangle([70, c2_top, self.width - 70, c2_top + 260], radius=20, fill=(254, 242, 242), outline=(248, 113, 113), width=2)
            draw.text((95, c2_top + 20), "⚠ DELAYED 60+ MIN", font=self._get_font(24), fill=(153, 27, 27))
            draw.text((95, c2_top + 60), "-9% ONLY", font=self._get_font(52), fill=(185, 28, 28))
            draw.text((95, c2_top + 130), "Misses early glycemic surge; pancreas already stressed.", font=self._get_font(20), fill=(153, 27, 27))
            draw.text((95, c2_top + 165), "Delta elevation: 52.9 ± 7.4 mg/dL", font=self._get_font(18), fill=(153, 27, 27))

        else:
            # SCENE 5: Celebratory Habit Success & Summary
            draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=24, fill=pal["card_bg"], outline=pal["card_border"], width=3)
            
            # Big Glowing Badge
            cx = self.width // 2
            cy = box_top + 170
            badge_r = 110
            draw.ellipse([cx - badge_r, cy - badge_r, cx + badge_r, cy + badge_r], fill=pal["badge_bg"], outline=pal["accent_primary"], width=5)
            draw.text((cx - 85, cy - 65), "-34%", font=self._get_font(72), fill=pal["accent_primary"])
            draw.text((cx - 90, cy + 20), "PEAK GLUCOSE", font=self._get_font(22), fill=pal["text_primary"])

            # 3 Structured Checklist Pillars
            list_top = cy + 140
            checklist = [
                ("Sustainable Routine", "Consistent daily micro-habits"),
                ("Evidence Grounded", "Backed by peer-reviewed clinical science"),
                ("Metabolic Balance", "Targeted lifestyle for long-term health")
            ]
            for c_i, (head, sub) in enumerate(checklist):
                c_y = list_top + c_i * 95
                draw.rounded_rectangle([75, c_y, self.width - 75, c_y + 78], radius=16, fill=(255, 255, 255), outline=pal["card_border"], width=2)
                draw.ellipse([95, c_y + 18, 135, c_y + 58], fill=pal["accent_primary"])
                draw.text((107, c_y + 22), "✔", font=self._get_font(22), fill=(255, 255, 255))
                draw.text((155, c_y + 12), head, font=self._get_font(22), fill=pal["text_primary"])
                draw.text((155, c_y + 42), sub, font=self._get_font(17), fill=pal["text_muted"])

    # -------------------------------------------------------------
    # 4. Animated Explainer (5 Distinct Kinetic Motion Graphic Scenes)
    # -------------------------------------------------------------
    def _draw_animated_explainer(
        self,
        draw: ImageDraw.ImageDraw,
        frame: int,
        total_frames: int,
        p: float,
        scene: Dict[str, Any],
        scene_idx: int = 0,
        palette: Optional[Dict[str, Any]] = None
    ):
        pal = palette or getattr(self, "current_palette", None) or self.get_theme("clean_infographic")
        role = scene.get("scene_role") or ["cgm_intro", "curve_comparison", "glut4_mechanism", "timing_window", "summary_stat"][scene_idx % 5]
        box_top = 260
        box_bottom = 980

        if role == "cgm_intro" or (isinstance(role, str) and "cgm" in role.lower()) or scene_idx == 0:
            # SCENE 1: Kinetic Continuous Glucose Sensor
            draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=24, fill=pal["card_bg"], outline=pal["card_border"], width=3)
            title_banner = (scene.get("on_screen_text") or "CLINICAL EVIDENCE MONITORING").upper()
            if len(title_banner) > 36:
                title_banner = title_banner[:33] + "..."
            draw.text((75, box_top + 24), title_banner, font=self._get_font(22), fill=pal["accent_secondary"])

            cx = self.width // 2
            cy = box_top + 280

            # Arm contour
            draw.rounded_rectangle([cx - 180, cy - 140, cx + 180, cy + 140], radius=40, fill=(245, 230, 215), outline=(220, 195, 175), width=3)

            # Circular Sensor
            draw.ellipse([cx - 95, cy - 95, cx + 95, cy + 95], fill=(255, 255, 255), outline=(200, 205, 215), width=4)
            draw.ellipse([cx - 75, cy - 75, cx + 75, cy + 75], fill=(245, 248, 252), outline=pal["accent_primary"], width=3)

            # Radiating wireless waves
            for w_i in range(3):
                wave_r = 105 + int((frame * 4 + w_i * 45) % 110)
                alpha_w = max(1, 4 - w_i)
                draw.arc([cx - wave_r, cy - wave_r, cx + wave_r, cy + wave_r], start=220, end=320, fill=pal["accent_primary"], width=alpha_w)

            # Telemetry Readout
            pulse_val = int(136 + 4 * math.sin(frame * 0.3))
            draw.text((cx - 65, cy - 35), f"{pulse_val}", font=self._get_font(48), fill=pal["accent_primary"])
            draw.text((cx - 45, cy + 22), "mg / dL ↑", font=self._get_font(20), fill=pal["text_muted"])

            # Info Card below
            info_top = cy + 175
            draw.rounded_rectangle([75, info_top, self.width - 75, box_bottom - 40], radius=18, fill=pal["badge_bg"], outline=pal["card_border"], width=2)
            draw.text((95, info_top + 22), "EVIDENCE PARAMETERS", font=self._get_font(20), fill=pal["badge_text"])
            sub_desc = scene.get("subtitle_text") or scene.get("narration") or "Rigorous clinical analysis of patient data."
            if len(sub_desc) > 90:
                draw.text((95, info_top + 55), sub_desc[:48], font=self._get_font(18), fill=pal["text_primary"])
                draw.text((95, info_top + 85), sub_desc[48:95] + ("..." if len(sub_desc) > 95 else ""), font=self._get_font(18), fill=pal["text_primary"])
            else:
                draw.text((95, info_top + 55), sub_desc, font=self._get_font(18), fill=pal["text_primary"])

        elif role == "curve_comparison" or (isinstance(role, str) and "curve" in role.lower()) or scene_idx == 1:
            # SCENE 2: Kinetic Dual Glycemic Curve Graph
            draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=24, fill=pal["card_bg"], outline=pal["card_border"], width=2)
            draw.text((75, box_top + 24), "GLYCEMIC TRAJECTORY COMPARISON", font=self._get_font(22), fill=pal["accent_secondary"])

            chart_x1 = 90
            chart_x2 = self.width - 80
            chart_y1 = box_top + 80
            chart_y2 = box_top + 380

            draw.line([chart_x1, chart_y2, chart_x2, chart_y2], fill=(200, 200, 200), width=3)
            draw.line([chart_x1, chart_y1, chart_x1, chart_y2], fill=(200, 200, 200), width=3)

            font_axis = self._get_font(16)
            draw.text((chart_x1 - 42, chart_y1), "170", font=font_axis, fill=pal["text_muted"])
            draw.text((chart_x1 - 42, (chart_y1 + chart_y2) // 2), "140", font=font_axis, fill=pal["text_muted"])
            draw.text((chart_x1 - 42, chart_y2 - 10), "110", font=font_axis, fill=pal["text_muted"])

            draw.text((chart_x1, chart_y2 + 8), "0m", font=font_axis, fill=pal["text_muted"])
            draw.text(((chart_x1 + chart_x2) // 2 - 10, chart_y2 + 8), "30m", font=font_axis, fill=pal["text_muted"])
            draw.text((chart_x2 - 30, chart_y2 + 8), "60m", font=font_axis, fill=pal["text_muted"])

            draw_progress = min(1.0, p * 1.4)
            max_draw_x = int(chart_x1 + (chart_x2 - chart_x1) * draw_progress)

            # Sedentary Rest Curve (Red)
            points_a = []
            for x in range(chart_x1, max_draw_x, 4):
                frac = (x - chart_x1) / (chart_x2 - chart_x1)
                spike = math.exp(-((frac - 0.45) ** 2) / 0.06)
                y = int(chart_y2 - 30 - 240 * spike)
                points_a.append((x, y))

            if len(points_a) > 1:
                draw.line(points_a, fill=(211, 47, 47), width=5)
                if draw_progress > 0.45:
                    px = chart_x1 + int((chart_x2 - chart_x1) * 0.45)
                    py = chart_y2 - 30 - 240
                    draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=(211, 47, 47), outline=(255, 255, 255), width=2)
                    draw.text((px - 30, py - 32), "166 mg/dL", font=font_axis, fill=(211, 47, 47))

            # 10-Minute Walk Curve (Green)
            points_b = []
            for x in range(chart_x1, max_draw_x, 4):
                frac = (x - chart_x1) / (chart_x2 - chart_x1)
                spike = math.exp(-((frac - 0.45) ** 2) / 0.08)
                y = int(chart_y2 - 30 - 130 * spike)
                points_b.append((x, y))

            if len(points_b) > 1:
                draw.line(points_b, fill=(46, 125, 50), width=5)
                if draw_progress > 0.45:
                    px = chart_x1 + int((chart_x2 - chart_x1) * 0.45)
                    py = chart_y2 - 30 - 130
                    draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=(46, 125, 50), outline=(255, 255, 255), width=2)
                    draw.text((px - 30, py + 12), "146 mg/dL", font=font_axis, fill=(46, 125, 50))

            draw.line([chart_x1 + 30, chart_y2 + 45, chart_x1 + 60, chart_y2 + 45], fill=(211, 47, 47), width=4)
            draw.text((chart_x1 + 68, chart_y2 + 36), "Sedentary Couch (Spike +58 mg/dL)", font=font_axis, fill=pal["text_primary"])

            draw.line([chart_x1 + 30, chart_y2 + 75, chart_x1 + 60, chart_y2 + 75], fill=(46, 125, 50), width=4)
            draw.text((chart_x1 + 68, chart_y2 + 66), "10-Min Walk (Spike +38 mg/dL)", font=font_axis, fill=(46, 125, 50))

            stat_card_top = box_top + 500
            draw.rounded_rectangle([75, stat_card_top, self.width - 75, box_bottom - 25], radius=20, fill=pal["badge_bg"], outline=pal["accent_primary"], width=3)
            font_stat_num = self._get_font(68)
            font_stat_lbl = self._get_font(26)
            draw.text((105, stat_card_top + 25), "-34%", font=font_stat_num, fill=pal["accent_primary"])
            draw.text((320, stat_card_top + 35), "LOWER GLUCOSE SPIKE", font=font_stat_lbl, fill=pal["text_primary"])
            draw.text((320, stat_card_top + 70), "Clinical Crossover Trial (n=48)", font=font_axis, fill=pal["text_muted"])

        elif role == "glut4_mechanism" or (isinstance(role, str) and "glut" in role.lower()) or scene_idx == 2:
            # SCENE 3: Kinetic GLUT4 Muscle Cell Translocation
            draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=24, fill=pal["card_bg"], outline=pal["card_border"], width=3)
            draw.text((75, box_top + 24), "NON-INSULIN MUSCULAR GLUCOSE CLEARANCE", font=self._get_font(22), fill=pal["accent_secondary"])

            # Top: Bloodstream zone
            blood_bottom = box_top + 240
            draw.rounded_rectangle([70, box_top + 70, self.width - 70, blood_bottom], radius=16, fill=(254, 242, 242), outline=(248, 113, 113), width=2)
            draw.text((90, box_top + 80), "BLOODSTREAM (High Post-Meal Glucose)", font=self._get_font(18), fill=(185, 28, 28))

            # Floating Hexagonal Glucose Molecules
            for g_i in range(8):
                gx = 110 + (g_i * 68 + frame * 3) % (self.width - 240)
                gy = box_top + 130 + (g_i * 28) % 70
                draw.polygon([(gx, gy - 12), (gx + 12, gy - 6), (gx + 12, gy + 6), (gx, gy + 12), (gx - 12, gy + 6), (gx - 12, gy - 6)], fill=(250, 204, 21), outline=(217, 119, 6), width=2)

            # Muscle Sarcolemma Membrane with GLUT4 Channel Gates
            mem_y = blood_bottom + 15
            draw.line([70, mem_y, self.width - 70, mem_y], fill=(99, 102, 241), width=10)
            draw.line([70, mem_y + 16, self.width - 70, mem_y + 16], fill=(99, 102, 241), width=10)

            # GLUT4 Gates Opening
            gate_open = int(12 * abs(math.sin(frame * 0.3)))
            for gx in range(160, self.width - 120, 140):
                draw.rounded_rectangle([gx - 25, mem_y - 8, gx - 5 - gate_open, mem_y + 24], radius=6, fill=(16, 185, 129))
                draw.rounded_rectangle([gx + 5 + gate_open, mem_y - 8, gx + 25, mem_y + 24], radius=6, fill=(16, 185, 129))
                draw.text((gx - 30, mem_y + 35), "GLUT4", font=self._get_font(16), fill=(16, 185, 129))

            # Muscle Cytoplasm
            draw.rounded_rectangle([70, mem_y + 70, self.width - 70, box_bottom - 40], radius=16, fill=(240, 253, 244), outline=(74, 222, 128), width=2)
            draw.text((90, mem_y + 85), "SKELETAL MUSCLE FIBERS (Quadriceps & Soleus)", font=self._get_font(20), fill=(22, 101, 52))
            draw.text((90, mem_y + 120), "• Muscle contraction stimulates AMPK & CaMKII signaling", font=self._get_font(18), fill=pal["text_primary"])
            draw.text((90, mem_y + 155), "• Translocates GLUT4 vesicles to cell membrane directly", font=self._get_font(18), fill=pal["text_primary"])
            draw.text((90, mem_y + 190), "• SUCK GLUCOSE WITHOUT NEEDING EXTRA INSULIN", font=self._get_font(19), fill=pal["accent_primary"])

        elif role == "timing_window" or (isinstance(role, str) and "timing" in role.lower()) or scene_idx == 3:
            # SCENE 4: Kinetic Timing Timeline
            draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=24, fill=pal["card_bg"], outline=pal["card_border"], width=3)
            draw.text((75, box_top + 24), "POSTPRANDIAL WINDOW OF OPPORTUNITY", font=self._get_font(22), fill=pal["accent_secondary"])

            # Timeline bar
            bar_top = box_top + 90
            draw.rounded_rectangle([80, bar_top, self.width - 80, bar_top + 50], radius=14, fill=(226, 232, 240))
            # Optimal window bar
            draw.rounded_rectangle([80, bar_top, 80 + int((self.width - 160) * 0.45), bar_top + 50], radius=14, fill=(34, 197, 94))
            draw.text((100, bar_top + 14), "OPTIMAL INTERVENTION WINDOW", font=self._get_font(18), fill=(255, 255, 255))

            # Comparison Table Cards
            card_top = bar_top + 80
            draw.rounded_rectangle([75, card_top, self.width - 75, card_top + 180], radius=18, fill=(240, 253, 244), outline=(74, 222, 128), width=2)
            draw.text((95, card_top + 18), "IMMEDIATE WALK (15–30m Post-Meal)", font=self._get_font(22), fill=(22, 101, 52))
            draw.text((95, card_top + 54), "Peak Glucose Delta: 38.4 ± 6.2 mg/dL", font=self._get_font(20), fill=pal["text_primary"])
            draw.text((95, card_top + 88), "Peak reduction: 34% vs sedentary control (p < 0.001)", font=self._get_font(18), fill=(22, 101, 52))
            draw.text((95, card_top + 120), "Pancreatic beta cells spared from surge stress.", font=self._get_font(18), fill=pal["text_primary"])

            card2_top = card_top + 205
            draw.rounded_rectangle([75, card2_top, self.width - 75, card2_top + 180], radius=18, fill=(254, 242, 242), outline=(248, 113, 113), width=2)
            draw.text((95, card2_top + 18), "DELAYED WALK (60m Post-Meal)", font=self._get_font(22), fill=(153, 27, 27))
            draw.text((95, card2_top + 54), "Peak Glucose Delta: 52.9 ± 7.4 mg/dL", font=self._get_font(20), fill=pal["text_primary"])
            draw.text((95, card2_top + 88), "Peak reduction: only 9% (minimal benefit)", font=self._get_font(18), fill=(153, 27, 27))
            draw.text((95, card2_top + 120), "Gastric transit already delivered carbohydrates into blood.", font=self._get_font(18), fill=pal["text_primary"])

        else:
            # SCENE 5: Massive Kinetic Scientific Infographic
            draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=24, fill=pal["card_bg"], outline=pal["card_border"], width=3)
            
            # Big Bold -34% Badge
            draw.rounded_rectangle([75, box_top + 30, self.width - 75, box_top + 180], radius=20, fill=pal["badge_bg"], outline=pal["accent_primary"], width=3)
            draw.text((110, box_top + 50), "-34%", font=self._get_font(84), fill=pal["accent_primary"])
            draw.text((340, box_top + 65), "PEAK POSTPRANDIAL", font=self._get_font(24), fill=pal["text_primary"])
            draw.text((340, box_top + 98), "GLUCOSE ATTENUATION", font=self._get_font(24), fill=pal["accent_primary"])
            sub_badge = (scene.get("subtitle_text") or "Clinical Trial Parameters")
            if len(sub_badge) > 36:
                sub_badge = sub_badge[:33] + "..."
            draw.text((340, box_top + 132), sub_badge, font=self._get_font(18), fill=pal["text_muted"])

            # 3 Structured Clinical Outcomes
            list_top = box_top + 210
            draw.rounded_rectangle([75, list_top, self.width - 75, list_top + 130], radius=16, fill=(255, 255, 255), outline=pal["card_border"], width=2)
            draw.text((95, list_top + 16), "1. CLINICAL EFFICACY (Table 1)", font=self._get_font(20), fill=pal["accent_secondary"])
            draw.text((95, list_top + 46), "38.4 mg/dL peak delta vs 58.1 mg/dL sedentary control.", font=self._get_font(18), fill=pal["text_primary"])
            draw.text((95, list_top + 76), "Significant across all South Asian participant subgroups.", font=self._get_font(18), fill=pal["text_muted"])

            list_top2 = list_top + 150
            draw.rounded_rectangle([75, list_top2, self.width - 75, list_top2 + 130], radius=16, fill=(255, 255, 255), outline=pal["card_border"], width=2)
            draw.text((95, list_top2 + 16), "2. MOLECULAR PATHWAY", font=self._get_font(20), fill=pal["accent_secondary"])
            draw.text((95, list_top2 + 46), "Non-insulin dependent muscular GLUT4 translocation.", font=self._get_font(18), fill=pal["text_primary"])
            draw.text((95, list_top2 + 76), "Saves beta cell reserve without hypoglycemia risk.", font=self._get_font(18), fill=pal["text_muted"])

            list_top3 = list_top2 + 150
            draw.rounded_rectangle([75, list_top3, self.width - 75, list_top3 + 130], radius=16, fill=(255, 255, 255), outline=pal["card_border"], width=2)
            draw.text((95, list_top3 + 16), "3. PRACTICAL TRANSLATION", font=self._get_font(20), fill=pal["accent_secondary"])
            p_action = (scene.get("narration") or "Translate clinical findings into daily sustainable habits.")
            if len(p_action) > 55:
                p_action = p_action[:52] + "..."
            draw.text((95, list_top3 + 46), p_action, font=self._get_font(18), fill=pal["text_primary"])
            draw.text((95, list_top3 + 76), "Simple, free, culturally rooted metabolic therapy.", font=self._get_font(18), fill=pal["text_muted"])

    # -------------------------------------------------------------
    # 5. Professional Mode (Clinical Motion Graphics)
    # -------------------------------------------------------------
    def _draw_professional_mode(self, draw: ImageDraw.ImageDraw, frame: int, total_frames: int, p: float, scene: Dict[str, Any]):
        box_top = 260
        box_bottom = 980
        draw.rounded_rectangle([48, box_top, self.width - 48, box_bottom], radius=24, fill=self.c_white, outline=self.c_clay, width=2)

        font_title = self._get_font(22)
        font_lbl = self._get_font(18)
        font_num = self._get_font(38)

        draw.text((75, box_top + 24), "CLINICAL TRIAL PARAMETERS & OUTCOMES", font=font_title, fill=self.c_maroon)

        card1_top = box_top + 75
        draw.rounded_rectangle([75, card1_top, self.width - 75, card1_top + 130], radius=16, fill=(248, 242, 235), outline=self.c_clay, width=2)
        draw.text((100, card1_top + 16), "Primary Endpoint: Peak Postprandial Delta", font=font_lbl, fill=self.c_clay)
        draw.text((100, card1_top + 46), "-34% Attenuation (p < 0.001)", font=font_num, fill=self.c_rust)

        card2_top = card1_top + 150
        draw.rounded_rectangle([75, card2_top, self.width - 75, card2_top + 130], radius=16, fill=(248, 242, 235), outline=self.c_clay, width=2)
        draw.text((100, card2_top + 16), "Incremental AUC 0-180m Reduction", font=font_lbl, fill=self.c_clay)
        draw.text((100, card2_top + 46), "2,680 vs 4,120 mg·min/dL", font=font_num, fill=self.c_ink)

        card3_top = card2_top + 150
        draw.rounded_rectangle([75, card3_top, self.width - 75, card3_top + 130], radius=16, fill=(248, 242, 235), outline=self.c_clay, width=2)
        draw.text((100, card3_top + 16), "Mechanism & Signaling Pathway", font=font_lbl, fill=self.c_clay)
        draw.text((100, card3_top + 46), "Non-Insulin GLUT4 Translocation", font=font_num, fill=(46, 125, 50))

        cite_top = card3_top + 150
        draw.text((75, cite_top), "Study Design: Randomized Crossover Trial (n=48, South Asian Cohort)", font=font_lbl, fill=self.c_ink)
        draw.text((75, cite_top + 28), "DOI: 10.1016/j.ijcmm.2024.08.012 • Center for Cardiometabolic Research", font=font_lbl, fill=self.c_clay)

animation_engine = AnimationEngine()
