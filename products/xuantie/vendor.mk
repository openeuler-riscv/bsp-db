XUANTIE_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

SOCS += $(XUANTIE_DIR)/th1520.yml
