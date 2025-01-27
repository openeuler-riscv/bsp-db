STARFIVE_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

BOARDS += $(STARFIVE_DIR)/visionfive2.yml
SOCS += $(STARFIVE_DIR)/jh7110.yml
