"""Module that provides the TIKZ Layer"""

# pylint: disable=invalid-name
import math

from pygf.geometry import Point, Rectangle
from pygf.layer import Layer

ALMOST_ZERO = 0.01


def dic_to_list(d):
    "convert a dictionary to a list string"
    return ",".join(x + "=" + y if y is not None else x for (x, y) in d.items())


def _escape(x):
    "escape latex symbols (rudimentary)"
    x = x.replace("_", r"\_")
    x = x.replace("^", r"\^{}")
    return x


class TikzLayer(Layer):
    """The Tikz Layer"""

    def __init__(self, transform=None):
        Layer.__init__(self, transform)
        self.layers = {0: [], 1: []}
        self.names = 0

    def add_to_layer(self, z_index, x):
        """helper function"""
        if z_index not in self.layers:
            self.layers[z_index] = []
        self.layers[z_index].append(x)

    def picture(self, point, img_name, width, height, *, z_index=1):
        # pictures are NOT subject to the transform (only the position is)
        self.add_to_layer(
            z_index,
            rf"\node at ({self.transform(point)}) "
            rf"{{\includegraphics[width={width:f}cm, height={height:f}cm]"
            f"{{{img_name}}}}};",
        )

    def text(self, point, text, z_index=1, **hints):
        #  text is NOT subject to the transform (only the position is)
        text = str(text)
        opts = {}
        self._parse_text(hints, opts)
        if "position" in hints:
            x = hints.pop("position")
            if x == "center":
                pass
            else:
                opts.update({x: None})
        opts.update(hints)
        self.add_to_layer(
            z_index,
            f"\\node[{dic_to_list(opts)}] at ({self.transform(point)})" f"{{{_escape(text)}}};",
        )

    def circle(self, p1, radius, labels=None, z_index=1, **style):
        tf = self.transform

        pointx = tf(Point(radius, 0) + p1)
        pointy = tf(Point(0, radius) + p1)

        rx = tf(p1).distance(pointx)
        ry = tf(p1).distance(pointy)

        x = tf(p1)

        x_axis_rotation = tf(Point(radius, 0)).angle * 180 / math.pi

        tikz_style = {}
        self._parse_style(style, tikz_style)
        tikz_style.update(style)
        if rx != ry:
            self.add_to_layer(
                z_index,
                f"\\path[{dic_to_list(tikz_style)}] ({x}) "
                f"circle[x radius={rx:2f}, y radius={ry:2f}, rotate={x_axis_rotation:2f}];",
            )
        else:
            self.add_to_layer(
                z_index,
                f"\\path[{dic_to_list(tikz_style)}] ({x}) " f"circle[radius={rx:2f}];",
            )

    def rectangle(self, p1, p2, z_index=1, **style):
        r = Rectangle(p1, p2)
        tikz_style = {}
        self._parse_style(style, tikz_style)
        tikz_style.update(style)
        (sw, se, nw, ne) = map(self.transform, (r.southwest, r.southeast, r.northwest, r.northeast))
        self.add_to_layer(
            z_index,
            f"\\path[{dic_to_list(tikz_style)}]" f"({sw}) -- ({se}) -- ({ne}) -- ({nw}) -- cycle;",
        )

    def _parse_thickness(self, gen_style, tikz_style):
        if "thickness" not in gen_style:
            return
        dic = {
            0.25: "ultra thin",  # 0.1pt
            0.5: "very thin",  # 0.2pt
            1: "thin",  # 0.4pt
            1.5: "semithick",  # 0.6pt
            2: "thick",  # 0.8pt
            3: "very thick",  # 1.2pt
            4: "ultra thick",  # 1.6pt
        }
        thick = gen_style.pop("thickness")
        if thick in dic:
            tikz_style.update({dic[thick]: None})
        else:
            tikz_style.update({"line width": f"{0.4*thick:.3g}pt"})

    def _parse_dashness(self, gen_style, tikz_style):
        if "dash" not in gen_style:
            return

        dash = gen_style.pop("dash")
        if dash not in [
            "solid",
            "dotted",
            "densely dotted",
            "loosely dotted",
            "dashed",
            "densely dashed",
            "loosely dashed",
            "dashdotted",
            "dash dot",
            "densely dashdotted",
            "densely dash dot",
            "loosely dashdotted",
            "loosely dash dot",
            "dashdotdotted",
            "densely dashdotdotted",
            "loosely dashdotdotted",
            "dash dot dot",
            "densely dash dot dot",
            "loosely dash dot dot",
        ]:
            raise ValueError

        tikz_style.update({dash: None})

    def _parse_fillness(self, gen_style, tikz_style):
        if "fill" not in gen_style:
            return
        fill = gen_style.pop("fill")
        tikz_style.update({"fill": fill})
        if "opacity" in gen_style:
            tikz_style.update({"fill opacity": gen_style.pop("opacity")})

    def _parse_drawness(self, gen_style, tikz_style):
        if "draw" not in gen_style:
            tikz_style.update({"draw": "black"})
            return
        color = gen_style.pop("draw")
        if color is not None:
            tikz_style.update({"draw": color})

    def _parse_arrows(self, gen_style, tikz_style):

        leftarrows = {
            "": "",
            ">": ">",
            "<": "<",
            "x": "Rays",
            "xetal": "latex",
            "latex": "latex reversed",
        }
        rightarrows = {
            "": "",
            ">": ">",
            "<": "<",
            "x": "Rays",
            "xetal": "latex reversed",
            "latex": "latex",
        }
        if "arrow" not in gen_style:
            return
        [first, last] = gen_style.pop("arrow").split("-")

        arrow = f"{leftarrows[first]}-{rightarrows[last]}"
        tikz_style.update({arrow: None})

    def _parse_text(self, gen_style, tikz_style):
        if "text_color" in gen_style:
            text_color = gen_style.pop("text_color")
            tikz_style.update({"color": text_color})

        if not ("font_family" in gen_style or "text_size" in gen_style):
            return
        font = ""
        if "text_size" in gen_style:
            text_size = gen_style.pop("text_size")
            dic = {"small": r"\tiny", "large": r"\large"}
            font = dic[text_size]
        if "font_family" in gen_style:
            family = gen_style.pop("font_family")
            dic = {"monospace": r"\ttfamily"}
            font += dic[family]

        tikz_style.update({"font": font})

    def _parse_style(self, style, tikz_style):
        self._parse_thickness(style, tikz_style)
        self._parse_dashness(style, tikz_style)
        self._parse_drawness(style, tikz_style)
        self._parse_fillness(style, tikz_style)
        self._parse_arrows(style, tikz_style)
        self._parse_text(style, tikz_style)
        if style.get("rounded"):
            del style["rounded"]
            tikz_style.update({"rounded corners": None})

    def convert_angle(self, angle):
        """convert the angle according to the transform and round"""
        p = Point(1, angle * math.pi / 180, polar=True)
        p = self.transform(p)
        a = p.angle * 180 / math.pi
        return int(a * 10 + 0.5) / 10

    def line(self, p1, p2, labels=None, *, z_index=0, **style):
        (p1, p2) = map(self.transform, (p1, p2))
        s = ""
        if style is None:
            style = {}
        tikz_style = {}
        self._parse_style(style, tikz_style)
        tikz_style.update(style)
        s += f"\\path[{dic_to_list(tikz_style)}] ({p1}) -- ({p2})"

        if (abs((p2 - p1).angle) - math.pi / 2) < ALMOST_ZERO:
            # hack
            reverse_start = False
        else:
            reverse_start = abs((p2 - p1).angle) > math.pi / 2
        reverse_end = reverse_start

        if labels is not None:
            for label in labels:
                text = _escape(labels[label])

                if label == "above":
                    s += " node [sloped,pos=0.5,above]"
                elif label == "below":
                    s += " node [sloped,pos=0.5,below]"
                elif label == "above start":
                    s += f" node [sloped,pos=0,above {'right' if not reverse_start else 'left'}]"
                elif label == "below start":
                    s += f" node [sloped,pos=0,below {'right' if not reverse_start else 'left'}]"
                elif label == "above end":
                    s += f" node [sloped,pos=1,above {'left' if not reverse_end else 'right'}]"
                elif label == "below end":
                    s += f" node [sloped,pos=1,below {'left' if not reverse_end else 'right'}]"
                s += f"{{{text}}}"
        self.add_to_layer(z_index, s + ";")

    def edge(self, points, labels=None, *, closed=False, z_index=0, **style):
        list_angles = self.find_angles(points, closed=closed)
        if closed:
            points.append(points[0])
            list_angles.append(list_angles[0])

        points = [*map(self.transform, points)]

        s = ""

        looseness = style.pop("looseness", 1)
        tikz_style = {}
        self._parse_style(style, tikz_style)
        tikz_style.update(style)

        list_edges = [f"({points[0]})"]
        for i in range(len(points) - 1):
            out_angle = self.convert_angle(list_angles[i])
            in_angle = self.convert_angle(180 + list_angles[i + 1])
            s = f" to[out={out_angle:3.3g}, in={in_angle:3.3g}"
            if looseness != 1:
                s += f", looseness={looseness:3.3g}"
            s += "]"
            list_edges.append(s)
            list_edges.append(f"({points[i+1]})")

        reverse_start = abs((points[1] - points[0]).angle) > math.pi / 2
        reverse_end = abs((points[-1] - points[-2]).angle) > math.pi / 2

        if labels is not None:
            for label in labels:
                text = _escape(labels[label])
                if label == "above start":
                    code = f"node [sloped,pos=0,above {'right' if not reverse_start else 'left'}]"
                    code += f"{{{text}}} "
                    list_edges[1] = list_edges[1] + code
                elif label == "below start":
                    code = f"node [sloped,pos=0,below {'right' if not reverse_start else 'left'}]"
                    code += f"{{{text}}} "
                    list_edges[1] = list_edges[1] + code
                elif label == "above":
                    code = "node [sloped,pos=0.5,above]"
                    code += f"{{{text}}} "
                    n = (len(list_edges) - 1) // 2
                    n = 2 * (n // 2) + 1
                    list_edges[n] = list_edges[n] + code
                elif label == "below":
                    code = "node [sloped,pos=0.5,below]"
                    code += f"{{{text}}} "
                    n = (len(list_edges) - 1) // 2
                    n = 2 * (n // 2) + 1
                    list_edges[n] = list_edges[n] + code
                elif label == "above end":
                    code = f" node [sloped,pos=1,above {'left' if not reverse_end else 'right'}]"
                    code += f"{{{text}}}"
                    list_edges[-2] = list_edges[-2] + code
                elif label == "below end":
                    code = f" node [sloped,pos=1,below {'left' if not reverse_end else 'right'}]"
                    code += f"{{{text}}}"
                    list_edges[-2] = list_edges[-2] + code

        s = rf"\path[{dic_to_list(tikz_style)}] " + " ".join(list_edges)

        self.add_to_layer(z_index, s + ";")

    def polyline(self, points, labels=None, *, closed=False, z_index=0, **style):
        points = [*map(self.transform, points)]

        if style is None:
            style = {}

        tikz_style = {}
        self._parse_style(style, tikz_style)
        tikz_style.update(style)

        reverse_start = abs((points[1] - points[0]).angle) > math.pi / 2
        if closed:
            reverse_end = abs((points[0] - points[-1]).angle) > math.pi / 2
        else:
            reverse_end = abs((points[-1] - points[-2]).angle) > math.pi / 2

        list_edges = [f"({points[0]})"]
        for i in range(len(points) - 1):
            list_edges.append("--")
            list_edges.append(f"({points[i+1]})")

        if closed:
            list_edges.append("--")
            list_edges.append("cycle")

        if labels is not None:
            for label in labels:
                text = _escape(labels[label])
                if label == "above start":
                    code = f"node [sloped,pos=0,above {'right' if not reverse_start else 'left'}]"
                    code += f"{{{text}}} "
                    list_edges[1] = list_edges[1] + code
                elif label == "below start":
                    code = f"node [sloped,pos=0,below {'right' if not reverse_start else 'left'}]"
                    code += f"{{{text}}} "
                    list_edges[1] = list_edges[1] + code
                elif label == "above":
                    code = "node [centered, sloped,pos=0.5,above]"
                    code += f"{{{text}}} "
                    n = (len(list_edges) - 1) // 2
                    n = 2 * (n // 2) + 1
                    list_edges[n] = list_edges[n] + code
                elif label == "below":
                    code = "node [centered, sloped,pos=0.5,below]"
                    code += f"{{{text}}} "
                    n = (len(list_edges) - 1) // 2
                    n = 2 * (n // 2) + 1
                    list_edges[n] = list_edges[n] + code
                elif label == "above end":
                    code = f" node [sloped,pos=1,above {'left' if not reverse_end else 'right'}]"
                    code += f"{{{text}}}"
                    list_edges[-2] = list_edges[-2] + code
                elif label == "below end":
                    code = f" node [sloped,pos=1,below {'left' if not reverse_end else 'right'}]"
                    code += f"{{{text}}}"
                    list_edges[-2] = list_edges[-2] + code

        s = rf"\path[{dic_to_list(tikz_style)}] " + " ".join(list_edges)

        self.add_to_layer(z_index, s + ";")

    def draw(self, rect, fs=None, options=None, *, preamble=False):
        if options is None:
            options = {}

        if preamble:
            print(
                r"""\documentclass{standalone}
\usepackage[svgnames]{xcolor}
\usepackage{tikz}
\usepackage{mathtools}
\usetikzlibrary{backgrounds,shapes.geometric,arrows.meta}
            """,
                file=fs,
            )

            print(r"\begin{document}", file=fs)

        clip = options.pop("clip", True)

        if options == {}:
            print(r"\begin{tikzpicture}", file=fs)
        else:
            if "center" in options:
                if options.get("center"):
                    options["baseline"] = "(current bounding box.center)"
            print(rf"\begin{{tikzpicture}}[{dic_to_list(options)}]", file=fs)

        tf = self.transform

        rect = Rectangle.bounding_box(
            [*map(tf, [rect.northwest, rect.northeast, rect.southeast, rect.southwest])]
        )

        if clip:
            print(rf"\clip ({rect.northwest}) rectangle ({rect.southeast});", file=fs)
        for i in sorted(self.layers.keys()):
            print("\n".join(self.layers[i]), file=fs, end="\n")
        print(r"\end{tikzpicture}", file=fs)
        if preamble:
            print(r"\end{document}", file=fs)
