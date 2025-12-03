STARFIVE_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

SOCS += $(STARFIVE_DIR)/jh7100.yml
SOCS += $(STARFIVE_DIR)/jh7110.yml

BOARDS += $(STARFIVE_DIR)/visionfive.yml
BOARDS += $(STARFIVE_DIR)/visionfive2.yml
