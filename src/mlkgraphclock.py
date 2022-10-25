#!/usr/bin/env python3
# coding=UTF8

from marko import Markdown
from mdlogseq import Logseq
from datetime import datetime, timedelta, date
import calendar
import getopt, sys
import os
from functions import help, processNode

# ------------------------------------
#
# Command line options
#
# ------------------------------------
try:
  opts, args = getopt.getopt(sys.argv[1:], "t:d:h")

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

# Process options
for o, a in opts:
  if o == "-t":
    timeLimit = a
  if o == "-d":
    dessagre = a
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

# To store .md files to iterate and process
files = []

# Generate list of .md files
for (dirpath, dirnames, filenames) in os.walk(path):
  for f in filenames:
    ext = os.path.splitext(f)[1].lower()

    if ext == ".md":
      # Filter logseq/bak/ pages
      if "logseq/bak/" not in dirpath:
        files.append(os.path.join(dirpath, f))

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
  g = Logseq()
  markdown = Markdown(extensions=[Logseq])
  f = open(file)
  md = f.read()
  b = markdown.parse(md)

  # Empty tag list
  tags = []

  # Process initial children
  for i in b.children:
    processNode(timeData, file, i, tags, dessagre, limitLow, limitHigh)

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

  lengths = [ len(i) for i in dt.keys()]

  maxLen = max(lengths)

  stimes = sorted(dt.keys())

  for d in stimes:
    padding = maxLen - len(d)
    print("    %s%s %s" % (d, " "*padding, timeData[k][d]))
