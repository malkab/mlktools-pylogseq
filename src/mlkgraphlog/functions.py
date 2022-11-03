# ------------------------------------
#
# Help function
#
# ------------------------------------
def help():
  print("""
Scans a Logseq graph to check for CLOCK entries and log tasks
done on a daily basis.

Usage:
  mlkgraphlog [-a] [-d day] [path to graph]

Arguments:
  [path to graph]    Path to graph, defaults to .

Options:
  -a        Logs all days
  -d        A given day to log in YYYY-MM-DD format, defaults to the last day
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
