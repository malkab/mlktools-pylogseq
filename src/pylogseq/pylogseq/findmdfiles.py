import os

# --------------------------------------
#
# Find all .md files in path
#
# --------------------------------------
def findMdFiles(path):
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

  return files
