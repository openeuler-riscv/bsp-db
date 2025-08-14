#!/usr/bin/env make

##### Have default "all" target listed at the beginning
.PHONY: default
default: all

##### Setup out-of-tree build
# ROOT_DIR & WORK_DIR are all absolute path.
# As well as DIST_DIR & STAGING_DIR

# Must be used before including any other Makefiles
define fetch_last_dir =
$(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))
endef

ROOT_DIR := $(realpath $(fetch_last_dir))
# O= must be an absolute path, otherwise unexpected behavior will occur when used in combination with make -C
ifdef O
WORK_DIR := $(realpath $(O))
else
WORK_DIR := $(ROOT_DIR)/build
endif
STAGING_DIR := $(WORK_DIR)/staging
# Generated JSON API compatiblity
JSON_API_VER := v2
DIST_DIR := $(WORK_DIR)/dist/$(JSON_API_VER)

##### Some useful shortcuts
dir_guard=@mkdir -p $(@D)

##### Collection of slices of build target
# I18N combinations
ALT_LANGS := zh_CN
# Provided by *.mk from subdirectories
# Those are ensured to be relative path to workdir
BOARDS :=
SOCS :=
VENDORS :=
DISTROS :=
DISTRO_RELEASES :=
IMAGESUITES :=
SCHEMAS :=

##### Populate sources
include $(ROOT_DIR)/products/products.mk
include $(ROOT_DIR)/distros/distros.mk
include $(ROOT_DIR)/schema/schema.mk
##### Processing sources
BOARDS := $(patsubst $(ROOT_DIR)/%,%,$(BOARDS))
SOCS := $(patsubst $(ROOT_DIR)/%,%,$(SOCS))
VENDORS := $(patsubst $(ROOT_DIR)/%,%,$(VENDORS))
DISTROS := $(patsubst $(ROOT_DIR)/%,%,$(DISTROS))
DISTRO_RELEASES := $(patsubst $(ROOT_DIR)/%,%,$(DISTRO_RELEASES))
IMAGESUITES := $(patsubst $(ROOT_DIR)/%,%,$(IMAGESUITES))
SCHEMAS := $(patsubst $(ROOT_DIR)/%,%,$(SCHEMAS))

##### Preparing staging dir
ALL_YAML_SRCS := $(BOARDS) $(SOCS) $(VENDORS) $(DISTROS) $(DISTRO_RELEASES) $(IMAGESUITES) $(SCHEMAS)
ALL_YAML_SRCS += $(foreach LANG,$(ALT_LANGS),$(addsuffix .$(LANG).yml,$(basename $(ALL_YAML_SRCS))))
STAGING_YAMLS := $(addprefix $(STAGING_DIR)/,$(ALL_YAML_SRCS))

$(STAGING_YAMLS): $(STAGING_DIR)/%: %
	$(dir_guard)
	cp $* $@
$(STAGING_DIR)/docs: $(ROOT_DIR)/docs
	$(dir_guard)
	ln -s $< $@
$(STAGING_DIR)/gallery: $(ROOT_DIR)/gallery
	$(dir_guard)
	ln -s $< $@
$(STAGING_DIR)/include: $(ROOT_DIR)/include
	$(dir_guard)
	ln -s $< $@

SYNC_STAGING_TARGETS := $(STAGING_YAMLS) $(STAGING_DIR)/docs $(STAGING_DIR)/gallery $(STAGING_DIR)/include

##### Check if all yamls have their i18n counterpart key-matched
ALL_I18N_MATCHING_CHECK_TARGETS :=

define I18N_MATCHING_TEMPLETE =
$(1).$(2).MATCHING_TARGETS = $$(addsuffix .$(2).i18n.matching,$$($(1)))
.PHONY: $$($(1).$(2).MATCHING_TARGETS)
$$($(1).$(2).MATCHING_TARGETS): %.yml.$(2).i18n.matching: \
		$(STAGING_DIR)/%.yml $(STAGING_DIR)/%.$(2).yml \
		$(ROOT_DIR)/scripts/check_matching.py \
		$(SYNC_STAGING_TARGETS)
	$(ROOT_DIR)/scripts/check_matching.py -r $(STAGING_DIR) $$*.yml $$*.$(2).yml
