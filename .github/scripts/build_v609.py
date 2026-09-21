#!/usr/bin/env python3
# AURISI v60.9: Exactly 4 themes.
#   1) Lofi Coffee (unchanged)
#   2) Dark Roast — lofi coffee jaisi hi, lekin thodi aur dark (new)
#   3) Peaches Dark — dark peach palette (new)
#   4) Pure Black #000000 (unchanged)
# Old themes (tangerine, peach, lavender, cyber, crunch) removed from the
# picker; their CSS stays (harmless dead code); saved old themes fall back
# to Pure Black via the boot validator.
# Transport note: backslashes are written as ~B~ and unwrapped by Q().
# Base: AURISI.html v60.8. Idempotent: no-op if already v60.9.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.9"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.9 - no-op")
    sys.exit(0)

assert 'APP_VERSION="60.8"' in h, "base must be v60.8"

# P1: CSS — new theme variable blocks + dark element overrides,
# inserted right after the lofi .screen rule.
F1 = Q('''[data-ai-theme="lofi"] .screen{background-image:radial-gradient(rgba(120,90,60,.075) 1px,transparent 1px);background-size:12px 12px}''')
R1 = Q('''[data-ai-theme="lofi"] .screen{background-image:radial-gradient(rgba(120,90,60,.075) 1px,transparent 1px);background-size:12px 12px}
[data-ai-theme="lofidark"]{
  --bg:#241C16; --surface:#2E241C; --surface2:#3A2D23; --text:#EFE4D6; --muted:#A2917F;
  --line:#453628; --accent:#C08A5A; --accent2:#9C8261; --danger:#C0564F;
  --ai-bg:#241C16; --ai-surface:#2E241C; --ai-text:#EFE4D6; --ai-muted:#A2917F;
  --ai-border:#453628; --ai-card-bg:#3A2D23; --ai-accent:#C08A5A; --ai-accent2:#9C8261;
  --ai-user-bg:#6F7D68; --ai-user-text:#ffffff;
  --ai-code-bg:#1D1610; --ai-code-head:#181209; --ai-code-text:#f2e8de; --ai-code-border:#3B2D21;
  --tk-comment:#8a7a68; --tk-keyword:#C08A5A; --tk-string:#8fa67c;
  --tk-number:#D09A62; --tk-func:#B39A78; --tk-attr:#b08968; --tk-built:#96a891;
  --on-accent:#1c130b;
}
[data-ai-theme="lofidark"] .screen{background-image:radial-gradient(rgba(255,235,210,.05) 1px,transparent 1px);background-size:12px 12px}
[data-ai-theme="peachdark"]{
  --bg:#1E1210; --surface:#2A1A16; --surface2:#37221C; --text:#FBEDE6; --muted:#C0A398;
  --line:#402620; --accent:#FF8A65; --accent2:#FF6A3D; --danger:#FF5A4E;
  --ai-bg:#1E1210; --ai-surface:#2A1A16; --ai-text:#FBEDE6; --ai-muted:#C0A398;
  --ai-border:#402620; --ai-card-bg:#37221C; --ai-accent:#FF8A65; --ai-accent2:#FF6A3D;
  --ai-user-bg:#FF6A3D; --ai-user-text:#ffffff;
  --ai-code-bg:#1A100D; --ai-code-head:#150C0A; --ai-code-text:#f8ece6; --ai-code-border:#3B221C;
  --tk-comment:#9a8078; --tk-keyword:#FF8A65; --tk-string:#8fa67c;
  --tk-number:#FFB300; --tk-func:#FFA07A; --tk-attr:#d98a66; --tk-built:#96a891;
  --on-accent:#ffffff;
}
[data-ai-theme="lofidark"] body,[data-ai-theme="peachdark"] body,[data-ai-theme="lofidark"] #app,[data-ai-theme="peachdark"] #app{background:var(--bg);color:var(--text)}
[data-ai-theme="lofidark"] .topbar,[data-ai-theme="peachdark"] .topbar{background:transparent;border-bottom-color:transparent}
[data-ai-theme="lofidark"] .wsrail,[data-ai-theme="peachdark"] .wsrail{border-right-color:rgba(255,255,255,.07);box-shadow:2px 0 14px rgba(0,0,0,.45)}
[data-ai-theme="lofidark"] .wsbot,[data-ai-theme="peachdark"] .wsbot{border-top-color:rgba(255,255,255,.08);box-shadow:0 -6px 20px rgba(0,0,0,.4)}
[data-ai-theme="lofidark"] .ws-card,[data-ai-theme="peachdark"] .ws-card{border-color:rgba(255,255,255,.08);box-shadow:0 8px 24px rgba(0,0,0,.35)}
[data-ai-theme="lofidark"] .qa-btn,[data-ai-theme="peachdark"] .qa-btn,[data-ai-theme="lofidark"] .ch-btn,[data-ai-theme="peachdark"] .ch-btn{border-color:rgba(255,255,255,.11)}
[data-ai-theme="lofidark"] .qa-btn:hover,[data-ai-theme="peachdark"] .qa-btn:hover{box-shadow:0 6px 14px rgba(0,0,0,.4)}
[data-ai-theme="lofidark"] .ts-drop,[data-ai-theme="peachdark"] .ts-drop{box-shadow:0 14px 34px rgba(0,0,0,.55)}
[data-ai-theme="lofidark"] .modal,[data-ai-theme="peachdark"] .modal{box-shadow:0 30px 80px rgba(0,0,0,.6)}
[data-ai-theme="lofidark"] .exam-pal,[data-ai-theme="peachdark"] .exam-pal,[data-ai-theme="lofidark"] .exam-top,[data-ai-theme="peachdark"] .exam-top{border-color:rgba(255,255,255,.08)!important}
[data-ai-theme="lofidark"] .studio-head,[data-ai-theme="peachdark"] .studio-head{border-bottom-color:rgba(255,255,255,.07)}
[data-ai-theme="lofidark"] #studioPanel,[data-ai-theme="peachdark"] #studioPanel{border-right-color:rgba(255,255,255,.08);box-shadow:8px 0 30px rgba(0,0,0,.5)}
[data-ai-theme="lofidark"] .ws-hero,[data-ai-theme="peachdark"] .ws-hero{background:linear-gradient(135deg,rgba(255,255,255,.07),rgba(255,255,255,.02));border-color:rgba(255,255,255,.12)}
[data-ai-theme="lofidark"] .file-btn,[data-ai-theme="peachdark"] .file-btn{background:var(--surface2)}
[data-ai-theme="lofidark"] .stab-btn.on,[data-ai-theme="peachdark"] .stab-btn.on{background:linear-gradient(135deg,rgba(255,255,255,.1),rgba(255,255,255,.03));border-color:rgba(255,255,255,.16);color:var(--accent)}
[data-ai-theme="lofidark"] .agent-card,[data-ai-theme="peachdark"] .agent-card{border-color:rgba(255,255,255,.11);box-shadow:0 8px 22px rgba(0,0,0,.4)}
[data-ai-theme="lofidark"] .snap-stage,[data-ai-theme="peachdark"] .snap-stage{border-color:rgba(255,255,255,.08)}
[data-ai-theme="lofidark"] .snap-item.on,[data-ai-theme="peachdark"] .snap-item.on{border-color:rgba(255,255,255,.16)}
[data-ai-theme="lofidark"] mark.amk-imp,[data-ai-theme="peachdark"] mark.amk-imp{background:rgba(255,213,0,.3)}
[data-ai-theme="lofidark"] mark.amk-def,[data-ai-theme="peachdark"] mark.amk-def{background:rgba(0,230,118,.22)}
[data-ai-theme="lofidark"] mark.amk-fact,[data-ai-theme="peachdark"] mark.amk-fact{background:rgba(64,156,255,.22)}
[data-ai-theme="lofidark"] mark.amk-cause,[data-ai-theme="peachdark"] mark.amk-cause{background:rgba(255,105,180,.33)}''')
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: THEMES JS object — exactly 4 entries
F2 = Q('const THEMES={pureblack:{label:"~B~u{2B1B} Pure Black",meta:"#000000"},tangerine:{label:"~B~u{1F305} Tangerine Sky",meta:"#000000"},peach:{label:"~B~u{1F351} Peach Horizon",meta:"#fff7f0"},lavender:{label:"~B~u{1F49C} Lavender",meta:"#f7f5fc"},cyber:{label:"~B~u{1F52E} Cyberpunk",meta:"#0B0C10"},lofi:{label:"~B~u{2615} Lofi Coffee",meta:"#F4EAE1"},crunch:{label:"~B~u{1F6A8} Exam Crunch",meta:"#111111"}};')
R2 = Q('const THEMES={lofi:{label:"~B~u{2615} Lofi Coffee",meta:"#F4EAE1"},lofidark:{label:"~B~u{2615} Dark Roast",meta:"#241C16"},peachdark:{label:"~B~u{1F351} Peaches Dark",meta:"#1E1210"},pureblack:{label:"~B~u{2B1B} Pure Black",meta:"#000000"}};')
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: theme popup rows — exactly 4
F3 = Q('''    <div class="theme-pop-row" data-th="pureblack" onclick="themePick('pureblack')"><span class="th-cap" style="background:linear-gradient(to right,#000000,#f2f2f2)"></span>⬛ Pure Black</div>
    <div class="theme-pop-row" data-th="tangerine" onclick="themePick('tangerine')"><span class="th-cap" style="background:linear-gradient(to right,#000000,#ff8c42)"></span>🌅 Tangerine Sky</div>
    <div class="theme-pop-row" data-th="peach" onclick="themePick('peach')"><span class="th-cap" style="background:linear-gradient(to right,#fff7f0,#ff6a3d)"></span>🍑 Peach Horizon</div>
    <div class="theme-pop-row" data-th="lavender" onclick="themePick('lavender')"><span class="th-cap" style="background:linear-gradient(to right,#f7f5fc,#8b5cf6)"></span>💜 Lavender</div>
    <div class="theme-pop-row" data-th="cyber" onclick="themePick('cyber')"><span class="th-cap" style="background:linear-gradient(to right,#0B0C10,#66FCF1)"></span>🔮 Cyberpunk</div>
    <div class="theme-pop-row" data-th="lofi" onclick="themePick('lofi')"><span class="th-cap" style="background:linear-gradient(to right,#F4EAE1,#8E9A86)"></span>☕ Lofi Coffee</div>
    <div class="theme-pop-row" data-th="crunch" onclick="themePick('crunch')"><span class="th-cap" style="background:linear-gradient(to right,#111111,#FF3333)"></span>🚨 Exam Crunch</div>''')
