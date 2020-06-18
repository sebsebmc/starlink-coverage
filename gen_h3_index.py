#!/usr/bin/env python3

import h3

base_cells = h3.get_res0_indexes()

all_cells = []
for base_cell in base_cells:
    res5_cells = h3.h3_to_children(base_cell, 5)
    all_cells += res5_cells

with open("h3_5_index.txt", "w") as fd:
    for cell in all_cells:
        fd.write(f"{cell}\n")