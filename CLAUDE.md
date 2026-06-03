# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

基于 NoneBot2 的 QQ 机器人，提供物理实验图片查询功能，支持精确匹配和 AI 模糊匹配。彩蛋插件提供迪士尼角色查询和随机文本功能，通过依赖注入与主插件联动。

## 开发命令

```bash
uv sync              # 安装依赖
uv run bot.py        # 运行机器人
uv run pyright       # 静态类型检查
```

## 项目架构

```
RzyL/
├── bot.py                    # 机器人入口，注册适配器和插件
├── pyproject.toml             # 项目配置
├── src/
│   ├── plugins/
│   │   ├── dawu/              # 主插件 - 物理实验查询
│   │   │   ├── __init__.py    # 主逻辑: 命令处理、关键词匹配、AI回退
│   │   │   ├── config.py      # 配置: ALLOWED_GROUPS, get_image_path
│   │   │   ├── keywords.py     # 关键词加载（从keywords.json读取）
│   │   │   └── ai_match.py    # AI匹配逻辑（异步API调用，信号量控制8并发）
│   │   ├── easter_egg/        # 彩蛋插件 - 迪士尼角色查询、随机文本
│   │   │   ├── __init__.py    # 彩蛋命令处理，导出 try_load_random_text 等接口
│   │   │   ├── keywords.py     # 迪士尼关键词加载（8个角色）
│   │   │   ├── random_text.py # 随机文本加载（概率发送一言或小问题）
│   │   │   ├── sentences.txt  # 随机一言句子库
│   │   │   └── question.txt   # 随机小问题库
│   │   └── echo/             # Echo插件(示例)
│   ├── asserts/
│   │   ├── dawu/             # 物理实验图片和关键词JSON
│   │   └── easter_egg/        # 迪士尼角色图片和关键词JSON
```

## 核心机制

- **命令解析**: 使用 Alconna，命令格式为 `大雾1 <实验名称>` 和 `彩蛋 <角色名>`
- **关键词匹配**: 各插件的 `keywords.py` 中定义 KEYWORDS 字典，支持别名匹配
- **AI回退**: 精确匹配失败时调用 AI API 进行模糊匹配（8并发限制），仅匹配物理关键词
- **速率限制**: 每用户每分钟最多10次请求
- **群组过滤**: 可通过 `dawu_allowed_groups` 配置允许的群组
- **随机文本**: dawu 通过 `require("src.plugins.easter_egg")` 导入 `try_load_random_text`，查询物理实验后有概率发送随机一言或小问题
- **跨插件联动**: dawu 依赖 easter_egg（require + 直接导入），easter_egg 导出 `EASTER_EGG_KEYWORDS`、`get_easter_egg_image_path`、`try_load_random_text`

## 关键文件

- `bot.py` - 机器人入口，注册适配器和插件
- `src/plugins/dawu/__init__.py` - 主插件逻辑，包含 `大雾1` 命令处理器
- `src/plugins/dawu/config.py` - 群组配置和图片路径获取
- `src/plugins/dawu/keywords.py` - 关键词加载器（从 asserts/dawu/keywords.json 读取）
- `src/plugins/dawu/ai_match.py` - AI匹配逻辑（异步API调用）
- `src/plugins/easter_egg/__init__.py` - 彩蛋插件，包含 `彩蛋` 命令处理器
- `src/plugins/easter_egg/random_text.py` - 随机文本加载
- `.env.secret` - API密钥配置（从 `.env.secret.temple` 复制）