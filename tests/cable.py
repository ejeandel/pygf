import sys
from pygf.Layer import MultiLayer
from pygf.Tikz import TikzLayer
from pygf.Svg import SvgLayer
from pygf.Geometry import Point as p, Rectangle
import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument("--tex", dest="tex", action="store_true", help="tex or svg output")

args = parser.parse_args()

if args.tex:
    layer1, layer2, layer3, layer4 = TikzLayer(), TikzLayer(), TikzLayer(), TikzLayer()
    fns = [f"cable1.tex", f"cable2.tex", f"cable3.tex", f"cable4.tex"]
else:
    layer1, layer2, layer3, layer4 = SvgLayer(), SvgLayer(), SvgLayer(), SvgLayer()
    fns = [f"cable1.svg", f"cable2.svg", f"cable3.svg", f"cable4.svg"]
layer = MultiLayer([layer1, layer2, layer3, layer4])
layer123 = MultiLayer([layer1, layer2, layer3])

color = "Yellow"

for i in range(0, 2):
    x = 0 - 4 * i

    layer.polyline(
        [p(0, 0 + x), p(1, 0 + x), p(2, 0.35 + x), p(2, 0.45 + x), p(1, 0.1 + x), p(0, 0.1 + x)],
        closed=True,
        fill="Brown",
        thickness=2,
    )
    A, B, C, D, E, F = (
        p(0, 0.2 + x),
        p(1, 0.2 + x),
        p(2, 0.45 + x),
        p(2, 0.55 + x),
        p(1, 0.3 + x),
        p(0, 0.3 + x),
    )
    layer.polyline([A, B, C, D, E, F], closed=True, thickness=2)
    layer.polyline([A, 0.5 * (A + B), 0.5 * (E + F), F], closed=True, draw=None, fill="Brown")
    layer.polyline([B, 0.5 * (B + C), 0.5 * (D + E), E], closed=True, draw=None, fill="Brown")

    layer123.polyline(
        [
            p(0, 0.4 + x),
            p(1, 0.4 + x),
            p(2, 0.55 + x),
            p(2, 0.65 + x),
            p(1, 0.5 + x),
            p(0, 0.5 + x),
        ],
        closed=True,
        fill="Green",
        thickness=2,
    )
    layer4.polyline(
        [
            p(0, 0.4 + x),
            p(1, 0.4 + x),
            p(2, 0.55 + x),
            p(2, 0.65 + x),
            p(1, 0.5 + x),
            p(0, 0.5 + x),
        ],
        closed=True,
        fill="Green" if i == 0 else "Orange",
        thickness=2,
    )

    A, B, C, D, E, F = (
        p(0, 0.6 + x),
        p(1, 0.6 + x),
        p(2, 0.65 + x),
        p(2, 0.75 + x),
        p(1, 0.7 + x),
        p(0, 0.7 + x),
    )
    layer.polyline([A, B, C, D, E, F], closed=True, thickness=2)
    layer.polyline([A, 0.5 * (A + B), 0.5 * (E + F), F], closed=True, draw=None, fill="Blue")
    layer.polyline([B, 0.5 * (B + C), 0.5 * (D + E), E], closed=True, draw=None, fill="Blue")

    layer.polyline(
        [
            p(0, 0.8 + x),
            p(1, 0.8 + x),
            p(2, 0.75 + x),
            p(2, 0.85 + x),
            p(1, 0.9 + x),
            p(0, 0.9 + x),
        ],
        closed=True,
        fill="Blue",
        thickness=2,
    )
    A, B, C, D, E, F = (
        p(0, 1 + x),
        p(1, 1 + x),
        p(2, 0.85 + x),
        p(2, 0.95 + x),
        p(1, 1.1 + x),
        p(0, 1.1 + x),
    )
    layer.polyline([A, B, C, D, E, F], closed=True, thickness=2)
    layer123.polyline([A, 0.5 * (A + B), 0.5 * (E + F), F], closed=True, draw=None, fill="Green")
    layer123.polyline([B, 0.5 * (B + C), 0.5 * (D + E), E], closed=True, draw=None, fill="Green")
    layer4.polyline(
        [A, 0.5 * (A + B), 0.5 * (E + F), F],
        closed=True,
        draw=None,
        fill="Green" if i == 0 else "Orange",
    )
    layer4.polyline(
        [B, 0.5 * (B + C), 0.5 * (D + E), E],
        closed=True,
        draw=None,
        fill="Green" if i == 0 else "Orange",
    )

    layer123.polyline(
        [
            p(0, 1.2 + x),
            p(1, 1.2 + x),
            p(2, 0.95 + x),
            p(2, 1.05 + x),
            p(1, 1.3 + x),
            p(0, 1.3 + x),
        ],
        closed=True,
        fill="Orange",
        thickness=2,
    )
    layer4.polyline(
        [
            p(0, 1.2 + x),
            p(1, 1.2 + x),
            p(2, 0.95 + x),
            p(2, 1.05 + x),
            p(1, 1.3 + x),
            p(0, 1.3 + x),
        ],
        closed=True,
        fill="Orange" if i == 0 else "Green",
        thickness=2,
    )
    A, B, C, D, E, F = (
        p(0, 1.4 + x),
        p(1, 1.4 + x),
        p(2, 1.05 + x),
        p(2, 1.15 + x),
        p(1, 1.5 + x),
        p(0, 1.5 + x),
    )
    layer.polyline([A, B, C, D, E, F], closed=True, thickness=2)
    layer123.polyline([A, 0.5 * (A + B), 0.5 * (E + F), F], closed=True, draw=None, fill="Orange")
    layer123.polyline([B, 0.5 * (B + C), 0.5 * (D + E), E], closed=True, draw=None, fill="Orange")
    layer4.polyline(
        [A, 0.5 * (A + B), 0.5 * (E + F), F],
        closed=True,
        draw=None,
        fill="Orange" if i == 0 else "Green",
    )
    layer4.polyline(
        [B, 0.5 * (B + C), 0.5 * (D + E), E],
        closed=True,
        draw=None,
        fill="Orange" if i == 0 else "Green",
    )

    layer.polyline([p(2, 1.4 + x), p(2, 0.1 + x)])
    layer.edge(
        [
            p(2, 1.4 + x) @ {"angle": 0},
            p(3, 1.2 + x) @ {"angle": 0},
            p(4, 1.2 + x) @ {"angle": 0},
            p(4, 0.3 + x) @ {"angle": 180},
            p(3, 0.3 + x) @ {"angle": 180},
            p(2, 0.1 + x) @ {"angle": 180},
        ],
        fill=color,
    )

    layer.polyline([p(-0.2, 1.15 + x), p(0.6, 1.15 + x), p(0.6, 0.35 + x), p(-0.2, 0.35 + x)], closed=True)
    layer.polyline([p(0.6, 0.95 + x), p(1.4, 0.95 + x), p(1.4, 0.55 + x), p(0.6, 0.55 + x)], closed=True)


