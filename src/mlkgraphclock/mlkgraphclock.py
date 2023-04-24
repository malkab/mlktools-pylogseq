#!/usr/bin/env python3
# coding=UTF8

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import typer
from pylogseq.pylogseq import Graph, Page, Block

# Typer app
app = typer.Typer()

# To store the processed graphs
processed_graphs = []


@app.command()
def clock(
    graphs: list[str] = typer.Argument(..., help="List of graphs to parse.")
):
    for graph_path in graphs:
        g = Graph(graph_path)
        g.get_md_pages()

        processed_graphs.append(g)

    # Total pages
    total_pages = 0

    for g in processed_graphs:
        total_pages = total_pages + len(g.pages_file_name)

    print(total_pages)

    with typer.progressbar(length=total_pages) as progress:
        for g in processed_graphs:
            for p in g.read_pages():
                # print("D: 999", p.file_name)
                progress.update(1)


    # print("D: 000", processed_graphs)




# g = Graph("../pylogseq/tests/assets/Agenda")

# g.get_md_pages()

# g.read_pages()

# block: Block = None
# page: Page = None

# for page in g.pages:
#     for block in page.blocks:
#         print("D: 000 ", block.title, block.logbook)

if __name__ == "__main__":
    app()
