Layers
======

The main class in the library is the layer class, along with its subclasses.


The most typical use of a program is to first create a layer (usually tikz or svg) and then use all graphics methods of this layer.


Commands in layers are divided into two parts: edge commands and shape commands.
Essentially an edge command is a command that draws a line (or multiple lines) and shape commands are all other commands.

Regardless of their order when you call them, edge commands are always executed *before* shape commands.






The abstract layer
==================

.. autoclass:: pygf.layer.Layer
   :members:
   :exclude-members: find_angles


Other layers
============

.. autoclass:: pygf.layer.NoLayer


.. autoclass:: pygf.layer.MultiLayer
   :members: draw_all
	     

