# How tikz works

This is the set of notes on how tikz works internally.

Some of this information can be found in the pgfmanual, some of them is found in the `tikz.code.tex` file.

## pt

For reference, 1 pt is equal to 1/72.27in and 1in is equal to 2.54cm, so 1 pt is equal to 2.54/72.27= 0.035146cm  as a first approximation.

## edge

All of this can be found in the file `tikzlibrarytopaths.code.tex`, more precisely in the function `\tikz@to@compute@distance@main`.

Here is what happens when one writes:
```
\draw (0,0) edge[in=90,out=60] (5,0);
```

- The distance between the two points is computed.
- This distance is multiplied by 65280/65536 then by 0.3915 to obtain a number $d$
- The two control points for the Bezier curve are then defined in the following way:
  - The first control point is at distance d and angle `out` from the first point.
  - The second control point is at distance d and angle `in` from the second point
  


65280/65536 is probably due to fixed point arithmetics. 0.3915 is chosen so the curve looks like half a circle in the obvious case.




## line width

The default line width in tikz is 0.4pt.

The following styles are predefined:

|             |       |                           |
|-------------|-------|---------------------------|
| ultra thin  | 0.1pt | 0.25 * default line width |
| very thin   | 0.2pt | 0.5 * default line width  |
| thin        | 0.4pt | default line width        |
| semithick   | 0.6pt | 1.5 * default line width  |
| thick       | 0.8pt | 2 * default line width    |
| very thick  | 1.2pt | 3 * default line width    |
| ultra thick | 1.6pt | 4 * default line width    |


This can be found in the pgfmanual (Section 15: Actions on Path) or in the file `tikz.code.tex`.

## Dash Patterns

Dash patterns are defined only in the file `tikz.code.tex`. Each format is a list of lengths, the odd ones for the length of the dashes, and the even ones for the length of the gaps.
This is similar to `stroke-dasharray` in SVG.



|                       |                                     |
|-----------------------|-------------------------------------|
| solid                 | (empty)                             |
| dotted                | linewidth 2pt                       |
| densely dotted        | linewidth 1pt                       |
| loosely dotted        | linewidth 4pt                       |
| dashed                | 3pt 3pt                             |
| densely dashed        | 3pt 2pt                             |
| loosely dashed        | 3pt 6pt                             |
| dashdotted            | 3pt 2pt linewidth 2pt               |
| dash dot              | 3pt 2pt linewidth 2pt               |
| densely dashdotted    | 3pt 1pt linewidth 1pt               |
| densely dash dot      | 3pt 1pt linewidth 1pt               |
| loosely dashdotted    | 3pt 4pt linewidth 4pt               |
| loosely dash dot      | 3pt 4pt linewidth 4pt               |
| dashdotdotted         | 3pt 2pt linewidth 2pt linewidth 2pt |
| densely dashdotdotted | 3pt 1pt linewidth 1pt linewidth 1pt |
| loosely dashdotdotted | 3pt 4pt linewidth 4pt linewidth 4pt |
| dash dot dot          | 3pt 2pt linewidth 2pt linewidth 2pt |
| densely dash dot dot  | 3pt 1pt linewidth 1pt linewidth 1pt |
| loosely dash dot dot  | 3pt 4pt linewidth 4pt linewidth 4pt |

## Arrows

Here is what happens when you write:

```
\draw[->] (0,0) -- (5,0);
```


- The line is drawn slightly shorter, to give room for the arrow. For this to work, tikz computes how far the arrow protrudes on the right, and also how far it does on the left (this is used for instance if the arrow is drawn in reverse)
- The arrow is then drawn


### The arrow to

The arrow `to` is the one that is drawn with `->`.

- Forward protrusion: 0.21pt + .625 linewidth
- Backward protrusion 0.84pt + 1.3 linewidth

- Linewidth: 0.8*linewidth
- No dash, roundcap, roundjoin
- x = 0.28pt + .3linewidth
- Go to (-3x, 4x)
- Curveto (0.75x,0) with control points (-2.75x,2.5x) and (0, 0.25x)
- Curveto (-3x,-4x) with control points (0, -0.25x) and (-2.75x,-2.5x)


