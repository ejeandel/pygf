from .Layer import Layer
from .Geometry import Point, Rectangle, Transform
from .Options import Options, register_layer
import math
import base64
import sys
def dic_to_svglist(d):    
    return ' '.join(f'{x}="{y}"' for (x,y) in d.items())

class SvgLayer(Layer):
    def __init__(self, transform = None):
        Layer.__init__(self, transform)
        self.nodes = {}
        self.names = 0
        self.nodelayer = []
        self.edgelayer = []
        self.defs = {}
        self.svgtransform = Transform(50,-50)

        self.arrows = {
            "->": '<marker id="marker_{_id}"  markerUnits = "userSpaceOnUse" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polyline points="0 0, 10 3.5, 0 7" /></marker>',
            "-x": '<marker id="marker_{_id}"  markerUnits = "userSpaceOnUse" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto"><polyline points="0 0, 7 7" /><line x1="0" y1="7" x2="7" y2="0"  /></marker>'  
        }
        pass
       
    def new_name(self):
        self.names += 1
        return f"{self.names}"

    

    def picture(self, point, img_name, width, height):
        r = Rectangle(Point(0,0), self.svgtransform(Point(width, -height)))
        with open(img_name, 'rb') as f:
            data = f.read()
            self.nodelayer+= [f'<image xlink:href="data:image/png;base64,{str(base64.b64encode(data),"utf-8")}" transform="translate({self.svgtransform(point)-r.center})" width="{r.width}" height="{r.height}" preserveAspectRatio="none"/>']
            
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
        scale = 0.01 * self.svgtransform(Point(1,1)).x
        strokewidth = thickness * scale
        svg_style["stroke-width"] = f"{strokewidth:.2g}"

        """ ---------
            dash
            --------- """
        if "dash" in style:
            dash = style["dash"]
            del style["dash"]
            if dash == "dotted":
                svg_style["stroke-dasharray"] = f"{thickness * scale:.2g} {5*scale:.2g}"
            elif dash == "dashed":
                svg_style["stroke-dasharray"] = f"{6* scale:.2g} {6*scale:.2g}"

        """ -------
            draw
            -------- """
        if "draw" in style:
            color = style["draw"]
            del style["draw"]
            if color == None:
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
            if fill == None:
                fill = "none"
        else:
            fill = "none"
        svg_style["fill"] = fill

        
        #self.parse_arrows(style, svg_style) TODO

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
        

    def __path(self, path, reverse_path, reverse_start, reverse_end, labels = None, style = None):
        if style is None:
            style = {} #todo wire.wire_style
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
          
        if "clip" in style:
            r = style['clip']
            tf = self.svgtransform * self.transform            
            clip = f'<clipPath id="clip-{_id}"> <rect x="{tf(r.northwest).x}" y="{tf(r.northwest).y}" width="{(tf(r.northeast)-tf(r.northwest)).x}" height="{(tf(r.southwest)-tf(r.northwest)).y}" /></clipPath>'
            svg_style["clip-path"] = f'url(#clip-{_id})'
            del style["clip"]
        else:
            clip = ""
            

        self.edgelayer+= [f'{clip} <g  {dic_to_svglist(svg_style)} >  <path id="{_id}" d="{path}" /> {markers} </g>']

        if reverse_start or reverse_end:
            self.edgelayer+= [f'<path id="r-{_id}" d="{reverse_path}" display="none"/>']
            
        if labels is not None:
            for position in labels:

                label_style = {}
                label_style.update(text_style)
                
                text = labels[position]
                if "above" in position:
                    label_style["dy"] = -5
                else:
                    label_style["dy"] = 5
                    label_style["dominant-baseline"] = "hanging"

                if "start" in position:
                    label_style["text-anchor"] = "start" if not reverse_start else "end"
                    startOffset = 0 if not reverse_start else 100
                    mainpath = f"#{_id}"  if not reverse_start else f"#r-{_id}"
                elif "end" in position:
                    label_style["text-anchor"] = "end" if not reverse_end else "start"
                else:
                    label_style["text-anchor"] = "middle"
                    
                
                if "above start" == position:
                    self.nodelayer+= [f'<text  {dic_to_svglist(label_style)}  ><textPath href="{mainpath}" startOffset="{startOffset}%"> {text} </textPath></text>']
                elif "above" == position :
                    if not reverse_start:
                        self.nodelayer+= [f'<text   {dic_to_svglist(label_style)} ><textPath href="#{_id}" startOffset="50%"> {text} </textPath></text>']
                    else:
                        self.nodelayer+= [f'<text  {dic_to_svglist(label_style)} ><textPath href="#r-{_id}" startOffset="50%"> {text} </textPath></text>']
                elif  "above end" == position:
                    if not reverse_end:
                        self.nodelayer+= [f'<text  {dic_to_svglist(label_style)} ><textPath href="#{_id}"  startOffset="100%"> {text} </textPath></text>']
                    else:
                        self.nodelayer+= [f'<text  {dic_to_svglist(label_style)} ><textPath href="#r-{_id}"> {text} </textPath></text>']
                elif "below start" == position:
                    self.nodelayer+= [f'<text  {dic_to_svglist(label_style)}  ><textPath href="{mainpath}" startOffset="{startOffset}%"> {text} </textPath></text>']
                elif  "below end" == position:
                    if not reverse_end:
                        self.nodelayer+= [f'<text  {dic_to_svglist(label_style)}><textPath href="#{_id}"  startOffset="100%"> {text} </textPath></text>']
                    else:
                        self.nodelayer+= [f'<text  {dic_to_svglist(label_style)}><textPath href="#r-{_id}"> {text} </textPath></text>']
                elif "below" == position:
                    if not reverse_end:
                        self.nodelayer+= [f'<text  {dic_to_svglist(label_style)}><textPath href="#{_id}"  startOffset="50%"> {text} </textPath></text>']
                    else:
                        self.nodelayer+= [f'<text  {dic_to_svglist(label_style)}><textPath href="#r-{_id}" startOffset="50%"> {text} </textPath></text>']
                    
        
    def line(self, p1, p2, labels = None, **style):

        tf = self.svgtransform * self.transform
        path = f"M {tf(p1)} L {tf(p2)}"
        reverse_path = f"M {tf(p2)} L {tf(p1)}"
                
        reverse_start = abs((p2 - p1).angle) > math.pi/2
        reverse_end = reverse_start
        self.__path(path, reverse_path, reverse_start, reverse_end, labels, style)

    def circle(self, p1, radius, labels = None, **style):

        tf = self.svgtransform * self.transform
        r = tf(Point(radius,0)).distance(tf(Point(0,0)))

        x1 = tf(p1+Point(radius, 0))
        x2 = tf(p1-Point(radius, 0))
        path = f"M {x1} a {r} {r} 0 1 1 {x2 - x1} a {r} {r} 0 1 1 {x1 - x2}"
        reverse_path = f"M {x2} a {r} {r} 0 1 0 {x1 - x2} a {r} {r} 0 1 0 {x2 - x1}"        
        
        reverse_start = False
        reverse_end = False
        self.__path(path, reverse_path, reverse_start, reverse_end, labels, style)
        
 
        
    def rectangle(self, p1, p2, **style):
        tf = self.svgtransform * self.transform
        r = Rectangle(p1,p2)
        svg_style = {}
        self.parse_style(style, svg_style)
        if "rounded" in style and style["rounded"]:
            svg_style.update({"rx": "2%"})            
        #self.nodelayer += [f'<polygon  points="{tf(r.southeast)} {tf(r.southwest)} {tf(r.northwest)} {tf(r.northeast)}" {dic_to_svglist(svg_style)}/>']
        self.nodelayer += [f'<rect x="{tf(r.northwest).x}" y="{tf(r.northwest).y}" width="{(tf(r.northeast)-tf(r.northwest)).x}" height="{(tf(r.southwest)-tf(r.northwest)).y}" {dic_to_svglist(svg_style)}/>']        
                
            

    
    def text(self, point, text, **style):
        def compute_anchors(position):
            if position == "center":
                x = 0
                y = 0
                valign='central'
                align='middle'
                return (x,y,align, valign)                
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
            return (x,y,align, valign)
        
        if "position" in style:
            position = style["position"]
            del style["position"]
        else:
            position = "center"
        (x,y,align,valign) = compute_anchors(position)

        text_style = {}
        self.parse_text_style(style, text_style)        
        
        self.nodelayer += [f'<text x="{x}" y="{y}"   {dic_to_svglist(text_style)} text-anchor="{align}"  dominant-baseline="{valign}" transform="translate({self.svgtransform(point)})">{text}</text>']
        


        
    def do_style(self, style):
        r = 0.1
        thickness = 1        
        attributes = {}
        attributes['vector-effect'] = "non-scaling-stroke"
        object_transform = Transform(1,1)

            
        attributes["fill"] = style["fill"] if "fill" in style else "none"
        if "draw" in style:
            if style["draw"] != '':
                attributes["stroke"] = style["draw"]
            else:
                attributes["stroke"] = "black"
        else:
            attributes["stroke"] = "black"
        scale = (self.svgtransform(Point(1,1))).x
        attributes["stroke-width"] = "%.3g" % (0.03*scale)
        return dic_to_svglist(attributes)
        
        

    
    def parse_style_old(self, style, pos):
        r = 0.1
        thickness = 1        
        attributes = {}
        attributes['vector-effect'] = "non-scaling-stroke"
        attributes['transform'] = f"translate({self.svgtransform(pos)})"
        object_transform = Transform(1,1)

            
        attributes["fill"] = style["fill"] if "fill" in style else "none"
        if "draw" in style:
            if style["draw"] != '':
                attributes["stroke"] = style["draw"]
            else:
                attributes["stroke"] = "black"
        else:
            attributes["stroke"] = "none"
        scale = (self.svgtransform(Point(1,1))).x
        attributes["stroke-width"] = "%.3g" % (0.01*scale)
        return dic_to_svglist(attributes)
        

    def do_text(self, style,pos, placement = lambda x:Point(0,0)):
        if not "label" in style:
            return
        
        def parse_position(position):
            angles = {'right': 0, 'above right': 45, 'above': 90, 'above left': 135,
                      'left': 180, 'below left': 225, 'below': 270, 'below right' : 315}
            if position in angles:
                return angles[position]
            else:
                try:
                    position = int(position)
                    if position < 0:
                        position = 360+position                
                    return position
                except:
                    raise TypeError
                
        def compute_anchors(position):
            x = 0
            y = 0
            if position in [92,91,90,89,88,268, 269,270,271,272]:
                align = "center"
                x = -50
            elif position < 90 or position > 270:
                align = "left"
                x = 0
            else:
                x = -100
                align = "right"

            if position in [358,359,0,1,2,178,179,180,181,182]:
                valign = "middle"
                y = -50
            elif position < 180:
                valign = "bottom"
                y = -100
            else:
                valign = "top"
                y = 0
            return (x,y,align, valign)
            
        if not "label_hints" in style:
            label_hints = {"label position": "right"}
        else:
            label_hints = style["label_hints"]
        position = label_hints["label position"] if "label position" in label_hints else "right"
        if position == "center":
            tpos = pos
            x = -50
            y = -50
            valign='middle'
            align='center'
        else:
            angle = parse_position(position)
            (x,y,align,valign)= compute_anchors(angle)
            where = placement(angle*math.pi/180)            
            tpos = pos + where
        self.nodelayer += [f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="0.2" text-anchor="center"  transform="translate({self.svgtransform(tpos)})">{style["label"]}</text>']

        pass

    def new_node(self, node):
        Layer.new_node(self, node)        
        if node.style is not None:
            st = {}
            st.update(node.style)
            if "style" in node.style:
                st.update(Options.styles[style['style']])
            style = st
            if not ("shape" in node.style):
                self.do_text(style, name, self.transform(node.position))
            elif style["shape"] == "circle":
                self.circle_node(node,self.transform(node.position))
            elif style["shape"] == "rectangle":
                self.rectangle_node(node.style, name, self.transform(pos))
        pass


    
    def edge(self, points, labels = None, **style):
       
        tf = self.svgtransform * self.transform
        angles = list(map(lambda x: x*math.pi/180, self.find_angles(points)))
        (current_node, _) = points[0]
        
        if "looseness" in style:
            looseness = style["looseness"]
            del style["looseness"]
        else:
            looseness = 1
                
        curve = []
        point=current_node
        for i in range(len(points)-1):            
            (current_node, _) = points[i+1]
            newpoint = current_node
            dst = looseness * 0.3951*newpoint.distance(point)
            fstcontrol = point + Point(dst, angles[i], polar=True)
            sndcontrol = newpoint - Point(dst, angles[i+1], polar=True)
            curve += [(point, fstcontrol, sndcontrol, newpoint)]
            point=newpoint
            

        path = f"M {tf(curve[0][0])}"
        for (a,b,c,d) in curve:
            path += f"C {tf(b)} {tf(c)} {tf(d)}"
        
        
        curve.reverse()
        reverse_path = f"M {tf(curve[0][3])}"
        for (a,b,c,d) in curve:
            reverse_path += f"C {tf(c)} {tf(b)} {tf(a)}"
            
        # todo: on peut faire mieux je pense
        reverse_start = abs((points[1][0] - points[0][0]).angle) > math.pi/2
        reverse_end = abs((points[-1][0] - points[-2][0]).angle) > math.pi/2
        self.__path(path, reverse_path, reverse_start, reverse_end, labels, style)
        

                

    def draw(self, rect,f= None, commands = "", preamble = False):
        x = self.svgtransform(self.transform(rect.fst))
        y = self.svgtransform(self.transform(rect.snd))
        rect = Rectangle(x,y)        
        print(fr'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{rect.width}" height="{rect.height}" viewBox="{rect.fst.x} {rect.fst.y} {rect.width} {rect.height}">', file=f)
        print("\n".join(self.edgelayer), file = f)
        print("\n".join(self.nodelayer), file = f)
        print(r'</svg>', file=f) 
            

register_layer('svg',SvgLayer)
        
"""
from io import StringIO
from Diagrams.Core import Diagram
def repr_jupyter(d):
        f = StringIO()
        d.draw(f, output='svg')
        return f.getvalue()

    
Diagram._repr_html_ = repr_jupyter
"""
