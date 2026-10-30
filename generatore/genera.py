"""E ti pareva – carosello FantaVeggente nello stile approvato (slide "Difesa Juve").
Font: Big Shoulders Display (titoli, percentuale, frasi, firma), Geist (testi), Geist Mono (etichette).
Uso: python3 genera.py giornate/gN.json  -> out/ig (1080x1350) e out/tiktok (1080x1920)"""
import json, sys, pathlib, base64, random, math, re
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
import os
NOSTARS = os.environ.get("NOSTARS") == "1"
FS = ROOT / "node_modules/@fontsource"

def inline_css(pkg, weights, family):
    out = []
    for w in weights:
        css = (FS / pkg / f"{w}.css").read_text()
        for block in re.findall(r"@font-face\s*{[^}]*}", css):
            if "vietnamese" in block or "cyrillic" in block or "greek" in block:
                continue
            f = re.search(r"url\(\./files/([^)]+\.woff2)\)", block).group(1)
            data = base64.b64encode((FS / pkg / "files" / f).read_bytes()).decode()
            rng = re.search(r"unicode-range:([^;]+);", block)
            out.append(f"@font-face{{font-family:'{family}';font-weight:{w};src:url(data:font/woff2;base64,{data}) format('woff2');"
                       + (f"unicode-range:{rng.group(1)};" if rng else "") + "}")
    return "".join(out)

FONTS = (inline_css("big-shoulders-display", [700, 800, 900], "BS")
         + inline_css("geist", [400, 500, 600], "Geist")
         + inline_css("geist-mono", [500], "GM"))
b64 = lambda p: "data:image/png;base64," + base64.b64encode((ROOT / p).read_bytes()).decode()
BALL = b64("ball.png")          # vecchia sfera (non più usata)
LOGO = b64("logo_tight.png")    # logo ufficiale scontornato (copertina, chiusura, footer)
BALL_R = b64("ball_round.png")  # pallone-sfera senza piedistallo (griglia)

WHITE, GOLD, SUB, MUTED, RED, DOT = "#F4F1E8", "#F5B23E", "#C6CBEA", "#8E96C8", "#F06A5B", "#212A5E"

def stars(w, h, n, seed=11):
    r = random.Random(seed); out = []
    for _ in range(n):
        x, y = r.uniform(0, w), r.uniform(0, h)
        big = r.random() < .08
        s = r.uniform(1.6, 2.6) if big else r.choice([.6, .8, 1, 1.1, 1.3])
        o = r.uniform(.35, .75) if big else r.uniform(.12, .55)
        blur = " filter='url(#bl)'" if big else ""
        out.append(f"<circle cx='{x:.0f}' cy='{y:.0f}' r='{s:.1f}' fill='#DCE2FF' fill-opacity='{o:.2f}'{blur}/>")
    return (f"<svg class=sky viewBox='0 0 {w} {h}'><defs><filter id=bl><feGaussianBlur stdDeviation='.8'/></filter></defs>"
            f"{''.join(out)}</svg>")