R3 = Q('''    <div class="theme-pop-row" data-th="lofi" onclick="themePick('lofi')"><span class="th-cap" style="background:linear-gradient(to right,#F4EAE1,#8E9A86)"></span>☕ Lofi Coffee</div>
    <div class="theme-pop-row" data-th="lofidark" onclick="themePick('lofidark')"><span class="th-cap" style="background:linear-gradient(to right,#241C16,#C08A5A)"></span>☕ Dark Roast</div>
    <div class="theme-pop-row" data-th="peachdark" onclick="themePick('peachdark')"><span class="th-cap" style="background:linear-gradient(to right,#1E1210,#FF6A3D)"></span>🍑 Peaches Dark</div>
    <div class="theme-pop-row" data-th="pureblack" onclick="themePick('pureblack')"><span class="th-cap" style="background:linear-gradient(to right,#000000,#f2f2f2)"></span>⬛ Pure Black</div>''')
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: settings theme tiles — exactly 4
F4 = Q('''          <button class="theme-tile" data-th="pureblack" onclick="themePick('pureblack')"><span class="th-prev" style="background:linear-gradient(135deg,#000000 55%,#f2f2f2)"></span>Pure Black</button>
          <button class="theme-tile" data-th="tangerine" onclick="themePick('tangerine')"><span class="th-prev" style="background:linear-gradient(135deg,#000000 55%,#ff8c42)"></span>Tangerine Sky</button>
          <button class="theme-tile" data-th="peach" onclick="themePick('peach')"><span class="th-prev" style="background:linear-gradient(135deg,#fff7f0 55%,#ff6a3d)"></span>Peach Horizon</button>
          <button class="theme-tile" data-th="lavender" onclick="themePick('lavender')"><span class="th-prev" style="background:linear-gradient(135deg,#f7f5fc 55%,#8b5cf6)"></span>Lavender</button>
          <button class="theme-tile" data-th="cyber" onclick="themePick('cyber')"><span class="th-prev" style="background:linear-gradient(135deg,#0B0C10 55%,#66FCF1)"></span>Cyberpunk</button>
          <button class="theme-tile" data-th="lofi" onclick="themePick('lofi')"><span class="th-prev" style="background:linear-gradient(135deg,#F4EAE1 55%,#8E9A86)"></span>Lofi Coffee</button>
          <button class="theme-tile" data-th="crunch" onclick="themePick('crunch')"><span class="th-prev" style="background:linear-gradient(135deg,#111111 55%,#FF3333)"></span>Exam Crunch</button>''')
