#!/usr/bin/env python3
import argparse, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT/"prompts"; RESP = ROOT/"responses"; EVAL = ROOT/"eval"
SCRIPTS = ROOT/"scripts"

def find_inputs(prompt):
    base = prompt.stem.replace("_prompt","")
    files = list(PROMPTS.glob(f"{base}_input.*"))
    return files

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--models",default="gpt4,mistral")
    ap.add_argument("--pattern",default="*_prompt.txt")
    args=ap.parse_args()

    RESP.mkdir(exist_ok=True); (RESP/"gpt4").mkdir(exist_ok=True); (RESP/"mistral").mkdir(exist_ok=True)
    EVAL.mkdir(exist_ok=True)

    prompts=sorted(PROMPTS.glob(args.pattern))
    for p in prompts:
        base=p.stem.replace("_prompt","")
        inputs=find_inputs(p)
        if not inputs: 
            print("No inputs para",p); continue
        inp=inputs[0]

        if "gpt4" in args.models:
            out=RESP/"gpt4"/f"{base}_out.txt"
            met=EVAL/f"{base}_gpt4.csv"
            cmd=[sys.executable,str(SCRIPTS/"gpt4_run_and_metrics.py"),
                 "--prompt",str(p),"--input",str(inp),
                 "--out",str(out),"--metrics",str(met)]
            subprocess.run(cmd,check=True)

        if "mistral" in args.models:
            out=RESP/"mistral"/f"{base}_out.txt"
            met=EVAL/f"{base}_mistral.csv"
            cmd=[str(SCRIPTS/"ollama_run_and_metrics.sh"),"mistral",str(p),str(inp),str(out),str(met)]
            subprocess.run(cmd,check=True)

if __name__=="__main__": main()
