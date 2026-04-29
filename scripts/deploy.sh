#!/bin/bash
# LabMind 部署脚本
PORT=${1:-8081}

echo "🧪 LabMind — 实验室AI文档助手"
echo "============================="

# 语法检查
python3 -m py_compile src/parser.py && echo "✅ parser.py 语法正确"

# 创建必要目录
mkdir -p output data

echo ""
echo "✅ 部署完成"
echo "使用: python src/parser.py"
