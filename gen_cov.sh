date
seq 0 3 | parallel -j4 "./main.py {}"
mv tle_cache/starlink.txt tle_cache/starlink-`date -u +%F`.txt
mv h3_4_cov_full.txt h3_4_cov_op_`date -u +%F`.txt
./merge_cover.py