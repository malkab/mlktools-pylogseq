#!/usr/bin/env python3
# coding=UTF8

from marko import Markdown
from mdlogseq import Logseq
from datetime import datetime, timedelta, date
import calendar

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

# Parameters
# Time limit:    today (default), week, month, year, all
# Desagregación: diario (default), semanal, mensual, total

b = markdown.parse(md)

# Time limit
tl = "month"

if tl == "today":
  limitLow = date.today()
  limitHigh = date.today() + timedelta(days=1)

if tl == "week":
  limitLow = date.today() - timedelta(days=date.today().weekday())
  limitHigh = limitLow + timedelta(days=7)

if tl == "month":
  t = date.today()
  mr = calendar.monthrange(t.year, t.month)
  print("HHH", mr)

  limitLow = datetime(t.year, t.month, 1)
  limitHigh = datetime(t.year, t.month, mr[1]) + timedelta(days=1)

if tl == "year":
  t = date.today()
  limitLow = datetime(t.year, 1, 1)
  limitHigh = datetime(t.year, 12, 31) + timedelta(days=1)

print(tl, limitLow, limitHigh)

timeData = {}

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

      start = datetime.strptime("%s %s" % (node.target["startDate"], node.target["startHour"]), '%Y-%m-%d %H:%M:%S')
      end = datetime.strptime("%s %s" % (node.target["endDate"], node.target["endHour"]), '%Y-%m-%d %H:%M:%S')

      print("date: ", start, end, end - start)

      if start >= datetime.now() - filter:
        for t in tags:
          if node.target["startDate"] not in timeData:
            timeData[node.target["startDate"]] = {}
          elif t not in timeData[node.target["startDate"]]:
            timeData[node.target["startDate"]][t] = end - start
          else:
            timeData[node.target["startDate"]][t] += end - start

      print("Clock", node.target, tags)

    for i in node.children:
      processNode(i, tags)

  except:
    pass

tags = []

for i in b.children:
  processNode(i, tags)

print(timeData)

print()
