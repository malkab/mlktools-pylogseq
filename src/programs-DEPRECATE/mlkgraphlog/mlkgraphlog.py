#!/usr/bin/env python3
# coding=UTF8

import sys
import getopt
from marko import Markdown
from common import findMdFiles, shortenString, clockError
from common.mdlogseq import LogseqParseLog
from functions import help, processNode


# ------------------------------------
#
# Command line options
#
# ------------------------------------
try:
  opts, args = getopt.getopt(sys.argv[1:], "ad:h")

except getopt.GetoptError as err:
  print("Error: ", err)
  help()
  sys.exit(2)

# Default values
# Show all
showAll = False
# Graph path
path = "."
# Day
day = None

# Process options
for o, a in opts:
  if o == "-a":
    showAll = True
  if o == "-d":
    day = a
  if o == "-h":
    help()
    sys.exit(0)

# Process path arg
if len(args) > 0:
  path = args[0]


# --------------------------------------
#
# Debugging section
#
# --------------------------------------
# showAll = True
# path = "../../grafo_ejemplo_gestion/test"
# path = "grafo_ejemplo_gestion/test"
# day = "2022-10-24"

# print("D: showAll", showAll)
# print("D: path", path)
# print("D: day", day)
# print()


# --------------------------------------
#
# Run
#
# --------------------------------------
# Get files
files = findMdFiles(path)

# No graph found
if files == []:
  print("ERROR! No .md files found")
  sys.exit(1)

# To store final data
finalData = {}


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

  # Process clocked data
  for k, c in clocked:
    key = "".join(k[:-1])

    for clock in c:
      # Check for error
      if "errorInCLOCK" in clock.keys():
        clockError(clock, file)

        sys.exit(1)

      else:
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
          "start": clock["start"],
          "end": clock["end"],
          "duration": clock["calculatedElapsedTime"]
        })


# --------------------------------------
#
# Data results presentation
#
# --------------------------------------
# Sort days
skeys = sorted(finalData.keys(), reverse=True)

# Sort days
if showAll:
  for k in skeys:
    # Sort chronollogically by starting hour
    sv = sorted(finalData[k], key=lambda x: x["startHour"])

    # Check for overlapping time segments
    for i in range(0, len(sv)-1):
      if sv[i]["end"] > sv[i+1]["start"]:
        print("ERROR! Overlapping in day %s, tasks \"%s\" / \"%s\": end %s, start %s" % \
          (sv[i]["startDate"], sv[i]["key"], sv[i+1]["key"], sv[i]["endHour"], sv[i+1]["startHour"]))
        sys.exit(1)

    # Print the day
    print(k)

    # Print task and time segment, with duration
    for i in sv:
      print("   %s   %s - %s (%s)" % \
        (shortenString(i["key"], 100), i["startHour"], i["endHour"], i["duration"]))

    print("")

# Show only a day (last by default)
else:
  # Check for a given day
  if day:
    try:
      dayData = finalData[day]

    except:
      print("No data for given day")
      sys.exit(0)

  else:
    day = skeys[0]
    dayData = finalData[skeys[0]]

  # Sort chronollogically by starting hour
  sv = sorted(dayData, key=lambda x: x["startHour"])

  # Check for overlapping time segments
  for i in range(0, len(sv)-1):
    if sv[i]["end"] > sv[i+1]["start"]:
      print("ERROR! Overlapping in day %s, tasks \"%s\" / \"%s\": end %s, start %s" % \
        (sv[i]["startDate"], sv[i]["key"], sv[i+1]["key"], sv[i]["endHour"], sv[i+1]["startHour"]))
      sys.exit(1)

  # Print the day
  print(day)

  # Print task and time segment, with duration
  for i in sv:
    print("   %s   %s - %s (%s)" % \
      (shortenString(i["key"], 100), i["startHour"], i["endHour"], i["duration"]))

  print("")
