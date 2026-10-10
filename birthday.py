import math as m
import random as r
import turtle as t
import tkinter.font as tkf

OY = 56
TICK = 16
GAP = 7
SIZES = (9, 10, 11, 12)
FONT = "Arial"
BG = "#060208"

INTRO = 120
BLOW_GAP = 40
BLOW_N = 26
BITE_GAP = 46
EAT_TARGET = 1.0

s = t.Screen()
s.setup(800, 800)
s.bgcolor(BG)
s.title("Happy Birthday")
s.tracer(0)

cv = s.getcanvas()
rng = r.Random(11)

PHRASES = [
    "Happy Birthday",
    "İyi ki doğdun",
    "Feliz cumpleaños",
    "Joyeux anniversaire",
    "Alles Gute zum Geburtstag",
    "Buon compleanno",
    "Feliz aniversário",
    "С днём рождения",
    "생일 축하해요",
    "お誕生日おめでとう",
    "生日快乐",
    "जन्मदिन मुबारक हो",
    "Χρόνια πολλά",
    "Gefeliciteerd",
    "Grattis på födelsedagen",
    "Wszystkiego najlepszego",
    "สุขสันต์วันเกิด",
    "Chúc mừng sinh nhật",
    "Selamat ulang tahun",
    "З днем народження",
    "عيد ميلاد سعيد",
    "تولدت مبارک",
    "יום הולדת שמח",
    "Tillykke med fødselsdagen",
    "Všechno nejlepší",
]

PARTS = [
    ("plate", 350, -302, -262, 18, 18),
    ("base", 300, -262, -110, 22, 10),
    ("mid", 225, -110, -5, 22, 0),
    ("top", 150, -5, 85, 20, 0),
]
TOPS = {p[0]: p[3] for p in PARTS}
BOTS = {p[0]: p[2] for p in PARTS}
CANDLE_X = [-100, -50, 0, 50, 100]
CANDLE_Y0, CANDLE_Y1 = 96, 166
FLAME_Y = 170

_fonts = {}


def font_for(size):
    if size not in _fonts:
        _fonts[size] = tkf.Font(root=cv, family=FONT, size=size, weight="bold")
    return _fonts[size]


def hx(c):
    return "#%02x%02x%02x" % tuple(int(max(0, min(1, v)) * 255) for v in c)


def mix(a, b, k):
    return tuple(p + (q - p) * k for p, q in zip(a, b))


def dim(c, k):
    return tuple(v * k for v in c)


def clamp(v):
    return max(0.0, min(1.0, v))


def cy(y):
    return -(y + OY)


YMAX = max(p[3] for p in PARTS)
YMIN = min(p[2] for p in PARTS)


def half_w(part, y):
    _, W, y1, y2, Rt, Rb = part
    w = W
    if Rt and y > y2 - Rt:
        d = y - (y2 - Rt)
        w = W - Rt + m.sqrt(max(0.0, Rt * Rt - d * d))
    elif Rb and y < y1 + Rb:
        d = (y1 + Rb) - y
        w = W - Rb + m.sqrt(max(0.0, Rb * Rb - d * d))
    return w


def spans(y):
    for part in PARTS:
        if part[2] <= y < part[3]:
            w = half_w(part, y)
            return [(-w, w)] if w > 0 else []
    return []


def intersect(A, B):
    out = []
    for a in A:
        for b in B:
            lo, hi = max(a[0], b[0]), min(a[1], b[1])
            if hi - lo > 14:
                out.append((lo, hi))
    return out


def part_of(y):
    for p in PARTS:
        if p[2] <= y < p[3]:
            return p[0]
    return "base"


def phrase_cycle():
    while True:
        order = PHRASES[:]
        rng.shuffle(order)
        yield from order


PAL = {
    "plate": (0.95, 0.72, 0.30),
    "base": (0.80, 0.12, 0.42),
    "mid": (0.95, 0.30, 0.55),
    "top": (1.00, 0.55, 0.70),
}
CREAM = (1.0, 0.90, 0.93)
FILL = (1.0, 0.80, 0.55)
FLASH = (1.0, 0.78, 0.78)
PHASE = {"base": 0.0, "mid": 1.7, "top": 3.1}