layer.edge(
    [
        p(3, 1.2) @ {"angle": 0},
        p(8, 1.2) @ {"angle": 0},
        p(13, -1.25) @ {"angle": -90},
        p(8, -3.7) @ {"angle": 180},
        p(3, -3.7) @ {"angle": 180},
        p(3, -2.8) @ {"angle": 0},
        p(8, -2.8) @ {"angle": 0},
        p(12, -1.25) @ {"angle": 90},
        p(8, 0.3) @ {"angle": 180},
        p(3, 0.3) @ {"angle": 180},
        p(3, 1.2) @ {"angle": 0},
    ],
    draw=None,
    fill=color,
)


layer.edge(
    [
        p(3, 1.2) @ {"angle": 0},
        p(8, 1.2) @ {"angle": 0},
        p(13, -1.25) @ {"angle": -90},
        p(8, -3.7) @ {"angle": 180},
        p(3, -3.7) @ {"angle": 180},
    ]
)
layer.edge(
    [
        p(3, -2.8) @ {"angle": 0},
        p(8, -2.8) @ {"angle": 0},
        p(12, -1.25) @ {"angle": 90},
        p(8, 0.3) @ {"angle": 180},
        p(3, 0.3) @ {"angle": 180},
    ]
)
layer.polyline([p(0, 1.6), p(3, 1.6), p(3, -0.1), p(0, -0.1)], closed=True)
layer.polyline([p(0, -2.4), p(3, -2.4), p(3, -4.1), p(0, -4.1)], closed=True)


# PC au dessus
for l in layer1, layer3, layer4:
    l.text(p(-4, 1), "PC")
    l.text(p(-2, 1.35), "Envoi")
    l.line(p(-1, 1.45), p(-0.5, 1.45), arrow="->")
    l.line(p(-1, 1.25), p(-0.5, 1.25), arrow="->")
    l.text(p(-2, 0.725), "Réception")
    l.line(p(-0.5, 1.05), p(-1, 1.05), arrow="->")
    l.line(p(-0.5, 0.45), p(-1, 0.45), arrow="->")

# HUB au dessus
for l in (layer2,):
    l.text(p(-4, 1), "HUB")
    l.text(p(-2, 1.35), "Réception")
    l.line(p(-0.5, 1.45), p(-1, 1.45), arrow="->")
    l.line(p(-0.5, 1.25), p(-1, 1.25), arrow="->")
    l.text(p(-2, 0.725), "Envoi")
    l.line(p(-1, 1.05), p(-0.5, 1.05), arrow="->")
    l.line(p(-1, 0.45), p(-0.5, 0.45), arrow="->")

# PC en dessous:
for l in layer2, layer3, layer4:
    l.text(p(-4, -3), "PC")
    l.text(p(-2, 1.35 - 4), "Envoi")
    l.line(p(-1, 1.45 - 4), p(-0.5, 1.45 - 4), arrow="->")
    l.line(p(-1, 1.25 - 4), p(-0.5, 1.25 - 4), arrow="->")
    l.text(p(-2, 0.725 - 4), "Réception")
    l.line(p(-0.5, 1.05 - 4), p(-1, 1.05 - 4), arrow="->")
    l.line(p(-0.5, 0.45 - 4), p(-1, 0.45 - 4), arrow="->")


# HUB en dessous
for l in (layer1,):
    l.text(p(-4, -3), "HUB")
    l.text(p(-2, 1.35 - 4), "Réception")
    l.line(p(-0.5, 1.45 - 4), p(-1, 1.45 - 4), arrow="->")
    l.line(p(-0.5, 1.25 - 4), p(-1, 1.25 - 4), arrow="->")
    l.text(p(-2, 0.725 - 4), "Envoi")
    l.line(p(-1, 1.05 - 4), p(-0.5, 1.05 - 4), arrow="->")
    l.line(p(-1, 0.45 - 4), p(-0.5, 0.45 - 4), arrow="->")


layer.draw_all(Rectangle(p(-5, 2), p(13.5, -4.5)), [open(fn, "w") for fn in fns], preamble=True)
