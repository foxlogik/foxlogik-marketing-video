#!/usr/bin/env python3
"""
Foxlogik Lego Spaceballs Video - Image Generation Script
Generates all 14 reference images using FAL AI
"""

import os
import json
import urllib.request
from pathlib import Path
import fal_client

# FAL AI Configuration.
# fal_client authenticates via the FAL_KEY env var. Accept FAL_API_KEY as a
# convenience alias and normalize it to FAL_KEY so the client can see it.
FAL_KEY = os.getenv("FAL_KEY") or os.getenv("FAL_API_KEY")

if not FAL_KEY:
    raise ValueError(
        "❌ No API key found. Set FAL_KEY (or FAL_API_KEY) and try again.\n"
        '   PowerShell:  $env:FAL_KEY = "your_key_here"'
    )

os.environ["FAL_KEY"] = FAL_KEY

# Reference images directory
OUTPUT_DIR = Path("reference-images")
OUTPUT_DIR.mkdir(exist_ok=True)

# Image Generation Prompts (extracted from IMAGE_GENERATION_PROMPTS_Lego_Spaceballs.md)
PROMPTS = [
    {
        "name": "01_Frame1A_Office_Cubicle",
        "prompt": """Generate a professional Lego construction office cubicle in high detail.
Yellow Lego minifigure wearing orange construction vest and yellow hard hat
sitting at a tan/brown Lego brick desk with a light blue Lego monitor.
The desk has a Lego keyboard, small office supplies made of Lego blocks.
Warm office lighting, soft shadows. Clean, organized workspace.
Professional Lego plastic texture visible throughout.
The minifigure looks calm, working at the desk, yellow cylindrical hands on keyboard.
Bright primary colors. Lego movie style animation aesthetic.
High detail, cinematic lighting, 4K quality, photorealistic Lego render.""",
    },
    {
        "name": "02_Frame1B_DarkHelmet_Invasion",
        "prompt": """Close-up of an absolutely MASSIVE Lego Dark Helmet filling 70% of the screen.
The helmet is metallic silver-gray with a menacing design.
Large red glowing visor (like an angry eye). Metallic shiny Lego brick texture.
Helmet is disproportionately huge, comically oversized, filling left side of screen.
Background: Lego office cubicle blurred behind helmet (small in comparison).
Small tan Lego desk visible, papers flying everywhere in background.
Space starfield visible behind everything (Spaceballs aesthetic).
Theatrical, menacing but comedic scale mismatch.
Red laser beams shooting from visor into scene.
High quality 3D Lego render, cinematic, dramatic lighting.""",
    },
    {
        "name": "03_Frame1C_Colonel_Panicking",
        "prompt": """Medium shot of Lego minifigure Colonel Sandurz in dark military uniform
looking extremely panicked inside a Lego spaceship control room interior.
Black hair piece, worried facial expression (printed on yellow face).
Military dark-gray/black Lego uniform with rank insignia print.
Background: Futuristic Lego control panels with glowing buttons,
three Lego monitors showing conflicting numbers (40, 45, 38 in white text).
Spaceship interior walls: metallic gray Lego bricks with tech details.
Fluorescent blue and white Lego lighting.
Colonel's arms raised in panic gesture (Lego snap-pose).
Dark Helmet's red visor glow visible in background, menacing.
High detail, professional Lego render, 4K quality.""",
    },
    {
        "name": "04_Frame2A_ThreeMonitors",
        "prompt": """Three large Lego monitor panels floating in space starfield (Spaceballs nebula background).
Left panel: GREEN Lego brick background with white text "TIMESHEET SYSTEM",
"LONE STARR", "40 HOURS", green checkmark icon.
Center panel: YELLOW/AMBER Lego brick background with white text "PAYROLL SYSTEM",
"LONE STARR", "45 HOURS", yellow question mark icon.
Right panel: ORANGE Lego brick background with white text "PROJECT TRACKER",
"LONE STARR", "38 HOURS", orange warning triangle icon.
Bright red connecting arrows/lines between panels with electrical zap effects.
Pixelated Lego brick texture visible on each panel.
High contrast, clear readability, colorful Lego primary colors.
Space background: Purple/blue nebula with twinkling stars.
Professional dashboard aesthetic, clean borders on panels.
4K quality, detailed Lego brick render.""",
    },
    {
        "name": "05_Frame2B_Lone_Starr_Confused",
        "prompt": """Lego minifigure Lone Starr at desk with bewildered expression, eyes wide open,
mouth in O-shape of confusion (printed face). Yellow construction worker outfit, hard hat.
Three Lego monitor screens behind desk spinning/rotating, showing different data.
Numbers visible: 40, 45, 38 (each monitor different, conflicting).
Red error X marks and question marks floating around screens.
Papers flying everywhere (Lego tan/beige brick blocks with printed spreadsheet data).
Spaceship interior and construction office blended setting.
Lego office desk, chair, keyboard visible.
Confusion energy: chaos, disorganization, "nothing makes sense" aesthetic.
Warm lighting mixed with cool spaceship lighting.
Motion blur effect on flying papers showing chaos.
High detail, cinematic, 4K Lego render.""",
    },
    {
        "name": "06_Frame3A_BudgetExplosion",
        "prompt": """Large Lego budget dashboard screen center-frame showing:
"PROJECT: Site #42 - Warehouse Extension"
"BUDGET: $500,000"
"SPENT: $497,000 (climbing rapidly)"
Budget bar made of Lego bricks: GREEN on left, YELLOW middle, RED overflow on right.
Red Lego bricks stacking ABOVE the bar (overflow metaphor).
Semi-transparent gold/red dollar sign ($) symbols falling/floating downward
throughout the scene like rain, fading off-screen.
15-20 dollar signs visible at peak chaos.
Dark background with Lego construction office environment.
Alarm lights flashing red (emergency mode).
Deep ominous colors: dark gray, red, golds.
Dramatic, devastating aesthetic but still comedic in Lego style.
4K quality, detailed Lego render, dramatic lighting.""",
    },
    {
        "name": "07_Frame3B_Lone_Starr_Defeated",
        "prompt": """Lego minifigure Lone Starr at desk, completely defeated posture.
Head resting in hand (arm on desk), slumped shoulders, giving up gesture.
Sad printed face expression (downturned mouth, sad eyes on yellow minifigure).
Optional: Single blue Lego tear rolling down face.
Wrench prop on desk (hero weapon, now useless).
Lego office desk and chair visible.
Lego monitor showing red budget disaster in background (still visible).
Dark Helmet's massive helmet visible far in background, glowing red (celebrating victory).
Overall dark, sad, defeated mood.
Lighting: Dim, shadowy, minor-key emotional atmosphere.
Dark grays, dark blues dominate color palette.
Comedic but touching defeat moment.
4K quality, dramatic Lego render.""",
    },
    {
        "name": "08_Frame4A_BlackScreen",
        "prompt": """Pure black background, absolutely void of detail.
Optional: Faint starfield silhouettes barely visible through darkness.
Mystical, ominous, anticipatory atmosphere.
No characters, no objects, just pure black space.
Preparation for hero reveal, dramatic pause aesthetic.""",
    },
    {
        "name": "09_Frame4B_Logo_Assembly",
        "prompt": """Foxlogik logo materializing as Lego bricks assembling piece by piece.
Center: First single Lego brick appears.
Expanding outward: Rings of colorful Lego bricks clicking into place around center.
Final result: Logo made entirely of bright colored Lego bricks
(blues, teals, bright accent colors - professional tech aesthetic).
Each brick has visible shiny plastic Lego texture with slight wear details.
CAPE attached to logo: Flowing Lego fabric cape in brand color, gently fluttering.
Background: Bright white or light gradient (hope breaking through darkness).
Starburst light rays emanating from logo (heroic reveal effect).
Space starfield visible at edges (Spaceballs aesthetic maintained).
Glowing outer aura around completed logo (mystical, powerful).
Triumphant, heroic, inspiring visual.
4K quality, detailed Lego brick render, dramatic lighting.""",
    },
    {
        "name": "10_Frame4C_Dashboard_Materialized",
        "prompt": """Lego dashboard with 2x2 grid of panels materializing:

TOP-LEFT PANEL - Green background:
"ACTIVE WORKERS" header, list of workers with green checkmarks:
"✓ Lone Starr | On-site | 8h 42m"
"✓ Barf | On-site | 8h 15m"
"✓ Vespa | Office | 5h 20m"

TOP-RIGHT PANEL - Green background:
"SYSTEMS SYNCED" header, perfect alignment:
"Timesheet: 40h ✓"
"Payroll: 40h ✓"
"Project: 40h ✓"

BOTTOM-LEFT PANEL - Green background:
"PROJECT BUDGET" header:
"Allocated: $500,000"
"Spent: $447,000"
"Remaining: $53,000 ✓"
"Status: ON TRACK (85%)"
Green budget bar, healthy 85% fill.

BOTTOM-RIGHT PANEL - Mixed colors:
"LIVE ACTIVITY" header, scrolling feed:
"14:42 - Lone Starr clocked in"
"14:38 - Site #42 labor: $1,240"
"14:32 - Barf completed task"

All panels: Dark charcoal gray background, white text,
bright GREEN accents, Lego brick texture visible.
Multiple large green checkmarks visible.
Starfield background (space visible behind dashboard).
Clean, professional, organized, all-systems-GO feeling.
Bright green glow around successful elements.
Premium tech aesthetic meets Lego authenticity.
4K quality, highly detailed, professional dashboard render.""",
    },
    {
        "name": "11_Frame5A_Lone_Starr_Transformed",
        "prompt": """Lego minifigure Lone Starr at same desk, now COMPLETELY TRANSFORMED.
Confident, relaxed posture, leaning back slightly.
Wearing cool dark Lego sunglasses (cool-guy minifigure style).
Happy printed face (smile, confident eyes on yellow minifigure).
Lego office desk now CLEAN and organized (no papers, minimal clutter).
Laptop/monitor showing bright Foxlogik dashboard on screen (glowing, visible).
Tablet nearby also showing LEM data.
Everything in place, organized, peaceful.
Warm, comfortable office lighting (not stressed, not dim).
Background: Clean construction office, successful energy.
Barf and Princess Vespa visible in background celebrating (optional).
Dark Helmet visible far away, defeated (optional).
Professional, confident, accomplished hero energy.
Victory, success, transformation complete.
4K quality, warm Lego render, successful aesthetic.""",
    },
    {
        "name": "12_Frame5B_Dashboard_CloseUp",
        "prompt": """Close-up of Lego laptop/tablet screen showing Foxlogik LEM dashboard.
Screen slightly tilted (natural viewing angle).
Same 2x2 grid panels, visible and glowing.
Dashboard clearly readable, data visible, green checkmarks prominent.
Professional tech aesthetic, high-quality display.
Subtle reflection of Lone Starr's face optional in screen reflection.
Bright, active, healthy data visualization.
Real-time metrics showing operational excellence.
4K quality, detailed screen render, tech-forward look.""",
    },
    {
        "name": "13_Frame5C_Benefits_SlideIn",
        "prompt": """Clean white or light gray background.
Four benefits displayed vertically, one by one:
"✓ Defeat Data Chaos"
"✓ Master the Foxlogik Force"
"✓ Build Your Empire"
"✓ Sync All Systems"

Each with large bright GREEN checkmark before text.
Text: Blocky, chunky sans-serif font (Lego-style), 40-48px.
Color: Dark gray or black.
Spacing: Even, professional vertical alignment.
Layout: Left-aligned or center-aligned, clean spacing.
Minimalist, professional, clear, easy to read.
Background: Pure white or subtle light texture.
Premium motion graphics aesthetic meets Lego authenticity.
4K quality, clean, readable, inspiring.""",
    },
    {
        "name": "14_Frame5D_CTA_Frame",
        "prompt": """Clean professional CTA screen with white background.
Centered, vertical stack layout:

Top: Foxlogik logo (Lego brick style) - 40-50px height.

Below: "LEM PROCESSING GUIDE" headline - Bold, blocky font, 56-64px, dark gray.
Below: "Free Download" subheading - Regular font, 24px, medium gray.
Below: Subtle gray divider line.
Below: Four benefits with green arrows:
"→ Defeat Data Chaos"
"→ Master the Foxlogik Force"
"→ Build Your Empire"
"→ Sync All Systems"
Below: URL "foxlogik.com/lem-guide" - Bold, clickable blue color.
Bottom-right: QR code (40x40px, optional).

All text: High contrast, easy to read.
Colors: White background, dark text, green accents, brand color URL.
Lego aesthetic: Blocky fonts, primary colors, clean design.
Professional, trustworthy, action-oriented feel.
No distracting elements, clear CTA hierarchy.
4K quality, professional design, landing page quality.""",
    },
]