CSS = f"""*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:var(--h);color:{WHITE};font-family:Geist,sans-serif;overflow:hidden;position:relative;
background:
 radial-gradient(45% 16% at 50% 100%,rgba(70,50,40,.55),transparent 75%),
 radial-gradient(60% 40% at 100% 0%,rgba(40,55,140,.35),transparent 70%),
 linear-gradient(180deg,#101745 0%,#0D1340 25%,#0B1033 55%,#0A0E2E 80%,#090D29 100%)}}
.sky{{position:absolute;inset:0;width:100%;height:100%}}
.a{{position:absolute;left:80px;right:80px;z-index:1}}
.top{{display:flex;justify-content:space-between;font-family:GM;font-weight:500;font-size:28px;line-height:1;letter-spacing:.13em;text-transform:uppercase;color:{GOLD}}}
.top span+span{{color:{MUTED};letter-spacing:.09em}}
.chip{{display:inline-flex;align-items:center;height:66px;padding:0 30px 0 31px;border-radius:999px;background:#1A1F47;border:1.5px solid #2A3368;
font-family:GM;font-weight:500;font-size:28px;letter-spacing:.03em;color:{WHITE}}}
.flow{{display:flex;flex-direction:column}}
.name{{font-family:BS;font-weight:900;font-size:143.5px;line-height:1;letter-spacing:.8px;text-transform:uppercase;white-space:nowrap}}
.name b{{color:{GOLD};font-weight:900}}
.what{{font-family:BS;font-weight:700;font-size:39px;line-height:1.15;letter-spacing:.3px;color:{SUB}}}
.pctrow{{display:flex;align-items:center}}
.pct{{font-family:BS;font-weight:900;font-size:218px;line-height:1;padding:0 8px 0 4px;margin-left:-4px;
background:linear-gradient(180deg,#FFD582 0%,#F9C25F 30%,#F3AE3B 55%,#E99B2C 78%,#E19123 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
filter:drop-shadow(0 0 22px rgba(245,170,60,.32))}}
.pl{{display:flex;flex-direction:column;margin-left:22px;margin-top:60px}}
.pl b{{font-family:BS;font-weight:800;font-size:44px;line-height:1;text-transform:uppercase;white-space:nowrap;color:{WHITE}}}
.pl span{{font-family:GM;font-weight:500;font-size:31px;line-height:1;color:{MUTED};margin-top:14px}}
.field{{position:relative}}
.field svg{{display:block;overflow:visible}}
.card{{border-radius:24px;border:2px solid rgba(245,178,62,.45);background:linear-gradient(180deg,#1A1A33 0%,#15183A 50%,#10153D 100%);
box-shadow:0 0 26px rgba(245,178,62,.10);padding:0 34px}}
.k{{font-family:GM;font-weight:500;font-size:24px;line-height:1;letter-spacing:.135em;text-transform:uppercase;color:{GOLD}}}
.det{{font-family:Geist;font-weight:500;font-size:37.5px;line-height:1.3;color:{WHITE}}}
.det b{{color:{GOLD};font-weight:500}}.det i{{font-style:normal;color:{RED};font-weight:500}}
.kick{{font-family:BS;font-weight:800;font-size:46px;line-height:1.1;color:{GOLD}}}
.foot{{display:flex;justify-content:space-between;align-items:flex-end}}
.wm{{font-family:BS;font-weight:900;font-size:40px;line-height:1;letter-spacing:.7px;text-transform:uppercase;white-space:nowrap;color:{WHITE}}}
.wm b{{color:{GOLD};font-weight:900}}
.note{{font-family:Geist;font-weight:500;font-size:20.4px;line-height:1;color:{MUTED};text-align:right}}
.body{{font-family:Geist;font-weight:500;font-size:37px;line-height:1.35;color:{SUB}}}
.pill{{display:inline-flex;align-items:center;height:62px;padding:0 28px;border-radius:999px;border:2px solid rgba(245,178,62,.45);background:rgba(245,178,62,.06);
font-family:GM;font-weight:500;font-size:26px;letter-spacing:.13em;text-transform:uppercase;color:{GOLD}}}
"""
NEON = f"""
.card{{border:2px solid rgba(255,196,92,.9);box-shadow:0 0 6px rgba(255,190,80,.55),0 0 22px rgba(245,170,60,.32),inset 0 0 22px rgba(245,170,60,.10)}}
.chip{{border:1.5px solid rgba(125,150,255,.85);box-shadow:0 0 8px rgba(110,140,255,.55),0 0 20px rgba(90,120,255,.25),inset 0 0 10px rgba(110,140,255,.18)}}
.pct{{filter:drop-shadow(0 0 6px rgba(255,196,96,.75)) drop-shadow(0 0 26px rgba(245,160,50,.45))}}
.name b{{text-shadow:0 0 8px rgba(255,190,80,.55),0 0 26px rgba(245,170,60,.35)}}
.kick{{text-shadow:0 0 10px rgba(245,178,62,.45)}}
.wm b{{text-shadow:0 0 10px rgba(245,178,62,.5)}}
.top span:first-child{{text-shadow:0 0 10px rgba(245,178,62,.45)}}
.pill{{border-color:rgba(255,196,92,.9);box-shadow:0 0 8px rgba(255,190,80,.5),0 0 20px rgba(245,170,60,.25)}}
"""

