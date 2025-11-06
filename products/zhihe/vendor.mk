ZHIHE_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

SOCS += $(ZHIHE_DIR)/a210.yml
BOARDS += $(ZHIHE_DIR)/a210-dev.yml
