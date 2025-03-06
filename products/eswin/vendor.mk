ESWIN_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

SOCS += $(ESWIN_DIR)/eic7700x.yml
