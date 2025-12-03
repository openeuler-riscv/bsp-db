SOPHON_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

SOCS += $(SOPHON_DIR)/sg2042.yml
SOCS += $(SOPHON_DIR)/sg2044.yml

BOARDS += $(SOPHON_DIR)/sg2044-evb.yml
