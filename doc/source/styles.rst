Styles
======

Here are all the styles decorations currently in pygf.

The colors that can be used are the 147 color names in the SVG specification (also available in latex).


Path styles
-----------

:draw: (:py:class:`str`) color that will be used to render the path. color can be ``None`` for no color. Defaults to ``"black"``.
:thickness: (:py:class:`float`) thickness (line width) of the path, as a percentage of the default line width, which is 0.4pt. For instance ``thickness=2`` means a thickness of .8pt. In tikz, will be converted to "textual names" if they exist. ``thickness=3`` will be converted to ``very thick`` in tikz for instance.
:rounded: (:py:class:`bool`) whether to round the corners of the path.
:fill: (:py:class:`str`) color that will be used to fill the path. Relevant mostly for closed paths. Defaults to ``None``.
:opacity: (:py:class:`float`) opacity of the painting operation. Defaults to ``1``. This is ignored if fill is ``None``.
:shade: (:py:class:`Tuple[str]`) (**experimental**) paints as a shade given by  a pair of two colors, the color on the left and the color on the right of the shape. Do not use it and assume it might break.
:labels: (:py:class:`Dict`) add a list of labels to the path. It is a dictionary, where the key is the position of the label, and the value the text of the label.

The different possible positions are : "above start", "above", "above end", "below start", "below", "below end". pygf tries to be smart (like tikz) so that your label always appears naturally and not inverted. (pygf only supports left to right text).

:arrows: (:py:class:`str`) add arrows to the path.

An arrow is of the form ``"a-b"`` where ``a`` and ``b`` are to be chosen [#]_ among ``>``, ``<``, ``latex``, ``xetal``. They can also be empty if you need only one arrowhead.

The following pictures shows every arrowhead:

.. only:: html

   .. image:: _static/arrows.svg

.. only:: latex

   .. image:: _static/arrows.pdf


	    
:dash: (:py:class:`str`) dash style to use. Defaults to None.

The possible dash styles are taken from tikz/pgf and are as follows:  "solid", "dotted", "densely dotted", "loosely dotted", "dashed", "densely dashed", "loosely dashed", "dashdotted", "dash dot", "densely dashdotted", "densely dash dot", "loosely dashdotted", "loosely dash dot", "dashdotdotted", "densely dashdotdotted", "loosely dashdotdotted", "dash dot dot", "densely dash dot dot", "loosely dash dot dot".

The following pictures shows how every dash style looks like

.. only:: html

   .. image:: _static/dash.svg

.. only:: latex

   .. image:: _static/dash.pdf

       

Text styles
-----------

Text styles can be used for any instruction that renders text, but also for any instruction that renders a path that includes text.

:text_color: (:py:class:`str`) color that will be used to render the text. Defaults to ``"black"``. 
:text_size: (:py:class:`str`) size of the text.	At the moment only ``"small"`` and ``"large"`` are supported.
:font_family: (:py:class:`str`) font of the text. At the moment only ``"monospace"`` is supported.
:position: (:py:class:`str`) position of the text relative to the anchor. This works only for the ``text`` instruction and not for paths instructions where you are supposed to use the ``labels`` dict to position the text.
	   
The possible positions are "below", "center", "above", "left", right" and any reasonasble combination of these.

       

Le champ **name** est de type :py:class:`pygf.geometry.Point`.





    



.. rubric:: Notes

.. [#] Currently the tikz output also supports "Rays". This might change in the future.