R4 = Q('''          <button class="theme-tile" data-th="lofi" onclick="themePick('lofi')"><span class="th-prev" style="background:linear-gradient(135deg,#F4EAE1 55%,#8E9A86)"></span>Lofi Coffee</button>
          <button class="theme-tile" data-th="lofidark" onclick="themePick('lofidark')"><span class="th-prev" style="background:linear-gradient(135deg,#241C16 55%,#C08A5A)"></span>Dark Roast</button>
          <button class="theme-tile" data-th="peachdark" onclick="themePick('peachdark')"><span class="th-prev" style="background:linear-gradient(135deg,#1E1210 55%,#FF6A3D)"></span>Peaches Dark</button>
          <button class="theme-tile" data-th="pureblack" onclick="themePick('pureblack')"><span class="th-prev" style="background:linear-gradient(135deg,#000000 55%,#f2f2f2)"></span>Pure Black</button>''')
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

# P5: toggleTheme cycle — 4 themes
F5 = Q('''function toggleTheme(){
  const cur=localStorage.getItem(STORAGE+"theme")||"pureblack";
  const order=["pureblack","tangerine","peach","lavender"];
  const next=order[(order.indexOf(cur)+1)%order.length];
  applyTheme(next);toast(THEMES[next].label);
}''')
R5 = Q('''function toggleTheme(){
  const cur=localStorage.getItem(STORAGE+"theme")||"pureblack";
  const order=["lofi","lofidark","peachdark","pureblack"];
  const next=order[(order.indexOf(cur)+1)%order.length];
  applyTheme(next);toast(THEMES[next].label);
}''')
assert h.count(F5) == 1, "P5 anchor not found"
h = h.replace(F5, R5)

# P6: boot validator — only the 4 accepted, everything else -> Pure Black
F6 = Q('  if(t!=="pureblack"&&t!=="tangerine"&&t!=="peach"&&t!=="lavender")t="pureblack";')
R6 = Q('  if(t!=="lofi"&&t!=="lofidark"&&t!=="peachdark"&&t!=="pureblack")t="pureblack";')
assert h.count(F6) == 1, "P6 anchor not found"
h = h.replace(F6, R6)

F7 = 'var APP_VERSION="60.8"'
R7 = 'var APP_VERSION="60.9"'
assert h.count(F7) == 1
h = h.replace(F7, R7)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied 4 Themes, size: %d bytes" % len(h.encode("utf-8")))
