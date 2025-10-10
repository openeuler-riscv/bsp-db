SIPEED_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

BOARDS += $(SIPEED_DIR)/licheepi_3a.yml
BOARDS += $(SIPEED_DIR)/licheepi_4a.yml
