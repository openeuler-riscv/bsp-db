SPACEMIT_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

BOARDS += $(SPACEMIT_DIR)/muse_pi.yml
BOARDS += $(SPACEMIT_DIR)/muse_card.yml
SOCS += $(SPACEMIT_DIR)/m1.yml
SOCS += $(SPACEMIT_DIR)/k1.yml
