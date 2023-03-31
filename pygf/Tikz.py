from .Layer import Layer
from .Options import Options, register_layer, getStyle
from .Geometry import Point, Rectangle
import math
""" code pour gérer tikz """

def dic_to_list(d):
    return ','.join(x+'='+y if y is not None else x for (x,y) in d.items())


### escape latex symbols (rudimentary)
def escape(x):
    x = x.replace('_', r"\_")
    x = x.replace('^', r"\^{}")
    return x

class TikzLayer(Layer):
    def __init__(self, transform = None):
        Layer.__init__(self, transform)
        self.nodelayer = ""
        self.edgelayer = ""
        self.names = 0


    def picture(self, point, img_name, width, height):
        # pictures are NOT subject to the transform (only the position is)
        self.nodelayer += "\\node at ({position}) {{\includegraphics[width={w:f}cm, height={h:f}cm]{{{name}}}}};\n".format(position=self.transform(point), name=img_name, h=height, w=width)
        
    def text(self, point, text, **hints):
        #  text is NOT subject to the transform (only the position is)
        text = str(text)
        opts = {}
        self.parse_text(hints, opts)
        if 'position' in hints:
            x = hints['position']
            del hints['position']
            if x == 'center':
                pass
            else:
                opts.update({x: None})                
        opts.update(hints)                    
        self.nodelayer += "\\node[{opts}] at ({position}) {{{text}}};\n".format(opts=dic_to_list(opts), text=escape(text), position=self.transform(point))
        

    def circle(self, p1, radius, **style):
        tf = self.transform

        pointx = tf(Point(radius,0)+p1)
        pointy = tf(Point(0, radius)+p1)

        rx = tf(p1).distance(pointx)
        ry = tf(p1).distance(pointy)
        
        x1 = tf(p1+Point(radius, 0))
        x2 = tf(p1-Point(radius, 0))
        x = tf(p1)
        
        x_axis_rotation = tf(Point(radius,0)).angle*180/math.pi

        tikz_style={}
        self.parse_style(style, tikz_style)
        tikz_style.update(style)
        if rx != ry:
            self.edgelayer += f"\\path[{dic_to_list(tikz_style)}] ({x}) circle[x radius={rx:2f}, y radius={ry:2f}, rotate={x_axis_rotation:2f}];\n"
        else:
            self.edgelayer += f"\\path[{dic_to_list(tikz_style)}] ({x}) circle[radius={rx:2f}];\n"
                 
    def rectangle(self, p1, p2, **style):
        r = Rectangle(p1,p2)
        tikz_style={}
        self.parse_style(style, tikz_style)
        tikz_style.update(style)
        (sw,se,nw,ne) = map(self.transform, (r.southwest,r.southeast, r.northwest, r.northeast))
        self.nodelayer += f"\\path[{dic_to_list(tikz_style)}] ({sw}) -- ({se}) -- ({ne}) -- ({nw}) -- cycle;\n"
        
         
    def new_brace(self, end, path, msg):
        if len(path) != 1:
            raise ("exception")
        end = end[0]
        start = path[0][0]
        self.edgelayer += r"\draw [decorate,decoration={brace,amplitude=10pt},xshift=-4pt] (%d.center) -- (%d.center) node [black,midway,xshift=-1cm] {%s};" % (self.nodes[end], self.nodes[start], msg)+"\n"


    def parse_thickness(self, gen_style, tikz_style):
        if not "thickness" in gen_style:
            return
        dic = {
            0.25: "ultra thin", #0.1pt
            0.5: "very thin", #0.2pt
            1 : "thin",  # 0.4pt
            1.5: "semithick", # 0.6pt
            2: "thick", # 0.8pt
            3: "very thick", #1.2pt
            4: "ultra thick"} #1.6pt
        thick = gen_style["thickness"]
        if thick in dic:
            tikz_style.update({dic[thick]: None})
        else:
            tikz_style.update({"line width": "{thick:.3g}pt".format(thick=0.4*thick)})
        del gen_style["thickness"]


    def parse_dashness(self, gen_style, tikz_style):
        if not "dash" in gen_style:
            return
        dash = gen_style["dash"]
        if dash == "solid":
            return
        elif dash == "dotted":
            tikz_style.update({"dotted": None})
        elif dash == "dashed":
            tikz_style.update({"dashed": None})
        del gen_style["dash"]

    def parse_fillness(self, gen_style, tikz_style):
        if not "fill" in gen_style:
            return
        fill = gen_style["fill"]
        tikz_style.update({"fill": fill})
        if "opacity" in gen_style:
            tikz_style.update({"fill opacity": gen_style["opacity"]})
            del gen_style["opacity"]
        del gen_style["fill"]

    def parse_drawness(self, gen_style, tikz_style):
        if not "draw" in gen_style:
            tikz_style.update({"draw": "black"})            
            return
        color = gen_style["draw"]
        if color is not None:
            tikz_style.update({"draw": color})            
        del gen_style["draw"]
        
    def parse_arrows(self, gen_style, tikz_style):
        arrows = {'->': '->', '-x' : '-Rays' }        
        if not "arrow" in gen_style:
            return
        arrow = arrows[gen_style["arrow"]]
        tikz_style.update({arrow: None})
        del gen_style["arrow"]

    def parse_text(self, gen_style, tikz_style):
        if not ("text_size" in gen_style or "font_family" in gen_style):
            return
        font = ""
        if "text_size" in gen_style:
            text_size = gen_style["text_size"]
            dic = {"small" : r"\tiny" , "large": r"\large"}
            font = dic[text_size]
            del gen_style["text_size"]
        if "font_family" in gen_style:
            family = gen_style["font_family"]
            dic = {"monospace" : r"\ttfamily" }
            font += dic[family]
            del gen_style["font_family"]
            
        tikz_style.update({"font" : font})
            

        

    def parse_style(self, style, tikz_style):
        self.parse_thickness(style, tikz_style)
        self.parse_dashness(style, tikz_style)
        self.parse_drawness(style, tikz_style)
        self.parse_fillness(style, tikz_style)
        self.parse_arrows(style, tikz_style)
        self.parse_text(style, tikz_style)
        if "rounded" in style and style["rounded"]:
            del style["rounded"]
            tikz_style.update({"rounded corners": None})
        
        

    def convert_angle(self, angle):
        p = Point(1, angle*math.pi/180, polar=True)
        p = self.transform(p)
        a = p.angle * 180/math.pi
        return int(a*10+0.5)/10        
        

    def line(self, p1, p2, labels = None, **style):
        (p1,p2) = map(self.transform, (p1,p2))
        s = ""
        if style is None:
            style = {}
        tikz_style={}
        self.parse_style(style, tikz_style)
        tikz_style.update(style)
        s += "\\path[%s] (%s) -- (%s)" % (dic_to_list(tikz_style),p1, p2)

        if (abs((p2 - p1).angle) - math.pi/2) < 0.01:
            # hack 
            reverse_start = False
        else:            
            reverse_start = abs((p2 - p1).angle) > math.pi/2
        reverse_end = reverse_start


        if labels is not None:
             if "above" in labels:
                  s += f"node [sloped,pos=0.5,above ] {{{labels['above']}}} " 
             if "below" in labels:
                  s += f"node [sloped,pos=0.5,below ] {{{labels['below']}}} " 
             if "above start" in labels:
                  s += f"node [sloped,pos=0,above {'right' if not reverse_start else 'left'} ] {{{labels['above start']}}} " 
             if "below start" in labels:
                  s += f"node [sloped,pos=0,below {'right' if not reverse_start else 'left'}] {{{labels['below start']}}} " 
             if "above end" in labels:
                  s += f"node [sloped,pos=1,above {'left' if not reverse_end else 'right'}] {{{labels['above end']}}} " 
             if "below end" in labels:
                  s += f"node [sloped,pos=1,below {'left' if not reverse_end else 'right'}] {{{labels['below end']}}} " 
        self.edgelayer+= s + ";\n"



        
    def edge(self, points, labels = None, **style):
        l = self.find_angles(points)
        points = [*map(self.transform, points)]
        
        current_node = points[0]
        s = ""
        if style is None:
            style = {}

        if "looseness" in style:
            looseness = style["looseness"]
            del style["looseness"]
        else:
            looseness = 1
        tikz_style={}
        self.parse_style(style, tikz_style)
        tikz_style.update(style)
        s += "\\path[%s] (%s)" % (dic_to_list(tikz_style),points[0])
            
        for i in range(len(points)-1):
            current_node = points[i+1]
            if looseness != 1:
                s += " to[out=%3.3g, in=%3.3g, looseness=%3.3g] (%s) " % (self.convert_angle(l[i]),self.convert_angle(180+l[i+1]), looseness, current_node)
            else:
                s += " to[out=%3.3g, in=%3.3g] (%s) " % (self.convert_angle(l[i]),self.convert_angle(180+l[i+1]), current_node)

        reverse_start = abs((points[1] - points[0]).angle) > math.pi/2
        reverse_end = abs((points[-1] - points[-2]).angle) > math.pi/2

        if labels is not None:
             if "above start" in labels:
                  s += f"node [sloped,pos=0,above {'right' if not reverse_start else 'left'} ] {{{labels['above start']}}} " 
             if "below start" in labels:
                  s += f"node [sloped,pos=0,below {'right' if not reverse_start else 'left'}] {{{labels['below start']}}} " 
             if "above end" in labels:
                  s += f"node [sloped,pos=100,above {'left' if not reverse_end else 'right'}] {{{labels['above end']}}} " 
             if "below end" in labels:
                  s += f"node [sloped,pos=0,below {'left' if not reverse_end else 'right'}] {{{labels['below end']}}} " 
        self.edgelayer+= s + ";\n"

    def polyline(self, points, labels = None, closed = False, **style):
        if style is None:
            style = {}

        tikz_style={}
        self.parse_style(style, tikz_style)
        tikz_style.update(style)

        reverse_start = abs((points[1] - points[0]).angle) > math.pi/2
        if closed:
            reverse_end = abs((points[0] - points[-1]).angle) > math.pi/2
        else:
            reverse_end = abs((points[-1] - points[-2]).angle) > math.pi/2

        listpoints = list(map(lambda x: f"({x})", points))
        if closed:
            listpoints += ["cycle"]
            
        if labels is not None:
             if "above start" in labels:
                 listpoints[1] = listpoints[1] + f"node [sloped,pos=0,above {'right' if not reverse_start else 'left'} ] {{{labels['above start']}}} " 
             if "below start" in labels:
                 listpoints[1] = listpoints[1] + f"node [sloped,pos=0,below {'right' if not reverse_start else 'left'}] {{{labels['below start']}}} " 
             if "above end" in labels:
                 listpoints[-1] = listpoints[-1] + f"node [sloped,pos=100,above {'left' if not reverse_end else 'right'}] {{{labels['above end']}}} " 
             if "below end" in labels:
                 listpoints[-1] = listpoints[-1] + f"node [sloped,pos=0,below {'left' if not reverse_end else 'right'}] {{{labels['below end']}}} "

        s = "\\path[%s] " % dic_to_list(tikz_style) + "--".join(listpoints)
        
        self.edgelayer+= s + ";\n"
                
    def draw(self, rect,f, options = None, preamble = False):
        if options is None:
            options = {}

        if preamble:
            print(r"""\documentclass{standalone}
\usepackage[svgnames]{xcolor}            
\usepackage{tikz}
\usepackage{mathtools}
\usetikzlibrary{backgrounds,shapes.geometric,arrows.meta}
            """, file = f)

            print(r"\begin{document}", file = f)
            
        if options == {}:
            print(r"\begin{tikzpicture}", file = f)
        else:
            if "center" in options:
                if options["center"] == True:
                    options["baseline"] = "(current bounding box.center)"
                del options["center"]
            print(r"\begin{tikzpicture}[%s]" % dic_to_list(options), file = f)

        tf = self.transform

        rect = Rectangle.bounding_box([*map(tf, [rect.northwest, rect.northeast, rect.southeast, rect.southwest])])

        print(rf"\clip ({rect.northwest}) rectangle ({rect.southeast});", file=f)
        print(self.edgelayer, file = f, end="")
        print(self.nodelayer, file = f, end="")
        print(r"\end{tikzpicture}", file = f)
        if preamble:
            print(r"\end{document}", file=f)
            


register_layer('tikz',TikzLayer)
        
