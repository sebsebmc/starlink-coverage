CURRENT_DATE = $(shell date -u +%F)

.PHONY: install-deps generate-coverage

install-deps:
	pip3 install -r requirements.txt

generate-coverage:
	./gen_cov.sh
