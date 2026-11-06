# 카톡 공유용 카드 이미지 생성: python make_cards.py
# 문구 탭 이름이 바뀌면 CARDS 의 title 만 고치고 다시 실행 → card1~5.png
import math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, S = 1600, 800, 2  # 2:1 비율, S배 크게 그린 뒤 축소(안티앨리어싱)
FONT_B = "C:/Windows/Fonts/malgunbd.ttf"
FONT_R = "C:/Windows/Fonts/malgun.ttf"

CARDS = [
    {"title": "고마워요", "top": (255, 214, 190), "bottom": (255, 160, 130), "heart": (255, 92, 70),  "ink": (90, 30, 20)},
    {"title": "미안해요", "top": (208, 240, 236), "bottom": (130, 205, 200), "heart": (30, 150, 145), "ink": (15, 60, 60)},
    {"title": "사랑해요", "top": (255, 222, 236), "bottom": (255, 150, 190), "heart": (240, 60, 120), "ink": (90, 20, 50)},
    {"title": "응원해요", "top": (255, 242, 196), "bottom": (255, 205, 110), "heart": (245, 140, 20), "ink": (95, 55, 10)},
    {"title": "약속해요", "top": (214, 228, 255), "bottom": (196, 178, 255), "heart": (120, 96, 235), "ink": (40, 30, 90)},
]
SUB = "가족에게 마음이 도착했어요"


def heart_points(cx, cy, size, rot=0.0, n=120):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        x, y = x * size / 32, y * size / 32
        xr = x * math.cos(rot) - y * math.sin(rot)
        yr = x * math.sin(rot) + y * math.cos(rot)
        pts.append((cx + xr, cy + yr))
    return pts


def make(card, path, seed):
    w, h = W * S, H * S
    img = Image.new("RGB", (w, h))
    px = ImageDraw.Draw(img)
    for y in range(h):  # 세로 그라데이션
        r = y / (h - 1)
        c = tuple(int(card["top"][k] * (1 - r) + card["bottom"][k] * r) for k in range(3))
        px.line([(0, y), (w, y)], fill=c)

    # 흩어진 작은 하트들
    rnd = random.Random(seed)
    deco = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(deco)
    for _ in range(26):
        size = rnd.uniform(40, 120) * S
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        if 0.35 * w < x < 0.95 * w and 0.25 * h < y < 0.75 * h:
            continue  # 글자 영역 비우기
        d.polygon(heart_points(x, y, size, rnd.uniform(-0.5, 0.5)), fill=(255, 255, 255, rnd.randint(70, 140)))
    img.paste(deco, (0, 0), deco)

    # 큰 하트 + 그림자 + 하이라이트
    cx, cy, size = int(w * 0.22), int(h * 0.52), 520 * S
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).polygon(heart_points(cx + 18 * S, cy + 30 * S, size, -0.15), fill=(0, 0, 0, 60))
    shadow = shadow.filter(ImageFilter.GaussianBlur(30 * S))
    img.paste(shadow, (0, 0), shadow)
    big = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(big)
    bd.polygon(heart_points(cx, cy, size, -0.15), fill=card["heart"] + (255,))
    bd.ellipse([cx - 200 * S, cy - 140 * S, cx - 120 * S, cy - 85 * S], fill=(255, 255, 255, 110))
    img.paste(big, (0, 0), big)

    # 글자
    t = ImageDraw.Draw(img)
    fb = ImageFont.truetype(FONT_B, 150 * S)
    fr = ImageFont.truetype(FONT_R, 52 * S)
    tx = int(w * 0.47)
    t.text((tx, int(h * 0.36)), card["title"], font=fb, fill=card["ink"], anchor="lm")
    t.text((tx + 6 * S, int(h * 0.60)), SUB, font=fr, fill=card["ink"] + (0,), anchor="lm")

    img.resize((W, H), Image.LANCZOS).save(path, optimize=True)
    print(path)


for i, c in enumerate(CARDS, 1):
    make(c, f"card{i}.png", i)
