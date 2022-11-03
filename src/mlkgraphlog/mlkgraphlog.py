#!/usr/bin/env python3
# coding=UTF8

import sys
import getopt
from marko import Markdown
from datetime import datetime, timedelta
from common import findMdFiles, shortenString
from common.mdlogseq import LogseqParseLog
from functions import help, processNode

sys.path.append("..")
sys.path.append("src")


# ------------------------------------
#
# Command line options
#
# ------------------------------------
try:
  opts, args = getopt.getopt(sys.argv[1:], "ah")

except getopt.GetoptError as err:
  print("Error: ", err)
  help()
  sys.exit(2)

# Default values
# Show all
showAll = False
# Graph path
path = "."

# Process options
for o, a in opts:
  if o == "-a":
    showAll = True
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
# Debugging section
#
# --------------------------------------
path = "../../grafo_ejemplo_gestion/test"
#path = "grafo_ejemplo_gestion/test"


# --------------------------------------
#
# Run
#
# --------------------------------------
# Get files
files = findMdFiles(path)
# To store final data
finalData = {}

# print("D: files", files)


# --------------------------------------
#
# Iterate all files
#
# --------------------------------------
for file in files:
  # Load parser and parse file
  markdown = Markdown(extensions=[LogseqParseLog])
  f = open(file)
  md = f.read()
  b = markdown.parse(md)
  f.close()

  # To store clocked tasks
  clocked = []

  # Process children, starting the recursive process, storing
  # results in clocked
  for i in b.children:
    processNode(i, [], [], clocked)

  # print("D: final", clocked)

  # Process clocked data
  for k, c in clocked:
    key = "".join(k[:-1])

    # print("\nD: Key\n", key)

    for clock in c:
      # print("D: clock", clock)

      # Check different days clocking
      if clock["startDate"] != clock["endDate"]:
        print("ERROR! Clocking in different days in file %s: %s <> %s" % \
          (file, clock["startDate"], clock["endDate"]))
        sys.exit(1)

      # Store the start and end time as timestamps
      start = datetime.strptime("%s %s" % \
        (clock["startDate"], clock["startHour"]), '%Y-%m-%d %H:%M:%S')
      end = datetime.strptime("%s %s" % \
        (clock["endDate"], clock["endHour"]), '%Y-%m-%d %H:%M:%S')

      # Check mismatch start / end time
      if end<start:
        print("ERROR! Start time bigger than end time in file %s: %s > %s" % \
          (file, clock["startHour"], clock["endHour"]))
        sys.exit(1)

      # print("D: se", start, end)

      # If there is no entry for the current day in the
      # final data storage, create it
      if clock["startDate"] not in finalData:
        finalData[clock["startDate"]] = []

      # Insert the data in final data storage
      finalData[clock["startDate"]].append({
        "key": key,
        "startDate": clock["startDate"],
        "startHour": clock["startHour"],
        "endDate": clock["endDate"],
        "endHour": clock["endHour"],
        "start": start,
        "end": end,
        "duration": end - start
      })

    # print("\n\n")

# Sort days
skeys = sorted(finalData.keys(), reverse=True)

# print("D: UIUI", skeys)

# Sort days
for k in skeys:
  # print("D: uuuu", k, v)

  # Sort chronollogically by starting hour
  sv = sorted(finalData[k], key=lambda x: x["startHour"])

  # print("D: sv", sv)

  # Check for overlapping time segments
  for i in range(0, len(sv)-1):
    # print("\nD: diff", sv[i]["end"], sv[i+1]["start"])

    if sv[i]["end"] > sv[i+1]["start"]:
      print("ERROR! Overlapping in day %s, tasks \"%s\" / \"%s\": end %s, start %s" % \
        (sv[i]["startDate"], sv[i]["key"], sv[i+1]["key"], sv[i]["endHour"], sv[i+1]["startHour"]))
      sys.exit(1)

  # Print the day
  print(k)

  # Print task and time segment, with duration
  for i in sv:
    print("   %s   %s - %s (%s)" % \
      (shortenString(i["key"], 80), i["startHour"], i["endHour"], i["duration"]))

    # print("\nD: rr ", i)

  print("")



print("\n\n\n")
print("D: FINAL")
# print(finalData)
