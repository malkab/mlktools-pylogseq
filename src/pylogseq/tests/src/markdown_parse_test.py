# import sys
# import os
# sys.path.insert(0,
#   os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

# import pytest

# from marko import Markdown
# import marko
# from pylogseq.mdlogseq.logseqparse import LogseqParse
# from pylogseq.mdlogseq.exceptions.errorclock import ErrorClock

# # --------------------------------------
# #
# # Markdown parsing tests.
# #
# # --------------------------------------
# @pytest.skip
# class TestMarkdownParser:

#   # --------------------------------------
#   #
#   # Parses
#   # CLOCK: [2022-11-25 Fri 12:17:38]--[2022-11-25 Fri 12:19:27] =>  00:01:49
#   # items
#   #
#   # --------------------------------------
#   def test_clock(self):
#     mark = Markdown(extensions=[LogseqParse])

#     markdown = """- DONE #[[Gestión/Gestión general]] Something
#       :LOGBOOK:
#       CLOCK: [2022-11-25 Fri 08:57:12]--[2022-11-25 Fri 09:09:45] =>  00:12:33
#       CLOCK: [2022-11-25 Fri 10:01:13]--[2022-11-25 Fri 10:01:17] =>  00:00:04
#       CLOCK: [2022-11-25 Fri 10:01:18]--[2022-11-25 Fri 10:07:58] =>  00:06:40
#       CLOCK: [2022-11-25 Fri 12:17:38]--[2022-11-25 Fri 12:19:27] =>  00:01:49
#       CLOCK: [2022-11-25 Fri 14:49:56]--[2022-11-25 Fri 14:54:06] =>  00:04:10
#       :END:"""

#     parsed = mark.parse(markdown)

#     assert isinstance(parsed, marko.block.Document) == True
#     assert isinstance(parsed.children[0], marko.block.List) == True

#     listItem = parsed.children[0].children[0]

#     assert isinstance(listItem, marko.block.ListItem) == True

#   # --------------------------------------
#   #
#   # Errores de parseo de clocks
#   #
#   # --------------------------------------

#   # Parseo indeterminado
#   def test_error_clock_undefined(self):
#     with pytest.raises(ErrorClock) as e:

#       mark = Markdown(extensions=[LogseqParse])

#       markdown = """- DONE #[[Gestión/Gestión general]] Something
#         :LOGBOOK:
#         CLOCK: [2022-11-25 Fri 08:57:12]- e3 -[2022-11-25 Fri 09:09:45] =>  00:12:33
#         :END:"""

#       mark.parse(markdown)

#     assert e.value.message == "CLOCK error: undefined error parsing CLOCK: [2022-11-25 Fri 08:57:12]- e3 -[2022-11-25 Fri 09:09:45] =>  00:12:33"

#   # Error de parseo de la starting timestamp
#   def test_error_clock_starting_timestamp(self):
#     with pytest.raises(ErrorClock) as e:

#       mark = Markdown(extensions=[LogseqParse])

#       markdown = """- DONE #[[Gestión/Gestión general]] Something
#         :LOGBOOK:
#         CLOCK: [2022-11-25.3 Fri 08:57:12]--[2022-11-25 Fri 09:09:45] =>  00:12:33
#         :END:"""

#       mark.parse(markdown)

#     assert e.value.message == "CLOCK error: unparseable start timestamp 2022-11-25.3 08:57:12"

#   # Error de parseo de la ending timestamp
#   def test_error_clock_ending_timestamp(self):
#     with pytest.raises(ErrorClock) as e:

#       mark = Markdown(extensions=[LogseqParse])

#       markdown = """- DONE #[[Gestión/Gestión general]] Something
#         :LOGBOOK:
#         CLOCK: [2022-11-25 Fri 08:57:12]--[2022-11-25.6 Fri 09:09:45] =>  00:12:33
#         :END:"""

#       mark.parse(markdown)

#     assert e.value.message == "CLOCK error: unparseable ending timestamp 2022-11-25.6 09:09:45"

#   # Error en clocking en días diferentes
#   def test_error_clock_different_days(self):
#     with pytest.raises(ErrorClock) as e:

#       mark = Markdown(extensions=[LogseqParse])

#       markdown = """- DONE #[[Gestión/Gestión general]] Something
#         :LOGBOOK:
#         CLOCK: [2022-11-25 Fri 08:57:12]--[2022-11-26 Sat 09:09:45] =>  00:12:33
#         :END:"""

#       mark.parse(markdown)

#     assert e.value.message == "CLOCK error: clocking in different days 2022-11-25 <> 2022-11-26"

#   # Error en que la hora de comienzo es mayor que la de finalización
#   def test_error_clock_start_bigger(self):

#     with pytest.raises(ErrorClock) as e:

#       mark = Markdown(extensions=[LogseqParse])

#       markdown = """- DONE #[[Gestión/Gestión general]] Something
#         :LOGBOOK:
#         CLOCK: [2022-11-26 Fri 09:57:12]--[2022-11-26 Sat 09:09:45] =>  00:12:33
#         :END:"""

#       mark.parse(markdown)

#     assert e.value.message == "CLOCK error: start time bigger than end time 2022-11-26 Fri 09:57:12 > 2022-11-26 Sat 09:09:45"
