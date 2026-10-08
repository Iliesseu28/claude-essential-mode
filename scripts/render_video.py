import os
import sys
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont

W = 1920
H = 1080
FPS = 30
TOTAL_FRAMES = 990  # 33.0 seconds

def get_font(size, bold=False, mono=False):
    fonts = [
        "C:/Windows/Fonts/cascadiacode.ttf" if mono else ("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        "C:/Windows/Fonts/consola.ttf" if mono else ("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf")
    ]
    for f in fonts:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, size)
            except Exception:
                pass
    return ImageFont.load_default()

font_badge = get_font(20, bold=True)
font_hero = get_font(56, bold=True)
font_sub = get_font(26, bold=False)
font_card_title = get_font(28, bold=True)
font_mono = get_font(22, mono=True)
font_mono_bold = get_font(24, bold=True, mono=True)
font_caption = get_font(26, bold=True)
font_stat_num = get_font(48, bold=True)
font_stat_lbl = get_font(18, bold=False)

def draw_background(draw, frame):
    # Dark stage
    # Ambient breathing radial glow
    breathe = (math.sin(frame * 0.08) + 1.0) * 0.5
    glow_r1 = int(350 + breathe * 50)
    for r in range(glow_r1, 0, -8):
        alpha = int(22 * (1 - r / glow_r1))
        draw.ellipse([1400 - r, 200 - r, 1400 + r, 200 + r], fill=(217, 119, 87, alpha))

    glow_r2 = int(300 + (1 - breathe) * 40)
    for r in range(glow_r2, 0, -8):
        alpha = int(18 * (1 - r / glow_r2))
        draw.ellipse([300 - r, 800 - r, 300 + r, 800 + r], fill=(78, 186, 101, alpha))

    # Tech grid
    grid_color = (255, 255, 255, 8)
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=grid_color, width=1)
    for y in range(0, H, 80):
        draw.line([(0, y), (width := W, y)], fill=grid_color, width=1)

def draw_subtitles(draw, text):
    if not text:
        return
    # Bottom subtitle container
    box_w = 1200
    box_h = 56
    box_x = (W - box_w) // 2
    box_y = 960
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=28, fill=(15, 17, 24, 230), outline=(50, 56, 75, 200), width=1)
    
    # Yellow voice icon
    draw.ellipse([box_x + 24, box_y + 20, box_x + 40, box_y + 36], fill=(217, 119, 87, 255))
    draw.text((box_x + 55, box_y + 13), text, font=font_caption, fill=(245, 245, 250, 255))

