SCHEMAS_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

SCHEMAS += $(SCHEMAS_DIR)/board.yml
SCHEMAS += $(SCHEMAS_DIR)/distro.yml
SCHEMAS += $(SCHEMAS_DIR)/distro_release.yml
SCHEMAS += $(SCHEMAS_DIR)/imagesuite.yml
SCHEMAS += $(SCHEMAS_DIR)/soc.yml
SCHEMAS += $(SCHEMAS_DIR)/vendor.yml
