"""Common editor tookits, typical usage example:

.. code-block:: python
   :linenos:

   from editor.common import sample_tool
   sample_tool.doSomeThing()

   # or,
   from editor.common.sample_tool import doSomeThing
   doSomeThing()

.. admonition:: Emmmm

   This is note text. Use a note for information you want the user to
   pay particular attention to.

   If note text runs over a line, make sure the lines wrap and are indented to
   the same level as the note tag. If formatting is incorrect, part of the note
   might not render in the HTML output.

   Notes can have more than one paragraph. Successive paragraphs must
   indent to the same level as the rest of the note.

.. warning::
    This is warning text. Use a warning for information the user must
    understand to avoid negative consequences.

    Warnings are formatted in the same way as notes. In the same way,
    lines must be broken and indented under the warning tag.
"""