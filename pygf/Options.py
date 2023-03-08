from .Geometry import Transform
import math
DEBUG = False
#Layer = TikzLayer
#StyleOptions = TikzStyles

# static class
class Options:
    __slots__ = ()
    Output = None
    styles = { "none": {}, 'default_label': {"label position": "right"}}
    layers = {}
    transform = Transform()
    pass
    
def register_layer(name, myclass):
    Options.layers[name] = myclass


def use_layer(name = None, transform = None):
    tf = Options.transform
    if transform is not None:
        tf = transform*tf
    if name is None:
        return Options.layers[Options.Output](tf)
    else:
        return Options.layers[name](tf)
        
def _d_(x):
    return x[Options.Output]

def set_default_output(output):
    if not output in Options.layers :
        raise KeyError
    Options.Output = output
        
def setStyle(name, params):
    Options.styles[name] = params.copy()
    
def getStyle(name):
    return Options.styles[name]

def writeStyle(fn):
    Options.layers[Options.Output](Options.transform).writeStyle(fn)
    # TODO
    pass
#    Layer.writeStyle(fn)



def rotate(angle):
    Options.transform = Transform.Rotation(angle*math.pi/180) * Options.transform


def xscale(x):
    Options.transform = Transform(x,1) * Options.transform

def yscale(y):
    Options.transform = Transform(1,y) * Options.transform

    
