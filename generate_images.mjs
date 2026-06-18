#!/usr/bin/env node
/**
 * Foxlogik Lego Spaceballs Video - Image Generation Script (Node.js)
 * Generates all 14 reference images using FAL AI's official client.
 *
 * Setup:
 *   npm install @fal-ai/client
 *   $env:FAL_KEY = "your_key_here"   # PowerShell
 *   node generate_images.mjs
 */

import { fal } from "@fal-ai/client";
import { writeFile, mkdir } from "node:fs/promises";
import path from "node:path";

// --- Auth ---------------------------------------------------------------
// The fal client reads FAL_KEY automatically. Accept FAL_API_KEY as an alias.
const FAL_KEY = process.env.FAL_KEY || process.env.FAL_API_KEY;
if (!FAL_KEY) {
  console.error(
    '❌ No API key found. Set FAL_KEY (or FAL_API_KEY) and try again.\n' +
      '   PowerShell:  $env:FAL_KEY = "your_key_here"'
  );
  process.exit(1);
}
fal.config({ credentials: FAL_KEY });

const MODEL_ID = "fal-ai/flux-pro/v1.1";
const OUTPUT_DIR = "reference-images";

// --- Prompts (mirror of IMAGE_GENERATION_PROMPTS_Lego_Spaceballs.md) -----
const PROMPTS = [
  {
    name: "01_Frame1A_Office_Cubicle",
    prompt:
      "Professional Lego construction office cubicle in high detail. Yellow Lego minifigure wearing orange construction vest and yellow hard hat sitting at a tan/brown Lego brick desk with a light blue Lego monitor. Lego keyboard and small office supplies made of Lego blocks. Warm office lighting, soft shadows, clean organized workspace. Professional Lego plastic texture. Minifigure calm, working at the desk. Bright primary colors, Lego movie style. Cinematic lighting, 4K, photorealistic Lego render.",
  },
  {
    name: "02_Frame1B_DarkHelmet_Invasion",
    prompt:
      "Close-up of an absolutely massive Lego Dark Helmet filling 70% of the screen, metallic silver-gray menacing design, large red glowing visor like an angry eye, shiny Lego brick texture. Comically oversized, filling the left side. Background: Lego office cubicle blurred and small in comparison, tan Lego desk, papers flying. Space starfield behind everything (Spaceballs aesthetic). Red laser beams from visor. Theatrical, menacing but comedic scale mismatch. High quality 3D Lego render, cinematic, dramatic lighting.",
  },
  {
    name: "03_Frame1C_Colonel_Panicking",
    prompt:
      "Medium shot of a Lego minifigure army colonel in dark military uniform looking extremely panicked inside a Lego spaceship control room. Black hair piece, worried printed face, dark-gray military Lego uniform with rank insignia. Background: futuristic Lego control panels with glowing buttons, three Lego monitors showing conflicting numbers 40, 45, 38 in white text. Metallic gray Lego brick walls, fluorescent blue and white lighting. Arms raised in panic. Red visor glow in background. High detail, professional Lego render, 4K.",
  },
  {
    name: "04_Frame2A_ThreeMonitors",
    prompt:
      "Three large Lego monitor panels floating in a space starfield nebula background. Left panel green with white text 'TIMESHEET' and '40 HOURS' and a green checkmark. Center panel yellow with white text 'PAYROLL' and '45 HOURS' and a yellow question mark. Right panel orange with white text 'PROJECT TRACKER' and '38 HOURS' and an orange warning triangle. Bright red connecting arrows between panels with electrical zap effects. Pixelated Lego brick texture, high contrast, colorful primary colors. Purple/blue nebula with twinkling stars. 4K detailed Lego brick render.",
  },
  {
    name: "05_Frame2B_Lone_Starr_Confused",
    prompt:
      "Lego minifigure construction worker at desk with bewildered expression, eyes wide, mouth in an O of confusion, yellow construction outfit and hard hat. Three Lego monitor screens behind the desk showing different conflicting numbers 40, 45, 38. Red error X marks and question marks floating around. Tan Lego brick blocks with printed spreadsheet data flying everywhere. Blended spaceship and construction office setting. Chaos and disorganization energy. Warm light mixed with cool spaceship light, motion blur on flying papers. 4K cinematic Lego render.",
  },
  {
    name: "06_Frame3A_BudgetExplosion",
    prompt:
      "Large Lego budget dashboard screen center frame showing 'PROJECT: Site 42 Warehouse', 'BUDGET $500,000', 'SPENT $497,000'. Budget bar made of Lego bricks: green on left, yellow middle, red overflow on right, red bricks stacking above the bar. Semi-transparent gold and red dollar sign symbols falling like rain and fading off-screen. Dark Lego construction office, red alarm lights flashing. Deep ominous colors: dark gray, red, gold. Dramatic devastating yet comedic Lego style. 4K detailed Lego render, dramatic lighting.",
  },
  {
    name: "07_Frame3B_Lone_Starr_Defeated",
    prompt:
      "Lego minifigure construction worker at desk in a completely defeated posture, head resting in hand, slumped shoulders. Sad printed face, single blue Lego tear rolling down. A wrench prop on the desk. Lego monitor showing red budget disaster in background. A massive Lego Dark Helmet far in the background glowing red, celebrating. Dark, sad, defeated mood. Dim shadowy minor-key lighting, dark grays and dark blues. Comedic but touching defeat. 4K dramatic Lego render.",
  },
  {
    name: "08_Frame4A_BlackScreen",
    prompt:
      "Pure black background, nearly void of detail, with faint starfield silhouettes barely visible through the darkness. Mystical, ominous, anticipatory atmosphere. No characters, just deep black space. Dramatic pause aesthetic before a hero reveal. 4K.",
  },
  {
    name: "09_Frame4B_Logo_Assembly",
    prompt:
      "An abstract tech company logo materializing as Lego bricks assembling piece by piece, rings of bright colored Lego bricks (blues, teals, bright accents) clicking into place around a center brick. Shiny plastic Lego texture. A flowing Lego fabric cape attached to the logo, gently fluttering. Bright white gradient background, hope breaking through darkness. Starburst light rays emanating from the logo, glowing aura. Space starfield at edges. Triumphant, heroic, inspiring. 4K detailed Lego brick render, dramatic lighting.",
  },
  {
    name: "10_Frame4C_Dashboard_Materialized",
    prompt:
      "A clean Lego dashboard with a 2x2 grid of panels on a dark charcoal background, white text, bright green accents, Lego brick texture. Top-left panel 'ACTIVE WORKERS' with three names and green checkmarks. Top-right panel 'SYSTEMS SYNCED' showing 'Timesheet 40h, Payroll 40h, Project 40h' all with green checkmarks. Bottom-left panel 'PROJECT BUDGET' with a healthy green bar at 85% and 'ON TRACK'. Bottom-right panel 'LIVE ACTIVITY' with a scrolling feed. Multiple large green checkmarks, green glow, starfield background. Premium tech aesthetic meets Lego. 4K highly detailed professional dashboard render.",
  },
  {
    name: "11_Frame5A_Lone_Starr_Transformed",
    prompt:
      "Lego minifigure construction worker at a desk, completely transformed: confident relaxed posture leaning back, wearing cool dark Lego sunglasses, happy printed face. The Lego desk is now clean and organized, no flying papers. A laptop shows a bright green dashboard. Warm comfortable office lighting. Background: clean construction office, successful energy, other Lego minifigures celebrating, a defeated Dark Helmet far away. Confident accomplished hero energy, victory and transformation. 4K warm Lego render.",
  },
  {
    name: "12_Frame5B_Dashboard_CloseUp",
    prompt:
      "Close-up of a Lego laptop/tablet screen showing a clean green dashboard with a 2x2 grid of panels, slightly tilted natural viewing angle, glowing and readable, green checkmarks prominent. Professional tech aesthetic, high quality display, bright healthy data visualization, real-time metrics. 4K detailed screen render, tech-forward look.",
  },
  {
    name: "13_Frame5C_Benefits_SlideIn",
    prompt:
      "Clean white background with four benefit lines stacked vertically, each preceded by a large bright green checkmark: 'Defeat Data Chaos', 'Master Real-Time Data', 'Build Your Empire', 'Sync All Systems'. Blocky chunky sans-serif Lego-style font in dark gray, even professional spacing, minimalist and clear. Premium motion graphics aesthetic meets Lego authenticity. 4K, clean, readable, inspiring.",
  },
  {
    name: "14_Frame5D_CTA_Frame",
    prompt:
      "Clean professional call-to-action screen, white background, centered vertical layout. A blocky Lego-brick-style tech logo at top. Bold headline 'LEM PROCESSING GUIDE', subheading 'Free Download', a subtle divider line, then four benefits each with a green arrow: 'Defeat Data Chaos', 'Master Real-Time Data', 'Build Your Empire', 'Sync All Systems'. A URL line in brand blue. A small QR code bottom-right. High contrast, white background, dark text, green accents, blocky Lego fonts, primary colors. Professional, trustworthy, clear hierarchy. 4K landing-page quality.",
  },
];

