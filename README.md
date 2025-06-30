# 培养方案优化智能体系统 (Curriculum Optimization Agent System)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 项目简介

培养方案优化智能体系统是一个基于多智能体系统(MAS)的创新教育工具，旨在通过模拟多方利益相关者的视角，对高校专业培养方案进行智能化优化。

### 核心特性

- 🤖 **多智能体协作**: 五大利益相关者智能体协同工作
- 🔄 **迭代式优化**: 多轮优化循环直至收敛
- 🤝 **冲突调解**: 智能处理不同立场间的需求冲突
- 📊 **可视化分析**: 实时展示优化过程和结果
- 📑 **多格式支持**: 支持PDF、Word、Excel等文档解析

## 🏗️ 系统架构

```
培养方案优化系统
├── 项目协调官 (Project Coordinator)
│   ├── 优化流程管理
│   ├── 冲突调解
│   └── 方案集成
├── 利益相关者智能体
│   ├── 🏫 高校教务处代表
│   ├── 💼 企业HR代表  
│   ├── 🔬 行业技术专家
│   ├── 🎓 学生代表
│   └── 👨‍🏫 教师代表
└── 核心工具包
    ├── 📄 文档解析器
    ├── ⚡ 冲突检测器
    └── 📈 收敛性检查器
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 稳定的网络连接（用于AI模型调用）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 环境配置

创建 `.env` 文件并配置必要的API密钥：

```env
# AI模型配置
SILICONFLOW_API_KEY=your_siliconflow_api_key

# 搜索引擎配置
TAVILY_API_KEY=your_tavily_api_key
```

### 运行示例

```python
from agents.project_coordinator import ProjectCoordinator
from models import OptimizationConfig

# 初始化项目协调官
coordinator = ProjectCoordinator()

# 设置优化配置
config = OptimizationConfig(
    max_rounds=5,
    target_positions=["软件工程师", "数据分析师"],
    stakeholder_weights={
        "academic_admin": 0.2,
        "enterprise_hr": 0.25,
        "industry_expert": 0.2,
        "student": 0.2,
        "teacher": 0.15
    }
)

# 开始优化
result = coordinator.optimize_curriculum(
    curriculum_document="path/to/curriculum.pdf",
    config=config
)

print(f"优化完成！最终得分: {result.final_score}")
```

## 📁 项目结构

```
curriculum_optimization_agent/
├── models.py                 # 数据模型定义
├── requirements.txt          # 依赖包列表
├── PROJECT_PLAN_V2.md       # 详细项目计划
├── agents/                   # 智能体模块
│   ├── __init__.py
│   ├── base_agent.py        # 基础智能体类
│   └── project_coordinator.py # 项目协调官
├── utils/                    # 工具包
│   ├── __init__.py
│   ├── document_parser.py   # 文档解析器
│   ├── conflict_detector.py # 冲突检测器
│   └── convergence_checker.py # 收敛性检查器
└── README.md                 # 项目文档
```

## 🎭 智能体角色

### 高校教务处代表 🏫
- **关注重点**: 教学资源、政策符合性、实施可行性
- **评估维度**: 师资配置、设备需求、成本控制

### 企业HR代表 💼  
- **关注重点**: 就业匹配度、市场需求、技能实用性
- **评估维度**: 岗位适配、技能覆盖、就业前景

### 行业技术专家 🔬
- **关注重点**: 技术前沿性、行业标准、实际应用
- **评估维度**: 技术深度、标准符合、创新能力

### 学生代表 🎓
- **关注重点**: 学习体验、课业负担、个人发展
- **评估维度**: 难度平衡、兴趣匹配、能力提升

### 教师代表 👨‍🏫
- **关注重点**: 学术质量、知识体系、教学效果
- **评估维度**: 课程连贯、知识深度、教学负担

## 🔧 技术栈

- **AI模型**: DeepSeek-R1 (通过SiliconFlow调用)
- **搜索引擎**: Tavily API
- **文档处理**: PyPDF2, python-docx, pandas
- **并发处理**: asyncio
- **前端界面**: Streamlit (规划中)

## 📊 优化流程

1. **初始化阶段**
   - 培养方案文档解析
   - 目标岗位需求分析
   - 基线评估建立

2. **多轮优化循环**
   - 各智能体并行分析
   - 改进建议生成
   - 冲突检测与调解
   - 方案迭代优化
   - 收敛性判断

3. **结果生成**
   - 优化效果量化
   - 实施指导生成
   - 可视化报告输出

## 🚧 开发计划

### 第一期 (5-7天) ✅
- [x] 基础框架搭建
- [x] 核心数据模型
- [x] 基础智能体实现
- [x] 简单文档解析

### 第二期 (7-10天) 🚧
- [ ] 五个利益相关者智能体
- [ ] 完整冲突调解机制
- [ ] 高级文档解析
- [ ] Streamlit用户界面

### 第三期 (3-5天) 📋
- [ ] 性能优化
- [ ] 高级可视化
- [ ] 批量处理功能
- [ ] 部署配置

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📧 联系方式

如有问题或建议，请通过以下方式联系：

- 创建 [Issue](https://github.com/your-username/curriculum-optimization-agent/issues)
- 发送邮件至: your-email@example.com

---

⭐ 如果这个项目对您有帮助，请给我们一个Star！ 