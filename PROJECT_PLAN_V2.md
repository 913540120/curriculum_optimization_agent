# 培养方案智能优化平台 V2.0 - 项目技术方案

## 🎯 核心愿景

构建一个基于多利益相关者智能体系统（MAS）的**专业培养方案智能优化平台**。通过模拟高校教务、企业HR、行业专家、学生代表、教师代表等多方角色的虚拟圆桌会议，对输入的专业培养方案进行多轮迭代优化，最终输出符合目标岗位群需求且平衡各方利益的优化培养方案。

## 🏗️ 系统架构设计

### 核心数据流
```
培养方案文档 + 目标岗位群 
    ↓
培养方案解析与建模
    ↓
多轮优化循环 {
    多利益相关者并行批判
    ↓
    冲突检测与调解
    ↓
    培养方案优化执行
    ↓
    收敛性判断
}
    ↓
优化报告与实施指南生成
```

### 技术栈选型
- **前端框架**: Streamlit (实时优化展示)
- **AI模型**: DeepSeek-R1 (通过SiliconFlow)
- **搜索引擎**: Tavily API (行业趋势搜索)
- **文档解析**: PyPDF2, python-docx, pandas
- **状态管理**: TypedDict + Streamlit Session State
- **并发处理**: asyncio (多Agent并行执行)

## 🤖 智能体团队架构

### 1. 项目协调官 (ProjectCoordinator)
**职责**: 优化流程总指挥
- 管理优化状态和轮次控制
- 协调各利益相关者的发言顺序  
- 判断收敛条件和终止时机
- 生成最终优化报告

### 2. 培养方案分析师 (CurriculumAnalyst)
**职责**: 培养方案解析专家
- 解析多格式培养方案文档(PDF/Word/Excel)
- 建立结构化的课程数据模型
- 提取课程体系、学分分配、技能映射
- 为优化提供基础数据支撑

### 3. 多利益相关者批判团队

#### 高校教务处代表 (AcademicAffairsAgent)
**立场**: 教学管理和资源约束
**关注点**: 
- 课程安排可行性 (师资、教室、设备)
- 学分结构合理性 (总学分、各类别学分比例)
- 实施成本和复杂度 (新增课程的师资需求)
- 政策法规符合性 (教育部要求、专业认证标准)

#### 企业HR代表 (HRRecruiterAgent) 
**立场**: 人才需求和招聘标准
**关注点**:
- 毕业生技能与目标岗位匹配度
- 实习和项目经验安排
- 行业热门技术趋势跟进
- 软技能培养 (沟通、团队协作、解决问题)
- 就业竞争力和薪资前景

#### 行业技术专家 (IndustryExpertAgent)
**立场**: 技术发展和行业标准  
**关注点**:
- 前沿技术和工具的应用
- 行业认证和标准培训
- 实际工作场景需求
- 技术栈深度和广度要求
- 创新能力和技术敏感度培养

#### 学生代表 (StudentRepresentativeAgent)
**立场**: 学习体验和个人发展
**关注点**:
- 课程难度梯度和学习负担
- 兴趣培养和专业选择空间
- 就业前景和职业发展机会
- 实践机会充分性 (实验、实习、项目)
- 国际化视野和竞争力

#### 教师代表 (FacultyRepresentativeAgent)
**立场**: 教学质量和学术水平
**关注点**:
- 知识体系完整性和科学性
- 理论基础扎实性
- 教学方法和手段创新
- 学术研究能力培养
- 课程间逻辑关系和递进性

### 4. 冲突调解员 (ConflictMediatorAgent)
**职责**: 利益冲突协调专家
- 识别各方建议中的冲突点
- 评估冲突严重程度和影响范围
- 提出平衡性解决方案
- 寻找多方共识和妥协点
- 设定优先级权重和取舍策略

### 5. 培养方案优化师 (CurriculumOptimizerAgent)
**职责**: 方案执行和优化专家
- 根据调解结果实际修改培养方案
- 保证方案内在逻辑性和完整性
- 进行优化可行性验证
- 量化改进效果和满意度
- 生成详细变更说明和实施指导

## 📊 核心数据模型

### 培养方案优化状态
```python
class CurriculumOptimizationState(TypedDict):
    # 基础信息
    major_name: str                          # 专业名称
    target_positions: List[str]              # 目标岗位群
    optimization_round: int                  # 当前优化轮次
    max_rounds: int                          # 最大优化轮次
    
    # 培养方案演进
    original_curriculum: Dict[str, Any]      # 原始培养方案
    current_curriculum: Dict[str, Any]       # 当前培养方案
    curriculum_versions: List[Dict]          # 历史版本记录
    optimization_history: List[Dict]         # 优化历史轨迹
    
    # 利益相关者反馈
    stakeholder_feedback: Dict[str, List]    # 各方改进建议
    conflict_analysis: Dict[str, Any]        # 冲突分析结果
    mediated_solutions: List[Dict]           # 调解方案集
    consensus_points: List[str]              # 共识要点
    
    # 优化指标
    optimization_log: List[Dict]             # 详细优化记录
    convergence_metrics: Dict[str, float]    # 收敛性指标
    stakeholder_satisfaction: Dict[str, float] # 各方满意度
    is_consensus_reached: bool               # 是否达成共识
```

