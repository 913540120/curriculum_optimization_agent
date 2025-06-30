"""
培养方案智能优化平台 V2.0 - 核心数据模型

定义系统中所有关键数据结构，包括培养方案、优化状态、改进建议等
"""

from typing import TypedDict, List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# ==================== 枚举类型定义 ====================

class CourseCategory(Enum):
    """课程类别枚举"""
    GENERAL = "通识教育"
    BASIC = "专业基础"
    CORE = "专业核心"
    ELECTIVE = "专业选修"
    PRACTICAL = "实践教学"
    GRADUATION = "毕业环节"

class SuggestionType(Enum):
    """建议类型枚举"""
    ADD = "add"           # 新增
    MODIFY = "modify"     # 修改
    REMOVE = "remove"     # 删除
    MERGE = "merge"       # 合并

class AgentType(Enum):
    """智能体类型枚举"""
    ACADEMIC_AFFAIRS = "academic_affairs"
    HR_RECRUITER = "hr_recruiter"
    INDUSTRY_EXPERT = "industry_expert"
    STUDENT_REP = "student_representative"
    FACULTY_REP = "faculty_representative"

class ConflictType(Enum):
    """冲突类型枚举"""
    RESOURCE = "resource_conflict"     # 资源冲突
    CONTENT = "content_conflict"       # 内容冲突
    PRIORITY = "priority_conflict"     # 优先级冲突
    TIMELINE = "timeline_conflict"     # 时间冲突

class OptimizationStatus(Enum):
    """优化状态枚举"""
    IDLE = "idle"
    PARSING = "parsing"
    OPTIMIZING = "optimizing"
    CONVERGED = "converged"
    ERROR = "error"

# ==================== 基础数据结构 ====================

@dataclass
class Course:
    """课程信息"""
    code: str                    # 课程代码
    name: str                    # 课程名称
    credits: float               # 学分
    hours: int                   # 学时
    category: CourseCategory     # 课程类别
    semester: int                # 开设学期
    prerequisites: List[str]     # 先修课程
    description: str = ""        # 课程描述
    skills: List[str] = None     # 培养技能

    def __post_init__(self):
        if self.skills is None:
            self.skills = []

@dataclass
class PracticalTraining:
    """实践教学环节"""
    name: str                    # 实践名称
    type: str                    # 实践类型 (实习/实训/项目等)
    duration: int                # 持续时间(周)
    credits: float               # 学分
    semester: int                # 开设学期
    description: str = ""        # 描述
    objectives: List[str] = None # 实践目标

    def __post_init__(self):
        if self.objectives is None:
            self.objectives = []

# ==================== 培养方案结构 ====================

class CurriculumStructure(TypedDict):
    """培养方案结构模型"""
    
    # 基本信息
    basic_info: Dict[str, str]               # 专业名称、学制、学位等
    
    # 课程体系
    courses: List[Dict[str, Any]]            # 课程列表 (Course对象序列化)
    course_categories: Dict[str, List[str]]  # 课程分类映射
    credit_distribution: Dict[str, float]    # 学分分配
    prerequisite_relations: Dict[str, List[str]]  # 先修关系
    
    # 能力培养
    skill_mapping: Dict[str, List[str]]      # 课程-技能映射
    learning_outcomes: List[str]             # 学习成果
    competency_framework: Dict[str, Any]     # 能力框架
    
    # 实践环节
    practical_training: List[Dict[str, Any]] # 实践教学环节
    lab_experiments: List[Dict[str, Any]]    # 实验课程
    graduation_project: Dict[str, Any]       # 毕业设计/论文
    
    # 质量保障
    assessment_methods: Dict[str, str]       # 考核方式
    graduation_requirements: Dict[str, Any]  # 毕业要求
    quality_standards: List[str]             # 质量标准

class ImprovementSuggestion(TypedDict):
    """改进建议模型"""
    suggestion_id: str                       # 建议ID
    agent_type: str                          # 建议者类型
    agent_name: str                          # 建议者名称
    suggestion_type: str                     # 建议类型 (add/modify/remove)
    target_component: str                    # 目标组件 (course/credit/skill等)
    detailed_suggestion: str                 # 详细建议内容
    justification: str                       # 建议理由
    priority: int                            # 优先级 (1-5)
    feasibility: float                       # 可行性评分 (0-1)
    expected_benefit: str                    # 预期收益
    potential_risks: List[str]               # 潜在风险
    timestamp: str                           # 建议时间

class ConflictAnalysis(TypedDict):
    """冲突分析结果"""
    conflict_id: str                         # 冲突ID
    conflict_type: str                       # 冲突类型
    involved_suggestions: List[str]          # 涉及的建议ID
    conflict_description: str                # 冲突描述
    severity_score: float                    # 严重程度 (0-1)
    affected_components: List[str]           # 受影响的组件
    resolution_strategies: List[str]         # 解决策略选项

class MediatedSolution(TypedDict):
    """调解方案"""
    solution_id: str                         # 方案ID
    resolved_conflicts: List[str]            # 解决的冲突ID
    compromise_suggestions: List[str]        # 妥协建议
    implementation_plan: str                 # 实施计划
    stakeholder_acceptance: Dict[str, float] # 各方接受度
    final_decision: str                      # 最终决策

# ==================== 优化状态管理 ====================

