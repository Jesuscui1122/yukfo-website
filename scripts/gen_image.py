"""DashScope 万相文生图脚本（可复用，异步任务）
用法: python scripts/gen_image.py "<prompt>" <output_path> [--size 1024*1024] [--model wanx2.1-t2i-turbo]
依赖: DASHSCOPE_API_KEY 环境变量
"""
import json, os, sys, time, urllib.request

BASE = "https://dashscope.aliyuncs.com/api/v1"

def post(url, payload, key):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "X-DashScope-Async": "enable"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def get(url, key):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def main():
    if len(sys.argv) < 3:
        print("usage: gen_image.py <prompt> <output> [--size W*H] [--model M]")
        sys.exit(1)
    prompt, out = sys.argv[1], sys.argv[2]
    size = "1024*1024"
    model = "wanx2.1-t2i-turbo"
    if "--size" in sys.argv:
        size = sys.argv[sys.argv.index("--size") + 1]
    if "--model" in sys.argv:
        model = sys.argv[sys.argv.index("--model") + 1]
    key = os.environ.get("DASHSCOPE_API_KEY")
    if not key:
        print("DASHSCOPE_API_KEY missing"); sys.exit(1)

    try:
        resp = post(f"{BASE}/services/aigc/text2image/image-synthesis",
            {"model": model, "input": {"prompt": prompt}, "parameters": {"size": size, "n": 1}}, key)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:500]
        print(f"ERROR: submit HTTP {e.code}: {detail}", file=sys.stderr); sys.exit(1)
    task_id = resp["output"]["task_id"]
    print(f"task: {task_id}")

    for i in range(60):
        time.sleep(5)
        st = get(f"{BASE}/tasks/{task_id}", key)["output"]
        if st["task_status"] == "SUCCEEDED":
            url = st["results"][0]["url"]
            urllib.request.urlretrieve(url, out)
            print(f"OK -> {out} ({os.path.getsize(out)//1024}KB)")
            return
        if st["task_status"] == "FAILED":
            print("FAILED:", st.get("message", "")); sys.exit(1)
        print(f"  ...{st['task_status']}")
    print("timeout"); sys.exit(1)

if __name__ == "__main__":
    main()
