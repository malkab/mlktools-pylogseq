#!/usr/bin/env python3
# coding=UTF8

from marko import Markdown
from datetime import datetime, timedelta
import sys
sys.path.append("..")
sys.path.append("src")
from common.findmdfiles import findMdFiles
from common.mdlogseq import LogseqParseLog


path = "../../grafo_ejemplo_gestion/test"
# path = "grafo_ejemplo_gestion/test"

files = findMdFiles(path)

print("D: files", files)




def processNode(node, nodeText, times, clocked):
  t = node.get_type()

  if t == "ListItem":
    nodeText = []
    times = []

  if t == "RawText":
    nodeText.append(node.children)

  if t == "LineBreak":
    nodeText.append(" ")

  if t == "LogseqClock":
    times.append(node.target)

  if t == "LogseqEnd":
    clocked.append((nodeText, times))

  try:
    for i in node.children:
      processNode(i, nodeText, times, clocked)
  except:
    pass



finalData = {}


# --------------------------------------
#
# Iterate all files
#
# --------------------------------------
for file in files:
  markdown = Markdown(extensions=[LogseqParseLog])
  f = open(file)
  md = f.read()
  b = markdown.parse(md)
  f.close()

  clocked = []

  for i in b.children:
    processNode(i, [], [], clocked)

  # print("D: final", clocked)

  for k, c in clocked:
    key = "".join(k[:-1])

    print("\nD: Key\n", key)

    for clock in c:
      # print("D: clock", clock)

      if clock["startDate"] != clock["endDate"]:
        print("ERROR! Clocking in different days in file %s: %s <> %s" % \
          (file, clock["startDate"], clock["endDate"]))
        sys.exit(1)

      start = datetime.strptime("%s %s" % \
        (clock["startDate"], clock["startHour"]), '%Y-%m-%d %H:%M:%S')
      end = datetime.strptime("%s %s" % \
        (clock["endDate"], clock["endHour"]), '%Y-%m-%d %H:%M:%S')

      if end<start:
        print("ERROR! Start time bigger than end time in file %s: %s > %s" % \
          (file, clock["startHour"], clock["endHour"]))
        sys.exit(1)

      # print("D: se", start, end)

      if clock["startDate"] not in finalData:
        finalData[clock["startDate"]] = []

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

    print("\n\n")

  for k, v in finalData.items():
    # print("D: uuuu", k, v)

    sv = sorted(v, key=lambda x: x["startHour"])

    # print("D: sv", sv)

    for i in range(0, len(sv)-1):
      # print("\nD: diff", sv[i]["end"], sv[i+1]["start"])

      if sv[i]["end"] > sv[i+1]["start"]:
        print("ERROR! Overlapping in day %s, tasks \"%s\" / \"%s\": end %s, start %s" % \
          (sv[i]["startDate"], sv[i]["key"], sv[i+1]["key"], sv[i]["endHour"], sv[i+1]["startHour"]))
        sys.exit(1)


    print(k)

    for i in sv:
      print("   %s                 %s - %s: %s" % \
        (i["key"], i["startHour"], i["endHour"], i["duration"]))

      # print("\nD: rr ", i)

    print("\n")



  print("\n\n\n")
  print("D: FINAL")
  # print(finalData)
