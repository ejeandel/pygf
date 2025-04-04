from pygf.geometry import Point, Rectangle
from pygf.layer import MultiLayer
from pygf.svg import SvgLayer
from pygf.tikz import TikzLayer

layer1, layer2 = TikzLayer(), SvgLayer()
layer = MultiLayer([layer1, layer2])


layer.polyline(
    [Point(0, 0), Point(2, 3), Point(4, 3), Point(6, 0)],
    labels={
        "above start": "above start",
        "above": "above",
        "above end": "above end",
        "below start": "below start",
        "below": "below",
        "below end": "below end",
    },
)


layer.polyline(
    [Point(0, 4), Point(2, 7), Point(4, 7), Point(6, 4)][::-1],
    labels={
        "above start": "above start",
        "above": "above",
        "above end": "above end",
        "below start": "below start",
        "below": "below",
        "below end": "below end",
    },
)


layer.edge(
    [Point(-7, 0), Point(-5, 3), Point(-3, 3), Point(-1, 0)],
    labels={
        "above start": "above start",
        "above": "above",
        "above end": "above end",
        "below start": "below start",
        "below": "below",
        "below end": "below end",
    },
)


layer.edge(
    [Point(-7, 4), Point(-5, 7), Point(-3, 7), Point(-1, 4)][::-1],
    labels={
        "above start": "above start",
        "above": "above",
        "above end": "above end",
        "below start": "below start",
        "below": "below",
        "below end": "below end",
    },
)

with open("poly.tex", "w") as f1, open("poly.svg", "w") as f2:
    layer.draw_all(
        Rectangle(Point(-8, -1), Point(7, 8)),
        [f1, f2],
        preamble=True,
    )
