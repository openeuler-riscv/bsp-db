SPACEMIT_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

BOARDS += $(SPACEMIT_DIR)/muse_pi.yml
BOARDS += $(SPACEMIT_DIR)/muse_card.yml
BOARDS += $(SPACEMIT_DIR)/muse_box.yml
BOARDS += $(SPACEMIT_DIR)/muse_pi_pro.yml

SOCS += $(SPACEMIT_DIR)/k1.yml