def drip(part, x):
    ph = PHASE[part]
    a = 0.5 + 0.5 * m.sin(x / 15.0 + ph)
    b = 0.5 + 0.5 * m.sin(x / 38.0 + ph * 2)
    return 22 + 26 * a * b


def color_for(p):
    part = part_of(p["y"])
    base = PAL[part]
    y, x = p["y"], p["x"]
    if part == "plate":
        base = mix(base, (1, 1, 1), rng.uniform(0.0, 0.35))
    else:
        top = TOPS[part]
        bot = BOTS[part]
        if y > top - drip(part, x):
            base = mix(CREAM, base, rng.uniform(0.0, 0.18))
        elif part != "base" and y < bot + 16:
            base = mix(FILL, base, rng.uniform(0.0, 0.25))
        else:
            base = mix(base, (1, 1, 1), rng.uniform(0.0, 0.18) + (0.15 if p["edge"] else 0))
    return tuple(min(1, v) for v in base)


def build():
    cycle = phrase_cycle()
    row_h = max(font_for(z).metrics("linespace") for z in SIZES) + 4
    half = row_h / 2
    placed = []

    y = YMAX - half
    while y > YMIN + half:
        row = intersect(spans(y + half), spans(y - half))

        for lo, hi in row:
            lo += 4
            hi -= 4
            cur = lo + rng.uniform(0, 8)
            line = []

            while True:
                fit = None
                for _ in range(12):
                    text = next(cycle)
                    size = rng.choice(SIZES)
                    w = font_for(size).measure(text)
                    if cur + w <= hi:
                        fit = (text, size, w)
                        break
                if not fit:
                    break
                text, size, w = fit
                line.append([cur + w / 2, text, size, w])
                cur += w + GAP

            if not line:
                continue

            if len(line) > 1:
                left = hi - (line[-1][0] + line[-1][3] / 2)
                for i, it in enumerate(line):
                    it[0] += left * i / (len(line) - 1)
            else:
                line[0][0] = (lo + hi) / 2

            for i, (x, text, size, w) in enumerate(line):
                edge = i == 0 or i == len(line) - 1
                placed.append(dict(x=x, y=y, text=text, size=size, edge=edge))

        y -= row_h

    for p in placed:
        p["color"] = color_for(p)
        p["kind"] = "plate" if part_of(p["y"]) == "plate" else "body"

    extras = []
    for cx in (-75, -25, 25, 75):
        extras.append(dict(x=cx, y=TOPS["top"] - 2, text="●", size=13, edge=False,
                           color=(0.92, 0.04, 0.12), kind="cherry"))

    candles = []
    for ci, cx in enumerate(CANDLE_X):
        k = 0
        yy = CANDLE_Y0
        while yy <= CANDLE_Y1:
            col = (1.0, 0.92, 0.95) if k % 2 == 0 else (0.45, 0.80, 1.0)
            candles.append(dict(x=cx, y=yy, text="|", size=12, edge=False,
                                color=col, kind="candle", ci=ci))
            yy += 13
            k += 1
    return placed + extras + candles


BGC = tuple(int(BG[i:i + 2], 16) / 255 for i in (1, 3, 5))

ITEMS = build()


def make(p):
    x, y = p["x"], cy(p["y"])
    size, text, c = p["size"], p["text"], p["color"]
    font = (FONT, size, "bold")
    big = (FONT, size + 1, "bold")
    p["px"], p["py"] = x, y
    p["shadow"] = cv.create_text(x + 2, y + 3, text=text, font=font, fill=hx(dim(c, 0.30)))
    p["halo"] = cv.create_text(x, y, text=text, font=big, fill=hx(dim(c, 0.20)))
    p["main"] = cv.create_text(x, y, text=text, font=font, fill=hx(c))
    p["alive"] = True


for _p in ITEMS:
    make(_p)

RED = (0.95, 0.10, 0.05)
ORANGE = (1.00, 0.55, 0.05)
YELLOW = (1.00, 0.80, 0.25)
EMBER = (0.30, 0.04, 0.02)
flames = []

