SPACEMIT_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

BOARDS += $(SPACEMIT_DIR)/muse_pi.yml
BOARDS += $(SPACEMIT_DIR)/muse_card.yml
BOARDS += $(SPACEMIT_DIR)/muse_box.yml

SOCS += $(SPACEMIT_DIR)/k1_m1.yml
