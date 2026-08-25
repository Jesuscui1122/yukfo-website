"""Ollama 本地视觉通道：批量看图，短提示词 + 图压缩（绕 8k 上下文坑）。
用法: python -X utf8 scripts/ollama_vision.py <图片路径> [更多路径...]
"""
import sys, io, base64, json, urllib.request
from PIL import Image

MODEL = "qwen3-vl:8b"
PROMPT = "用中文简短描述这张图：主体是什么（产品/零件/场景）、画面里有无文字、背景是什么、照片质量如何。两三句话。"

def to_b64(path):
    img = Image.open(path)
    img.thumbnail((900, 900))
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def ask(path):
    body = {
        "model": MODEL, "stream": False,
        "messages": [{"role": "user", "content": PROMPT, "images": [to_b64(path)]}],
        "options": {"temperature": 0.1},
    }
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["message"]["content"].strip()

for p in sys.argv[1:]:
    try:
        print(f"=== {p.split('/')[-1]} ===")
        print(ask(p))
        print()
    except Exception as e:
        print(f"=== {p} === ERROR: {e}")
