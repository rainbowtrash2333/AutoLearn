# AutoLearn

一个自动学习[银保学院](https://learning.cbit.com.cn)课程的Python工具，支持批量处理多用户并自动完成在线课程学习。

## 功能特点

- 🚀 **自动化学习**: 模拟正常观看过程，自动完成课程学习
- 📱 **验证码识别**: 使用OCR技术自动识别登录验证码
- 🔒 **数据加密**: 支持AES加密，保护用户敏感信息
- ⚡ **并发处理**: 支持多用户并发学习，提高效率
- 📝 **详细日志**: 完整的日志记录系统，便于监控和调试
- ⚙️ **灵活配置**: 通过配置文件自定义学习参数

## 系统要求

- Python 3.12+
- 支持的操作系统: Windows, Linux, macOS

## 安装

1. 克隆项目
```bash
git clone <repository-url>
cd AutoLearn
```

2. 安装 Poetry (如果尚未安装)
```bash
curl -sSL https://install.python-poetry.org | python3 -
# 或在 Windows 上
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

3. 使用 Poetry 安装依赖
```bash
poetry install
```

4. 激活虚拟环境
```bash
poetry shell
```

## 配置

### 1. 用户配置 (token.json)
创建 `token.json` 文件，配置用户信息：
```json
[
  {
    "phone": "手机号码",
    "name": "用户姓名", 
    "passwd": "登录密码",
    "tcid": "课程库ID"
  }
]
```

### 2. 系统配置 (config.yaml)
项目包含完整的配置文件，主要配置项：

- **学习模式**:
  - `fast`: 快速模式，直接发送请求完成课程
  - `normal`: 正常模式，模拟真实观看过程
- **播放速度**: 默认1.5倍速
- **重试次数**: 请求失败时的重试次数
- **日志配置**: 日志级别和输出路径

## 使用方法

### 单用户学习
```python
from Learn_Cbit_v2 import Learn_Cbit

# 创建学习实例
learner = Learn_Cbit(
    phone="手机号",
    name="姓名", 
    password="密码",
    lessonLibrary_id="课程ID"
)

# 开始学习
learner.learn()
```

### 批量学习
```bash
poetry run python main.py
```

## 项目结构

```
AutoLearn/
├── main.py              # 主程序入口，支持多用户并发
├── Learn_Cbit_v2.py     # 核心学习模块
├── Learn_Cbit.py        # 旧版本学习模块
├── Learn_Cela.py        # CELA平台学习模块
├── AESCipher.py         # AES加密工具
├── requests_tool.py     # HTTP请求工具
├── aiohttp_tool.py      # 异步HTTP请求工具
├── tools.py             # 通用工具函数
├── yamlUtils.py         # YAML配置文件处理
├── exceptions.py        # 自定义异常类
├── config.yaml          # 系统配置文件
├── token.json           # 用户信息配置
└── pyproject.toml       # 项目依赖配置
```

## 技术栈

- **HTTP请求**: requests, aiohttp
- **OCR识别**: easyocr
- **加密解密**: pycryptodomex
- **并发处理**: multiprocessing
- **配置管理**: PyYAML

## 安全性

- 使用AES加密保护敏感数据
- 模拟真实浏览器行为，避免被检测
- 支持自定义请求头和用户代理
- 完整的错误处理和重试机制

## 注意事项

⚠️ **重要提示**:
- 本工具仅用于学习和研究目的
- 请遵守相关平台的使用条款
- 建议合理设置学习速度，避免过于频繁的请求
- 妥善保管用户凭据信息

## 更新日志

- v2: 改进了学习算法和用户体验
- 支持中国干部网络学院平台
- 优化了并发处理和错误处理机制

## 作者

- **twikura** - rainbowtrash2333@gmail.com

## 许可证

本项目仅供学习交流使用，请勿用于商业目的。
