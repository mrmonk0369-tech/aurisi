#!/usr/bin/env python3
# AURISI v60.11: Theme retune per owner feedback.
#   Dark Roast   -> LIGHT GREY  (cloud light grey + slate accent)
#   Peaches Dark -> PEACHES (light peach + peach-orange accent)
# Old saved keys lofidark/peachdark auto-map to the new themes.
# 4 themes stay: Lofi Coffee, Light Grey, Peaches, Pure Black.
# Transport note: backslashes are written as ~B~ and unwrapped by Q().
# Base: AURISI.html v60.10. Idempotent: no-op if already v60.11.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.11"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.11 - no-op")
    sys.exit(0)

assert 'APP_VERSION="60.10"' in h, "base must be v60.10"

# P1: CSS — replace lofidark + peachdark (dark palettes + dark overrides)
# with two LIGHT palettes. Light themes need no dark element overrides
# (same as lofi/lavender, which rely on base styles).
F1 = Q('''[data-ai-theme="lofidark"]{
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
R1 = Q('''[data-ai-theme="grey"]{
  --bg:#F2F3F5; --surface:#FBFBFC; --surface2:#E8EAEE; --text:#2B2F36; --muted:#8A919C;
  --line:#DCE0E6; --accent:#64748B; --accent2:#475569; --danger:#C0564F;
  --ai-bg:#F2F3F5; --ai-surface:#FBFBFC; --ai-text:#2B2F36; --ai-muted:#8A919C;
  --ai-border:#DCE0E6; --ai-card-bg:#E8EAEE; --ai-accent:#64748B; --ai-accent2:#475569;
  --ai-user-bg:#64748B; --ai-user-text:#ffffff;
  --ai-code-bg:#26282D; --ai-code-head:#202226; --ai-code-text:#E8EAEE; --ai-code-border:#3A3D44;
  --tk-comment:#8A919C; --tk-keyword:#64748B; --tk-string:#8fa67c;
  --tk-number:#c08a4a; --tk-func:#64748B; --tk-attr:#b08968; --tk-built:#96a891;
  --on-accent:#ffffff;
}
[data-ai-theme="grey"] .screen{background-image:radial-gradient(rgba(100,116,139,.06) 1px,transparent 1px);background-size:12px 12px}
[data-ai-theme="peachlight"]{
  --bg:#FFF7F0; --surface:#FFFCF8; --surface2:#FFEDE0; --text:#4A342B; --muted:#B08D7E;
  --line:#F5DFD0; --accent:#FF6A3D; --accent2:#F0511E; --danger:#C0564F;
  --ai-bg:#FFF7F0; --ai-surface:#FFFCF8; --ai-text:#4A342B; --ai-muted:#B08D7E;
  --ai-border:#F5DFD0; --ai-card-bg:#FFEDE0; --ai-accent:#FF6A3D; --ai-accent2:#F0511E;
  --ai-user-bg:#FF6A3D; --ai-user-text:#ffffff;
  --ai-code-bg:#3A2117; --ai-code-head:#321B12; --ai-code-text:#F8ECE6; --ai-code-border:#4E2B1D;
  --tk-comment:#B08D7E; --tk-keyword:#F0511E; --tk-string:#8fa67c;
  --tk-number:#c08a4a; --tk-func:#FF6A3D; --tk-attr:#b08968; --tk-built:#96a891;
  --on-accent:#ffffff;
}
[data-ai-theme="peachlight"] .screen{background-image:radial-gradient(rgba(255,106,61,.06) 1px,transparent 1px);background-size:12px 12px}''')
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: THEMES JS object — grey + peachlight
F2 = Q('const THEMES={lofi:{label:"~B~u{2615} Lofi Coffee",meta:"#F4EAE1"},lofidark:{label:"~B~u{2615} Dark Roast",meta:"#241C16"},peachdark:{label:"~B~u{1F351} Peaches Dark",meta:"#1E1210"},pureblack:{label:"~B~u{2B1B} Pure Black",meta:"#000000"}};')
R2 = Q('const THEMES={lofi:{label:"~B~u{2615} Lofi Coffee",meta:"#F4EAE1"},grey:{label:"~B~u{2601} Light Grey",meta:"#F2F3F5"},peachlight:{label:"~B~u{1F351} Peaches",meta:"#FFF7F0"},pureblack:{label:"~B~u{2B1B} Pure Black",meta:"#000000"}};')
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: theme popup rows
F3 = Q('''    <div class="theme-pop-row" data-th="lofidark" onclick="themePick('lofidark')"><span class="th-cap" style="background:linear-gradient(to right,#241C16,#C08A5A)"></span>☕ Dark Roast</div>
    <div class="theme-pop-row" data-th="peachdark" onclick="themePick('peachdark')"><span class="th-cap" style="background:linear-gradient(to right,#1E1210,#FF6A3D)"></span>🍑 Peaches Dark</div>''')
R3 = Q('''    <div class="theme-pop-row" data-th="grey" onclick="themePick('grey')"><span class="th-cap" style="background:linear-gradient(to right,#F2F3F5,#64748B)"></span>☁️ Light Grey</div>
    <div class="theme-pop-row" data-th="peachlight" onclick="themePick('peachlight')"><span class="th-cap" style="background:linear-gradient(to right,#FFF7F0,#FF6A3D)"></span>🍑 Peaches</div>''')
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: settings tiles
F4 = Q('''          <button class="theme-tile" data-th="lofidark" onclick="themePick('lofidark')"><span class="th-prev" style="background:linear-gradient(135deg,#241C16 55%,#C08A5A)"></span>Dark Roast</button>
          <button class="theme-tile" data-th="peachdark" onclick="themePick('peachdark')"><span class="th-prev" style="background:linear-gradient(135deg,#1E1210 55%,#FF6A3D)"></span>Peaches Dark</button>''')
R4 = Q('''          <button class="theme-tile" data-th="grey" onclick="themePick('grey')"><span class="th-prev" style="background:linear-gradient(135deg,#F2F3F5 55%,#64748B)"></span>Light Grey</button>
          <button class="theme-tile" data-th="peachlight" onclick="themePick('peachlight')"><span class="th-prev" style="background:linear-gradient(135deg,#FFF7F0 55%,#FF6A3D)"></span>Peaches</button>''')
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

# P5: toggleTheme cycle
F5 = Q('  const order=["lofi","lofidark","peachdark","pureblack"];')
R5 = Q('  const order=["lofi","grey","peachlight","pureblack"];')
assert h.count(F5) == 1, "P5 anchor not found"
h = h.replace(F5, R5)

# P6: boot validator — map old keys, then validate
F6 = Q('  if(t!=="lofi"&&t!=="lofidark"&&t!=="peachdark"&&t!=="pureblack")t="pureblack";')
R6 = Q('''  if(t==="lofidark")t="grey";
  if(t==="peachdark")t="peachlight";
  if(t!=="lofi"&&t!=="grey"&&t!=="peachlight"&&t!=="pureblack")t="pureblack";''')
assert h.count(F6) == 1, "P6 anchor not found"
h = h.replace(F6, R6)

# P7: AI system prompt theme list
F7 = 'Themes: Lofi Coffee, Dark Roast, Peaches Dark, Pure Black.'
R7 = 'Themes: Lofi Coffee, Light Grey, Peaches, Pure Black.'
assert h.count(F7) == 1, "P7 anchor not found"
h = h.replace(F7, R7)

F8 = 'var APP_VERSION="60.10"'
R8 = 'var APP_VERSION="60.11"'
assert h.count(F8) == 1
h = h.replace(F8, R8)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied theme retune, size: %d bytes" % len(h.encode("utf-8")))
