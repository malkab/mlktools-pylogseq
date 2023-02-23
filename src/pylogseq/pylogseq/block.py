from marko.block import ListItem, FencedCode
from typing import Any
import hashlib
from .parser import Parser

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
    def __init__(self, content: str=None):
        """Constructor.

        """
        self.hash: str = None
        self.tags: list[str] = []
        self.content: str = self._sanitize_content(content)
        self.content_hash: str = hashlib.sha256(content.encode()).hexdigest()
        self.highest_priority: str = None

        p = Parser()

        self.process(p.parse(self.content))


    def _sanitize_content(self, content):
        current_length = len(content) + 1

        while len(content) < current_length:
            current_length = len(content)

            content = content.strip("\n").strip()

        return content

    # --------------------------------------
    #
    # Process the block from ListItem (a Logseq block) found in the
    # parsing of the Markdown of a Logseq page.
    #
    # --------------------------------------
    def process(self, item: Any, rank: int=0) -> None:
        """Process the block from a ListItem (a Logseq block) found in the
        parsing of the Markdown of a Logseq page.

        Args:
            listItem (ListItem): A Markdown ListItem object obtained from the parser.

            This comes from the parsing of the Markdown of a Logseq page. Logseq block's
            are ListItems.

            rank (int, optional): Ranking of this block. Controls indentation of children blocks. Defaults to 0.
        """
        # Check the type's name
        t: str = type(item).__name__

        # AQUÍ: Aquí identificamos qué tipo de objeto es y reaccionamos. Si tiene hijos
        # en children, procesamos esos hijos recursivamente.

        # AQUI: Checkeamos si tiene el atributo children. Si lo tiene, procesamos lo de abajo
        # Si no, entramos a ver qué tipo de
        # print("D: ", t, hasattr(item,  'children'))

        # try:
        #     if type(item.children).__name__ == "str":
        #         print ("D: str", item.children)

        #     else:
        #         for child in item.children:
        #             self.process(child, rank=rank+1)

        # except Exception as e:
        #     print("D: ", e)


        # # A growing list of Markdown parsed items to process
        # try:
        #     items: list[Any] = item.children

        #     # While there are items to process...
        #     while len(items)>0:



                # # Get the first item
                # i: any = items.pop(0)

                # # Check the type's name
                # t: str = type(i).__name__

                # # Process each item based on its type, composing the string representation
                # if t in [ "LogseqDone", "LogseqLogBook", "LogseqLater" ]:
                #     self.strBlock += i.target

                # if t == "LogseqEnd":
                #     self.strBlock += "\n%s" % i.target

                # if t == "LogseqClock":
                #     self.strBlock += "\nCLOCK: [%s %s %s]--[%s %s %s] =>  %s" % \
                #     (i.target["startDate"], i.target["startDay"], i.target["startHour"],
                #     i.target["endDate"], i.target["endDay"], i.target["endHour"],
                #     i.target["calculatedElapsedTime"])

                # if t == "LogseqPriority":
                #     self._setPriority(i.target)

                #     if self.parentBlock:
                #         self.parentBlock._setPriority(i.target)

                #     self.strBlock += "[#%s]" % i.target

                # if t == "RawText":
                #     self.strBlock += i.children

                # if t in "LogseqComposedTag":
                #     self.strBlock += "#[[%s]]" % i.target[-1]
                #     self.tags.extend(i.target)

                # if t in "LogseqTag":
                #     self.strBlock += "#%s " % i.target[-1]
                #     self.tags.extend(i.target)

                # if t in "LogseqSquareTag":
                #     self.strBlock += "[[%s]]" % i.target[-1]
                #     self.tags.extend(i.target)

                # if t == "LineBreak":
                #     self.strBlock += "\n"

                # if t == "ListItem":
                #     self.process(i, rank=rank+1)

                # if t == "List":
                #     for listItem in i.children:
                #         self.process(listItem, rank=rank+1)

                # try:
                #     if t not in [ "RawText", "LogseqComposedTag", "LogseqTag",
                #     "LogseqSquareTag", "FencedCode" ]:
                #         items.extend(i.children)
                # except:
                #     pass

        # except:
        #     pass

        # Process unique tags
        # self.tags = list(set(self.tags))

    # # --------------------------------------
    # #
    # # Set highest priority found in the block, including childrens.
    # #
    # # --------------------------------------
    # def _setPriority(self, priority: str) -> None:
    #   """Set highest priority found in the block, including childrens.

    #   Args:
    #       priority (str): The new priority found.
    #   """
    #   # If there is a parent block, pass the priority to it
    #   if self.parentBlock:
    #     self.parentBlock._setPriority(priority)

    #   # Set the highest priority using an alphabetical order logic
    #   if self.highestPriority == None:
    #     self.highestPriority = priority
    #   else:
    #     self.highestPriority = sorted([ self.highestPriority, priority ])[0]
