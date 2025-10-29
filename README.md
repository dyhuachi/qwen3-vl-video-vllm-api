# Qwen3-VL Video Inference Service with vLLM 🚀

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![vLLM](https://img.shields.io/badge/vLLM-%E2%9C%93-brightgreen)](https://github.com/vllm-project/vllm)

**基于 vLLM 的 Qwen3-VL 视频多模态大模型推理服务**  
⚡ 高性能 | 🎥 视频理解 | 🌐 RESTful API

---

## 🌟 项目简介

本项目基于 **Qwen3-VL** 多模态大模型，利用 **vLLM** 框架提供高性能的视频理解推理服务。支持通过 RESTful API 对视频内容进行智能分析、问答和描述生成，适用于视频内容理解、智能监控、媒体分析等场景。

> **Qwen3-VL** 是通义千问系列最新一代视觉语言模型，具备强大的视频理解能力，能够处理长视频序列并进行复杂的跨模态推理。

---

## 🚀 快速开始

### 环境要求
- Python 3.9+
- CUDA 12.1+
- NVIDIA GPU (建议 24GB+ 显存)
- Docker (可选)

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/your-username/qwen3-vl-video-vllm-api.git
cd qwen3-vl-video-vllm-api
```

### 启动服务

```bash
# 方式1: 直接启动
uvicorn qwen3app:app --host 0.0.0.0 --port 8000 --workers 1

```bash
# 构建镜像
docker build -t qwen3-vl-video-api .

# 运行容器
docker run -d --gpus all -p 8000:8000 \
    -v /path/to/videos:/app/videos \
    qwen3-vl-video-api
```

---

## 📡 API 使用

### 视频理解请求

```bash
curl -X POST http://localhost:8000/infer \
     -F "video=@111.mp4" \
     -F "question=视频里的人在做什么？"
```

### 响应示例

```✅ 视频已预处理并保存到: output/10min_proc_320x240_5fps.mp4
📤 正在上传视频并请求推理...
总用时：55.11s
✅ 推理成功:
视频主要描述的是位于中国贵州的北盘江大桥，这座桥是世界最高的桥梁，其高度达到了200米，横跨在北盘江之上。视频通过多个镜头展示了大桥的壮丽景色和工程细节，包括其独特的设计、施工过程以及对当地环境和居民的影响。此外，视频还提到了大桥的建设背景，即为了连接贵州和云南，促进区域经济发展，以及其在世界桥梁史上的重要地位。视频通过航拍和实地拍摄相结合的方式，展现了大桥的雄伟和壮观，同时也突出了其在工程技术和自然环境中的和谐共存。

```

---

## 📁 项目结构

```
qwen3-vl-video-vllm-api/
├── server.py              # 主服务入口
├── requirements.txt       # 依赖包列表
├── Dockerfile            # Docker 镜像配置
├── config/               # 配置文件
├── examples/             # 使用示例
│   ├── video_qa.py       # 视频问答示例
│   └── batch_process.py  # 批量处理示例
└── README.md
```

---

## ⚙️ 配置选项

| 参数 | 默认值 | 描述 |
|------|--------|------|
| `--model-path` | `Qwen/Qwen3-VL` | 模型路径或HuggingFace ID |
| `--port` | `8000` | 服务端口 |
| `--host` | `0.0.0.0` | 服务主机 |
| `--max-model-len` | `8192` | 最大上下文长度 |
| `--dtype` | `bfloat16` | 模型数据类型 |
| `--tensor-parallel-size` | `2` | 张量并行大小 |

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/your-feature`)
3. 提交更改 (`git commit -am 'Add some feature'`)
4. 推送到分支 (`git push origin feature/your-feature`)
5. 创建 Pull Request

---

## 📜 许可证

本项目基于 [Apache License 2.0](LICENSE) 开源。

---

## 🙏 求 Star！

如果你觉得这个项目对你有帮助，请给个 ⭐ **Star**！  
你的支持是我持续维护和改进项目的最大动力！

[![GitHub stars](https://img.shields.io/github/stars/your-username/qwen3-vl-video-vllm-api?style=social)](https://github.com/your-username/qwen3-vl-video-vllm-api/stargazers)

---

## 📧 联系方式

- Issues: [GitHub Issues](https://github.com/dyhuachi/qwen3-vl-video-vllm-api/issues)
- Email: 515648571@qq.com

---

**Made with ❤️ | Power by Qwen & vLLM**
