<div align="center">
    <a href="https://v2.nonebot.dev/store">
    <img src="https://raw.githubusercontent.com/fllesser/nonebot-plugin-template/refs/heads/resource/.docs/NoneBotPlugin.svg" width="310" alt="logo"></a>

## ✨ Nonebot2 表情回应插件 ✨

<a href="https://raw.githubusercontent.com/fllesser/nonebot-plugin-emojilike/master/LICENSE">
    <img src="https://img.shields.io/github/license/fllesser/nonebot-plugin-emojilike" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-emojilike">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-emojilike.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
<a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json" alt="ruff">
</a>
<a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
</a>
<a href="https://results.pre-commit.ci/latest/github/fllesser/nonebot-plugin-resolver2/master">
    <img src="https://results.pre-commit.ci/badge/github/fllesser/nonebot-plugin-resolver2/master.svg" alt="pre-commit" />
</a>
<a href="https://codecov.io/gh/fllesser/nonebot-plugin-emojilike" > 
    <img src="https://codecov.io/gh/fllesser/nonebot-plugin-emojilike/graph/badge.svg?token=OC91SWU8YE"/> 
</a>
</div>


## 📖 介绍

NoneBot onebotV11 点赞，表情回应插件

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-emojilike --upgrade

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>uv</summary>

    uv add nonebot-plugin-emojilike
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-emojilike
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-emojilike
</details>


打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_emojilike"]

</details>


## 🎉 使用
### 指令表
|   指令   | 权限  | 需要@ | 范围  |   说明   |
| :------: | :---: | :---: | :---: | :------: |
|   赞我   | 群员  |  否   | 群聊  | 顾名思义 |
| 天天赞我 | 群员  |  否   | 群聊  | 顾名思义 |

## 效果图
<img src="docs/1.png">
<img src="docs/2.png">
<img src="docs/3.png">