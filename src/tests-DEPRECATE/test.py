import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

from marko import Markdown
from pylogseq.src.pylogseq.mdlogseq.logseqparse import LogseqParse
from pylogseq.src.pylogseq.block import Block
from pylogseq.src.pylogseq.page import Page

# g = LogseqParse()
mark = Markdown(extensions=[LogseqParse])

p = Page()

markdown = """
- DONE #[[A/B/C/Gestión general]] #H/N/T [[P/YU]] Something
  :LOGBOOK:
  CLOCK: [2022-11-25 Fri 08:50:00]--[2022-11-25 Fri 09:00:00] =>  00:12:33
  CLOCK: [2022-11-25 Fri 10:01:13]--[2022-11-25 Fri 10:01:17] =>  00:00:04
  CLOCK: [2022-11-25 Fri 10:01:18]--[2022-11-25 Fri 10:07:58] =>  00:06:40
  CLOCK: [2022-11-25 Fri 12:17:38]--[2022-11-25 Fri 12:19:27] =>  00:01:49
  CLOCK: [2022-11-25 Fri 14:49:56]--[2022-11-25 Fri 14:54:06] =>  00:04:10
  :END:
  - LATER [#C] Algo que se escribe así como el que no quiere la cosa
  - [#B] Otra cosa escrita a voleo total
    - [#A] KKKKK
      - [#C] 44444
  - [#C] #H/N/T Ya estoy un poco cansado
    ```txt
    jejwer
    kekrwer

    4k3k3
    lk3k4

    eker
    34343
    ```

    ```Python
    a = 4
    ```
- LATER [#C] #A/J/O Something in the way
- A
- B
- C
"""

blocks = p.getBlocks(p.parseMarkdown(mark, markdown))

for x in blocks:
  print("\n\nBlocks str:")
  print(x.strBlock)
  print(x.tags)
  print(x.highestPriority)
