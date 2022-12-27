import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pylogseq.src.pylogseq.page import Page

import pytest

# --------------------------------------
#
# Page tests.
#
# --------------------------------------
class TestPage:

  # --------------------------------------
  #
  # Loads a page from file.
  #
  # --------------------------------------
  def test_read_page_file(self):
    # A Page object
    p = Page()

    # Read a page
    p.readPageFile("src/tests/assets/Agenda/pages/Fechas clave.md")

    # Check the content
    assert p.content == "- #procesar\n- Las fechas clave de verdad tienen que estar en **000-Gestión**, aquí puede haber algunas, pero no es su sitio de verdad\n"

    # Check the blocks
    p.parseMarkdown()
