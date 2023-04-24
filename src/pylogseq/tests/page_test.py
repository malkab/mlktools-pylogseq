from pylogseq.page import Page
from pylogseq.parser import Parser

import pytest


# @pytest.mark.skip
class TestPage:

    def test_read_page_file(self):
        """Loads a page from file.
        """
        # A Page object
        p = Page()

        # Read a page
        p.read_page_file("tests/assets/Agenda/pages/Gestión.md")

        # Check the content
        # assert p.content == "- #procesar\n- Las fechas clave de verdad tienen que estar en **000-Gestión**, aquí puede haber algunas, pero no es su sitio de verdad\n"

        # Check the blocks
        p.parse_markdown()
