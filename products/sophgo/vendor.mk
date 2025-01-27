SOPHON_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

SOCS += $(SOPHON_DIR)/sg2042.yml
