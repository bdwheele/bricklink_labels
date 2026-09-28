#!/bin/env python3

from pathlib import Path
import sys
import argparse

from bricklink import BrickLink
from brickstore import BrickStore
from brickarchitect import BrickArchitect

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('bsx_file', type=Path, help="BSX file to process")
    parser.add_argument('html_file', type=Path, help="Output HTML file")
    parser.add_argument('part_indexes', nargs='*', help="BSX file indexes to generate, leave blank for all")
    args = parser.parse_args()

    cachedir = Path(sys.path[0], 'cache')
    cachedir.mkdir(exist_ok=True)
    bl = BrickLink()
    bs = BrickStore(args.bsx_file)
    ba = BrickArchitect('https://brickarchitect.com', cachedir)

    if not args.part_indexes:
        args.part_indexes = list(range(len(bs.items)))

    html = "<html><head>"
    html += """<style>
body {
    font-family: Arial, sans-serif;
}
    
.container {
    display: flex;
    flex-wrap: wrap;
}
    
.box {
    width: 3in;
    height: 1in;
    border: 1pt solid black;
    display: flex;
    padding: 2px;
    gap: 2px;
}

.part_description {
    white-space: wrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 2in;
    height: 0.95in;    
}

.part_image {
    width: 1in;
    height: 1in;
    object-fit: contain;
}


</style>
"""

    html += '</head><body><div class="container">'
    for idx in args.part_indexes:
        item = bl.catalog_by_number(bs.items[idx].id)
        html += '<div class="box">'
        html += f'<div><img class="part_image" src="{bl.get_image_data(item, bs.items[idx].color)}"/></div>'        
        html += f'<div class="part_description">{item.type_id}: <b>{bs.items[idx].id}</b> / {bs.items[idx].condition}<br/>'
        html += f'<hr style="margin-top: 1px; margin-bottom: 1px;" />'
        if bs.items[idx].color != 0:
            html += f'{bs.items[idx].color_name}<br/>'
        html += f'{bs.items[idx].name}</div>'
        html += '</div>'
    html += "</div></body></html>"
    args.html_file.write_text(html)


if __name__ == "__main__":
    main()