// --- Generation ---------------------------------------------------------
async function generateImage({ name, prompt }) {
  console.log(`🎨 Generating: ${name}`);
  try {
    const result = await fal.subscribe(MODEL_ID, {
      input: {
        prompt,
        image_size: "landscape_16_9",
        output_format: "png",
      },
      logs: false,
    });

    const imageUrl = result.data?.images?.[0]?.url;
    if (!imageUrl) throw new Error("No image URL in response");

    const res = await fetch(imageUrl);
    if (!res.ok) throw new Error(`Download failed: HTTP ${res.status}`);
    const buf = Buffer.from(await res.arrayBuffer());
    const outPath = path.join(OUTPUT_DIR, `${name}.png`);
    await writeFile(outPath, buf);

    console.log(`✅ Saved: ${outPath}\n`);
    return { frame: name, url: imageUrl, prompt };
  } catch (e) {
    console.error(`❌ Failed to generate ${name}: ${e.message}\n`);
    return null;
  }
}

async function main() {
  console.log("=".repeat(60));
  console.log("🎬 Foxlogik Lego Spaceballs Video - Image Generation");
  console.log("=".repeat(60));
  console.log(`Generating ${PROMPTS.length} reference images...\n`);

  await mkdir(OUTPUT_DIR, { recursive: true });

  const results = [];
  let completed = 0;
  let failed = 0;

  for (let i = 0; i < PROMPTS.length; i++) {
    console.log(`[${i + 1}/${PROMPTS.length}] ${PROMPTS[i].name}`);
    const r = await generateImage(PROMPTS[i]);
    if (r) {
      results.push(r);
      completed++;
    } else {
      failed++;
    }
  }

  const manifest = { total: PROMPTS.length, completed, failed, images: results };
  await writeFile(
    path.join(OUTPUT_DIR, "manifest.json"),
    JSON.stringify(manifest, null, 2)
  );

  console.log("\n" + "=".repeat(60));
  console.log("🎉 Generation Complete!");
  console.log("=".repeat(60));
  console.log(`✅ Generated: ${completed}/${PROMPTS.length}`);
  console.log(`❌ Failed: ${failed}/${PROMPTS.length}`);
  console.log(`📁 Output directory: ${OUTPUT_DIR}`);
}

main();
