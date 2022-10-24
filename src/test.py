#!/usr/bin/env python3
# coding=UTF8

import sys

print(sys.path)

from marko import Markdown
from mdlogseq import Logseq

g = Logseq()

print(g.elements)

markdown = Markdown(extensions=[Logseq])

a = markdown.parse("- #[[Actividad diaria]] #[[A B]] #GGG **Actividad**")

# # print(a.get_type())

# # print(a.children)

# # print()

# f = open("grafo_ejemplo_gestion/journals/a.md")

# md = f.read()

# b = markdown.parse(md)

# print(b)

print()
