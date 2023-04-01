# pylint: disable=invalid-name
import math
import base64
from .Layer import Layer
from .Geometry import Point, Rectangle, Transform
from .Options import register_layer


def dic_to_svglist(d):
    return ' '.join(f'{x}="{y}"' for (x, y) in d.items())


""" TeX to SVG

The common unit between TeX and SVG are centimeters.

1cm is represented here by 50 pixels via the svgtransform that takes care automatically of the conversion

"""


def pt_to_cm(x):
    return x * 2.54 / 72.27


class SvgLayer(Layer):

    def __init__(self, transform=None):
        Layer.__init__(self, transform)
        self.names = 0
        self.nodelayer = []
        self.edgelayer = []
        self.defs = {}
        self.svgtransform = Transform(50, -50)

        self.arrows = {
            "->":
            '<marker id="marker_{_id}"  markerUnits = "userSpaceOnUse" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polyline points="0 0, 10 3.5, 0 7" /></marker>',
            "-x":
            '<marker id="marker_{_id}"  markerUnits = "userSpaceOnUse" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto"><polyline points="0 0, 7 7" /><line x1="0" y1="7" x2="7" y2="0"  /></marker>'
        }

    def new_name(self):
        self.names += 1
        return f"{self.names}"

    def picture(self, point, img_name, width, height):
        tf = self.svgtransform * self.transform
        r = Rectangle(Point(0, 0), self.svgtransform(Point(width, -height)))
        with open(img_name, 'rb') as f:
            data = f.read()
            self.nodelayer += [
                f'<image xlink:href="data:image/png;base64,{str(base64.b64encode(data),"utf-8")}" transform="translate({tf(point)-r.center})" width="{r.width}" height="{r.height}" preserveAspectRatio="none"/>'
            ]

        # TODO: none ou xMidYMid

    def parse_style(self, style, svg_style):
        """ ---------
            thickness
            --------- """

        if "thickness" in style:
            thickness = style["thickness"]
            del style["thickness"]
        else:
            thickness = 1
        pt = pt_to_cm(1) * self.svgtransform(Point(1, 1)).x
        # in thickness 1, the strokewidth should be 0.4pt
        strokewidth = 0.4 * pt * thickness
        svg_style["stroke-width"] = f"{strokewidth:.2g}"
        """ ---------
            dash
            --------- """
        if "dash" in style:
            dash = style["dash"]
            del style["dash"]
            sw = strokewidth
            dasharray = {
                "solid": "none",
                "dotted": f"{sw:.2g} {2*pt:.2g}",
                "densely dotted": f"{sw:.2g} {1*pt:.2g}",
                "loosely dotted": f"{sw:.2g} {4*pt:.2g}",
                "dashed": f"{3*pt:.2g}",
                "densely dashed": f"{3*pt:.2g} {2*pt:.2g}",
                "loosely dashed": f"{3*pt:.2g} {6*pt:.2g}",
                "dashdotted": f"{3*pt:.2g} {2*pt:.2g} {sw:.2g} {2*pt:.2g}",
                "dash dot": f"{3*pt:.2g} {2*pt:.2g} {sw:.2g} {2*pt:.2g}",
                "densely dashdotted": f"{3*pt:.2g} {1*pt:.2g} {sw:.2g} {1*pt:.2g}",
                "densely dash dot": f"{3*pt:.2g} {1*pt:.2g} {sw:.2g} {1*pt:.2g}",
                "loosely dashdotted": f"{3*pt:.2g} {4*pt:.2g} {sw:.2g} {4*pt:.2g}",
                "loosely dash dot": f"{3*pt:.2g} {4*pt:.2g} {sw:.2g} {4*pt:.2g}",
                "dashdotdotted": f"{3*pt:.2g} {2*pt:.2g} {sw:.2g} {2*pt:.2g} {sw:.2g} {2*pt:.2g}",
                "densely dashdotdotted": f"{3*pt:.2g} {1*pt:.2g} {sw:.2g} {1*pt:.2g} {sw:.2g} {1*pt:.2g}",
                "loosely dashdotdotted": f"{3*pt:.2g} {4*pt:.2g} {sw:.2g} {4*pt:.2g} {sw:.2g} {4*pt:.2g}",
                "dash dot dot": f"{3*pt:.2g} {2*pt:.2g} {sw:.2g} {2*pt:.2g} {sw:.2g} {2*pt:.2g}",
                "densely dash dot dot": f"{3*pt:.2g} {1*pt:.2g} {sw:.2g} {1*pt:.2g} {sw:.2g} {1*pt:.2g}",
                "loosely dash dot dot": f"{3*pt:.2g} {4*pt:.2g} {sw:.2g} {4*pt:.2g} {sw:.2g} {4*pt:.2g}"
            }.get(dash)
            svg_style["stroke-dasharray"] = dasharray
        """ -------
            draw
            -------- """
        if "draw" in style:
            color = style["draw"]
            del style["draw"]
            if color is None:
                color = "none"
        else:
            color = "black"
        svg_style["stroke"] = color
        """ --------
            fill
            -------- """
        if "fill" in style:
            fill = style["fill"]
            del style["fill"]
            if fill is None:
                fill = "none"
            if "opacity" in style:
                svg_style["fill-opacity"] = style["opacity"]
                del style["opacity"]
        else:
            fill = "none"
        svg_style["fill"] = fill

        if "rounded" in style and style["rounded"]:
            del style["rounded"]
            svg_style["stroke-linejoin"] = "round"

        # self.parse_arrows(style, svg_style) TODO

    def parse_text_style(self, style, text_style):
        if "text_size" in style:
            if style["text_size"] == "small":
                text_style["font-size"] = "x-small"
            if style["text_size"] == "large":
                text_style["font-size"] = "x-large"
            del style["text_size"]

        if "font_family" in style:
            text_style["font-family"] = style["font_family"]
            del style["font_family"]
        else:
            text_style["font-family"] = "sans-serif"

    def __path(self,
               path,
               reverse_path,
               reverse_start,
               reverse_end,
               labels=None,
               style=None):
        if style is None:
            style = {}  # todo wire.wire_style
        # partie qui par les styles: pas vraiment bien faite

        svg_style = {}
        self.parse_style(style, svg_style)

        text_style = {}
        self.parse_text_style(style, text_style)

        _id = self.new_name()

        markers = ""
        if "arrow" in style:
            markers = self.arrows[style['arrow']].format(_id=_id)
            svg_style['marker-end'] = f'url(#marker_{_id})'

        self.edgelayer += [
            f'<g {dic_to_svglist(svg_style)} >'
            f'<path id="{_id}" d="{path}" />'
            f'{markers}'
            '</g>'
        ]

        if reverse_start or reverse_end:
            self.edgelayer += [
                f'<path id="r-{_id}" d="{reverse_path}" display="none"/>'
            ]

        if labels is not None:
            for position in labels:

                label_style = {}
                label_style.update(text_style)

                text = labels[position]
                if "above" in position:
                    label_style["dy"] = -5
                else:
                    # below
                    label_style["dy"] = 5
                    label_style["dominant-baseline"] = "hanging"

                if "start" in position:
                    label_style[
                        "text-anchor"] = "start" if not reverse_start else "end"
                    startOffset = 0 if not reverse_start else 100
                    mainpath = f"#{_id}" if not reverse_start else f"#r-{_id}"
                elif "end" in position:
                    label_style[
                        "text-anchor"] = "end" if not reverse_end else "start"
                    startOffset = 100 if not reverse_end else 0
                    mainpath = f"#{_id}" if not reverse_end else f"#r-{_id}"
                else:
                    label_style["text-anchor"] = "middle"
                    mainpath = f"#{_id}" if not reverse_start else f"#r-{_id}"
                    mainpath_end = f"#{_id}" if not reverse_end else f"#r-{_id}"

                if position in ["above start", "below start"]:
                    self.edgelayer += [
                        f'<text  {dic_to_svglist(label_style)}  ><textPath href="{mainpath}" startOffset="{startOffset}%"> {text} </textPath></text>'
                    ]
                elif "above" == position:
                    self.edgelayer += [
                        f'<text   {dic_to_svglist(label_style)} ><textPath href="{mainpath}" startOffset="50%"> {text} </textPath></text>'
                    ]
                elif position in ["above end", "below end"]:
                    self.edgelayer += [
                        f'<text  {dic_to_svglist(label_style)} ><textPath href="{mainpath}"  startOffset="{startOffset}%"> {text} </textPath></text>'
                    ]
                elif "below" == position:
                    self.edgelayer += [
                        f'<text  {dic_to_svglist(label_style)}><textPath href="{mainpath_end}"  startOffset="50%"> {text} </textPath></text>'
                    ]

    def line(self, p1, p2, labels=None, **style):
        (p1, p2) = map(self.svgtransform * self.transform, (p1, p2))
        path = f"M {p1} L {p2}"
        reverse_path = f"M {p2} L {p1}"

        reverse_start = abs((p2 - p1).angle) > math.pi / 2
        reverse_end = reverse_start
        self.__path(path, reverse_path, reverse_start, reverse_end, labels,
                    style)

    def circle(self, p1, radius, labels=None, **style):
        tf = self.svgtransform * self.transform

        rx = tf(p1).distance(tf(Point(radius, 0) + p1))
        ry = tf(p1).distance(tf(Point(0, radius) + p1))

        x1 = tf(p1 + Point(radius, 0))
        x2 = tf(p1 - Point(radius, 0))

        x_axis_rotation = tf(Point(radius, 0)).angle * 180 / math.pi

        path = f"M {x1} A {rx} {ry} {x_axis_rotation:f} 1 1 {x2} A {rx} {ry} {x_axis_rotation:f} 1 1 {x1}"
        reverse_path = f"M {x1} A {rx} {ry} {x_axis_rotation:f} 1 0 {x2} A {rx} {ry} {x_axis_rotation:f} 1 0 {x1}"

        reverse_start = False
        reverse_end = False
        self.__path(path, reverse_path, reverse_start, reverse_end, labels,
                    style)

    def rectangle(self, p1, p2, **style):
        r = Rectangle(p1, p2)
        self.polyline([r.northwest, r.northeast, r.southeast, r.southwest],
                      closed=True,
                      **style)

    def text(self, point, text, **style):

        def compute_anchors(position):
            if position == "center":
                x = 0
                y = 0
                valign = 'central'
                align = 'middle'
                return (x, y, align, valign)
            x = 0
            y = 0
            if position in ["above", "below"]:
                align = "middle"
                x = 0
            elif "left" in position:
                align = "end"
                x = -5
            else:
                x = 5
                align = "start"

            if position in ["left", "right"]:
                valign = "middle"
                y = 0
            elif "below" in position:
                valign = "hanging"
                y = 5
            else:
                valign = "text-top"
                y = -5
            return (x, y, align, valign)

        if "position" in style:
            position = style["position"]
            del style["position"]
        else:
            position = "center"
        (x, y, align, valign) = compute_anchors(position)

        text_style = {}
        self.parse_text_style(style, text_style)

        self.nodelayer += [
            f'<text x="{x}" y="{y}"   {dic_to_svglist(text_style)} text-anchor="{align}"  dominant-baseline="{valign}" transform="translate({self.svgtransform(self.transform(point))})">{text}</text>'
        ]

    def edge(self, points, labels=None, **style):

        tf = self.svgtransform * self.transform
        angles = list(
            map(lambda x: x * math.pi / 180, self.find_angles(points)))
        current_node = points[0]

        if "looseness" in style:
            looseness = style["looseness"]
            del style["looseness"]
        else:
            looseness = 1

        curve = []
        point = current_node
        for i in range(len(points) - 1):
            current_node = points[i + 1]
            newpoint = current_node
            dst = looseness * 0.3902 * newpoint.distance(point)
            fstcontrol = point + Point(dst, angles[i], polar=True)
            sndcontrol = newpoint - Point(dst, angles[i + 1], polar=True)
            curve += [(point, fstcontrol, sndcontrol, newpoint)]
            point = newpoint

        path = f"M {tf(curve[0][0])}"
        for (a, b, c, d) in curve:
            path += f"C {tf(b)} {tf(c)} {tf(d)}"

        curve.reverse()
        reverse_path = f"M {tf(curve[0][3])}"
        for (a, b, c, d) in curve:
            reverse_path += f"C {tf(c)} {tf(b)} {tf(a)}"

        # todo: on peut faire mieux je pense
        reverse_start = abs((points[1] - points[0]).angle) > math.pi / 2
        reverse_end = abs((points[-1] - points[-2]).angle) > math.pi / 2
        self.__path(path, reverse_path, reverse_start, reverse_end, labels,
                    style)

    def polyline(self, points, labels=None, closed=False, **style):
        tf = self.svgtransform * self.transform

        if closed:
            points += [points[0]]

        if "rounded" in style and style["rounded"] and len(points) != 2:
            path = ""
            reverse_path = ""
            for i in range(len(points) - 2):
                p0 = points[i]
                p1 = points[i + 1]
                p2 = points[i + 2]
                if p1.distance(p2) > p0.distance(p1):
                    ratio = min(12, p1.distance(p2) / p0.distance(p1))
                    t1 = 0.04 * ratio
                    t2 = 0.04
                else:
                    ratio = min(12, p0.distance(p1) / p1.distance(p2))
                    t1 = 0.04
                    t2 = 0.04 * ratio
                beforep1 = p0 * t1 + p1 * (1 - t1)
                afterp1 = p1 * (1 - t2) + p2 * t2
                path += f" L {tf(beforep1)}"
                path += f" Q {tf(p1)} {tf(afterp1)}"
                # reverse_path starts from p2, goes to afterp1
                reverse_path = f" Q {tf(p1)} {tf(beforep1)}" + reverse_path
                reverse_path = f" L {tf(afterp1)}" + reverse_path
            if not closed:
                path = f"M {tf(points[0])}" + path + f" L {tf(p2)}"
                reverse_path = f"M {tf(p2)}" + reverse_path + f"L {tf(points[0])}"
            else:
                p0 = points[-2]
                p1 = points[0]
                p2 = points[1]
                if p1.distance(p2) > p0.distance(p1):
                    ratio = min(12, p1.distance(p2) / p0.distance(p1))
                    t1 = 0.04 * ratio
                    t2 = 0.04
                else:
                    ratio = min(12, p0.distance(p1) / p1.distance(p2))
                    t1 = 0.04
                    t2 = 0.04 * ratio
                beforep1 = p0 * t1 + p1 * (1 - t1)
                afterp1 = p1 * (1 - t2) + p2 * t2
                path = f"M {tf(afterp1)}" + path + f" L {tf(beforep1)} Q {tf(p1)} {tf(afterp1)}"
                reverse_path = f"M {tf(afterp1)} Q {tf(p1)} {tf(beforep1)}" + reverse_path + f" L {tf(afterp1)}"
        else:
            # not rounded
            path = f"M {tf(points[0])} L " + " ".join(
                str(tf(p)) for p in points[1:])
            reverse_path = f"M {tf(points[-1])} L " + " ".join(
                str(tf(p)) for p in points[-2::-1])

        # todo: on peut faire mieux je pense
        reverse_start = abs((points[1] - points[0]).angle) > math.pi / 2
        reverse_end = abs((points[-1] - points[-2]).angle) > math.pi / 2
        self.__path(path, reverse_path, reverse_start, reverse_end, labels,
                    style)

    def draw(self, rect, fs=None, commands="", preamble=False):
        tf = self.svgtransform * self.transform
        rect = Rectangle.bounding_box([
            *map(tf, [
                rect.northwest, rect.northeast, rect.southeast, rect.southwest
            ])
        ])

        print(
            fr'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{rect.width}" height="{rect.height}" viewBox="{rect.fst.x} {rect.fst.y} {rect.width} {rect.height}">',
            file=fs)
        print("\n".join(self.edgelayer), file=fs)
        print("\n".join(self.nodelayer), file=fs)
        print(r'</svg>', file=fs)


register_layer('svg', SvgLayer)
"""
from io import StringIO
from Diagrams.Core import Diagram
def repr_jupyter(d):
        f = StringIO()
        d.draw(f, output='svg')
        return f.getvalue()


Diagram._repr_html_ = repr_jupyter
"""
