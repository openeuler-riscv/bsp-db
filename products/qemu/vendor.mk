QEMU_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

BOARDS += $(QEMU_DIR)/system.yml