def neon_deco(h, foot, right=80, arc=(1200, 330, 250, 300)):
    """Tocchi neon fissi: due archi blu in alto a destra e una linea d'oro sopra la firma."""
    ly = h - foot - 41 - 30
    return (f"<svg style='position:absolute;inset:0;width:1080px;height:{h}px;z-index:0' viewBox='0 0 1080 {h}'>"
            "<defs><filter id=ng x='-50%' y='-50%' width='200%' height='200%'><feGaussianBlur stdDeviation='4' result='b'/>"
            "<feMerge><feMergeNode in='b'/><feMergeNode in='SourceGraphic'/></feMerge></filter>"
            f"<linearGradient id=nl gradientUnits='userSpaceOnUse' x1='80' x2='{1080 - right}' y1='0' y2='0'><stop offset='0' stop-color='#F5B23E' stop-opacity='0'/>"
            "<stop offset='.25' stop-color='#FFC45C' stop-opacity='.9'/><stop offset='.75' stop-color='#FFC45C' stop-opacity='.9'/>"
            "<stop offset='1' stop-color='#F5B23E' stop-opacity='0'/></linearGradient></defs>"
            "<g fill='none' filter='url(#ng)'>"
            f"<circle cx='{arc[0]}' cy='{arc[1]}' r='{arc[2]}' stroke='#7D96FF' stroke-opacity='.55' stroke-width='2'/>"
            f"<circle cx='{arc[0]}' cy='{arc[1]}' r='{arc[3]}' stroke='#7D96FF' stroke-opacity='.22' stroke-width='1.5' stroke-dasharray='2 10'/>"
            f"<line x1='80' x2='{1080 - right}' y1='{ly}' y2='{ly}' stroke='url(#nl)' stroke-width='2'/></g></svg>")

WM = "<div class=wm>Fanta<b>Veggente</b></div>"
WM_LOGO = (f"<div class=wm style=\"display:flex;align-items:flex-end;gap:14px\"><img src=\"{LOGO}\" style=\"height:62px;margin-bottom:-12px;"
           "filter:drop-shadow(0 0 8px rgba(245,170,60,.45))\"><span>Fanta<b>Veggente</b></span></div>")

