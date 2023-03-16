"""DearEditor’s command line toos module.

This module provides a set of command line toos.
Each folder inside represents a certain tool being able to invoked from command line.
Every tool contains two major interface: ``description()-> str`` and ``main(argv)``.

Typical usage example:

.. code-block:: bash
   :linenos:

   dear list # to check all available tools.
   dear tool_name -h # to see certain tool's help info.
   dear tool_name args... # to invoke certain tool.
"""