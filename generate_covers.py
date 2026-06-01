from PIL import Image, ImageDraw, ImageFont
import os, math

OUT = os.path.dirname(__file__)
W_GIG, H_GIG = 1100, 740   # 550x370 @2x for retina
W_GUM, H_GUM = 1232, 706   # 616x353 @2x

# Colors (match landing page)
DARK  = (10, 10, 15)
CARD  = (19, 19, 26)
PURPLE = (108, 92, 231)
TEAL  = (0, 212, 170)
WHITE = (228, 228, 236)
DIM   = (136, 136, 160)

def load_font(size, bold=False):
    paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for p in paths:
        try:
            if bold and "Bold" not in p:
                return ImageFont.truetype(p.replace(".ttf"," Bold.ttf").replace(".ttc",""), size)
            return ImageFont.truetype(p, size)
        except:
            pass
    return ImageFont.load_default()

def gradient_bg(w, h, c1, c2):
    """Vertical gradient from c1 to c2"""
    img = Image.new('RGBA', (w, h), DARK)
    for y in range(h):
        ratio = y / h
        r = int(c1[0]*(1-ratio) + c2[0]*ratio)
        g = int(c1[1]*(1-ratio) + c2[1]*ratio)
        b = int(c1[2]*(1-ratio) + c2[2]*ratio)
        for x in range(w):
            img.putpixel((x, y), (r, g, b, 255))
    return img

def draw_rounded_rect(draw, xy, r, fill, outline=None):
    """Draw rounded rectangle"""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline)

