from datetime import datetime, timedelta
from common import clockError

# ------------------------------------
#
# Help function
#
# ------------------------------------
def help():
  print("""
Scans a Logseq graph to check for CLOCK entries and aggregate
them by tags and time.

Usage:
  mlkgraphclock [-t lapse] [-d dessagregation] [-w] [-h] [path to graph]

Arguments:
  [path to graph]    Path to graph, defaults to .

Options:
  -t        Time lapse: today (default), week, month, year
  -d        Time dessagregation: daily (default), weekly, monthly, yearly
  -w        Process tags not prefixed by Work/ or Gestión general
  -h        This help
""")


# ------------------------------------
#
# 0 padding function
#
# ------------------------------------
def zeroPad(s):
  if len(str(s)) == 1:
    return "0%s" % s
  else:
    return s


# ------------------------------------
#
# Recursive node processing function
#
# ------------------------------------
def processNode(timeData, file, node, tags, dessagre, limitLow, limitHigh, tagsToBlock, onlyWork):
  try:
    type = node.get_type()

    # If the node is a ListItem, reset the tags. CLOCK entries will be
    # added to parent node tags, and not goes upwards more than that
    if type == "ListItem":
      tags = []

    # If a tag, add the tag to the tags list
    if type == "LogseqComposedTag" or type == "LogseqTag" or type == "LogseqSquareTag":
      t = node.target

      # Filter Work tags
      if onlyWork:
        tagsD = [ i for i in t if i[0:4] == "Work" or i == "Gestión general" ]
      else:
        tagsD = [ i for i in t if not(i[0:4] == "Work" or i == "Gestión general") ]

      tags.extend(tagsD)

    # If a CLOCK, process
    if type == "LogseqClock":

      # Check for error
      if "errorInCLOCK" in node.target.keys():
        clockError(node.target, file)

      else:
        if node.target["startDate"] != node.target["endDate"]:
          print("WARNING! Clocking in different days in file %s: %s <> %s" % \
            (file, node.target["startDate"], node.target["endDate"]))
          print()

        start = datetime.strptime("%s %s" % (node.target["startDate"], node.target["startHour"]), '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime("%s %s" % (node.target["endDate"], node.target["endHour"]), '%Y-%m-%d %H:%M:%S')

        # Generate the time tag for timeData based on dessagre: daily weekly monthly yearly
        # Daily, default
        timeTag = node.target["startDate"]

        # weekly
        if dessagre == "weekly":
          monday = datetime(start.year, start.month, start.day) - \
            timedelta(days=start.weekday())
          timeTag = "%s-%s-%s" % (monday.year, zeroPad(monday.month), zeroPad(monday.day))

        # monthly
        if dessagre == "monthly":
          timeTag = "%s-%s" % (start.year, zeroPad(start.month))

        # yearly
        if dessagre == "yearly":
          timeTag = start.year

        # If start time is between time limit, process for tags
        if limitLow <= start <= limitHigh:
          # Iterate the tags found in the parent ListItem
          for t in tags:
            # Check the tag is not blocked
            if t not in tagsToBlock:
              # Check if the startDate has an entry in timeData
              if timeTag not in timeData:
                timeData[timeTag] = {}

              # Total clock
              if "#TOTAL CLOCK" not in timeData[timeTag]:
                timeData[timeTag]["#TOTAL CLOCK"] = timedelta(seconds=0)

              if "/" not in t:
                timeData[timeTag]["#TOTAL CLOCK"] += end - start

              # Check if the tag has an entry for the day
              if t not in timeData[timeTag]:
                timeData[timeTag][t] = end - start

              # Both entries exists
              else:
                timeData[timeTag][t] += end - start

    for i in node.children:
      processNode(timeData, file, i, tags, dessagre, limitLow, limitHigh, tagsToBlock, onlyWork)

  except:
    pass
