import os
import tempfile
import subprocess
import time
from pathlib import Path
import requests

# === 配置 ===
INPUT_VIDEO = "/home/dieu/10min.mp4"
QUESTION = "视频主要描述的是什么"
API_URL = "http://172.16.20.52:8000/infer"

# 预处理参数
TARGET_WIDTH = 320
TARGET_HEIGHT = 240
TARGET_FPS = 5

# 🆕 新增开关：是否保存预处理视频到 ./output 且不清理
SAVE_OUTPUT = True  # ← 设置为 True 保存，False 则临时处理并清理

def preprocess_video(input_path: str, output_path: str, width: int, height: int, fps: int):
    """
    使用 ffmpeg 降低视频分辨率和帧率
    """
    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-vf", f"scale={width}:{height},fps={fps}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr}")
        print(f"✅ 视频已预处理并保存到: {output_path}")
    except FileNotFoundError:
        raise RuntimeError("FFmpeg 未安装，请先运行: sudo apt install ffmpeg")

def main():
    if SAVE_OUTPUT:
        # 确保 output 目录存在
        output_dir = Path("./output")
        output_dir.mkdir(exist_ok=True)
        # 生成唯一输出文件名
        input_name = Path(INPUT_VIDEO).stem
        processed_path = output_dir / f"{input_name}_proc_{TARGET_WIDTH}x{TARGET_HEIGHT}_{TARGET_FPS}fps.mp4"
        preprocess_video(INPUT_VIDEO, str(processed_path), TARGET_WIDTH, TARGET_HEIGHT, TARGET_FPS)
        cleanup = False
    else:
        # 使用临时文件
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            processed_path = Path(tmp.name)
        preprocess_video(INPUT_VIDEO, str(processed_path), TARGET_WIDTH, TARGET_HEIGHT, TARGET_FPS)
        cleanup = True

    try:
        # 上传处理后的视频
        filename = processed_path.name
        with open(processed_path, "rb") as f:
            files = {"video": (filename, f, "video/mp4")}
            data = {"question": QUESTION}
            print("📤 正在上传视频并请求推理...")
            start = time.time()
            response = requests.post(API_URL, files=files, data=data, timeout=120)
            endtime = time.time()
            print(f"总用时：{endtime - start:.2f}s")

        if response.status_code == 200:
            print("✅ 推理成功:")
            print(response.json()["answer"])
        else:
            print(f"❌ 请求失败: {response.status_code} - {response.text}")

    finally:
        # 仅在非 SAVE_OUTPUT 模式下清理
        if cleanup and processed_path.exists():
            processed_path.unlink()
            print("🧹 临时文件已清理")

if __name__ == "__main__":
    main()