# TODO: DOCUMENT

# Process a tag in the form A/B/C and return
# all tags
def processMultiTags(tag):
  out = []
  sp = str.split(tag, "/")

  for i in sp:
    if len(out) == 0:
      out.append(i.strip())
    else:
      out.append((out[-1]+"/"+i).strip())

  return out
