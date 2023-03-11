About
=====

Hello world!


Contents
--------

.. toctree::
   :maxdepth: 1

   about/introduction
   about/frequently_asked_questions
   about/troubleshooting
   about/license


CodeBlock
---------

.. code-block:: python
   :lineno-start: 10
   :emphasize-lines: 9
   :linenos:
   :caption: demo_python.py
   :name: code-PythonGenerateEllipse

   import pytool
   import numpy as np
   import matplotlib.pyplot as plt

   # =====================generate Ellipse=====================
   a = 6  # major axis
   b = 2  # minor axis
   x0 = 10  # center x0
   y0 = 10  # center y0
   N = 1000  # number of points

   # angle for rotating ellipse data
   theta = np.pi * 30 / 180

   x, y = pytool.ellipse_surface(a, b, x0, y0, N, 'rand')

   x = x - np.mean(x)
   y = y - np.mean(y)