def render_frame(frame):
    img = Image.new("RGBA", (W, H), (11, 12, 16, 255))
    draw = ImageDraw.Draw(img)
    draw_background(draw, frame)

    # SCENE 1: Frames 0 to 174 (0.0s - 5.8s) -> The Problem
    if frame < 175:
        # Badge
        draw.rounded_rectangle([160, 90, 360, 134], radius=22, fill=(45, 18, 18, 240), outline=(235, 80, 80, 200), width=1)
        draw.text((185, 98), "● THE PROBLEM", font=font_badge, fill=(255, 120, 120, 255))

        draw.text((160, 160), "Tired of Bloated AI Coding Responses?", font=font_hero, fill=(255, 255, 255, 255))
        draw.text((160, 240), "Standard AI tools waste time, clutter screens, and burn expensive tokens.", font=font_sub, fill=(160, 165, 180, 255))

        # Terminal Card
        cw, ch = 1100, 480
        cx, cy = 160, 310
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=16, fill=(16, 18, 25, 245), outline=(50, 56, 75, 255), width=1)
        # Bar
        draw.rounded_rectangle([cx, cy, cx + cw, cy + 48], radius=16, fill=(24, 27, 38, 255))
        draw.rectangle([cx, cy + 28, cx + cw, cy + 48], fill=(24, 27, 38, 255))
        draw.ellipse([cx + 20, cy + 18, cx + 34, cy + 32], fill=(255, 95, 86, 255))
        draw.ellipse([cx + 44, cy + 18, cx + 58, cy + 32], fill=(255, 189, 46, 255))
        draw.ellipse([cx + 68, cy + 18, cx + 82, cy + 32], fill=(39, 201, 63, 255))
        draw.text((cx + 105, cy + 14), "bash — claude code default session", font=font_mono, fill=(120, 125, 145, 255))

        # Content
        draw.text((cx + 35, cy + 75), "> Why is my React component re-rendering?", font=font_mono_bold, fill=(240, 240, 245, 255))

        # Text stream
        lines = [
            '"Certainly! I would be delighted to assist you with this problem.',
            'The reason your React component is continually re-rendering is most likely',
            'caused by an object reference instantiated inline on every single render cycle.',
            'When you pass an inline object or callback prop without memoization,',
            'React shallow comparison sees a distinct object, triggering cascading renders.',
            'Let me explain 5 theoretical architectural options to fix this..."'
        ]
        
        visible_lines = min(len(lines), max(1, (frame - 20) // 22))
        for i in range(visible_lines):
            draw.text((cx + 35, cy + 130 + i * 40), lines[i], font=font_mono, fill=(175, 180, 195, 255))

        # Token counter badge
        tok = min(184, max(0, int((frame / 150) * 184)))
        draw.rounded_rectangle([cx + cw + 40, cy + 80, cx + cw + 420, cy + 280], radius=16, fill=(28, 16, 16, 240), outline=(235, 80, 80, 220), width=2)
        draw.text((cx + cw + 65, cy + 105), f"{tok}", font=font_stat_num, fill=(255, 100, 100, 255))
        draw.text((cx + cw + 175, cy + 122), "output tokens", font=font_card_title, fill=(255, 255, 255, 255))
        draw.text((cx + cw + 65, cy + 180), "● High Latency (4.8s)", font=font_sub, fill=(240, 120, 120, 255))
        draw.text((cx + cw + 65, cy + 220), "● Conversational Fluff", font=font_sub, fill=(240, 120, 120, 255))

        draw_subtitles(draw, "Tired of bloated AI responses that waste your time and burn through tokens?")

    # SCENE 2: Frames 175 to 449 (5.8s - 15.0s) -> The Solution
    elif frame < 450:
        f2 = frame - 175
        # Badge
        draw.rounded_rectangle([160, 90, 420, 134], radius=22, fill=(40, 25, 18, 240), outline=(217, 119, 87, 220), width=1)
        draw.text((185, 98), "● ESSENTIAL MODE", font=font_badge, fill=(245, 150, 110, 255))

        draw.text((160, 160), "Meet Essential Mode for Claude Code", font=font_hero, fill=(255, 255, 255, 255))
        draw.text((160, 240), "Native output style: cuts 65% of tokens without sounding like a caveman.", font=font_sub, fill=(160, 165, 180, 255))

        # Command terminal
        tw, th = 700, 110
        tx, ty = 160, 310
        draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=14, fill=(18, 20, 28, 255), outline=(60, 68, 90, 255), width=1)
        draw.text((tx + 30, ty + 25), "outputStyle: \"Essential\"", font=font_mono_bold, fill=(217, 119, 87, 255))
        draw.text((tx + 30, ty + 65), "✓ Native session layer • Zero runtime prompt overhead", font=font_mono, fill=(78, 186, 101, 255))

        # 4 Pillars cards
        pillars = [
            ("⚡ -65% Output Tokens", "5x cheaper output generation, answers in 1.8s"),
            ("🎯 Conclusion in Line 1", "Direct answer immediately, details only if needed"),
            ("📊 Tables & Checklists", "Never reads walls of text when a table works"),
            ("🚫 Zero Em-Dashes", "Natural human tone, eliminates AI writing tells")
        ]

        px, py = 160, 460
        pw, ph = 760, 85
        for i, (title, desc) in enumerate(pillars):
            if f2 > i * 15:
                draw.rounded_rectangle([px, py + i * 105, px + pw, py + i * 105 + ph], radius=12, fill=(18, 21, 29, 230), outline=(45, 52, 70, 255), width=1)
                draw.text((px + 24, py + i * 105 + 16), title, font=font_card_title, fill=(255, 255, 255, 255))
                draw.text((px + 24, py + i * 105 + 48), desc, font=font_sub, fill=(150, 155, 175, 255))

        # Right big badge
        rw, rh = 560, 480
        rx, ry = 1040, 320
        draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=20, fill=(22, 17, 16, 240), outline=(217, 119, 87, 200), width=2)
        draw.text((rx + 50, ry + 50), "Why Mode > Skill?", font=font_card_title, fill=(245, 160, 120, 255))
        
        reasons = [
            ("0 Input Token Tax", "Skills burn 500 input tokens per call"),
            ("Zero Instruction Drift", "Stays active across 50+ tool turns"),
            ("Pure Conversation Layer", "Never tampers with your code or diffs")
        ]
        for j, (rt, rd) in enumerate(reasons):
            draw.text((rx + 50, ry + 120 + j * 100), f"✓ {rt}", font=font_card_title, fill=(255, 255, 255, 255))
            draw.text((rx + 75, ry + 160 + j * 100), rd, font=font_sub, fill=(160, 165, 180, 255))

        draw_subtitles(draw, "Meet Essential Mode: Cuts 65% of output tokens without sounding like a caveman.")

    # SCENE 3: Frames 450 to 719 (15.0s - 24.0s) -> Side-by-side comparison
    elif frame < 720:
        # Badge
        draw.rounded_rectangle([160, 90, 460, 134], radius=22, fill=(20, 38, 26, 240), outline=(78, 186, 101, 220), width=1)
        draw.text((185, 98), "● REAL BENCHMARK", font=font_badge, fill=(120, 240, 140, 255))

        draw.text((160, 160), "Direct Side-by-Side Comparison", font=font_hero, fill=(255, 255, 255, 255))
        draw.text((160, 240), "Same technical accuracy. 65% fewer tokens. 2.6x faster clock time.", font=font_sub, fill=(160, 165, 180, 255))

        # Split windows
        card_w = 760
        card_h = 490

        # Left (Default)
        lx, ly = 160, 310
        draw.rounded_rectangle([lx, ly, lx + card_w, ly + card_h], radius=16, fill=(18, 16, 18, 245), outline=(180, 60, 60, 220), width=1)
        draw.rounded_rectangle([lx, ly, lx + card_w, ly + 50], radius=16, fill=(30, 20, 22, 255))
        draw.rectangle([lx, ly + 30, lx + card_w, ly + 50], fill=(30, 20, 22, 255))
        draw.text((lx + 25, ly + 14), "DEFAULT CLAUDE CODE", font=font_card_title, fill=(255, 100, 100, 255))
        draw.text((lx + card_w - 220, ly + 14), "184 tokens • 4.8s", font=font_mono_bold, fill=(255, 120, 120, 255))

        def_lines = [
            '"Certainly! I would be delighted to assist you with this problem.',
            'The reason your React component is continually re-rendering is most',
            'likely caused by an object reference instantiated inline on every single',
            'render cycle. When you pass an inline object or callback prop without',
            'memoization, React shallow comparison sees a distinct object reference,',
            'triggering cascading re-renders. Let me detail five theoretical options..."'
        ]
        for k, dl in enumerate(def_lines):
            draw.text((lx + 30, ly + 80 + k * 38), dl, font=font_mono, fill=(160, 165, 175, 255))
        
        draw.rounded_rectangle([lx + 30, ly + 390, lx + card_w - 30, ly + 460], radius=10, fill=(35, 18, 20, 255))
        draw.text((lx + 50, ly + 412), "✕ Heavy token cost • High waiting time • Conversational fluff", font=font_sub, fill=(255, 110, 110, 255))

        # Right (Essential Mode)
        rx, ry = 1000, 310
        draw.rounded_rectangle([rx, ry, rx + card_w, ry + card_h], radius=16, fill=(14, 20, 18, 245), outline=(78, 186, 101, 240), width=2)
        draw.rounded_rectangle([rx, ry, rx + card_w, ry + 50], radius=16, fill=(20, 35, 26, 255))
        draw.rectangle([rx, ry + 30, rx + card_w, ry + 50], fill=(20, 35, 26, 255))
        draw.text((rx + 25, ly + 14), "ESSENTIAL MODE", font=font_card_title, fill=(78, 186, 101, 255))
        draw.text((rx + card_w - 210, ly + 14), "38 tokens • 1.6s", font=font_mono_bold, fill=(78, 186, 101, 255))

        draw.text((rx + 30, ry + 80), "Conclusion: Inline object prop triggers shallow diff.", font=font_mono_bold, fill=(255, 255, 255, 255))

        # Mini table box
        draw.rounded_rectangle([rx + 30, ry + 140, rx + card_w - 30, ry + 280], radius=12, fill=(18, 28, 24, 255), outline=(45, 75, 55, 255), width=1)
        draw.text((rx + 50, ry + 165), "Issue: Inline object prop creates new reference", font=font_mono, fill=(220, 225, 235, 255))
        draw.text((rx + 50, ry + 215), "Fix: Wrap with useMemo or move outside component", font=font_mono, fill=(126, 231, 135, 255))

        draw.rounded_rectangle([rx + 30, ry + 390, rx + card_w - 30, ry + 460], radius=10, fill=(22, 42, 28, 255))
        draw.text((rx + 50, ry + 412), "✓ Instant, conclusion-first, 65% token reduction", font=font_sub, fill=(120, 240, 140, 255))

        draw_subtitles(draw, "Conclusion first • High-school clarity • Structured tables • Zero em-dashes")

    # SCENE 4: Frames 720 to 989 (24.0s - 33.0s) -> CTA & Install
    else:
        # Badge
        draw.rounded_rectangle([160, 90, 420, 134], radius=22, fill=(25, 22, 38, 240), outline=(160, 120, 240, 220), width=1)
        draw.text((185, 98), "● GET STARTED NOW", font=font_badge, fill=(200, 170, 255, 255))

        draw.text((160, 160), "Open Source on GitHub", font=font_hero, fill=(255, 255, 255, 255))
        draw.text((160, 240), "One line install for macOS, Linux, and Windows PowerShell.", font=font_sub, fill=(160, 165, 180, 255))

        # Command cards
        box_w = 900
        bx = 160
        # macOS / Linux
        draw.rounded_rectangle([bx, 310, bx + box_w, 410], radius=14, fill=(18, 20, 28, 255), outline=(55, 62, 85, 255), width=1)
        draw.text((bx + 30, 325), "macOS / Linux / WSL:", font=font_sub, fill=(150, 155, 175, 255))
        draw.text((bx + 30, 360), "curl -fsSL https://raw.githubusercontent.com/Iliesseu28/claude-essential-mode/main/install.sh | bash", font=font_mono_bold, fill=(217, 119, 87, 255))

        # Windows
        draw.rounded_rectangle([bx, 440, bx + box_w, 540], radius=14, fill=(18, 20, 28, 255), outline=(55, 62, 85, 255), width=1)
        draw.text((bx + 30, 455), "Windows PowerShell:", font=font_sub, fill=(150, 155, 175, 255))
        draw.text((bx + 30, 490), "irm https://raw.githubusercontent.com/Iliesseu28/claude-essential-mode/main/install.ps1 | iex", font=font_mono_bold, fill=(78, 186, 101, 255))

        # Star GitHub card
        star_w, star_h = 560, 360
        sx, sy = 1140, 310
        draw.rounded_rectangle([sx, sy, sx + star_w, sy + star_h], radius=20, fill=(20, 22, 32, 240), outline=(217, 119, 87, 220), width=2)
        draw.text((sx + 50, sy + 50), "Iliesseu28/claude-essential-mode", font=font_card_title, fill=(255, 255, 255, 255))
        draw.text((sx + 50, sy + 100), "MIT Licensed • Zero Dependencies", font=font_sub, fill=(150, 155, 175, 255))
        
        # Big Star Button
        btn_y = sy + 180
        draw.rounded_rectangle([sx + 50, btn_y, sx + star_w - 50, btn_y + 80], radius=16, fill=(217, 119, 87, 255))
        draw.text((sx + 100, btn_y + 22), "★ Star on GitHub", font=font_hero, fill=(255, 255, 255, 255))

        draw_subtitles(draw, "Zero input token overhead • Open source on GitHub • Star today!")

    return img.tobytes()

def main():
    print(f"Starting frame streaming to ffmpeg ({TOTAL_FRAMES} frames)...")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgba",
        "-r", f"{FPS}",
        "-i", "-",
        "-i", "audio/master_narration.mp3",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "19",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "docs/demo.mp4"
    ]

    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    for f in range(TOTAL_FRAMES):
        raw_bytes = render_frame(f)
        proc.stdin.write(raw_bytes)
        if f % 100 == 0:
            print(f"Rendered frame {f}/{TOTAL_FRAMES} ({f/TOTAL_FRAMES*100:.1f}%)")
    
    proc.stdin.close()
    proc.wait()
    print("Video generation completed: docs/demo.mp4")

if __name__ == "__main__":
    main()
