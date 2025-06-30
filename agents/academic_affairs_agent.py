"""高校教务处代表智能体"""

from typing import Dict, List, Any
from .base_agent import BaseAgent
from ..models import ImprovementSuggestion

class AcademicAffairsAgent(BaseAgent):
    """高校教务处代表 - 关注教学资源、政策符合性、实施可行性"""
    
    def __init__(self, openai_api_key: str):
        """初始化教务处代表智能体"""
        super().__init__(
            agent_name="教务处代表",
            agent_type="academic_affairs",
            openai_api_key=openai_api_key
        )

    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """
        你是高校教务处的资深管理人员，具有丰富的教学管理经验。你的主要职责是确保培养方案的可行性和规范性。

        ## 你的关注重点：
        1. **教学资源配置**
           - 师资队伍是否充足（专任教师、兼职教师比例）
           - 教学设备和实验室条件是否满足需求
           - 教室、实训场所安排的合理性
           - 图书资料和数字资源的充足性

        2. **政策法规符合性**
           - 是否符合教育部专业目录和基本要求
           - 学分设置是否符合国家标准
           - 专业认证标准的满足情况
           - 实习实训学时比例的规范性

        3. **实施可行性**
           - 课程安排的时间合理性
           - 师资配备的现实可行性
           - 成本预算和投入产出比
           - 与现有教学体系的兼容性

        4. **质量保障体系**
           - 教学质量监控机制
           - 考核评价体系的科学性
           - 毕业要求的达成度评估
           - 持续改进机制的建立

        ## 分析方法：
        - 从管理角度评估方案的操作性
        - 重点关注资源需求和配置合理性
        - 考虑政策风险和合规性问题
        - 提出切实可行的改进建议

        ## 输出要求：
        请以JSON格式返回分析结果，包含以下字段：
        {
            "overall_assessment": "总体评估（字符串）",
            "resource_analysis": "资源分析（字符串）",
            "compliance_check": "合规性检查（字符串）",
            "feasibility_rating": 可行性评分（1-5分），
            "main_concerns": ["主要关切点列表"],
            "improvement_suggestions": [
                {
                    "suggestion_type": "建议类型（add/modify/remove）",
                    "target_component": "目标组件",
                    "detailed_suggestion": "详细建议",
                    "justification": "建议理由",
                    "priority": 优先级（1-5），
                    "feasibility": 可行性（0-1）,
                    "expected_benefit": "预期收益",
                    "implementation_cost": "实施成本评估",
                    "timeline": "实施时间线"
                }
            ],
            "risk_assessment": "风险评估（字符串）",
            "resource_requirements": {
                "faculty_needs": "师资需求",
                "facility_needs": "设施需求",
                "budget_estimate": "预算估算"
            }
        }
        """

    def analyze(self, curriculum: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        分析培养方案并提出教务管理角度的建议
        
        Args:
            curriculum: 培养方案数据
            **kwargs: 其他参数（如目标岗位等）
            
        Returns:
            分析结果和改进建议
        """
        print(f"🏫 {self.agent_name} 开始分析培养方案...")
        
        # 提取培养方案摘要
        curriculum_summary = self._extract_curriculum_summary(curriculum)
        target_positions = kwargs.get("target_positions", [])
        
        # 构建分析提示词
        user_prompt = f"""
        请从高校教务处管理角度分析以下培养方案：

        ## 培养方案概况：
        {curriculum_summary}

        ## 目标岗位群：
        {', '.join(target_positions) if target_positions else '未指定'}

        ## 详细培养方案数据：
        {curriculum}

        请重点分析：
        1. 教学资源配置的合理性和充足性
        2. 与国家教育政策和专业标准的符合性
        3. 实施的可行性和操作难度
        4. 可能存在的管理风险和应对措施
        5. 需要的资源投入和成本评估

        请提供具体、可操作的改进建议，确保方案既符合教育规律，又具备实施的可行性。
        """

        # 调用AI模型进行分析
        analysis_result = self._call_ai_model(
            system_prompt=self.get_system_prompt(),
            user_prompt=user_prompt,
            response_format="json_object"
        )

        if "error" in analysis_result:
            print(f"❌ {self.agent_name} 分析失败: {analysis_result['error']}")
            return self._create_fallback_analysis()

        print(f"✅ {self.agent_name} 分析完成")
        return self._process_analysis_result(analysis_result)

    def _process_analysis_result(self, raw_result: Dict[str, Any]) -> Dict[str, Any]:
        """处理AI分析结果"""
        try:
            # 转换改进建议为标准格式
            suggestions = []
            raw_suggestions = raw_result.get("improvement_suggestions", [])
            
            for i, raw_suggestion in enumerate(raw_suggestions):
                suggestion = self.create_suggestion(
                    suggestion_type=raw_suggestion.get("suggestion_type", "modify"),
                    target_component=raw_suggestion.get("target_component", f"component_{i}"),
                    detailed_suggestion=raw_suggestion.get("detailed_suggestion", ""),
                    justification=raw_suggestion.get("justification", ""),
                    priority=raw_suggestion.get("priority", 3),
                    feasibility=raw_suggestion.get("feasibility", 0.8)
                )
                
                # 添加教务处特有的字段
                suggestion.update({
                    "expected_benefit": raw_suggestion.get("expected_benefit", ""),
                    "implementation_cost": raw_suggestion.get("implementation_cost", ""),
                    "timeline": raw_suggestion.get("timeline", ""),
                    "resource_impact": "教务处评估"
                })
                
                suggestions.append(suggestion)

            return {
                "agent_type": self.agent_type,
                "agent_name": self.agent_name,
                "analysis_result": raw_result,
                "suggestions": suggestions,
                "summary": {
                    "feasibility_rating": raw_result.get("feasibility_rating", 3),
                    "main_concerns": raw_result.get("main_concerns", []),
                    "resource_requirements": raw_result.get("resource_requirements", {})
                }
            }
            
        except Exception as e:
            print(f"⚠️ {self.agent_name} 结果处理出错: {str(e)}")
            return self._create_fallback_analysis()

    def _create_fallback_analysis(self) -> Dict[str, Any]:
        """创建备用分析结果"""
        return {
            "agent_type": self.agent_type,
            "agent_name": self.agent_name,
            "analysis_result": {
                "overall_assessment": "由于技术问题，无法完成详细分析，建议手动审查",
                "feasibility_rating": 3,
                "main_concerns": ["需要进一步分析"],
                "resource_requirements": {}
            },
            "suggestions": [
                self.create_suggestion(
                    suggestion_type="modify",
                    target_component="overall_plan",
                    detailed_suggestion="建议进行全面的教务可行性评估",
                    justification="确保方案符合教学管理要求",
                    priority=2,
                    feasibility=0.9
                )
            ],
            "summary": {
                "feasibility_rating": 3,
                "main_concerns": ["需要进一步分析"],
                "resource_requirements": {}
            }
        } 