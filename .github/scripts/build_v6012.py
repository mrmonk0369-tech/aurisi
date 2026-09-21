#!/usr/bin/env python3
# AURISI v60.12: Light Grey -> MEDIUM GREY per owner feedback.
# True medium-grey palette (between the old light grey and dark),
# dark slate accent, dark text for contrast. Theme key stays "grey".
# Transport note: backslashes are written as ~B~ and unwrapped by Q().
# Base: AURISI.html v60.11. Idempotent: no-op if already v60.12.
import sys, io

def Q(s):
    return s.replace("~B~", chr(92))

BASE = sys.argv[1] if len(sys.argv) > 1 else "AURISI.html"
OUT = sys.argv[2] if len(sys.argv) > 2 else "AURISI_new.html"

h = io.open(BASE, encoding="utf-8").read()

if 'APP_VERSION="60.12"' in h:
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("already v60.12 - no-op")
    sys.exit(0)

assert 'APP_VERSION="60.11"' in h, "base must be v60.11"

# P1: grey palette -> medium grey
F1 = Q('''[data-ai-theme="grey"]{
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
[data-ai-theme="grey"] .screen{background-image:radial-gradient(rgba(100,116,139,.06) 1px,transparent 1px);background-size:12px 12px}''')
R1 = Q('''[data-ai-theme="grey"]{
  --bg:#B7BCC4; --surface:#C2C7CE; --surface2:#A8AEB8; --text:#262A31; --muted:#5F6672;
  --line:#9BA1AB; --accent:#4A5462; --accent2:#3A4350; --danger:#B23E38;
  --ai-bg:#B7BCC4; --ai-surface:#C2C7CE; --ai-text:#262A31; --ai-muted:#5F6672;
  --ai-border:#9BA1AB; --ai-card-bg:#A8AEB8; --ai-accent:#4A5462; --ai-accent2:#3A4350;
  --ai-user-bg:#4A5462; --ai-user-text:#ffffff;
  --ai-code-bg:#26282D; --ai-code-head:#202226; --ai-code-text:#E8EAEE; --ai-code-border:#3A3D44;
  --tk-comment:#8A919C; --tk-keyword:#9FB6D9; --tk-string:#8fa67c;
  --tk-number:#c08a4a; --tk-func:#B7BCC4; --tk-attr:#b08968; --tk-built:#96a891;
  --on-accent:#ffffff;
}
[data-ai-theme="grey"] .screen{background-image:radial-gradient(rgba(255,255,255,.18) 1px,transparent 1px);background-size:12px 12px}''')
assert h.count(F1) == 1, "P1 anchor not found"
h = h.replace(F1, R1)

# P2: THEMES label + meta
F2 = Q('grey:{label:"~B~u{2601} Light Grey",meta:"#F2F3F5"}')
R2 = Q('grey:{label:"~B~u{1F32B} Medium Grey",meta:"#B7BCC4"}')
assert h.count(F2) == 1, "P2 anchor not found"
h = h.replace(F2, R2)

# P3: theme popup row
F3 = Q('''<div class="theme-pop-row" data-th="grey" onclick="themePick('grey')"><span class="th-cap" style="background:linear-gradient(to right,#F2F3F5,#64748B)"></span>☁️ Light Grey</div>''')
R3 = Q('''<div class="theme-pop-row" data-th="grey" onclick="themePick('grey')"><span class="th-cap" style="background:linear-gradient(to right,#B7BCC4,#4A5462)"></span>🌫️ Medium Grey</div>''')
assert h.count(F3) == 1, "P3 anchor not found"
h = h.replace(F3, R3)

# P4: settings tile
F4 = Q('''<button class="theme-tile" data-th="grey" onclick="themePick('grey')"><span class="th-prev" style="background:linear-gradient(135deg,#F2F3F5 55%,#64748B)"></span>Light Grey</button>''')
R4 = Q('''<button class="theme-tile" data-th="grey" onclick="themePick('grey')"><span class="th-prev" style="background:linear-gradient(135deg,#B7BCC4 55%,#4A5462)"></span>Medium Grey</button>''')
assert h.count(F4) == 1, "P4 anchor not found"
h = h.replace(F4, R4)

# P5: AI system prompt theme list
F5 = 'Themes: Lofi Coffee, Light Grey, Peaches, Pure Black.'
R5 = 'Themes: Lofi Coffee, Medium Grey, Peaches, Pure Black.'
assert h.count(F5) == 1, "P5 anchor not found"
h = h.replace(F5, R5)

F6 = 'var APP_VERSION="60.11"'
R6 = 'var APP_VERSION="60.12"'
assert h.count(F6) == 1
h = h.replace(F6, R6)

io.open(OUT, "w", encoding="utf-8").write(h)
print("applied Medium Grey, size: %d bytes" % len(h.encode("utf-8")))
