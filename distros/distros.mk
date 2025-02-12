DISTROS_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

include $(DISTROS_DIR)/openeuler/distro.mk
include $(DISTROS_DIR)/eulaceuia/distro.mk
