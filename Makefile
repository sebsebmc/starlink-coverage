CURRENT_DATE = $(shell date -u +%F)

.PHONY: install-deps generate-coverage

install-deps:
	pip3 install -r requirements.txt
	# this has to be installed separately until 0.19 is released https://github.com/SciTools/cartopy/issues/1552
	pip3 install cartopy==0.18

generate-coverage:
	seq 0 3 | parallel -j4 "./main.py {}"
	mv tle_cache/starlink.txt tle_cache/starlink-${CURRENT_DATE}.txt
	mv h3_4_cov_full.txt h3_4_cov_op_${CURRENT_DATE}.txt
	./merge_cover.py