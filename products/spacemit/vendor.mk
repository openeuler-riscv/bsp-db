SPACEMIT_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

BOARDS += $(SPACEMIT_DIR)/muse_pi.yml
SOCS += $(SPACEMIT_DIR)/m1.yml
