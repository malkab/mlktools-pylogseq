#!/usr/bin/env python3
# coding=UTF8

from marko import Markdown
from datetime import datetime, timedelta, date
import calendar
import getopt
import sys
from functions import help, processNode
from common.mdlogseq import LogseqParseClock
from common import findMdFiles, shortenString


# ------------------------------------
#
# Constants
#
# ------------------------------------
TAGSTOBLOCK = [ "BLK", "A]", "B]", "C]" ]


# ------------------------------------
#
# Command line options
#
# ------------------------------------
try:
  opts, args = getopt.getopt(sys.argv[1:], "t:d:wh")

except getopt.GetoptError as err:
  print("Error: ", err)
  help()
  sys.exit(2)

# Default values
# timeLimit: today week month year
timeLimit = "today"
# dessagre: daily weekly monthly yearly
dessagre = "daily"
# Graph path
path = "."
# Only Work/ tags
onlyWork = True

# Process options
for o, a in opts:
  if o == "-t":
    timeLimit = a
  if o == "-d":
    dessagre = a
  if o == "-w":
    onlyWork = False
  if o == "-h":
    help()
    sys.exit(0)

# Check validity of timeLimit
if timeLimit not in [ "today", "week", "month", "year" ]:
  print("Error: invalid time limit", timeLimit)
  sys.exit(2)

# Check validity of dessagre
if dessagre not in [ "daily", "weekly", "monthly", "yearly" ]:
  print("Error: invalid dessagregation", dessagre)
  sys.exit(2)

# Process path arg
if len(args) > 0:
  path = args[0]


# --------------------------------------
#
# Debug data imposting command line options
#
# --------------------------------------
# path = "grafo_ejemplo_gestion"
# #path = "../../grafo_ejemplo_gestion/"
# timeLimit = "year"
# dessagre = "year"
# onlyWork = False

# print("D: path", path)
# print("D: timeLimit", timeLimit)
# print("D: dessagre", dessagre)
# print("D: onlyWork", onlyWork)
# print()


# --------------------------------------
#
# Find .md files in graph
#
# --------------------------------------
files = findMdFiles(path)

# No graph found
if files == []:
  print("ERROR! No .md files found")
  sys.exit(1)


# ------------------------------------
#
# Calculate time limits
#
# ------------------------------------
if timeLimit == "today":
  t = date.today()
  limitLow = datetime(t.year, t.month, t.day)
  limitHigh = datetime(t.year, t.month, t.day) + timedelta(days=1)

if timeLimit == "week":
  t = date.today()
  limitLow = datetime(t.year, t.month, t.day) - \
    timedelta(days=date.today().weekday())
  limitHigh = limitLow + timedelta(days=7)

if timeLimit == "month":
  t = date.today()
  mr = calendar.monthrange(t.year, t.month)

  limitLow = datetime(t.year, t.month, 1)
  limitHigh = datetime(t.year, t.month, mr[1]) + timedelta(days=1)

if timeLimit == "year":
  t = date.today()
  limitLow = datetime(t.year, 1, 1)
  limitHigh = datetime(t.year, 12, 31) + timedelta(days=1)

# Final store for filtered data in days/tags
timeData = {}

# ------------------------------------
#
# Iterate all files
#
# ------------------------------------
for file in files:

  # Load file and parse it
  g = LogseqParseClock()
  markdown = Markdown(extensions=[LogseqParseClock])
  f = open(file)
  md = f.read()
  b = markdown.parse(md)
  f.close()

  # Empty tag list
  tags = []

  # Process initial children
  for i in b.children:
    processNode(timeData, file, i, tags, dessagre, limitLow, limitHigh, TAGSTOBLOCK, onlyWork)


# ------------------------------------
#
# Present results
#
# ------------------------------------
# Sort results chronologically (first stage in timeData final results)
skeys = sorted(timeData.keys(), reverse=True)

for k in skeys:
  print()
  print(k)
  dt = timeData[k]

  stimes = sorted(dt.keys())

  total = timeData[k]["#TOTAL CLOCK"]

  print("    %s   %s" % (shortenString("TOTAL", 30), timeData[k]["#TOTAL CLOCK"]))

  for d in stimes[1:]:
    print("    %s   %s (%s%%)" % (shortenString(d, 30), timeData[k][d], \
      round(timeData[k][d] / total * 100)))