def icon_py(draw, cx, cy, s=40):
    """Python-style icon: two brackets/chevrons"""
    color = TEAL
    for i in range(3):
        off = i * 12
        draw.line([(cx-s+off, cy-s//2), (cx-s//2+off, cy), (cx-s+off, cy+s//2)], fill=color, width=3)
        draw.line([(cx+s-off, cy-s//2), (cx+s//2-off, cy), (cx+s-off, cy+s//2)], fill=color, width=3)

def icon_ai(draw, cx, cy, s=40):
    """AI/brain icon: simple circuit nodes"""
    color = PURPLE
    r = s // 3
    # central node
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=3)
    # surrounding nodes
    for ang in [0, 60, 120, 180, 240, 300]:
        rad = math.radians(ang)
        nx = cx + int(s*0.6 * math.cos(rad))
        ny = cy + int(s*0.6 * math.sin(rad))
        draw.ellipse([nx-5, ny-5, nx+5, ny+5], fill=color)
        draw.line([cx, cy, nx, ny], fill=color, width=2)

def icon_doc(draw, cx, cy, s=40):
    """Document/presentation icon"""
    color = PURPLE
    # Paper shape
    draw.rectangle([cx-s, cy-s//2-5, cx, cy+s//2+5], outline=color, width=3)
    draw.rectangle([cx-s, cy-s//2-5, cx-s//2, cy-s//2+15], fill=color)  # fold corner
    # Lines for text
    for i in range(3):
        draw.line([(cx-s+12, cy-10+i*14), (cx-8, cy-10+i*14)], fill=DIM, width=2)

def icon_star(draw, cx, cy, s=40):
    """Star/sparkle icon for gumroad"""
    color = TEAL
    pts = []
    for i in range(5):
        ang = math.radians(-90 + i*72)
        pts.append((cx + int(s*math.cos(ang)), cy + int(s*math.sin(ang))))
        ang2 = math.radians(-90 + i*72 + 36)
        pts.append((cx + int(s*0.4*math.cos(ang2)), cy + int(s*0.4*math.sin(ang2))))
    draw.polygon(pts, outline=color, width=3)

def add_grid_pattern(draw, w, h):
    """Subtle tech grid"""
    for x in range(0, w, 40):
        draw.line([(x, 0), (x, h)], fill=(30, 30, 40, 80))
    for y in range(0, h, 40):
        draw.line([(0, y), (w, y)], fill=(30, 30, 40, 80))

def create_gig_cover(filename, title, subtitle, tag, icon_fn, theme_color=PURPLE):
    w, h = W_GIG, H_GIG
    img = Image.new('RGBA', (w, h), DARK)
    draw = ImageDraw.Draw(img)

    # Subtle grid
    add_grid_pattern(draw, w, h)

    # Gradient accent bar at bottom
    for y in range(h-6, h):
        ratio = (y - (h-6)) / 6
        r = int(PURPLE[0]*(1-ratio) + TEAL[0]*ratio)
        g = int(PURPLE[1]*(1-ratio) + TEAL[1]*ratio)
        b = int(PURPLE[2]*(1-ratio) + TEAL[2]*ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Left glow circle
    for r in range(200, 0, -1):
        alpha = int(20 * (r/200))
        draw.ellipse([w//4-r, h//2-r, w//4+r, h//2+r], fill=(*theme_color, alpha))

    # Right glow
    for r in range(150, 0, -1):
        alpha = int(15 * (r/150))
        draw.ellipse([3*w//4-r, h//3-r, 3*w//4+r, h//3+r], fill=(*TEAL, alpha))

    # Icon
    icon_fn(draw, 100, h//2, s=50)

    # Tag badge
    tag_w = 200
    draw_rounded_rect(draw, [170, 90, 170+tag_w, 90+36], 18, (*PURPLE, 40), outline=(*PURPLE, 100))
    font_tag = load_font(18, bold=True)
    draw.text((170+tag_w//2, 108), tag, fill=PURPLE, font=font_tag, anchor="mm")

    # Title
    font_title = load_font(46, bold=True)
    lines = title.split('\n')
    y_start = h//2 - 50 - (len(lines)-1)*28
    for i, line in enumerate(lines):
        draw.text((180, y_start + i*56), line, fill=WHITE, font=font_title)

    # Subtitle
    font_sub = load_font(24)
    draw.text((180, h//2 + 50), subtitle, fill=DIM, font=font_sub)

    # Watermark
    font_wm = load_font(16)
    draw.text((w-40, h-40), "DevForge", fill=(*DIM, 80), font=font_wm, anchor="rb")

    # Brand mark top-left
    font_logo = load_font(28, bold=True)
    draw.text((60, 40), "🛠️ DevForge", fill=DIM, font=font_logo)

    # Scale down to actual size
    img = img.resize((550, 370), Image.LANCZOS)
    path = os.path.join(OUT, filename)
    img.save(path, "PNG")
    print(f"Created: {path}")
    return path

def create_gumroad_cover(filename):
    w, h = W_GUM, H_GUM
    img = Image.new('RGBA', (w, h), DARK)
    draw = ImageDraw.Draw(img)

    add_grid_pattern(draw, w, h)

    # Gradient bar
    for y in range(h-8, h):
        ratio = (y - (h-8)) / 8
        r = int(PURPLE[0]*(1-ratio) + TEAL[0]*ratio)
        g = int(PURPLE[1]*(1-ratio) + TEAL[1]*ratio)
        b = int(PURPLE[2]*(1-ratio) + TEAL[2]*ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Glows
    for r in range(180, 0, -1):
        alpha = int(25 * (r/180))
        draw.ellipse([w//2-r, h//3-r, w//2+r, h//3+r], fill=(*PURPLE, alpha))

    # Star icon
    icon_star(draw, w//2, 140, s=45)

    # Title
    font_title = load_font(52, bold=True)
    draw.text((w//2, h//2-30), "200+ AI Prompts", fill=WHITE, font=font_title, anchor="mm")

    font_sub = load_font(28)
    draw.text((w//2, h//2+30), "For Work, Business & Creativity", fill=DIM, font=font_sub, anchor="mm")

    # Badges
    badges = ["ChatGPT", "Claude", "DeepSeek", "Gemini"]
    badge_w = 140
    badge_h = 36
    total_w = len(badges)*badge_w + (len(badges)-1)*16
    start_x = w//2 - total_w//2
    for i, b in enumerate(badges):
        bx = start_x + i*(badge_w+16)
        draw_rounded_rect(draw, [bx, h//2+60, bx+badge_w, h//2+60+badge_h], 18, (*PURPLE, 30), outline=(*PURPLE, 80))
        font_badge = load_font(18, bold=True)
        draw.text((bx+badge_w//2, h//2+60+badge_h//2), b, fill=PURPLE, font=font_badge, anchor="mm")

    # Bottom text
    font_btm = load_font(20)
    draw.text((w//2, h-60), "⭐ 80+ Pages · PDF & Notion · Lifetime Updates", fill=DIM, font=font_btm, anchor="mm")

    # Logo
    font_logo = load_font(28, bold=True)
    draw.text((50, 50), "🛠️ DevForge", fill=DIM, font=font_logo)

    # Scale down
    img = img.resize((616, 353), Image.LANCZOS)
    path = os.path.join(OUT, filename)
    img.save(path, "PNG")
    print(f"Created: {path}")
    return path

# Generate all covers
create_gig_cover(
    "cover-gig-python.png",
    "Python Scripts &\nTask Automation",
    "Web Scraping · Data Processing · Bots",
    "PYTHON AUTOMATION",
    icon_py,
    PURPLE
)

create_gig_cover(
    "cover-gig-ai.png",
    "Custom AI Chatbot\n& GPT Automation",
    "RAG Agents · OpenAI API · LangChain",
    "AI & CHATBOT",
    icon_ai,
    TEAL
)

create_gig_cover(
    "cover-gig-docs.png",
    "Automated PPT, Reports\n& Document Generation",
    "PowerPoint · PDF · Word · Charts",
    "DOCS & REPORTS",
    icon_doc,
    PURPLE
)

create_gumroad_cover("cover-gumroad-prompts.png")

print("\n✅ All covers generated!")
