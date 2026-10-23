#!/usr/bin/env python3
import os
import math
from PIL import Image, ImageDraw, ImageFont

os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
output_dir = os.path.dirname(os.path.abspath(__file__))

def create_garment_image(filename, bg_color, garment_type, primary_color, secondary_color, details_color, label_text, badge_color=None):
    W, H = 800, 1000
    img = Image.new("RGBA", (W, H), bg_color)
    draw = ImageDraw.Draw(img)

    # Subtle studio backdrop vignette / grid
    for r in range(400, 0, -10):
        alpha = int(15 * (1 - r / 400))
        draw.ellipse([W//2 - r, H//2 - r, W//2 + r, H//2 + r], fill=(255, 255, 255, alpha))

    # Base hanger / stand
    draw.line([(W//2, 80), (W//2, 160)], fill=(120, 120, 130, 255), width=8)
    draw.polygon([(W//2 - 180, 200), (W//2, 160), (W//2 + 180, 200)], outline=(140, 140, 150, 255), fill=(80, 80, 90, 200), width=6)

    # Garment silhouettes based on type
    if garment_type == "bomber":
        # Torso
        draw.polygon([
            (W//2 - 180, 210),  # L shoulder
            (W//2 - 240, 380),  # L underarm
            (W//2 - 290, 680),  # L cuff
            (W//2 - 200, 690),  # L sleeve inner
            (W//2 - 180, 480),  # L waist upper
            (W//2 - 170, 760),  # L hem
            (W//2 + 170, 760),  # R hem
            (W//2 + 180, 480),  # R waist upper
            (W//2 + 200, 690),  # R sleeve inner
            (W//2 + 290, 680),  # R cuff
            (W//2 + 240, 380),  # R underarm
            (W//2 + 180, 210),  # R shoulder
            (W//2 + 90, 210),   # R collar
            (W//2, 260),        # Collar dip
            (W//2 - 90, 210),   # L collar
        ], fill=primary_color, outline=(20, 20, 20, 255), width=4)

        # Collar ribbed knit
        draw.polygon([(W//2 - 100, 210), (W//2, 265), (W//2 + 100, 210), (W//2 + 80, 195), (W//2, 240), (W//2 - 80, 195)], fill=secondary_color)

        # Ribbed hem
        draw.rectangle([W//2 - 172, 730, W//2 + 172, 765], fill=secondary_color, outline=(20, 20, 20, 255), width=2)
        # Ribbed cuffs
        draw.rectangle([W//2 - 292, 650, W//2 - 200, 690], fill=secondary_color)
        draw.rectangle([W//2 + 200, 650, W//2 + 292, 690], fill=secondary_color)

        # Front zipper
        draw.line([(W//2, 265), (W//2, 730)], fill=details_color, width=6)
        draw.rectangle([W//2 - 6, 320, W//2 + 6, 345], fill=(220, 220, 230, 255))

        # Chest logo/patch
        if badge_color:
            draw.ellipse([W//2 - 120, 350, W//2 - 50, 420], fill=badge_color, outline=(255, 255, 255, 200), width=3)
            draw.polygon([(W//2 - 95, 365), (W//2 - 65, 385), (W//2 - 95, 405), (W//2 - 85, 385)], fill=(255, 255, 255, 255))

        # Slanted welt pockets
        draw.line([(W//2 - 140, 560), (W//2 - 70, 610)], fill=(30, 30, 30, 255), width=8)
        draw.line([(W//2 + 140, 560), (W//2 + 70, 610)], fill=(30, 30, 30, 255), width=8)

    elif garment_type == "leather":
        # Asymmetrical biker jacket
        draw.polygon([
            (W//2 - 190, 210),
            (W//2 - 250, 380),
            (W//2 - 300, 710),
            (W//2 - 210, 720),
            (W//2 - 190, 490),
            (W//2 - 180, 750),
            (W//2 + 180, 750),
            (W//2 + 190, 490),
            (W//2 + 210, 720),
            (W//2 + 300, 710),
            (W//2 + 250, 380),
            (W//2 + 190, 210),
            (W//2 + 80, 220),
            (W//2, 290),
            (W//2 - 80, 220),
        ], fill=primary_color, outline=(40, 10, 10, 255), width=4)

        # Wide lapels
        draw.polygon([(W//2 - 80, 220), (W//2 - 160, 330), (W//2 - 40, 350), (W//2 - 20, 280)], fill=secondary_color, outline=(50, 10, 10, 255), width=3)
        draw.polygon([(W//2 + 80, 220), (W//2 + 160, 330), (W//2 + 40, 380), (W//2 + 20, 280)], fill=secondary_color, outline=(50, 10, 10, 255), width=3)

        # Metallic snaps on lapels
        for pt in [(W//2 - 140, 325), (W//2 + 140, 325), (W//2 - 50, 340), (W//2 + 50, 370)]:
            draw.ellipse([pt[0]-6, pt[1]-6, pt[0]+6, pt[1]+6], fill=(210, 210, 220, 255), outline=(50, 50, 50, 255), width=2)

        # Asymmetrical diagonal zipper
        draw.line([(W//2 - 30, 340), (W//2 + 50, 750)], fill=details_color, width=6)
        # Zippered pockets
        draw.line([(W//2 - 130, 460), (W//2 - 50, 490)], fill=details_color, width=5)
        draw.line([(W//2 - 130, 580), (W//2 - 40, 580)], fill=details_color, width=5)
        draw.line([(W//2 + 60, 580), (W//2 + 140, 580)], fill=details_color, width=5)

        # Bottom belt
        draw.rectangle([W//2 - 182, 715, W//2 + 182, 752], fill=(45, 10, 10, 255), outline=(20, 5, 5, 255), width=2)
        draw.rectangle([W//2 - 40, 710, W//2 + 40, 756], outline=(220, 220, 230, 255), width=4)

    elif garment_type == "trench":
        # Long elegant trench coat
        draw.polygon([
            (W//2 - 180, 200),
            (W//2 - 250, 380),
            (W//2 - 290, 730),
            (W//2 - 210, 740),
            (W//2 - 200, 520),
            (W//2 - 220, 880),
            (W//2 + 220, 880),
            (W//2 + 200, 520),
            (W//2 + 210, 740),
            (W//2 + 290, 730),
            (W//2 + 250, 380),
            (W//2 + 180, 200),
            (W//2 + 70, 210),
            (W//2, 280),
            (W//2 - 70, 210),
        ], fill=primary_color, outline=(100, 80, 60, 255), width=4)

        # Large double-breasted lapels
        draw.polygon([(W//2 - 70, 210), (W//2 - 150, 320), (W//2 - 30, 350), (W//2, 280)], fill=secondary_color, outline=(120, 90, 70, 255), width=3)
        draw.polygon([(W//2 + 70, 210), (W//2 + 150, 320), (W//2 + 30, 350), (W//2, 280)], fill=secondary_color, outline=(120, 90, 70, 255), width=3)

        # Double-breasted horn buttons
        for y in [380, 460, 540]:
            draw.ellipse([W//2 - 60 - 10, y - 10, W//2 - 60 + 10, y + 10], fill=details_color, outline=(40, 30, 20, 255), width=2)
            draw.ellipse([W//2 + 60 - 10, y - 10, W//2 + 60 + 10, y + 10], fill=details_color, outline=(40, 30, 20, 255), width=2)

        # Waist belt with buckle
        draw.rectangle([W//2 - 200, 580, W//2 + 200, 620], fill=secondary_color, outline=(80, 60, 45, 255), width=3)
        draw.rectangle([W//2 - 35, 575, W//2 + 35, 625], outline=(210, 180, 120, 255), width=5)

        # Shoulder epaulettes
        draw.polygon([(W//2 - 180, 205), (W//2 - 100, 210), (W//2 - 110, 230), (W//2 - 180, 225)], fill=secondary_color)
        draw.polygon([(W//2 + 180, 205), (W//2 + 100, 210), (W//2 + 110, 230), (W//2 + 180, 225)], fill=secondary_color)

    elif garment_type == "denim":
        # Classic trucker jacket
        draw.polygon([
            (W//2 - 180, 210),
            (W//2 - 240, 370),
            (W//2 - 280, 690),
            (W//2 - 200, 700),
            (W//2 - 180, 480),
            (W//2 - 165, 710),
            (W//2 + 165, 710),
            (W//2 + 180, 480),
            (W//2 + 200, 700),
            (W//2 + 280, 690),
            (W//2 + 240, 370),
            (W//2 + 180, 210),
            (W//2 + 80, 210),
            (W//2, 250),
            (W//2 - 80, 210),
        ], fill=primary_color, outline=(20, 40, 70, 255), width=4)

        # Pointed denim collar
        draw.polygon([(W//2 - 80, 210), (W//2 - 120, 270), (W//2, 260)], fill=secondary_color, outline=(200, 160, 80, 200), width=3)
        draw.polygon([(W//2 + 80, 210), (W//2 + 120, 270), (W//2, 260)], fill=secondary_color, outline=(200, 160, 80, 200), width=3)

        # Twin flap chest pockets
        for sign in [-1, 1]:
            cx = W//2 + sign * 90
            draw.rectangle([cx - 45, 360, cx + 45, 440], fill=primary_color, outline=(200, 160, 80, 220), width=2)
            draw.polygon([(cx - 48, 360), (cx, 380), (cx + 48, 360)], fill=secondary_color, outline=(200, 160, 80, 255), width=2)
            draw.ellipse([cx - 5, 370, cx + 5, 380], fill=(220, 180, 110, 255))

        # Golden contrast stitching seams
        draw.line([(W//2 - 45, 270), (W//2 - 45, 710)], fill=(210, 170, 90, 220), width=2)
        draw.line([(W//2 + 45, 270), (W//2 + 45, 710)], fill=(210, 170, 90, 220), width=2)
        draw.line([(W//2, 260), (W//2, 710)], fill=(20, 40, 80, 255), width=4)

        # Metal rivets/buttons down center
        for y in range(290, 710, 70):
            draw.ellipse([W//2 - 8, y - 8, W//2 + 8, y + 8], fill=(220, 190, 120, 255), outline=(60, 40, 20, 255), width=2)

    elif garment_type == "cyberpunk":
        # Futuristic techwear hoodie
        draw.polygon([
            (W//2 - 190, 200),
            (W//2 - 260, 390),
            (W//2 - 300, 710),
            (W//2 - 210, 720),
            (W//2 - 190, 490),
            (W//2 - 180, 760),
            (W//2 + 180, 760),
            (W//2 + 190, 490),
            (W//2 + 210, 720),
            (W//2 + 300, 710),
            (W//2 + 260, 390),
            (W//2 + 190, 200),
            (W//2 + 90, 170),
            (W//2, 210),
            (W//2 - 90, 170),
        ], fill=primary_color, outline=(0, 255, 200, 255), width=4)

        # High cowl hood neckline
        draw.polygon([(W//2 - 100, 170), (W//2, 260), (W//2 + 100, 170), (W//2 + 80, 140), (W//2, 190), (W//2 - 80, 140)], fill=secondary_color, outline=(0, 255, 200, 255), width=2)

        # Neon geometric tech patterns
        draw.line([(W//2 - 140, 340), (W//2, 420), (W//2 + 140, 340)], fill=details_color, width=4)
        draw.line([(W//2 - 120, 480), (W//2, 540), (W//2 + 120, 480)], fill=details_color, width=4)
        draw.line([(W//2, 260), (W//2, 750)], fill=details_color, width=4)

        # Futuristic glowing accents
        draw.rectangle([W//2 - 120, 560, W//2 - 30, 640], outline=details_color, width=2)
        draw.rectangle([W//2 + 30, 560, W//2 + 120, 640], outline=details_color, width=2)
        draw.text((W//2 - 110, 570), "CYBER-01", fill=details_color)
        draw.text((W//2 + 40, 570), "LUCY-3.5", fill=details_color)

    elif garment_type == "blazer":
        # Sharp tailored navy suit blazer
        draw.polygon([
            (W//2 - 185, 200),
            (W//2 - 240, 370),
            (W//2 - 280, 710),
            (W//2 - 200, 720),
            (W//2 - 185, 490),
            (W//2 - 175, 780),
            (W//2 + 175, 780),
            (W//2 + 185, 490),
            (W//2 + 200, 720),
            (W//2 + 280, 710),
            (W//2 + 240, 370),
            (W//2 + 185, 200),
            (W//2 + 75, 205),
            (W//2, 360),
            (W//2 - 75, 205),
        ], fill=primary_color, outline=(15, 20, 40, 255), width=4)

        # White dress shirt and tie in V-neck opening
        draw.polygon([(W//2 - 60, 205), (W//2, 360), (W//2 + 60, 205)], fill=(245, 245, 250, 255))
        draw.polygon([(W//2 - 15, 230), (W//2, 340), (W//2 + 15, 230)], fill=(180, 30, 40, 255)) # Red silk tie

        # Notch lapels
        draw.polygon([(W//2 - 75, 205), (W//2 - 140, 320), (W//2 - 50, 360), (W//2, 360)], fill=secondary_color, outline=(20, 25, 50, 255), width=2)
        draw.polygon([(W//2 + 75, 205), (W//2 + 140, 320), (W//2 + 50, 360), (W//2, 360)], fill=secondary_color, outline=(20, 25, 50, 255), width=2)

        # Chest welt pocket with white pocket square
        draw.rectangle([W//2 - 130, 370, W//2 - 60, 382], fill=(20, 25, 55, 255), outline=(10, 15, 30, 255), width=2)
        draw.polygon([(W//2 - 110, 370), (W//2 - 95, 350), (W//2 - 80, 370)], fill=(255, 255, 255, 255))

        # Flap waist pockets
        draw.rectangle([W//2 - 150, 580, W//2 - 50, 600], fill=secondary_color, outline=(15, 20, 40, 255), width=2)
        draw.rectangle([W//2 + 50, 580, W//2 + 150, 600], fill=secondary_color, outline=(15, 20, 40, 255), width=2)

        # Blazer buttons
        draw.ellipse([W//2 - 8, 480 - 8, W//2 + 8, 480 + 8], fill=details_color, outline=(20, 20, 20, 255), width=2)
        draw.ellipse([W//2 - 8, 550 - 8, W//2 + 8, 550 + 8], fill=details_color, outline=(20, 20, 20, 255), width=2)

    elif garment_type == "floral":
        # Tropical Hawaiian vacation button-down shirt
        draw.polygon([
            (W//2 - 180, 210),
            (W//2 - 230, 340),
            (W//2 - 260, 500),
            (W//2 - 190, 510),
            (W//2 - 175, 390),
            (W//2 - 165, 720),
            (W//2 + 165, 720),
            (W//2 + 175, 390),
            (W//2 + 190, 510),
            (W//2 + 260, 500),
            (W//2 + 230, 340),
            (W//2 + 180, 210),
            (W//2 + 80, 210),
            (W//2, 270),
            (W//2 - 80, 210),
        ], fill=primary_color, outline=(20, 80, 70, 255), width=3)

        # Camp collar
        draw.polygon([(W//2 - 80, 210), (W//2 - 130, 280), (W//2, 270)], fill=secondary_color, outline=(20, 80, 70, 255), width=2)
        draw.polygon([(W//2 + 80, 210), (W//2 + 130, 280), (W//2, 270)], fill=secondary_color, outline=(20, 80, 70, 255), width=2)

        # Floral tropical print leaves & flowers
        flowers = [
            (W//2 - 80, 360), (W//2 + 60, 340), (W//2 - 40, 480), (W//2 + 90, 500),
            (W//2 - 90, 620), (W//2 + 50, 640), (W//2 - 200, 420), (W//2 + 200, 420)
        ]
        for fx, fy in flowers:
            # Petals
            for a in range(0, 360, 72):
                rad = math.radians(a)
                px = fx + int(24 * math.cos(rad))
                py = fy + int(24 * math.sin(rad))
                draw.ellipse([px-14, py-14, px+14, py+14], fill=(255, 120, 150, 230))
            # Flower center
            draw.ellipse([fx-10, fy-10, fx+10, fy+10], fill=(255, 230, 80, 255))
            # Palm leaf accents
            draw.arc([fx-40, fy-30, fx+40, fy+30], start=30, end=150, fill=(30, 160, 90, 240), width=6)

        # Center placket with coconut buttons
        draw.line([(W//2, 270), (W//2, 720)], fill=(20, 80, 70, 255), width=3)
        for y in range(310, 710, 80):
            draw.ellipse([W//2 - 7, y - 7, W//2 + 7, y + 7], fill=(160, 120, 80, 255), outline=(70, 40, 20, 255), width=2)

    # Clean lower card banner for title
    banner_y = 860
    draw.rounded_rectangle([40, banner_y, W - 40, banner_y + 100], radius=16, fill=(20, 24, 34, 230), outline=(50, 60, 80, 255), width=2)

    # Text overlay
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
        sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    draw.text((70, banner_y + 20), label_text, fill=(255, 255, 255, 255), font=font)
    draw.text((70, banner_y + 58), "Decart Lucy VTON 3.5 Ready", fill=(120, 190, 255, 255), font=sub_font)

    # Save
    out_path = os.path.join(output_dir, filename)
    img.save(out_path, "PNG")
    print(f"Generated: {out_path}")

# Generate full wardrobe presets
create_garment_image(
    "bomber-jacket.png",
    bg_color=(18, 22, 30, 255),
    garment_type="bomber",
    primary_color=(25, 28, 35, 255),     # Black bomber
    secondary_color=(15, 18, 22, 255),   # Dark charcoal trims
    details_color=(200, 200, 210, 255),  # Silver zipper
    label_text="Black Bomber Jacket (Blue Logo)",
    badge_color=(30, 130, 255, 255)      # Blue chest logo
)

create_garment_image(
    "red-leather-jacket.png",
    bg_color=(28, 18, 20, 255),
    garment_type="leather",
    primary_color=(190, 25, 35, 255),    # Vibrant red leather
    secondary_color=(140, 15, 25, 255),  # Deep burgundy lapels
    details_color=(220, 220, 230, 255),  # Chrome metal hardware
    label_text="Red Biker Leather Jacket"
)

create_garment_image(
    "denim-jacket.png",
    bg_color=(18, 24, 32, 255),
    garment_type="denim",
    primary_color=(55, 105, 175, 255),   # Washed indigo denim
    secondary_color=(45, 90, 155, 255),  # Darker collar
    details_color=(220, 185, 120, 255),  # Brass rivets
    label_text="Vintage Blue Denim Jacket"
)

create_garment_image(
    "beige-trench.png",
    bg_color=(28, 26, 24, 255),
    garment_type="trench",
    primary_color=(215, 195, 160, 255),  # Classic khaki/beige
    secondary_color=(195, 175, 140, 255),
    details_color=(70, 50, 35, 255),     # Tortoiseshell buttons
    label_text="Classic Double-Breasted Trench"
)

create_garment_image(
    "cyberpunk-hoodie.png",
    bg_color=(15, 18, 25, 255),
    garment_type="cyberpunk",
    primary_color=(25, 28, 35, 255),     # Matte black techwear
    secondary_color=(18, 20, 26, 255),
    details_color=(0, 255, 205, 255),    # Neon cyan glow
    label_text="Cyberpunk Neon Tech Hoodie"
)

create_garment_image(
    "navy-blazer.png",
    bg_color=(18, 20, 28, 255),
    garment_type="blazer",
    primary_color=(25, 38, 75, 255),     # Navy wool
    secondary_color=(20, 30, 60, 255),
    details_color=(210, 175, 100, 255),  # Gold blazer buttons
    label_text="Navy Tailored Blazer & Tie"
)

create_garment_image(
    "floral-shirt.png",
    bg_color=(20, 30, 28, 255),
    garment_type="floral",
    primary_color=(225, 245, 235, 255),  # Soft mint background
    secondary_color=(200, 230, 220, 255),
    details_color=(160, 120, 80, 255),   # Coconut buttons
    label_text="Tropical Floral Vacation Shirt"
)
print("All sample garments generated successfully!")