# FAL AI Model Configuration
# Valid endpoint for the hosted high-quality FLUX Pro model.
MODEL_ID = "fal-ai/flux-pro/v1.1"

def generate_image(prompt_text: str, name: str) -> str:
    """Generate a single image with FAL AI and download it to OUTPUT_DIR.

    Returns the remote image URL on success, or None on failure.
    """
    print(f"🎨 Generating: {name}")

    try:
        # subscribe() blocks until the job finishes and surfaces queue progress.
        result = fal_client.subscribe(
            MODEL_ID,
            arguments={
                "prompt": prompt_text,
                "image_size": "landscape_16_9",  # 16:9 aspect ratio
                "output_format": "png",
            },
        )

        image_url = result["images"][0]["url"]

        # Actually download the file to disk.
        output_path = OUTPUT_DIR / f"{name}.png"
        urllib.request.urlretrieve(image_url, output_path)

        print(f"✅ Saved: {output_path}\n")
        return image_url

    except Exception as e:
        print(f"❌ Failed to generate {name}: {str(e)}\n")
        return None

def main():
    """Generate all reference images"""
    print("=" * 60)
    print("🎬 Foxlogik Lego Spaceballs Video - Image Generation")
    print("=" * 60)
    print(f"Generating {len(PROMPTS)} reference images...\n")

    results = []
    completed = 0
    failed = 0

    for i, prompt_data in enumerate(PROMPTS, 1):
        name = prompt_data["name"]
        prompt = prompt_data["prompt"]

        print(f"[{i}/{len(PROMPTS)}] {name}")

        image_url = generate_image(prompt, name)

        if image_url:
            results.append({
                "frame": name,
                "url": image_url,
                "prompt": prompt
            })
            completed += 1
        else:
            failed += 1

    # Save manifest of generated images
    manifest_path = OUTPUT_DIR / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump({
            "total": len(PROMPTS),
            "completed": completed,
            "failed": failed,
            "images": results
        }, f, indent=2)

    print("\n" + "=" * 60)
    print("🎉 Generation Complete!")
    print("=" * 60)
    print(f"✅ Generated: {completed}/{len(PROMPTS)}")
    print(f"❌ Failed: {failed}/{len(PROMPTS)}")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print(f"📋 Manifest saved: {manifest_path}")
    print("\nImages are ready for animation team!")

if __name__ == "__main__":
    main()
