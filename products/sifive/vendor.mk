SIFIVE_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

BOARDS += $(SIFIVE_DIR)/hifive-premier-p550.yml
