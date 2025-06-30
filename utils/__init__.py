"""
培养方案智能优化平台 V2.0 - 工具包

包含文档解析、冲突检测、收敛性判断等核心工具
"""

from .document_parser import DocumentParser
from .conflict_detector import ConflictDetector
from .convergence_checker import ConvergenceChecker

__all__ = [
    "DocumentParser",
    "ConflictDetector", 
    "ConvergenceChecker"
] 