### 培养方案结构模型
```python
class CurriculumStructure(TypedDict):
    # 基本信息
    basic_info: Dict[str, str]               # 专业名称、学制、学位等
    
    # 课程体系
    course_categories: Dict[str, List]       # 课程分类 (通识、专业基础、专业核心等)
    course_details: List[Dict]               # 课程详细信息
    credit_distribution: Dict[str, int]      # 学分分配
    prerequisite_relations: Dict[str, List]  # 先修课程关系
    
    # 能力培养
    skill_mapping: Dict[str, List]           # 课程与技能映射
    learning_outcomes: List[str]             # 学习成果
    competency_framework: Dict[str, Any]     # 能力框架
    
    # 实践环节
    practical_training: List[Dict]           # 实习、实训、项目等
    lab_experiments: List[Dict]              # 实验课程
    graduation_project: Dict[str, Any]       # 毕业设计/论文
    
    # 质量保障
    assessment_methods: Dict[str, str]       # 考核方式
    graduation_requirements: Dict[str, Any]  # 毕业要求
    quality_standards: List[str]             # 质量标准
```

### 改进建议模型
```python
class ImprovementSuggestion(TypedDict):
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
```

## 🔄 优化流程设计

### Phase 1: 初始化阶段
1. **文档解析**: 培养方案分析师解析上传的培养方案文档
2. **结构建模**: 建立结构化的培养方案数据模型
3. **目标设定**: 明确目标岗位群和优化目标
4. **基线评估**: 对原始方案进行基础分析

### Phase 2: 多轮优化循环
```
FOR round = 1 to max_rounds:
    # 并行批判阶段
    PARALLEL {
        academic_affairs.analyze(current_curriculum)
        hr_recruiter.analyze(current_curriculum, target_positions)  
        industry_expert.analyze(current_curriculum, target_positions)
        student_rep.analyze(current_curriculum)
        faculty_rep.analyze(current_curriculum)
    }
    
    # 冲突检测与调解
    conflicts = conflict_detector.detect(all_suggestions)
    mediated_solutions = mediator.resolve(conflicts)
    
    # 方案优化执行
    optimized_curriculum = optimizer.apply(mediated_solutions)
    
    # 收敛性判断
    IF convergence_checker.is_converged(optimization_metrics):
        BREAK
    
    current_curriculum = optimized_curriculum
END FOR
```

### Phase 3: 报告生成阶段
1. **效果量化**: 计算优化前后的各项指标对比
2. **满意度评估**: 评估各利益相关者的满意度
3. **实施指导**: 生成详细的实施计划和风险评估
4. **持续改进**: 提供后续优化建议

## 🎨 用户界面设计

### 主界面布局
```
标题: 🎓 培养方案智能优化平台 V2.0

侧边栏:
├── 📄 培养方案上传
├── 🎯 目标岗位群设置  
├── ⚙️ 优化参数配置
├── 👥 利益相关者权重
└── 📊 优化进度监控

主界面:
├── 📋 原始方案展示
├── 🔄 实时优化过程
├── 📈 收敛性分析
└── 📑 优化结果对比
```

### 实时优化展示
- **轮次进度条**: 当前轮次/总轮次，预计剩余时间
- **利益相关者面板**: 各Agent的实时建议和观点
- **冲突热力图**: 可视化冲突点分布和严重程度  
- **方案演进图**: 显示培养方案的迭代变化轨迹
- **满意度雷达图**: 各方满意度的实时变化

## 🔧 实现优先级

### 第一期 (核心MVP, 预计5-7天)
- [x] 项目框架搭建
- [ ] 基础智能体框架
- [ ] 简单文档解析 (仅支持文本格式)
- [ ] 基础优化循环
- [ ] 简单UI展示

### 第二期 (完整功能, 预计7-10天)  
- [ ] 完整文档解析引擎 (PDF/Word/Excel)
- [ ] 五个利益相关者Agent
- [ ] 冲突检测与调解机制
- [ ] 收敛性判断算法
- [ ] 高级UI功能

### 第三期 (优化增强, 预计3-5天)
- [ ] 性能优化和错误处理
- [ ] 高级可视化功能
- [ ] 批量处理和模板管理
- [ ] 导出和分享功能

## 🚀 技术创新点

1. **多利益相关者模拟**: 首创性地引入真实教育生态中的各方角色
2. **智能冲突调解**: 自动识别和调解利益冲突的AI机制
3. **渐进式收敛优化**: 基于多维度指标的智能收敛判断
4. **实时协作可视化**: 直观展示多Agent协作过程
5. **可解释的优化路径**: 完整记录和展示每个优化决策的依据

这个技术方案为培养方案优化提供了一个全新的AI驱动解决方案，具有很强的实用价值和创新意义。 