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
- This distance is multiplied by 65280/65536 then by 0.3915 to obitan a number $d$
  - It looks to me as if the first multiplication occurs only because that's the better way to compute the distance using TeX numbers systems (which are essentially fixed point numbers). Assuming $x > y$:
    - The ratio $x/\sqrt{x^2+y^2}$ is first computed, then multiplied by 65536 and divided by $255$ to obtain the number $a$
	- $x$ is multiplied by 16, then divided by $a$, then multiplied again by $16$.
	
- The two control points for the Bezier curve are then defined in the following way:
  - The first control point is at distance d and angle `out` from the first point.
  - The second control point is at distance d and angle `in` from the second point
  

Why 0.3915 ?
Suppose we try:
```
\draw (0,0) edge[in=-90,out=0] (1,1);
```
and we want this to look the closest possible to a circle.

Following this [page](https://spencermortensen.com/articles/bezier-circle/) (section "a better approximation"), we want the first control point to be at coordinate $(0, c)$ where $c=0.551915$.

As the distance between the two points is $\sqrt{2}$, we want the distance $d$ to be multiplied by $0.551915/\sqrt{2} = 0.3902$.
As the distance between the two points is first multiplied by $65280/65536$, the last multiplication factor should be 

$$ 0.3902 * 65536/65280 = 0.3917 $$

That factor is close enough to the $0.3915$ found in the code to explain why it's there.





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

