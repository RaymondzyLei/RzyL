# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

基于 NoneBot2 的 QQ 机器人，提供物理实验图片查询功能，支持精确匹配和 AI 模糊匹配。

## 开发命令

```bash
uv sync              # 安装依赖
uv run bot.py        # 运行机器人
```

## 项目架构

```
src/
├── plugins/
│   ├── dawu/           # 主插件 - 物理实验查询
│   │   ├── __init__.py  # 主逻辑: 命令处理、关键词匹配、AI回退
│   │   ├── config.py    # 配置: ALLOWED_GROUPS, KEYWORDS
│   │   ├── ai_match.py  # AI匹配逻辑
│   │   └── sentences.txt # 随机发送的句子库
│   └── echo/            # Echo插件(示例)
└── asserts/
    └── dawu/            # 实验图片存储目录
```

## 核心机制

- **命令解析**: 使用 Alconna，命令格式为 `大雾1 <实验名称>`
- **关键词匹配**: `keywords.py` 中定义 KEYWORDS 字典，支持别名匹配
- **AI回退**: 精确匹配失败时调用 AI API 进行模糊匹配
- **速率限制**: 每用户每分钟最多10次请求
- **群组过滤**: 可通过 `ALLOWED_GROUPS` 配置允许的群组

## 关键文件

- `bot.py` - 机器人入口，注册适配器和插件
- `src/plugins/dawu/__init__.py` - 主插件逻辑，包含 `dawu1` 命令处理器
- `src/plugins/dawu/config.py` - 关键词定义和图片路径获取
- `.env.secret` - API密钥配置（从 `.env.secret.temple` 复制）