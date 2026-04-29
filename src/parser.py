"""
LabMind — 实验室AI文档解析引擎

用户视角：上传实验记录PDF/Word → 自动提取关键信息 → 结构化存储
"""

import re
import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ExtractedInfo:
    """提取的结构化信息"""
    doc_type: str            # protocol/report/sop/notebook
    title: str
    date: str
    authors: List[str]
    materials: List[str]
    methods: List[str]
    results: List[Dict]
    conclusions: List[str]
    keywords: List[str]
    confidence: float


class DocumentParser:
    """实验室文档解析引擎"""
    
    # 实验文档常见模式
    PATTERNS = {
        "reagent": r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\s*[\(（]?\s*(\d+\.?\d*)\s*(mL|mg|μL|g|M|mM|μM)",
        "temp": r"(\d+)\s*[°℃]?\s*[Cc]",
        "time": r"(\d+)\s*(hours?|hrs?|minutes?|mins?|seconds?|sec|天|小时|分钟)",
        "concentration": r"(\d+\.?\d*)\s*(μg/mL|mg/mL|ng/mL|mM|μM|M)",
        "protocol_id": r"(?:Protocol|SOP|方案)\s*[#:：]\s*([A-Z0-9\-]+)",
    }
    
    def parse_text(self, text: str) -> ExtractedInfo:
        """从文本提取结构化信息"""
        # 检测文档类型
        doc_type = self._detect_doc_type(text)
        
        # 提取各类信息
        materials = self._extract_pattern(text, "reagent")
        methods = self._extract_methods(text)
        keywords = self._extract_keywords(text)
        
        return ExtractedInfo(
            doc_type=doc_type,
            title=self._extract_title(text),
            date=self._extract_date(text),
            authors=self._extract_authors(text),
            materials=materials,
            methods=methods,
            results=[],
            conclusions=[],
            keywords=keywords,
            confidence=0.75
        )
    
    def _detect_doc_type(self, text: str) -> str:
        """检测文档类型"""
        text_lower = text.lower()
        if any(w in text_lower for w in ["protocol", "sop", "标准操作"]):
            return "sop"
        elif any(w in text_lower for w in ["result", "结果", "findings"]):
            return "report"
        elif any(w in text_lower for w in ["notebook", "lab note", "实验记录"]):
            return "notebook"
        return "general"
    
    def _extract_title(self, text: str) -> str:
        """提取标题"""
        lines = text.strip().split("\n")
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 5 and len(line) < 200:
                return line
        return "未命名文档"
    
    def _extract_date(self, text: str) -> str:
        """提取日期"""
        patterns = [
            r"(\d{4}[-/]\d{1,2}[-/]\d{1,2})",
            r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})",
        ]
        for p in patterns:
            match = re.search(p, text)
            if match:
                return match.group(1)
        return ""
    
    def _extract_authors(self, text: str) -> List[str]:
        """提取作者"""
        match = re.search(r"(?:Author|作者|编制)[：:]\s*(.+)", text)
        if match:
            return [a.strip() for a in match.group(1).split(",")]
        return []
    
    def _extract_pattern(self, text: str, pattern_name: str) -> List[str]:
        """提取特定模式"""
        pattern = self.PATTERNS.get(pattern_name, "")
        if not pattern:
            return []
        matches = re.findall(pattern, text)
        return [f"{m[0]} {m[1]}{m[2]}" for m in matches] if matches else []
    
    def _extract_methods(self, text: str) -> List[str]:
        """提取方法步骤"""
        steps = re.findall(r"(?:\d+[\.\)、]|Step\s*\d+)\s*(.+?)(?:\n|$)", text)
        return steps[:10]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        match = re.search(r"(?:Keywords|关键词)[：:]\s*(.+)", text)
        if match:
            return [k.strip() for k in match.group(1).split(",")]
        return []
    
    def to_json(self, info: ExtractedInfo) -> str:
        """转为JSON"""
        return json.dumps(asdict(info), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    parser = DocumentParser()
    sample = """
    Protocol ID: LAB-2026-001
    作者: 张三, 李四
    日期: 2026-04-22
    
    1. 将 NaCl (5.0 g) 溶于100 mL 水中
    2. 加热至 37℃ 保持 30 minutes
    3. 冷却后检测
    
    Keywords: 盐溶液, 温度控制, 实验方案
    """
    result = parser.parse_text(sample)
    print(parser.to_json(result))
