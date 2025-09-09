#!/usr/bin/env python3
import os, sys, time, csv, argparse, pathlib
from openai import OpenAI

def read_file(p):
    return pathlib.Path(p).read_text(encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--metrics", required=True)
    ap.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o"))
    ap.add_argument("--mode", choices=["streaming","nonstream"], default="streaming")
    args = ap.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        sys.exit("Falta OPENAI_API_KEY")

    prompt = read_file(args.prompt).strip()
    input_data = read_file(args.input).strip()
    payload = f"{prompt}\n\n=== INPUT ===\n{input_data}"

    client = OpenAI(api_key=api_key)

    t0 = time.perf_counter()
    if args.mode == "nonstream":
        resp = client.chat.completions.create(
            model=args.model,
            messages=[{"role":"system","content":"Auditor de seguridad."},
                      {"role":"user","content":payload}],
        )
        t1 = time.perf_counter()
        text = resp.choices[0].message.content
        usage = resp.usage
        prompt_tokens = usage.prompt_tokens
        completion_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens
        ttft_ms, gen_ms = "", ""
    else:
        stream = client.chat.completions.create(
            model=args.model,
            messages=[{"role":"system","content":"Auditor de seguridad."},
                      {"role":"user","content":payload}],
            stream=True,
        )
        chunks, first, t_first = [], True, None
        for ch in stream:
            delta = ch.choices[0].delta.content or ""
            if delta and first:
                t_first = time.perf_counter()
                first = False
            chunks.append(delta)
        t1 = time.perf_counter()
        text = "".join(chunks)
        prompt_tokens = completion_tokens = total_tokens = ""
        ttft_ms = (t_first - t0)*1000 if t_first else ""
        gen_ms = (t1 - t0)*1000 - (ttft_ms if ttft_ms else 0)

    total_ms = (t1 - t0)*1000

    pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(args.out).write_text(text, encoding="utf-8")

    header = ["modelo","modo","total_ms","ttft_ms","gen_ms","prompt_tokens","completion_tokens","total_tokens"]
    row = [args.model, args.mode, f"{total_ms:.2f}", ttft_ms, gen_ms, prompt_tokens, completion_tokens, total_tokens]
    pathlib.Path(args.metrics).parent.mkdir(parents=True, exist_ok=True)
    new = not pathlib.Path(args.metrics).exists()
    with open(args.metrics,"a",newline="",encoding="utf-8") as f:
        w=csv.writer(f)
        if new: w.writerow(header)
        w.writerow(row)

if __name__=="__main__": main()
