EULACEURA_23H1_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

DISTRO_RELEASES += $(EULACEURA_23H1_DIR)/release-info.yml
IMAGESUITES += $(wildcard $(EULACEURA_23H1_DIR)/imagesuites/*.yml)