def md(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return re.sub(r"!!(.+?)!!", r"<i>\1</i>", t)

def name_html(n):
    p = n.split(" ")
    return n if len(p) == 1 else " ".join(p[:-1]) + f" <b>{p[-1]}</b>"

def dots(n, seed, W=920):
    """Griglia come nel riferimento: 15 colonne da 44px, passo 60. Per N grandi i puntini si rimpiccioliscono
    nella stessa area (920 x ~104)."""
    r = random.Random(seed)
    if n <= 45:
        cols, d, step = int((W + 16) // 60), 44, 60
    else:
        area_h = 104                                   # stessa altezza della griglia da 1 su 25
        cols = max(15, round(math.sqrt(n * W / area_h)))
        while True:
            step = (W + (W / cols) * .27) / cols
            d = step * .73
            if math.ceil(n / cols) * step - (step - d) <= area_h + .5:
                break
            cols += 1
    rows = math.ceil(n / cols)
    win = r.randrange(min(n, cols * min(rows, 2)) if n <= 45 else n)
    out = []
    for i in range(n):
        if i == win:
            continue
        x, y = (i % cols) * step + d / 2, (i // cols) * step + d / 2
        out.append(f"<circle cx='{x:.2f}' cy='{y:.2f}' r='{d/2:.2f}' fill='{DOT}'/>")
    x, y = (win % cols) * step + d / 2, (win // cols) * step + d / 2
    bs = max(d, 30)
    glow = (f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{bs*0.95:.1f}' fill='url(#gl)'/>")
    ball = f"<image href='{BALL_R}' x='{x-bs/2:.1f}' y='{y-bs/2:.1f}' width='{bs:.1f}' height='{bs:.1f}'/>"
    H = rows * step - (step - d)
    return (f"<svg width='{W}' height='{H:.1f}' viewBox='0 0 {W} {H:.1f}'><defs><radialGradient id=gl>"
            f"<stop offset='.45' stop-color='#F5A93A' stop-opacity='.55'/><stop offset='1' stop-color='#F5A93A' stop-opacity='0'/></radialGradient></defs>"
            f"{''.join(out)}{glow}{ball}</svg>")

def frame(h):
    """Coordinate delle fasce fisse. IG = misure del riferimento; TikTok = stesse misure spostate,
    con margini liberi sotto (380) e a destra (160)."""
    if h <= 1350:
        return dict(top=83, chip=149, flow=270, foot=74, right=80)
    return dict(top=193, chip=259, flow=380, foot=380, right=160)

def page(inner, h, arc=(1200, 330, 250, 300)):
    f = frame(h)
    return (f"<!doctype html><html><head><meta charset=utf-8><style>{FONTS}{CSS}{NEON}.a{{right:{f['right']}px}}" + (".top span:first-child{letter-spacing:.09em}.foot .note{font-size:18px;white-space:nowrap}" if h > 1500 else "") + f"</style></head>"
            f"<body style='--h:{h}px'>{"" if NOSTARS else stars(1080, h, 330 if h > 1500 else 260)}{neon_deco(h, f['foot'], f['right'], arc)}{inner}</body></html>")

def progress_row(evs, cur, tall):
    """Barra di avanzamento: le percentuali di tutti gli eventi, accesa solo quella della slide corrente."""
    out = []
    for k, e in enumerate(evs):
        on = k == cur
        style = (f"display:inline-flex;align-items:center;height:{50 if tall else 54}px;padding:0 {12 if tall else 14}px;margin-right:{8 if tall else 10}px;"
                 f"border-radius:14px;font-family:BS;font-weight:900;font-size:{34 if tall else 38}px;color:{GOLD};background:rgba(14,20,62,.78);")
        if on:
            style += ("border:2px solid rgba(255,200,100,1);box-shadow:0 0 8px rgba(255,190,80,.75),0 0 24px rgba(245,170,60,.45),inset 0 0 12px rgba(245,170,60,.18);"
                      "text-shadow:0 0 10px rgba(255,190,80,.8)")
        else:
            style += "border:1.5px solid rgba(245,178,62,.55);opacity:.3"
        out.append(f"<span style=\"{style}\">{e['pct']}</span>")
    return f"<div style=\"display:flex;flex-wrap:nowrap\">{''.join(out)}</div>"

def event_slide(e, i, tot, tag, note, h, evs=None):
    f = dict(frame(h))
    n = int(e["n"].replace(".", ""))
    tall = h > 1500
    sh = 58 if not tall else 66                      # spazio per la barra delle percentuali
    row_top = f['top'] + (46 if not tall else 52)
    f['chip'] += sh; f['flow'] += sh
    return page(f"""
<div class="a top" style="top:{f['top']}px"><span>{tag}</span><span>{i}/{tot}</span></div>
<div class=a style="top:{row_top}px">{progress_row(evs or [e], i - 2, tall)}</div>
<div class=a style="top:{f['chip']}px"><span class=chip><span style="color:{GOLD};text-shadow:0 0 8px rgba(255,190,80,.6)">{i - 1}</span>&nbsp;·&nbsp;{e['partita']}</span></div>
<div class="a flow" style="top:{f['flow']}px">
  <div class=name style="margin-top:0">{name_html(e['nome'])}</div>
  <div class=what style="margin-top:6px">{e['cosa']}</div>
  <div class=pctrow style="margin-top:25px"><div class=pct>{e['pct']}</div>
    <div class=pl><b>di possibilità</b><span>1 su {e['n']}</span></div></div>
  <div class=field style="margin-top:31px">{dots(n, n * 7 + i, 1080 - 80 - f['right'])}</div>
  <div class=card style="margin-top:37px;padding-top:30px;padding-bottom:26px">
    <div class=k>Al fantacalcio</div><div class=det style="margin-top:13px">{md(e['card'])}</div></div>
  <div class=kick style="margin-top:41px">{e['frase']}</div>
</div>
<div class="a foot" style="bottom:{f['foot']}px">{WM_LOGO}<div class=note>{note}</div></div>""", h)

def cover_slide(d, tot, tag, h):
    """Copertina-gancio: promessa della lista, le percentuali senza nomi, frase 'contro di te'."""
    f = frame(h)
    c = d["copertina"]
    tall = h > 1500
    # logo grande tagliato a metà sul bordo destro, con gli archi neon concentrici alla sfera
    LW = 440
    scx, scy = 1072, (600 if tall else 430)          # centro della sfera sulla slide
    sr = round(LW * 0.4545)                           # raggio della sfera nel logo
    lx, ly = round(scx - LW * 0.5005), round(scy - LW * 1006 / 933 * 0.46)
    arc = (scx, scy, sr + 26, sr + 62)
    chips = "".join(
        f"<span style=\"display:inline-flex;align-items:center;height:{66 if tall else 72}px;padding:0 {14 if tall else 17}px;margin:0 {9 if tall else 11}px 0 0;border-radius:16px;"
        f"background:rgba(14,20,62,.78);border:2px solid rgba(255,196,92,{.45 + .08 * i:.2f});box-shadow:0 0 {4 + 2 * i}px rgba(255,190,80,{.25 + .06 * i:.2f}),0 0 {10 + 4 * i}px rgba(245,170,60,{.10 + .04 * i:.2f});"
        f"font-family:BS;font-weight:900;font-size:{38 if tall else 44}px;color:{GOLD};text-shadow:0 0 {6 + i}px rgba(255,190,80,.5)\">{e['pct']}</span>"
        for i, e in enumerate(d["eventi"]))
    return page(f"""
<div class="a top" style="top:{f['top']}px"><span>{tag}</span><span>1/{tot}</span></div>
<div class="a flow" style="top:{f['chip'] + (60 if tall else 26)}px">
  <div class=name style="font-size:{c.get('size', 124)}px;line-height:1;white-space:normal">{c['titolo']}</div>
  <div style="margin-top:{44 if tall else 36}px;display:flex;flex-wrap:nowrap">{chips}</div>
  <div class=kick style="margin-top:{44 if tall else 36}px;font-size:58px;line-height:1.05;color:{WHITE};text-shadow:none">{c['frase']}</div>
  <div class=what style="margin-top:{26 if tall else 20}px;font-size:44px">{c['vicini']}</div>
</div>
<div class="a foot" style="bottom:{f['foot']}px">{WM}<div class=note style="font-family:GM;font-size:28px;letter-spacing:.13em;color:{GOLD};text-shadow:0 0 10px rgba(245,178,62,.5)">SCORRI →</div></div>
<img src="{LOGO}" style="position:absolute;z-index:0;left:{lx}px;top:{ly}px;width:{LW}px;filter:drop-shadow(0 0 40px rgba(245,165,60,.35))">""", h, arc)

def outro_slide(d, tot, tag, h):
    f = frame(h)
    return page(f"""
<div class="a top" style="top:{f['top']}px"><span>{tag}</span><span>{tot}/{tot}</span></div>
<div class="a flow" style="top:{f['chip'] + 10}px">
  <img src="{LOGO}" style="width:{200 if h > 1500 else 165}px;margin-left:-6px;filter:drop-shadow(0 0 30px rgba(245,165,60,.35))">
  <div class=name style="margin-top:30px;white-space:normal;line-height:.95;font-size:118px">La prossima volta, <b>sappilo prima.</b></div>
  <div class=body style="margin-top:28px">Il Veggente simula la tua fantapartita 10.000 volte: chi vince, chi schierare, quante chance hai di rimontare.</div>
  <div style="margin-top:32px"><span class=pill>In arrivo a novembre</span></div>
  <div class=wm style="margin-top:26px;font-size:60px;text-transform:none;letter-spacing:.5px">fantaveggente.it</div>
</div>
<div class="a" style="bottom:{f['foot'] + 92}px"><div class=note style="text-align:left;font-size:21px;line-height:1.4">{d['metodo']}</div></div>
<div class="a foot" style="bottom:{f['foot']}px">{WM_LOGO}<div class=note style="font-family:GM;font-size:26px;letter-spacing:.12em">@FANTAVEGGENTE</div></div>""", h)

def cta_slide(d, i, tot, tag, h):
    """Invito a commentare: le cose della giornata numerate, si risponde con un numero."""
    f = frame(h)
    tall = h > 1500
    rows = "".join(
        f"<div style=\"display:flex;align-items:center;gap:22px;height:{66 if tall else 70}px;"
        f"{'border-top:1px solid rgba(245,178,62,.16);' if k else ''}\">"
        f"<span style=\"width:40px;font-family:BS;font-weight:900;font-size:44px;color:{GOLD};text-shadow:0 0 10px rgba(255,190,80,.6)\">{k + 1}</span>"
        f"<span style=\"flex:1;font-family:BS;font-weight:800;font-size:40px;text-transform:uppercase;color:{WHITE}\">{e['nome']}</span>"
        f"<span style=\"font-family:GM;font-weight:500;font-size:28px;color:{MUTED}\">{e['pct']}</span></div>"
        for k, e in enumerate(d["eventi"]))
    return page(f"""
<div class="a top" style="top:{f['top']}px"><span>{tag}</span><span>{i}/{tot}</span></div>
<div class="a flow" style="top:{f['chip'] + (60 if tall else 30)}px">
  <div class=name style="font-size:{140 if tall else 136}px;line-height:1">Quale ti è<br><b>successa?</b></div>
  <div class=what style="margin-top:14px;font-size:46px;color:{WHITE}">Diccelo nei commenti. <span style="color:{GOLD}">Basta il numero.</span></div>
  <div class=card style="margin-top:{36 if tall else 28}px;padding:{14 if tall else 10}px 34px">{rows}</div>
  <div class=kick style="margin-top:{34 if tall else 26}px">Più di una? Scrivile tutte. Ti siamo vicini.</div>
</div>
<div class="a foot" style="bottom:{f['foot']}px">{WM_LOGO}<div class=note style="font-family:GM;font-size:28px;letter-spacing:.12em;color:{GOLD};text-shadow:0 0 10px rgba(245,178,62,.5)">COMMENTA ↓</div></div>""", h)

def build(d, h):
    tot = len(d["eventi"]) + 3
    tag = f"{d.get('rubrica', 'Il Veggente dà i numeri')} · {d['giornata']}ª giornata"
    note = "Stima del Veggente prima della partita · voti Fantacalcio.it"
    return ([cover_slide(d, tot, tag, h)]
            + [event_slide(e, i, tot, tag, note, h, d["eventi"]) for i, e in enumerate(d["eventi"], 2)]
            + [cta_slide(d, tot - 1, tot, tag, h), outro_slide(d, tot, tag, h)])

def main(p):
    d = json.loads(pathlib.Path(p).read_text())
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for fmt, h in (("ig", 1350), ("tiktok", 1920)):
            od = ROOT / "out" / fmt; od.mkdir(parents=True, exist_ok=True)
            pg = b.new_page(viewport={"width": 1080, "height": h})
            for k, html in enumerate(build(d, h), 1):
                pg.set_content(html); pg.wait_for_timeout(250)
                gap = pg.evaluate("""(()=>{const k=document.querySelector('.flow .kick');const w=document.querySelector('.foot');
                    if(!k||!w) return 999; return w.getBoundingClientRect().top - k.getBoundingClientRect().bottom})()""")
                if gap < 50:
                    print(f"ATTENZIONE {fmt} slide {k}: spazio sopra il footer solo {gap:.0f}px")
                pg.screenshot(path=str(od / f"FantaVeggente-g{d['giornata']}-{k:02d}.png"))
        b.close()

if __name__ == "__main__":
    main(sys.argv[1])
