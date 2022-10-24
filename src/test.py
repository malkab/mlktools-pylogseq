#!/usr/bin/env python3
# coding=UTF8

import sys

print(sys.path)

from marko import Markdown
from mdlogseq import Logseq

g = Logseq()

print(g.elements)

markdown = Markdown(extensions=[Logseq])

a = markdown.parse("""
- #[[Actividad diaria]] #[[A B]] #GGG **Actividad**
  :LOGBOOK:
  CLOCK: [2022-10-24 Mon 07:54:14]--[2022-10-24 Mon 08:26:28] =>  00:32:14
  CLOCK: [2022-10-25 Mon 07:54:14]--[2022-10-25 Mon 08:26:28] =>  00:32:14
  CLOCK: [2022-10-26 Mon 07:54:14]--[2022-10-26 Mon 08:26:28] =>  00:32:14
  CLOCK: [2022-10-27 Mon 07:54:14]--[2022-10-27 Mon 08:26:28] =>  00:32:14
  :END:
""")

# # print(a.get_type())

# # print(a.children)

# # print()

# f = open("grafo_ejemplo_gestion/journals/a.md")

# md = f.read()

# b = markdown.parse(md)

# print(b)

print()
