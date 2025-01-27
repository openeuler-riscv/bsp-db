OPENEULER_24.03_SP1_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

DISTRO_RELEASES += $(OPENEULER_24.03_SP1_DIR)/release-info.yml
IMAGESUITES += $(wildcard $(OPENEULER_24.03_SP1_DIR)/imagesuites/*.yml)
