BANANAPI_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

BOARDS += $(BANANAPI_DIR)/f3.yml