class CurriculumOptimizationState(TypedDict):
    """培养方案优化状态管理"""
    
    # 基础信息
    session_id: str                          # 会话ID
    major_name: str                          # 专业名称
    target_positions: List[str]              # 目标岗位群
    optimization_round: int                  # 当前优化轮次
    max_rounds: int                          # 最大优化轮次
    status: str                              # 当前状态
    
    # 培养方案演进
    original_curriculum: CurriculumStructure # 原始培养方案
    current_curriculum: CurriculumStructure  # 当前培养方案
    curriculum_versions: List[Dict[str, Any]]# 历史版本记录
    optimization_history: List[Dict[str, Any]] # 优化历史轨迹
    
    # 利益相关者反馈
    stakeholder_feedback: Dict[str, List[ImprovementSuggestion]] # 各方建议
    conflict_analysis: List[ConflictAnalysis] # 冲突分析结果
    mediated_solutions: List[MediatedSolution] # 调解方案集
    consensus_points: List[str]              # 共识要点
    
    # 优化指标
    optimization_log: List[Dict[str, Any]]   # 详细优化记录
    convergence_metrics: Dict[str, float]    # 收敛性指标
    stakeholder_satisfaction: Dict[str, float] # 各方满意度
    is_consensus_reached: bool               # 是否达成共识
    
    # 元数据
    created_at: str                          # 创建时间
    updated_at: str                          # 更新时间
    optimization_duration: float             # 优化总耗时(秒)

# ==================== 结果数据结构 ====================

class OptimizationResult(TypedDict):
    """优化结果"""
    optimization_summary: str               # 优化总结
    improvement_metrics: Dict[str, float]   # 改进指标
    before_after_comparison: Dict[str, Any] # 前后对比
    implementation_guide: str               # 实施指导
    risk_assessment: List[str]              # 风险评估
    stakeholder_feedback_summary: Dict[str, str] # 各方反馈总结

class ConvergenceMetrics(TypedDict):
    """收敛性指标"""
    suggestion_reduction_rate: float        # 建议减少率
    conflict_severity_score: float          # 冲突严重度评分
    stakeholder_satisfaction_avg: float     # 平均满意度
    curriculum_stability_score: float       # 方案稳定性评分
    consensus_degree: float                 # 共识程度

# ==================== 配置参数 ====================

class OptimizationConfig(TypedDict):
    """优化配置参数"""
    max_rounds: int                          # 最大优化轮次
    convergence_threshold: float             # 收敛阈值
    stakeholder_weights: Dict[str, float]    # 利益相关者权重
    conflict_tolerance: float                # 冲突容忍度
    optimization_timeout: int                # 优化超时时间(秒)
    enable_parallel_processing: bool         # 启用并行处理
    document_parsing_mode: str               # 文档解析模式

# ==================== 工具函数 ====================

def create_optimization_state(
    major_name: str,
    target_positions: List[str],
    original_curriculum: CurriculumStructure,
    config: OptimizationConfig
) -> CurriculumOptimizationState:
    """创建初始优化状态"""
    now = datetime.now().isoformat()
    session_id = f"opt_{now.replace(':', '').replace('-', '').replace('.', '')}"
    
    return CurriculumOptimizationState(
        session_id=session_id,
        major_name=major_name,
        target_positions=target_positions,
        optimization_round=0,
        max_rounds=config["max_rounds"],
        status=OptimizationStatus.IDLE.value,
        
        original_curriculum=original_curriculum,
        current_curriculum=original_curriculum.copy(),
        curriculum_versions=[],
        optimization_history=[],
        
        stakeholder_feedback={},
        conflict_analysis=[],
        mediated_solutions=[],
        consensus_points=[],
        
        optimization_log=[],
        convergence_metrics={},
        stakeholder_satisfaction={},
        is_consensus_reached=False,
        
        created_at=now,
        updated_at=now,
        optimization_duration=0.0
    )

def create_improvement_suggestion(
    agent_type: AgentType,
    suggestion_type: SuggestionType,
    target_component: str,
    detailed_suggestion: str,
    justification: str,
    priority: int = 3,
    feasibility: float = 0.8
) -> ImprovementSuggestion:
    """创建改进建议"""
    now = datetime.now().isoformat()
    suggestion_id = f"sug_{agent_type.value}_{now.replace(':', '').replace('-', '').replace('.', '')}"
    
    return ImprovementSuggestion(
        suggestion_id=suggestion_id,
        agent_type=agent_type.value,
        agent_name=agent_type.value.replace('_', ' ').title(),
        suggestion_type=suggestion_type.value,
        target_component=target_component,
        detailed_suggestion=detailed_suggestion,
        justification=justification,
        priority=priority,
        feasibility=feasibility,
        expected_benefit="",
        potential_risks=[],
        timestamp=now
    )

# ==================== 默认配置 ====================

DEFAULT_OPTIMIZATION_CONFIG: OptimizationConfig = {
    "max_rounds": 5,
    "convergence_threshold": 0.85,
    "stakeholder_weights": {
        "academic_affairs": 0.25,
        "hr_recruiter": 0.25,
        "industry_expert": 0.20,
        "student_representative": 0.15,
        "faculty_representative": 0.15
    },
    "conflict_tolerance": 0.3,
    "optimization_timeout": 300,  # 5分钟
    "enable_parallel_processing": True,
    "document_parsing_mode": "intelligent"
} 