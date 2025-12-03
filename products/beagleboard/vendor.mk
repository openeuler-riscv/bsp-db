BEAGLEBOARD_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

BOARDS += $(BEAGLEBOARD_DIR)/beaglev-ahead.yml
BOARDS += $(BEAGLEBOARD_DIR)/beaglev-fire.yml
