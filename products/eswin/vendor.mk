ESWIN_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

SOCS += $(ESWIN_DIR)/eic7700x.yml
BOARDS += $(ESWIN_DIR)/ebc77.yml
BOARDS += $(ESWIN_DIR)/eic7700-evb-a2.yml
