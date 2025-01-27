THEAD_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

SOCS += $(THEAD_DIR)/th1520.yml
