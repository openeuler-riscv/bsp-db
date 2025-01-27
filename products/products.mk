PRODUCTS_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

include $(wildcard $(PRODUCTS_DIR)/*/vendor.mk)
VENDORS += $(wildcard $(PRODUCTS_DIR)/*/vendor.yml)