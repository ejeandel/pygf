import sys
import os
import os.path
from pygf.tikz import TikzLayer
from pygf.svg import SvgLayer
from pygf import params

import argparse    
parser = argparse.ArgumentParser(description='')
parser.add_argument('--tex', dest='tex', action="store_true", help='tex or svg output')
parser.add_argument('--dark', dest='dark', action="store_true", help='dark mode')

fn = sys.argv[0]
DN = os.path.dirname(fn)

if DN == "packets":
    parser.add_argument('filename')
    

args = parser.parse_args()

name = os.path.splitext(os.path.basename(fn))[0]    

if args.tex:
    layer = TikzLayer()
    fn = f"source/_static/{name}.tex"
else:
    layer = SvgLayer()
    if args.dark:
        fn = f"source/_static/{name}-dark.svg"
    else:
        fn = f"source/_static/{name}.svg"

if args.dark:
    params["draw"] = "white"
main_color = "white" if args.dark else "black"
black_color = "white" if args.dark else "black"
white_color = "black" if args.dark else "white"
tex = args.tex        
