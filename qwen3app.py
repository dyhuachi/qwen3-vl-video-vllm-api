# -*- coding: utf-8 -*-
import os
import tempfile
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from qwen_vl_utils import process_vision_info
from transformers import AutoProcessor
from vllm import LLM, SamplingParams

# 设置多进程启动方式（必须）
os.environ['VLLM_WORKER_MULTIPROC_METHOD'] = 'spawn'

# 模型路径
CHECKPOINT_PATH = "/home/dieu/Qwen3-VL-4B-Instruct"

# 全局变量（通过 lifespan 管理）
processor = None
llm = None
sampling_params = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global processor, llm, sampling_params
    print("Loading Qwen3-VL model and processor...")
    processor = AutoProcessor.from_pretrained(CHECKPOINT_PATH)
    llm = LLM(
        model=CHECKPOINT_PATH,
        tensor_parallel_size=2,
        gpu_memory_utilization=0.95,
        max_num_batched_tokens=4000,
        max_model_len=32000,
    )
    sampling_params = SamplingParams(
        temperature=0,
        max_tokens=1024,
        top_k=-1,
        top_p=0.9
    )
    print("Model loaded successfully.")
    
    # 这里 yield 之前是 startup，之后是 shutdown
    yield
    
    # Shutdown 阶段：清理资源（vLLM 通常不需要显式清理，但可留作扩展）
    print("Shutting down... Cleaning up resources.")
    # 注意：vLLM 的 LLM 实例在进程退出时自动释放，一般无需手动清理

# 创建 FastAPI 应用，传入 lifespan
app = FastAPI(title="Qwen3-VL Video Understanding API", lifespan=lifespan)

def prepare_inputs_for_vllm(messages, processor):
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs, video_kwargs = process_vision_info(
        messages,
        image_patch_size=processor.image_processor.patch_size,
        return_video_kwargs=True,
        return_video_metadata=True
    )

    mm_data = {}
    if image_inputs is not None:
        mm_data['image'] = image_inputs
    if video_inputs is not None:
        mm_data['video'] = video_inputs

    return {
        'prompt': text,
        'multi_modal_data': mm_data,
        'mm_processor_kwargs': video_kwargs
    }

@app.post("/infer")
async def infer(
    video: UploadFile = File(...),
    question: str = Form(...)
):
    if not video.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a video.")

    temp_dir = tempfile.mkdtemp()
    temp_video_path = os.path.join(temp_dir, f"{uuid.uuid4().hex}_{video.filename}")

    try:
        with open(temp_video_path, "wb") as f:
            content = await video.read()
            f.write(content)

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "video", "video": temp_video_path},
                    {"type": "text", "text": question},
                ],
            }
        ]

        inputs = [prepare_inputs_for_vllm(messages, processor)]
        outputs = llm.generate(inputs, sampling_params=sampling_params)
        generated_text = outputs[0].outputs[0].text.strip()

        return {"answer": generated_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

    finally:
        # 清理临时文件
        try:
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
            os.rmdir(temp_dir)
        except Exception as cleanup_error:
            print(f"Warning: Failed to clean up temp files: {cleanup_error}")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
