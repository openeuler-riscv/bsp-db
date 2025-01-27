MILKV_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

BOARDS += $(MILKV_DIR)/pioneer.yml
