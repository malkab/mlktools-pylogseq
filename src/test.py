#!/usr/bin/env python3
# coding=UTF8

from marko import Markdown
from mdlogseq import Logseq
import datetime

g = Logseq()

markdown = Markdown(extensions=[Logseq])

# a = markdown.parse("""
# - #[[Actividad diaria]] #[[A B]] #GGG **Actividad**
#   :LOGBOOK:
#   CLOCK: [2022-10-24 Mon 07:54:14]--[2022-10-24 Mon 08:26:28] =>  00:32:14
#   CLOCK: [2022-10-25 Mon 07:54:14]--[2022-10-25 Mon 08:26:28] =>  00:32:14
#   CLOCK: [2022-10-26 Mon 07:54:14]--[2022-10-26 Mon 08:26:28] =>  00:32:14
#   CLOCK: [2022-10-27 Mon 07:54:14]--[2022-10-27 Mon 08:26:28] =>  00:32:14
#   :END:
# """)

f = open("grafo_ejemplo_gestion/journals/2022_10_24.md")

md = f.read()

b = markdown.parse(md)

def processNode(node, tags):
  try:
    type = node.get_type()

    if type == "ListItem":
      print("ListItem")
      tags = []

    if type == "LogseqComposedTag" or type == "LogseqTag" or type == "LogseqSquareTag":
      tags.extend(node.target)
      print("Tag", node.target)

    if type == "LogseqClock":
      if node.target["startDate"] != node.target["endDate"]:
        print("WARNING! Clocking in different days: ", node.target)

      start = datetime.datetime("%s %s" % (node.target["startDate"], node.target["endDate"]))

      print(start)

      print("Clock", node.target, tags)

    for i in node.children:
      processNode(i, tags)

  except:
    pass

tags = []

for i in b.children:
  processNode(i, tags)

print()
