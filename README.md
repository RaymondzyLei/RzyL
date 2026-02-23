# RzyL - 物理实验查询机器人

基于 NoneBot2 的 QQ 机器人，提供物理实验图片查询功能，支持精确匹配和 AI 模糊匹配。

## 功能特性

- **关键词匹配**：支持精确匹配和 AI 模糊匹配物理实验关键词
- **图片查询**：根据关键词返回对应的实验图片
- **多关键词支持**：一次查询可返回多个匹配的实验图片
- **智能回退**：精确匹配失败时自动使用 AI 进行模糊匹配

## 安装

1. 克隆项目
2. 安装依赖：
   ```bash
   uv sync
   ```

## 配置

复制 `.env.secret.temple` 为 `.env.secret` 并填写配置：

```env
BASE_URL=https://api.longcat.chat/openai
API_KEY=your_api_key
MODEL_CHAT=your_chat_model
MODEL_THINK=your_think_model
MODEL_LITE=your_lite_model
```

## 使用方法

### 基本命令

- `大雾1 实验名称` - 查询实验图片
- `大雾1 ls` - 查看所有可用关键词
- `大雾1 help` - 查看帮助信息

### 示例

```
大雾1 杨氏模量        # 返回杨氏模量实验图片
大雾1 示波器          # 返回示波器使用图片
大雾1 光电            # 返回光电效应图片
大雾1 物理实验        # AI 模糊匹配相关实验
```

## 项目结构

```
RzyL/
├── src/
│   ├── plugins/
│   │   └── dawu/          # 主插件
│   │       ├── __init__.py  # 主逻辑
│   │       ├── config.py    # 配置
│   │       ├── keywords.py  # 关键词定义
│   │       └── ai_match.py  # AI 匹配
│   └── asserts/
│       └── dawu/           # 实验图片
├── bot.py                 # 机器人入口
├── pyproject.toml         # 项目配置
└── .env                   # 环境变量
```

## 技术栈

- **框架**：NoneBot2
- **适配器**：OneBot v11
- **命令解析**：Alconna
- **AI 匹配**：OpenAI 兼容 API

## 开发

运行机器人：
```bash
uv run bot.py
```

## 许可证

MIT
