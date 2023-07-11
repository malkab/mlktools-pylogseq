#!/usr/bin/env python3
# coding=UTF8

from pylogseq import Graph, Page, Block, Clock
import typer
import arrow
import datetime
import statistics


# ----------------------------------
#
# CLI application
#
# ----------------------------------

# Typer app
app = typer.Typer()

# ----------------------------------
#
# Command.
#
# ----------------------------------
@app.command()
def a(
    graph_path: str = typer.Argument(..., help="The path of the graph to analyze.")
):

    # Create a graph
    graph: Graph = Graph(graph_path)

    # Get pages
    pages: list[Page] = graph.get_pages()

    # Blocks
    blocks: list[Block] = []

    # Get blocks
    for p in pages:
        p.read_page_file()
        blocks.extend(p.parse())

    # Print medatada
    print(f"Total number of pages to process: {len(pages)}")
    print(f"Total number of blocks to process: {len(blocks)}")

    # Calculate Arrow spans for the last weeks
    today = arrow.now()

    # To store the total elapsed time for each of the weeks
    elapsed_time_weeks = []

    # TODO: codificado en duro para 4 semanas, posible parámetro
    for i in range(1, 5):

        # Get the clock interval spanning the week
        span = today.shift(weeks=-i).span("week")
        clock = Clock(span[0].naive, span[1].naive)

        # To store all clocks that collides with the week span
        colliding_clocks = []

        # Intersect all clocks
        for block in blocks:
            colliding_clocks.extend(block.intersect_clock(clock))

        # Aggregate elapsed time
        total_time = datetime.timedelta(0)

        for cc in colliding_clocks:
            total_time = total_time + cc.elapsed

        # Store
        elapsed_time_weeks.append(total_time.total_seconds() / 3600.0)

    average_speed_last_weeks = round(statistics.mean(elapsed_time_weeks))

    # Print the average speed of last weeks
    print(f"Average speed of last weeks: {average_speed_last_weeks}")

    # Get total T and S times in blocks, but substracting the already
    # elapsed time in the clocks, so calculating remaining T time
    for block in blocks:
        # print("D: ", block.allocated_time, block.current_time, block.total_elapsed_time)

        print("D: rrrr", block.title)
        print("D: jjje", block.allocated_time)
        print("D: kkkk", block.current_time)
        print("D: nnnn", block.total_elapsed_time.total_seconds() / 3600.0)
        print("D: nvee", block.remaining_time, block.remaining_time.total_seconds() / 3600.0 if block.remaining_time else 0)
        print()














# ----------------------------------
#
# Main entrypoint.
#
# ----------------------------------
if __name__ == "__main__":
    app()
