OPENEULER_25.09_DIR := $(fetch_last_dir)

DISTRO_RELEASES += $(OPENEULER_25.09_DIR)/release-info.yml
IMAGESUITES += $(wildcard $(OPENEULER_25.09_DIR)/imagesuites/*.yml)
