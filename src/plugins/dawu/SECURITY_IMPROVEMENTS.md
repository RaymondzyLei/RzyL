# Dawu 插件 - 安全性和鲁棒性改进建议

## 当前问题分析

### 安全性问题

1. **用户输入未验证**
   - 没有对用户输入进行长度限制
   - 没有对特殊字符进行过滤
   - 可能导致路径遍历攻击

2. **AI 匹配无限制**
   - 没有速率限制
   - 可能被滥用导致 API 消耗
   - 没有请求超时控制

3. **图片路径未验证**
   - 没有检查路径是否在允许目录内
   - 可能被利用读取系统文件

4. **缺少权限控制**
   - 没有用户级别权限
   - 没有操作日志记录

### 鲁棒性问题

1. **缺少异常处理**
   - AI 请求失败没有降级方案
   - 文件操作没有错误处理
   - 可能导致机器人崩溃

2. **无日志记录**
   - 无法追踪问题
   - 难以调试

3. **无并发控制**
   - 多个请求可能导致资源耗尽
   - 没有请求队列管理

4. **无输入验证**
   - 空输入或无效输入处理不当
   - 没有格式验证

## 改进建议

### 1. 添加输入验证 ✅ 已完成

```python
def validate_input(text: str) -> bool:
    if not text or not text.strip():
        return False
    if len(text) > 100:
        return False
    return True
```

**实施状态**：已在 `__init__.py` 中实施
**实施时间**：2025-02-27
**验证方式**：检查输入长度（1-100字符）和空值

### 2. 添加速率限制 ✅ 已完成

```python
from collections import defaultdict
import time

RATE_LIMIT = defaultdict(list)
MAX_REQUESTS_PER_MINUTE = 10

def check_rate_limit(user_id: int) -> bool:
    now = time.time()
    user_requests = RATE_LIMIT[user_id]
    user_requests = [t for t in user_requests if now - t < 60]
    RATE_LIMIT[user_id] = user_requests
    return len(user_requests) < MAX_REQUESTS_PER_MINUTE
```

**实施状态**：已在 `__init__.py` 中实施
**实施时间**：2025-02-27
**限制方式**：每用户每分钟最多 10 次请求

### 3. 添加路径安全检查

```python
def is_safe_path(image_path: Path) -> bool:
    try:
        image_path.resolve().relative_to(Path.cwd() / "src" / "asserts" / "dawu")
        return True
    except ValueError:
        return False
```

### 4. 添加异常处理

```python
async def send_keyword_images(keywords: list[str], prefix: str = "找到关键词"):
    try:
        messages = []
        missing_keywords = []
        for keyword in keywords:
            if keyword in KEYWORDS:
                try:
                    image_path = get_image_path(keyword)
                    if image_path.exists() and is_safe_path(image_path):
                        first_alias = KEYWORDS[keyword][0] if KEYWORDS[keyword] else keyword
                        messages.append(f"{prefix}: {first_alias}:")
                        messages.append(MessageSegment.image(image_path))
                    else:
                        missing_keywords.append(keyword)
                except Exception as e:
                    logger.error(f"处理关键词 {keyword} 时出错: {e}")
                    missing_keywords.append(keyword)
        
        if messages:
            if missing_keywords:
                messages.append(f"{prefix}: {', '.join(keywords)}，但部分图片文件不存在: {', '.join(missing_keywords)}")
            await dawu1.finish(messages, reply_message=True)
        else:
            await dawu1.finish(f"{prefix}: {', '.join(keywords)}，但所有图片文件都不存在", reply_message=True)
    except Exception as e:
        logger.error(f"发送关键词图片时出错: {e}")
        await dawu1.finish("处理请求时出错，请稍后重试", reply_message=True)
```

### 5. 添加日志记录

```python
import logging

logger = logging.getLogger(__name__)

@dawu1.handle()
async def _(event: GroupMessageEvent, name: Match[str]):
    logger.info(f"收到请求: 群{event.group_id}, 用户{event.user_id}, 内容{name.result}")
    # ... 处理逻辑
```

### 6. 添加 AI 请求超时和重试

```python
async def ai_match(message: str, keywords: dict, max_retries: int = 2) -> list[str]:
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.post(url, headers=headers, json=data) as response:
                    response_json = await response.json()
                    # 处理响应
                    return keywords_found
        except asyncio.TimeoutError:
            logger.warning(f"AI请求超时，重试 {attempt + 1}/{max_retries}")
            if attempt == max_retries - 1:
                return []
        except Exception as e:
            logger.error(f"AI匹配请求失败: {e}")
            return []
```

### 7. 添加并发控制 ✅ 已完成

```python
import asyncio

AI_SEMAPHORE = asyncio.Semaphore(3)

async def ai_match(message: str, keywords: dict) -> list[str]:
    async with AI_SEMAPHORE:
        # AI 请求逻辑
        pass
```

**实施状态**：已在 `ai_match.py` 中实施
**实施时间**：2025-02-27
**控制方式**：使用 Semaphore 限制并发 AI 请求数量为 8

### 8. 添加配置验证

```python
def validate_config() -> bool:
    if not ALLOWED_GROUPS:
        return True
    if not isinstance(ALLOWED_GROUPS, list):
        logger.error("ALLOWED_GROUPS 配置错误，应为列表")
        return False
    for group_id in ALLOWED_GROUPS:
        if not isinstance(group_id, int):
            logger.error(f"群号 {group_id} 不是整数")
            return False
    return True
```

## 优先级建议

### 高优先级（立即实施）
1. 添加异常处理
2. 添加日志记录
3. 添加输入验证
4. 添加路径安全检查

### 中优先级（近期实施）
5. 添加速率限制
6. 添加 AI 请求超时和重试
7. 添加配置验证

### 低优先级（长期优化）
8. 添加并发控制
9. 添加用户级别权限
10. 添加操作审计日志

## 实施建议

建议分阶段实施这些改进：

**第一阶段**：添加基本的异常处理和日志记录
**第二阶段**：添加输入验证和路径安全检查
**第三阶段**：添加速率限制和请求控制

这样可以确保插件的安全性和鲁棒性逐步提升，同时不影响现有功能。
