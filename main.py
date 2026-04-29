"""
LabMind — 实验室文档解析入口
Usage: python main.py --input doc.txt
"""

import argparse
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from parser import DocumentParser


def main():
    ap = argparse.ArgumentParser(description="LabMind文档解析")
    ap.add_argument("--input", required=True, help="输入文档路径")
    ap.add_argument("--output", default="output", help="输出目录")
    args = ap.parse_args()

    parser = DocumentParser()

    with open(args.input, 'r', encoding='utf-8') as f:
        text = f.read()

    result = parser.parse_text(text)
    json_output = parser.to_json(result)

    os.makedirs(args.output, exist_ok=True)
    out_path = os.path.join(args.output, "parsed.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(json_output)

    print(f"✅ 解析完成: {out_path}")
    print(f"  类型: {result.doc_type}")
    print(f"  标题: {result.title}")
    print(f"  材料: {len(result.materials)} 项")
    print(f"  步骤: {len(result.methods)} 步")


if __name__ == "__main__":
    main()
