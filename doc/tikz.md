# How tikz works

This is the set of notes on how tikz works internally.

Some of this information can be found in the pgfmanual, some of them is found in the `tikz.code.tex` file.

## pt

For reference, 1 pt is equal to 1/72.27in and 1in is equal to 2.54cm, so 1 pt is equal to 2.54/72.27= 0.035146cm  as a first approximation.

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

Dash patterns are defined only in the file `tikz.code.tex`. Each format is a list lengths, the odd ones for the length of the dashes, and the even ones for the length of the gaps.



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