ALL_I18N_MATCHING_CHECK_TARGETS += $$($(1).$(2).MATCHING_TARGETS)
endef
$(foreach LANG,$(ALT_LANGS),$(eval $(call I18N_MATCHING_TEMPLETE,SCHEMAS,$(LANG))))
$(foreach LANG,$(ALT_LANGS),$(eval $(call I18N_MATCHING_TEMPLETE,BOARDS,$(LANG))))
$(foreach LANG,$(ALT_LANGS),$(eval $(call I18N_MATCHING_TEMPLETE,SOCS,$(LANG))))
$(foreach LANG,$(ALT_LANGS),$(eval $(call I18N_MATCHING_TEMPLETE,VENDORS,$(LANG))))
$(foreach LANG,$(ALT_LANGS),$(eval $(call I18N_MATCHING_TEMPLETE,DISTROS,$(LANG))))
$(foreach LANG,$(ALT_LANGS),$(eval $(call I18N_MATCHING_TEMPLETE,DISTRO_RELEASES,$(LANG))))
$(foreach LANG,$(ALT_LANGS),$(eval $(call I18N_MATCHING_TEMPLETE,IMAGESUITES,$(LANG))))

.PHONY: check_i18n_matching
check_i18n_matching: $(ALL_I18N_MATCHING_CHECK_TARGETS)

##### Check if all yaml sources comform to schema
ALL_SCHEMA_VALIDATING_TARGETS :=
define SCHEMA_VALIDATING_TEMPLATE =
$(1)$(3).SCHEMA_VALIDATING_TARGETS := $$(addsuffix .schema.validating,$$(addsuffix $(3).yml,$$(basename $$($(1)))))
.PHONY: $(SOCS_SCHEMA_VALIDATING_TARGETS)
$$($(1)$(3).SCHEMA_VALIDATING_TARGETS): %.schema.validating: $(STAGING_DIR)/% \
		$(ROOT_DIR)/scripts/validate.py \
		$(STAGING_DIR)/schema/$(2)$(3).yml \
		$(SYNC_STAGING_TARGETS)
	$(ROOT_DIR)/scripts/validate.py -r $(STAGING_DIR) -s schema/$(2)$(3).yml $$*
ALL_SCHEMA_VALIDATING_TARGETS += $$($(1)$(3).SCHEMA_VALIDATING_TARGETS)
endef
$(eval $(call SCHEMA_VALIDATING_TEMPLATE,BOARDS,board,))
$(foreach LANG,$(ALT_LANGS),$(eval $(call SCHEMA_VALIDATING_TEMPLATE,BOARDS,board,.$(LANG))))
$(eval $(call SCHEMA_VALIDATING_TEMPLATE,SOCS,soc,))
$(foreach LANG,$(ALT_LANGS),$(eval $(call SCHEMA_VALIDATING_TEMPLATE,SOCS,soc,.$(LANG))))
$(eval $(call SCHEMA_VALIDATING_TEMPLATE,VENDORS,vendor,))
$(foreach LANG,$(ALT_LANGS),$(eval $(call SCHEMA_VALIDATING_TEMPLATE,VENDORS,vendor,.$(LANG))))
$(eval $(call SCHEMA_VALIDATING_TEMPLATE,DISTROS,distro,))
$(foreach LANG,$(ALT_LANGS),$(eval $(call SCHEMA_VALIDATING_TEMPLATE,DISTROS,distro,.$(LANG))))
$(eval $(call SCHEMA_VALIDATING_TEMPLATE,DISTRO_RELEASES,distro_release,))
$(foreach LANG,$(ALT_LANGS),$(eval $(call SCHEMA_VALIDATING_TEMPLATE,DISTRO_RELEASES,distro_release,.$(LANG))))
$(eval $(call SCHEMA_VALIDATING_TEMPLATE,IMAGESUITES,imagesuite,))
$(foreach LANG,$(ALT_LANGS),$(eval $(call SCHEMA_VALIDATING_TEMPLATE,IMAGESUITES,imagesuite,.$(LANG))))

.PHONY: check_schema
check_schema: $(ALL_SCHEMA_VALIDATING_TARGETS)

##### Check all
.PHONY: check
check: check_i18n_matching check_schema

##### Preparing dist dir
$(DIST_DIR)/resources/docs: $(ROOT_DIR)/docs
	$(dir_guard)
	rsync -avh $(ROOT_DIR)/docs $(DIST_DIR)/resources/
$(DIST_DIR)/resources/gallery: $(ROOT_DIR)/gallery
	$(dir_guard)
	rsync -avh $(ROOT_DIR)/gallery $(DIST_DIR)/resources/

