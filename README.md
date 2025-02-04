# OERV 板卡支持状态数据库

这里列出了 openEuler 对 RISC-V 支持的版本，以及该版本所支持的板卡信息、对应板卡的系统镜像下载链接、配套的使用文档等数据。

数据源采用 YAML 进行归档。数据的关联关系基于 “镜像 -> 板卡” 的逻辑进行组织，主视点为发布的镜像。即，发布的镜像信息里引用该镜像适配的板卡信息。

对于反向的查询需求，即查询某张板卡有哪些镜像支持，需要将 YAML 综合处理后得到。本仓库提供构建方法，生成对应的 JSON 数据。

## 目录结构

```
├── distros
│   ├── distros.mk
│   └── distro_A
│       ├── distro_release_A
│       │   ├── imagesuites
│       │   │   └── released_image_for_distroA_releaseA_with_feature_A.yml
│       │   ├── release-info.yml
│       │   └── release.mk
│       ├── distro.mk
│       └── distro.yml
├── docs
│   └── category_A
│       ├── md_docs_A.md
│       └── md_docs_A.resc
│           └── md_docs_A_pic1.png
├── Makefile
├── products
│   └── vendor_A
│       ├── product_A.yml
│       ├── vendor.mk
│       └── vendor.yml
├── README.md
├── requirements.txt
├── resources
│   └── some_directory
│       └── another_directoy
│           └── some_images.jpg
├── schema
│   └── some_schema.yml
└── scripts
    └── script_A.py
```

##### distros

发行版目录，包含 openEuler RISC-V 以及基于 OERV 制作的下游发行版。

##### docs

文档目录，里面的文档被镜像套件引用。可能存在同一份文档被多套镜像共享的情况。

##### products

产品目录，板卡、SoC 等均列入其中，供镜像套件引用。

##### resources

存储一些资源文件，目前主要是板卡图片。

##### schema

用来校验 YAML 的模板信息。

##### scripts

维护以及生成 JSON 数据使用到的脚本程序。

## JSON 生成方法

安装依赖：

```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

校验 YAML：

```shell
make -j$(nproc) validate
```

生成 JSON：

```shell
make O=./build -j$(nproc)
```

生成的 JSON 数据位于 `./build` 目录下。

当有脚本改动或构建系统改动时，清除构建产物并重新生成：

```shell
make clean; make O=./build -j$(nproc)
```

## 数据维护

### 增添新镜像套件

在 `distros/${distro}/${release}/imagesuites` 下创建一个新的 `.yml` 文件，命名应简短但包含镜像支持的板卡，关键特性等。

在该文件内填入必要信息。

## TBD

- [ ] YAML 自定义文件引用检查
- [ ] 精确到输出目标的资源文件构建规则
