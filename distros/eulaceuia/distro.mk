EULACEUIA_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

include $(EULACEUIA_DIR)/23h1/release.mk