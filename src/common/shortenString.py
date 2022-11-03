# --------------------------------------
#
# Shortens a string and adapt it to a
# min / max length
#
# --------------------------------------
def shortenString(string, maxLen, minLen=0):
  if minLen < maxLen:
    minLen = maxLen

  if len(string) > maxLen:
    s = string[:maxLen-3]+"..."
  else:
    s = string

  if len(s) < minLen:
    fs = "%s%s" % (s, " "*(minLen - len(s)))
  else:
    fs = s

  return fs
