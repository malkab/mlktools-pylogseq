from marko.block import ListItem, FencedCode
from typing import List

# START HERE: A BLOCK IS ONLY A - WHATEVER SEGMENT
# START BY PROVIDING A BLOCK LITERAL STRING (STORE IT FOR LATER
# RECONSTRUCTION) AND PARSE IT, STORING ALL KIND OF INFORMATION

# THEN, GO TO THE PAGE LEVEL, WHERE A MD IS READ AND THE INDIVIDUAL,
# TOP LEVEL "- " BLOCKS ARE STORED SEPARATELY (WITH ANY FRONT
# MATTER, IF ANY) AND CONVERTED TO BLOCKS LIKE THIS ONE. THE PAGE
# WILL CONTAIN A LIST OF PARSED BLOCKS, IN ORDER OF APPEARANCE,
# EASY TO CONVERT BACK TO STRING TO PUT INTO A NEW MD FILE.

# AT PAGE LEVEL, DO NOT STORE THE CONTENT OF THE PAGE, JUST THE
# FRONT MATTER. THE PAGE WILL BE RECONSTRUCTED FROM ITS BLOCKS.

# --------------------------------------
#
# A Logseq Block (a ListItem)
#
# --------------------------------------
class Block():
  """
  A single Logseq Block.

  Attributes
  ----------
  tags : List[str]
    dd

  Methods
  -------
  colorspace(c='rgb')
      Represent the photo in the given colorspace.
  gamma(n=1.0)
      Change the photo's gamma exposure.
  """

  # --------------------------------------
  #
  # Constructor.
  #
  # --------------------------------------
  def __init__(self, originalString: str=None):
    """Constructor.

    """
    self.tags: List[str] = []
    self.originalString: str = originalString
    self.highestPriority: str = None

  # --------------------------------------
  #
  # Process the block from ListItem (a Logseq block) found in the
  # parsing of the Markdown of a Logseq page.
  #
  # --------------------------------------
  def process(self, listItem: ListItem, rank: int=0) -> None:
    """Process the block from a ListItem (a Logseq block) found in the
    parsing of the Markdown of a Logseq page.

    Args:
        listItem (ListItem): A Markdown ListItem object obtained from the parser.

        This comes from the parsing of the Markdown of a Logseq page. Logseq block's
        are ListItems.

        rank (int, optional): Ranking of this block. Controls indentation of children blocks. Defaults to 0.
    """
    # A growing list of Markdown parsed items to process
    items: List[any] = listItem.children

    # While there are items to process...
    while len(items)>0:

      # Get the first item
      i: any = items.pop(0)

      # Check the type's name
      t: str = type(i).__name__

      # Process each item based on its type, composing the string representation
      if t in [ "LogseqDone", "LogseqLogBook", "LogseqLater" ]:
        self.strBlock += i.target

      if t == "LogseqEnd":
        self.strBlock += "\n%s" % i.target

      if t == "LogseqClock":
        self.strBlock += "\nCLOCK: [%s %s %s]--[%s %s %s] =>  %s" % \
          (i.target["startDate"], i.target["startDay"], i.target["startHour"],
           i.target["endDate"], i.target["endDay"], i.target["endHour"],
           i.target["calculatedElapsedTime"])

      if t == "LogseqPriority":
        self._setPriority(i.target)

        if self.parentBlock:
          self.parentBlock._setPriority(i.target)

        self.strBlock += "[#%s]" % i.target

      if t == "RawText":
        self.strBlock += i.children

      if t in "LogseqComposedTag":
        self.strBlock += "#[[%s]]" % i.target[-1]
        self.tags.extend(i.target)

      if t in "LogseqTag":
        self.strBlock += "#%s " % i.target[-1]
        self.tags.extend(i.target)

      if t in "LogseqSquareTag":
        self.strBlock += "[[%s]]" % i.target[-1]
        self.tags.extend(i.target)

      if t == "LineBreak":
        self.strBlock += "\n"

      if t == "ListItem":
        u = Block(parentBlock=self)
        u.process(i, rank=rank+1)
        self.strBlock += "\n%s%s" % ("  "*(rank+1), u.strBlock)

      try:
        if t not in [ "RawText", "LogseqComposedTag", "LogseqTag",
          "LogseqSquareTag", "FencedCode" ]:
          items.extend(i.children)
      except:
        pass

    # Process unique tags
    self.tags = list(set(self.tags))

  # --------------------------------------
  #
  # Set highest priority found in the block, including childrens.
  #
  # --------------------------------------
  def _setPriority(self, priority: str) -> None:
    """Set highest priority found in the block, including childrens.

    Args:
        priority (str): The new priority found.
    """
    # If there is a parent block, pass the priority to it
    if self.parentBlock:
      self.parentBlock._setPriority(priority)

    # Set the highest priority using an alphabetical order logic
    if self.highestPriority == None:
      self.highestPriority = priority
    else:
      self.highestPriority = sorted([ self.highestPriority, priority ])[0]
