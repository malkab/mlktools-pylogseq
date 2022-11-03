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

# --------------------------------------
#
# Process node
#
# --------------------------------------
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
