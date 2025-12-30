ORANGEPI_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

BOARDS += $(ORANGEPI_DIR)/rv.yml
BOARDS += $(ORANGEPI_DIR)/rv2.yml
BOARDS += $(ORANGEPI_DIR)/r2s.yml
