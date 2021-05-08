#!/usr/bin/env python3

from collections import defaultdict
from typing import Dict
import struct

coverage: Dict[str, int] = {}
with open(f"h3_4_index.txt", "r") as fd:
    lines = fd.readlines()
    coverage = {line.strip(): 0 for line in lines}
print(len(coverage))
for i in range(4):
    with open(f"h3_4_cov_{i}.txt", "r") as fd:
        lines = fd.readlines()
        for line in lines:
            [index, val] = line.strip().split(',')
            coverage[index] += int(val)

with open(f"h3_4_cov_full.txt", "w") as fd:
    for idx, val in coverage.items():
        fd.write(f"{idx},{val}\n")

with open(f"h3_4_cov_op.bin", "wb") as fd:
    for idx, val in coverage.items():
        idx_bytes = int(idx[:-8], 16)
        packed = struct.pack("<II", idx_bytes, int(val))
        fd.write(packed)

###################Come back to this########################
# this won't actually get me very useful statistics at the #
# moment because of the multiple satellites problem        #
exit()
base_cells = h3.get_res0_indexes()
all_cells = []
for base_cell in base_cells:
    res4_cells = h3.h3_to_children(base_cell, 4)
    res3_cells = h3.h3_to_children(base_cell, 3)
    res2_cells = h3.h3_to_children(base_cell, 2)

# res_4_cov
# with open(f"h3_4_cov_full.txt", "w") as fd:

# res_3_cov
# with open(f"h3_3_cov_full.txt", "w") as fd:

# res_2_cov
# with open(f"h3_2_cov_full.txt", "w") as fd:
