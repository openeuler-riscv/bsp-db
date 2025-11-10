OPENEULER_24.03_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

DISTRO_RELEASES += $(OPENEULER_24.03_DIR)/release-info.yml
IMAGESUITES += $(wildcard $(OPENEULER_24.03_DIR)/imagesuites/*.yml)
