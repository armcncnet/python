# 🤖 Python Framework SDK

⚡ Python development framework for armcnc. ⚡

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 已经内置在armcnc中，无需单独、重复安装，该仓库仅供学习参考。

## 📖 Initialization

> 安装相关依赖

```shell
pip3 install armcnc websocket-client==0.48.0 requests pyserial
```

## 📖 Using templates

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import armcnc as framework

def framework_start(cnc):
    pass

if __name__ == '__main__':
    framework_sdk = framework.Init()
```

## 📖 Development

> 安装相关依赖
>
> Install the required dependencies.

```shell
pip3 install twine setuptools wheel
```

> 构建软件包
>
> Build software package.

```shell
python3 setup.py sdist bdist_wheel
```

> 上传软件包到PyPI
>
> Upload software package to PyPI.

```shell
twine upload dist/*
```

## 🌞 Development Team

> https://www.armcnc.net