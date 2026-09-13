# -*- coding: utf-8 -*-
"""
골프 스코어카드 앱 아이콘 생성 스크립트
--------------------------------------
초록 배경(#1B6B3C) + 흰색 깃발/공 아이콘 PNG 3장을 만듭니다.

만들어지는 파일 (icons 폴더):
  - icon-192.png          안드로이드 홈화면 아이콘
  - icon-512.png          스플래시 화면 / 고해상도용
  - apple-touch-icon.png  아이폰 홈화면 아이콘 (180x180)

PIL(Pillow)을 사용합니다. 4배 크기로 그린 뒤 축소(LANCZOS)해서
계단 현상 없이 매끄럽게 만듭니다.

실행 방법 (윈도우 PowerShell):
  cd C:\\why2korea\\claude\\scorecard
  python tools\\make_icons.py
"""

import os
from PIL import Image, ImageDraw

BG_COLOR = (0x1B, 0x6B, 0x3C)   # 짙은 페어웨이 그린
FLAG_COLOR = (0xFF, 0xFF, 0xFF)  # 흰색 깃발/깃대
BALL_COLOR = (0xFF, 0xFF, 0xFF)  # 흰색 공
SUPERSAMPLE = 4

TARGETS = [
    ("icon-192.png", 192),
    ("icon-512.png", 512),
    ("apple-touch-icon.png", 180),
]


def build_icon(path, size):
    s = size * SUPERSAMPLE
    img = Image.new("RGB", (s, s), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 깃대 (세로선)
    pole_x = s * 0.42
    pole_top = s * 0.18
    pole_bottom = s * 0.80
    pole_w = s * 0.035
    draw.rectangle(
        [pole_x - pole_w / 2, pole_top, pole_x + pole_w / 2, pole_bottom],
        fill=FLAG_COLOR,
    )

    # 삼각 깃발 (깃대 오른쪽 위)
    flag_pts = [
        (pole_x, pole_top),
        (pole_x + s * 0.34, pole_top + s * 0.10),
        (pole_x, pole_top + s * 0.20),
    ]
    draw.polygon(flag_pts, fill=FLAG_COLOR)

    # 그린(받침) - 깃대 아래 타원
    green_w = s * 0.46
    green_h = s * 0.07
    draw.ellipse(
        [pole_x - green_w / 2, pole_bottom - green_h / 2,
         pole_x + green_w / 2, pole_bottom + green_h / 2],
        fill=FLAG_COLOR,
    )

    # 골프공 (깃대 오른쪽 아래)
    ball_r = s * 0.09
    ball_cx = s * 0.72
    ball_cy = s * 0.72
    draw.ellipse(
        [ball_cx - ball_r, ball_cy - ball_r, ball_cx + ball_r, ball_cy + ball_r],
        fill=BALL_COLOR,
    )

    img = img.resize((size, size), Image.LANCZOS)
    img.save(path, "PNG")
    print(f"  만들었습니다: {path}  ({size}x{size})")


def main():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icons_dir = os.path.join(project_dir, "icons")
    os.makedirs(icons_dir, exist_ok=True)

    print("아이콘 생성을 시작합니다...")
    for filename, size in TARGETS:
        build_icon(os.path.join(icons_dir, filename), size)
    print("완료! icons 폴더를 확인하세요.")


if __name__ == "__main__":
    main()
