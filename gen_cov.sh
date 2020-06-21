date
seq 0 3 | parallel -j4 "./main.py {}"
# mv h3_4_cov_full.txt h3_4_cov_full_`date -u +%F`.txt
./merge_cover.py