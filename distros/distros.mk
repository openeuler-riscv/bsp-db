DISTROS_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

include $(wildcard $(DISTROS_DIR)/*/distro.mk)