for _cx in CANDLE_X:
    _by = cy(FLAME_Y)
    _glow = cv.create_oval(_cx - 26, _by - 36, _cx + 26, _by + 16,
                           fill=hx(dim(ORANGE, 0.15)), outline="")
    _outer = cv.create_oval(_cx - 8, _by - 24, _cx + 8, _by + 2, fill=hx(RED), outline="")
    _inner = cv.create_oval(_cx - 4, _by - 14, _cx + 4, _by + 1, fill=hx(YELLOW), outline="")
    cv.tag_lower(_glow)
    flames.append(dict(glow=_glow, outer=_outer, inner=_inner, x=_cx))


def flicker(f):
    by = cy(FLAME_Y)
    cx = f["x"]
    k = rng.random()
    h = rng.uniform(20, 29)
    w = rng.uniform(7, 10)
    sway = rng.uniform(-2.5, 2.5)
    cv.coords(f["outer"], cx - w + sway, by - h, cx + w + sway, by + 2)
    cv.itemconfig(f["outer"], fill=hx(mix(RED, ORANGE, k)))
    cv.coords(f["inner"], cx - w * 0.45 + sway * 0.6, by - h * 0.55,
              cx + w * 0.45 + sway * 0.6, by + 1)
    cv.itemconfig(f["inner"], fill=hx(mix(ORANGE, YELLOW, rng.uniform(0.3, 1))))
    g = rng.uniform(22, 30)
    cv.coords(f["glow"], cx - g, by - g - 10, cx + g, by + g - 14)
    cv.itemconfig(f["glow"], fill=hx(dim(mix(RED, ORANGE, k), rng.uniform(0.13, 0.22))))


def blow_step(f, u):
    by = cy(FLAME_Y)
    cx = f["x"]
    lean = 14 * (u ** 1.4) + rng.uniform(-1.5, 1.5) * (1 - u)
    h = 24 * ((1 - u) ** 1.2) + 2 + rng.uniform(0, 4) * (1 - u)
    w = 8 * (1 - 0.55 * u)
    cv.coords(f["outer"], cx - w + lean, by - h, cx + w + lean, by + 2)
    cv.itemconfig(f["outer"], fill=hx(mix(mix(RED, ORANGE, 0.4), EMBER, u)))
    cv.coords(f["inner"], cx - w * 0.45 + lean * 0.6, by - h * 0.55,
              cx + w * 0.45 + lean * 0.6, by + 1)
    cv.itemconfig(f["inner"], fill=hx(mix(YELLOW, RED, clamp(u * 1.6))))
    g = 28 * (1 - 0.75 * u)
    cv.coords(f["glow"], cx - g, by - g - 10, cx + g, by + g - 14)
    cv.itemconfig(f["glow"], fill=hx(dim(ORANGE, 0.17 * ((1 - u) ** 1.5))))


smoke = []
removals = []


def finish_blow(f):
    for k in ("glow", "outer", "inner"):
        cv.delete(f[k])
    by = cy(FLAME_Y)
    for _ in range(4):
        oid = cv.create_oval(0, 0, 0, 0, fill=BG, outline="")
        smoke.append(dict(id=oid, x=f["x"] + 8, y=by - 2, f=-rng.randint(0, 14),
                          N=rng.randint(55, 80), ph=rng.uniform(0, 6),
                          drift=rng.uniform(6, 16)))


def update_smoke(sm):
    sm["f"] += 1
    if sm["f"] <= 0:
        return True
    u = clamp(sm["f"] / sm["N"])
    x = sm["x"] + sm["drift"] * u + 5 * m.sin(u * 7 + sm["ph"])
    y = sm["y"] - 60 * u
    rad = 2 + 8 * u
    cv.coords(sm["id"], x - rad, y - rad, x + rad, y + rad)
    cv.itemconfig(sm["id"], fill=hx(mix(BGC, (0.62, 0.62, 0.68), 0.75 * ((1 - u) ** 1.3))))
    if u >= 1:
        cv.delete(sm["id"])
        return False
    return True


def schedule_removal(p, dx, dy, n, delay=0):
    p["alive"] = False
    removals.append(dict(p=p, f=-delay, N=n, dx=dx, dy=dy))


