MICROCHIP_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

SOCS += $(MICROCHIP_DIR)/mpfs025t.yml
