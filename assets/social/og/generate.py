import subprocess, html, os

OUT_DIR = "/home/fadi/projects/fadi-labib/assets/social/og"
os.makedirs(OUT_DIR, exist_ok=True)

# repo, description (no '&'), language label
repos = [
    ("ethobot", "Nature-inspired path planning and swarm coordination", "C++"),
    ("bennu", "DIY photogrammetry drone · PX4 + ROS 2 + OpenDroneMap", "Python"),
    ("loupe", "Auditor-credible AI lenses for code review", "Python"),
    ("ellmo", "Edge LLM infrastructure for on-device inference", "Python"),
    ("nanonav", "Neural pathfinding that imitates A*", "Python"),
    ("genstart-wolfenstein", "AI-generated Wolfenstein-style raycaster", "JavaScript"),
]

TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="640" viewBox="0 0 1280 640">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a1628"/><stop offset="55%" stop-color="#0f1d35"/><stop offset="100%" stop-color="#162a4a"/>
    </linearGradient>
    <radialGradient id="glow" cx="80%" cy="30%" r="62%">
      <stop offset="0%" stop-color="#3b7dd8" stop-opacity="0.30"/><stop offset="70%" stop-color="#3b7dd8" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M48 0 H0 V48" fill="none" stroke="#3b7dd8" stroke-width="1" opacity="0.05"/>
    </pattern>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#3b7dd8"/><stop offset="100%" stop-color="#93c5fd"/>
    </linearGradient>
  </defs>

  <rect width="1280" height="640" fill="url(#bg)"/>
  <rect width="1280" height="640" fill="url(#grid)"/>
  <rect width="1280" height="640" fill="url(#glow)"/>

  <!-- edge-to-cloud motif echo (lower right, faint) -->
  <g>
    <line x1="876" y1="486" x2="1132" y2="486" stroke="#3b7dd8" stroke-width="2" stroke-dasharray="2 7" opacity="0.4"/>
    <rect x="868" y="478" width="16" height="16" rx="3" fill="#3b7dd8" stroke="#93c5fd" stroke-width="1"/>
    <circle cx="1004" cy="486" r="6" fill="#3b7dd8" stroke="#93c5fd" stroke-width="1"/>
    <circle cx="1132" cy="486" r="8" fill="#3b7dd8" stroke="#93c5fd" stroke-width="1"/>
  </g>

  <!-- left accent bar -->
  <rect x="100" y="208" width="8" height="226" rx="4" fill="url(#accent)"/>

  <!-- eyebrow: name -->
  <text x="134" y="230" font-family="'Inter','DejaVu Sans',sans-serif" font-size="26" font-weight="600" letter-spacing="6" fill="#6b9be3">FADI LABIB</text>

  <!-- repo name -->
  <text x="132" y="{NAME_Y}" font-family="'Inter','DejaVu Sans',sans-serif" font-size="{NAME_SIZE}" font-weight="700" fill="#ffffff">{NAME}</text>

  <!-- description -->
  <text x="134" y="420" font-family="'Inter','DejaVu Sans',sans-serif" font-size="34" font-weight="500" fill="#dbeafe">{DESC}</text>

  <!-- language pill -->
  <g transform="translate(134, 462)">
    <rect x="0" y="0" width="{PILL_W}" height="46" rx="23" fill="#0f1d35" stroke="#3b7dd8" stroke-width="1.5"/>
    <circle cx="27" cy="23" r="6" fill="url(#accent)"/>
    <text x="46" y="31" font-family="'Inter','DejaVu Sans',sans-serif" font-size="22" font-weight="600" fill="#93c5fd">{LANG}</text>
  </g>

  <!-- footer -->
  <text x="1148" y="560" text-anchor="end" font-family="'Inter','DejaVu Sans',sans-serif" font-size="24" font-weight="500" fill="#6b9be3">fadilabib.com</text>
</svg>
'''

for name, desc, lang in repos:
    n = len(name)
    name_size = 96 if n <= 10 else (76 if n <= 16 else 60)
    name_y = 348 if name_size == 96 else (344 if name_size == 76 else 340)
    pill_w = 46 + len(lang) * 12 + 28
    svg = (TEMPLATE
        .replace("{NAME}", html.escape(name))
        .replace("{DESC}", html.escape(desc))
        .replace("{LANG}", html.escape(lang))
        .replace("{NAME_SIZE}", str(name_size))
        .replace("{NAME_Y}", str(name_y))
        .replace("{PILL_W}", str(pill_w)))
    svg_path = f"/tmp/social-{name}.svg"
    with open(svg_path, "w") as f:
        f.write(svg)
    png_path = f"{OUT_DIR}/{name}.png"
    subprocess.run(["inkscape", svg_path, "-o", png_path, "-w", "1280", "-h", "640"],
                   stderr=subprocess.DEVNULL)
    print("rendered", png_path)
