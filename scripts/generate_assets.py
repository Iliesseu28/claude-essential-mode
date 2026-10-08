import os
from PIL import Image, ImageDraw, ImageFont

def create_banner():
    width = 1280
    height = 640
    img = Image.new("RGBA", (width, height), (11, 12, 16, 255))
    draw = ImageDraw.Draw(img)

    # Ambient radial glow in top-right and center
    for r in range(400, 0, -5):
        alpha = int(25 * (1 - r / 400))
        draw.ellipse([850 - r, 120 - r, 850 + r, 120 + r], fill=(217, 119, 87, alpha))
    for r in range(300, 0, -5):
        alpha = int(18 * (1 - r / 300))
        draw.ellipse([250 - r, 500 - r, 250 + r, 500 + r], fill=(78, 186, 101, alpha))

    # Grid lines (subtle tech grid)
    grid_color = (255, 255, 255, 10)
    for x in range(0, width, 60):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, 60):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # Fonts
    def get_font(size, bold=False):
        font_names = [
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/consola.ttf"
        ]
        for f in font_names:
            if os.path.exists(f):
                try:
                    return ImageFont.truetype(f, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    font_badge = get_font(16, bold=True)
    font_title = get_font(52, bold=True)
    font_sub = get_font(22, bold=False)
    font_card_title = get_font(18, bold=True)
    font_card_desc = get_font(14, bold=False)
    font_mono = get_font(15, bold=False)
    font_mono_bold = get_font(16, bold=True)

    # Top pill badge
    badge_x, badge_y = 80, 50
    badge_w, badge_h = 240, 36
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=18, fill=(28, 22, 21, 230), outline=(217, 119, 87, 180), width=1)
    draw.ellipse([badge_x + 14, badge_y + 13, badge_x + 24, badge_y + 23], fill=(217, 119, 87, 255))
    draw.text((badge_x + 36, badge_y + 8), "Claude Code Output Style", font=font_badge, fill=(235, 235, 240, 255))

    # Hero Title
    draw.text((80, 105), "claude-essential-mode", font=font_title, fill=(245, 245, 250, 255))
    draw.text((80, 175), "Cut 65% of output tokens without sounding like a caveman.", font=font_sub, fill=(180, 182, 195, 255))

    # 3 Stat pills
    stats = [
        ("⚡ -65% Output Tokens", "5x cost multiple saved"),
        ("🎯 Conclusion First", "No conversational fluff"),
        ("🚫 Zero Em-Dashes", "Natural human phrasing")
    ]
    stat_x = 80
    for title, desc in stats:
        sw, sh = 230, 68
        draw.rounded_rectangle([stat_x, 225, stat_x + sw, 225 + sh], radius=12, fill=(20, 22, 29, 220), outline=(45, 48, 62, 255), width=1)
        draw.text((stat_x + 16, 235), title, font=font_card_title, fill=(255, 255, 255, 255))
        draw.text((stat_x + 16, 262), desc, font=font_card_desc, fill=(140, 145, 160, 255))
        stat_x += sw + 20

    # Side-by-Side Comparison Terminal Window
    win_x, win_y = 80, 315
    win_w, win_h = 1120, 280
    draw.rounded_rectangle([win_x, win_y, win_x + win_w, win_y + win_h], radius=14, fill=(14, 16, 22, 245), outline=(42, 46, 60, 255), width=1)
    
    # Title bar
    draw.rounded_rectangle([win_x, win_y, win_x + win_w, win_y + 40], radius=14, fill=(22, 25, 34, 255))
    draw.rectangle([win_x, win_y + 25, win_x + win_w, win_y + 40], fill=(22, 25, 34, 255))
    draw.line([(win_x, win_y + 40), (win_x + win_w, win_y + 40)], fill=(42, 46, 60, 255), width=1)
    # Traffic lights
    draw.ellipse([win_x + 16, win_y + 14, win_x + 28, win_y + 26], fill=(255, 95, 86, 255))
    draw.ellipse([win_x + 36, win_y + 14, win_x + 48, win_y + 26], fill=(255, 189, 46, 255))
    draw.ellipse([win_x + 56, win_y + 14, win_x + 68, win_y + 26], fill=(39, 201, 63, 255))
    draw.text((win_x + 85, win_y + 11), "terminal — before & after comparison", font=font_card_desc, fill=(120, 125, 140, 255))

    # Split: Left (Default) vs Right (Essential Mode)
    split_x = win_x + win_w // 2
    draw.line([(split_x, win_y + 40), (split_x, win_y + win_h)], fill=(42, 46, 60, 255), width=1)

    # Left: Verbose Default
    draw.text((win_x + 25, win_y + 55), "DEFAULT CLAUDE CODE (184 tokens • 4.8s)", font=font_mono_bold, fill=(235, 100, 100, 255))
    draw.text((win_x + 25, win_y + 85), '"Certainly! I would be delighted to assist you with', font=font_mono, fill=(160, 165, 180, 255))
    draw.text((win_x + 25, win_y + 110), 'that problem. The root cause of the continuous', font=font_mono, fill=(160, 165, 180, 255))
    draw.text((win_x + 25, win_y + 135), 'component re-rendering is due to object references', font=font_mono, fill=(160, 165, 180, 255))
    draw.text((win_x + 25, win_y + 160), 'instantiated inline on every cycle. Let me detail', font=font_mono, fill=(160, 165, 180, 255))
    draw.text((win_x + 25, win_y + 185), 'a comprehensive 5-step mitigation strategy..."', font=font_mono, fill=(160, 165, 180, 255))
    draw.text((win_x + 25, win_y + 225), '↳ High latency, conversational fluff, high cost', font=font_card_desc, fill=(210, 80, 80, 255))

    # Right: Essential Mode
    draw.text((split_x + 25, win_y + 55), "ESSENTIAL MODE (38 tokens • 1.6s)", font=font_mono_bold, fill=(78, 186, 101, 255))
    draw.text((split_x + 25, win_y + 85), 'Conclusion: Inline object prop triggers shallow diff.', font=font_mono_bold, fill=(255, 255, 255, 255))
    
    # Table box
    tbl_y = win_y + 120
    draw.rounded_rectangle([split_x + 25, tbl_y, win_x + win_w - 25, tbl_y + 80], radius=8, fill=(20, 24, 32, 255), outline=(50, 56, 74, 255), width=1)
    draw.text((split_x + 40, tbl_y + 12), "Issue: Inline object prop triggers shallow diff", font=font_mono, fill=(220, 225, 235, 255))
    draw.text((split_x + 40, tbl_y + 44), "Fix: Wrap with useMemo or move outside component", font=font_mono, fill=(126, 231, 135, 255))
    
    draw.text((split_x + 25, win_y + 225), "✓ Instant, conclusion-first, 65% fewer tokens", font=font_card_desc, fill=(78, 186, 101, 255))

    os.makedirs("docs", exist_ok=True)
    img.save("docs/poster.png", format="PNG")
    print("Created docs/poster.png")

def create_icon():
    size = 128
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded icon background
    draw.rounded_rectangle([0, 0, size, size], radius=28, fill=(17, 19, 26, 255), outline=(217, 119, 87, 200), width=2)
    
    # Center lightning / flash icon with green accent
    # Draw lightning polygon
    poly = [(68, 18), (38, 66), (62, 66), (56, 110), (92, 54), (68, 54)]
    draw.polygon(poly, fill=(217, 119, 87, 255))

    # Dot
    draw.ellipse([88, 22, 102, 36], fill=(78, 186, 101, 255))

    img.save("docs/icon.png", format="PNG")
    print("Created docs/icon.png")

if __name__ == "__main__":
    create_banner()
    create_icon()