SYNC_DIST_TARGETS := $(DIST_DIR)/resources/docs $(DIST_DIR)/resources/gallery

##### Generate json dist: board-centric view
# Board data
PER_BOARD_JSON :=
define PER_BOARD_JSON_TEMPLATE =
PER_BOARD_JSON.$(1) := $(addsuffix .json,$(basename $(addprefix $(DIST_DIR)/$(1)/,$(BOARDS))))
.PHONY: $$(PER_BOARD_JSON.$(1))
$$(PER_BOARD_JSON.$(1)): $(DIST_DIR)/$(1)/%.json: $(STAGING_DIR)/%$(2).yml \
		$(SYNC_STAGING_TARGETS) \
		$(ROOT_DIR)/scripts/gen_board_json.py
	$$(dir_guard)
	$(ROOT_DIR)/scripts/gen_board_json.py -r $(STAGING_DIR) -i $$(*)$(2).yml -o $$@ -p $(JSON_API_VER)/resources
PER_BOARD_JSON += $$(PER_BOARD_JSON.$(1))
endef
$(eval $(call PER_BOARD_JSON_TEMPLATE,en_US,))
$(foreach LANG,$(ALT_LANGS),$(eval $(call PER_BOARD_JSON_TEMPLATE,$(LANG),.$(LANG))))

# Walk through imagesuites
WALK_IMAGESUITE_TARGETS :=
define WALK_IMAGESUITE_TARGETS_TEMPLATE =
WALK_IMAGESUITE_TARGETS.$1 := $(addsuffix $2.yml.WALK,$(basename $(addprefix $(STAGING_DIR)/,$(IMAGESUITES))))
.PHONY: $$(WALK_IMAGESUITE_TARGETS.$1)
.NOTPARALLEL: $$(WALK_IMAGESUITE_TARGETS.$1)
$$(WALK_IMAGESUITE_TARGETS.$1): $(STAGING_DIR)/%$2.yml.WALK: $(STAGING_DIR)/%$2.yml \
		$(SYNC_STAGING_TARGETS) \
		$(PER_BOARD_JSON) \
		$(ROOT_DIR)/scripts/parse_imagesuite.py
	$(ROOT_DIR)/scripts/parse_imagesuite.py -r $(STAGING_DIR) -i $$(*)$(2).yml -o $(DIST_DIR)/$1 -p $(JSON_API_VER)/resources
WALK_IMAGESUITE_TARGETS += $$(WALK_IMAGESUITE_TARGETS.$1)
endef
$(eval $(call WALK_IMAGESUITE_TARGETS_TEMPLATE,en_US,))
$(foreach LANG,$(ALT_LANGS),$(eval $(call WALK_IMAGESUITE_TARGETS_TEMPLATE,$(LANG),.$(LANG))))

.PHONY: walk_imagesuites
walk_imagesuites: $(WALK_IMAGESUITE_TARGETS)

,PHONY: per_board_json
per_board_json: walk_imagesuites

# Board list
BOARD_LIST_TARGETS :=
define BOARD_LIST_TEMPLATE =
$(DIST_DIR)/$1/boards.json: per_board_json $(addsuffix .json,$(basename $(addprefix $(DIST_DIR)/$(1)/,$(BOARDS))))
	$(ROOT_DIR)/scripts/gen_board_list_json.py -r $(WORK_DIR)/dist -o $$@ $$(filter-out per_board_json,$$^)
BOARD_LIST_TARGETS += $(DIST_DIR)/$1/boards.json
endef
$(eval $(call BOARD_LIST_TEMPLATE,en_US,))
$(foreach LANG,$(ALT_LANGS),$(eval $(call BOARD_LIST_TEMPLATE,$(LANG),.$(LANG))))

.PHONY: board_list_json
board_list_json: $(BOARD_LIST_TARGETS)

.PHONY: riscv_isa_info
riscv_isa_info: $(DIST_DIR)/resources/riscv64_isa_extensions.json
$(DIST_DIR)/resources/riscv64_isa_extensions.json: $(STAGING_DIR)/include/yaml/riscv-extensions.yml
	$(ROOT_DIR)/scripts/gen_isa_info.py -i $< -o $@

.PHONY: dist
dist: $(SYNC_DIST_TARGETS) per_board_json board_list_json riscv_isa_info

.PHONY: clean
clean:
	rm -rf $(WORK_DIR)

.PHONY: all
all: clean check dist