def update_removal(rm):
    rm["f"] += 1
    if rm["f"] <= 0:
        return True
    p = rm["p"]
    u = clamp(rm["f"] / rm["N"])
    c = p["color"]
    dy = rm["dy"]
    off = dy * (u * u) if dy > 0 else dy * (1 - (1 - u) ** 2)
    ox = rm["dx"] * u
    x, y = p["px"] + ox, p["py"] + off
    cv.coords(p["shadow"], x + 2, y + 3)
    cv.coords(p["halo"], x, y)
    cv.coords(p["main"], x, y)
    cv.itemconfig(p["shadow"], fill=hx(mix(BGC, dim(c, 0.30), 1 - u)))
    cv.itemconfig(p["halo"], fill=hx(mix(BGC, dim(c, 0.20), 1 - u)))
    cv.itemconfig(p["main"], fill=hx(mix(c, BGC, u)))
    if u >= 1:
        for k in ("shadow", "halo", "main"):
            cv.delete(p[k])
        return False
    return True


def lift_candle(ci):
    for p in ITEMS:
        if p["kind"] == "candle" and p["ci"] == ci and p["alive"]:
            schedule_removal(p, 0, -36, 24)


EATABLE = [p for p in ITEMS if p["kind"] in ("body", "cherry")]
TOTAL = len(EATABLE)
eat_done = False


def finish_eating():
    global eat_done
    eat_done = True
    for p in ITEMS:
        if p["kind"] == "plate" and p["alive"]:
            delay = int((p["x"] + 350) / 700 * 40)
            schedule_removal(p, rng.uniform(-6, 6), rng.uniform(20, 40),
                             rng.randint(20, 28), delay)


def bite():
    pool = [p for p in EATABLE if p["alive"]]

    if len(pool) <= 5:
        for p in pool:
            schedule_removal(p, rng.uniform(-8, 8), rng.uniform(16, 42),
                             rng.randint(18, 26), rng.randint(0, 10))
        finish_eating()
        return

    th = rng.uniform(0, 2 * m.pi)
    vx, vy = m.cos(th), m.sin(th)
    ext = max(pool, key=lambda p: p["x"] * vx + p["y"] * vy)
    bx, by = ext["x"], ext["y"]
    R = rng.uniform(85, 115)

    for p in pool:
        d = m.hypot((p["x"] - bx) / 1.6, (p["y"] - by) * 1.2)
        d += rng.uniform(-10, 10)
        if d <= R:
            schedule_removal(p, rng.uniform(-8, 8), rng.uniform(16, 42),
                             rng.randint(18, 26), rng.randint(0, 8))


def shimmer():
    alive = [p for p in ITEMS if p["alive"] and p["kind"] != "candle"]
    if not alive:
        return
    p = rng.choice(alive)
    c = p["color"]
    cv.itemconfig(p["main"], fill=hx(mix(c, FLASH, 0.6)))

    def back(p=p, c=c):
        if p["alive"]:
            cv.itemconfig(p["main"], fill=hx(c))
    cv.after(260, back)


def blow_t0(i):
    return INTRO + i * BLOW_GAP


EAT_START = blow_t0(len(CANDLE_X) - 1) + BLOW_N + 40
fr = 0


def tick():
    global fr
    fr += 1

    for i, f in enumerate(flames):
        t0 = blow_t0(i)
        if fr < t0:
            if fr % 5 == 0:
                flicker(f)
        elif fr < t0 + BLOW_N:
            blow_step(f, (fr - t0) / BLOW_N)
        elif fr == t0 + BLOW_N:
            finish_blow(f)
        if fr == t0 + BLOW_N + 6:
            lift_candle(i)

    smoke[:] = [sm for sm in smoke if update_smoke(sm)]

    if fr >= EAT_START and not eat_done and (fr - EAT_START) % BITE_GAP == 0:
        bite()

    removals[:] = [rm for rm in removals if update_removal(rm)]

    if fr % 16 == 0 and not eat_done:
        shimmer()

    if eat_done and not removals and not smoke:
        return
    cv.after(TICK, tick)


try:
    cv.after(300, tick)
    t.done()
except (t.Terminator, Exception):
    pass