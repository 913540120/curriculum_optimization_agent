"""行业技术专家智能体"""

from typing import Dict, List, Any
from .base_agent import BaseAgent
from ..models import ImprovementSuggestion

class IndustryExpertAgent(BaseAgent):
    """行业技术专家 - 关注技术前沿性、行业标准、实际应用"""
    
    def __init__(self, openai_api_key: str):
        """初始化行业专家智能体"""
        super().__init__(
            agent_name="行业技术专家",
            agent_type="industry_expert",
            openai_api_key=openai_api_key
        )

    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """
        你是一名资深的行业技术专家，对前沿技术发展和行业实践有深入的理解。你的主要职责是从技术发展和行业应用角度评估培养方案。

        ## 你的关注重点：
        1. **技术前沿性与创新性**
           - 课程内容与最新技术趋势的同步性
           - 新兴技术领域的覆盖程度（AI、云计算、大数据等）
           - 技术深度与广度的平衡
           - 前瞻性技术的引入和培养

        2. **行业标准与规范**
           - 符合国际和国内行业标准
           - 专业认证体系的对接
           - 技术规范和最佳实践的传授
           - 质量管理体系的建立

        3. **实际应用能力**
           - 理论与实践的结合程度
           - 真实项目经验的积累
           - 问题解决能力的培养
           - 工程化思维的建立

        4. **技术生态认知**
           - 对技术栈和工具链的全面了解
           - 跨技术领域的整合能力
           - 开源社区参与和贡献
           - 技术选型和架构设计能力

        5. **创新能力培养**
           - 研发思维和创新方法论
           - 技术调研和学习能力
           - 原创性项目和专利申请
           - 技术创业和产品化能力

        ## 分析方法：
        - 基于行业最新发展趋势评估课程内容
        - 对比国际先进院校和企业实践
        - 关注技术技能的实用性和前瞻性
        - 提供符合行业发展方向的优化建议

        ## 输出要求：
        请以JSON格式返回分析结果，包含以下字段：
        {
            "overall_assessment": "总体评估（字符串）",
            "technology_analysis": "技术水平分析（字符串）",
            "industry_alignment": "行业对齐度分析（字符串）",
            "innovation_rating": 创新性评分（1-5分），
            "technology_gaps": ["技术缺口列表"],
            "emerging_technologies": ["新兴技术建议列表"],
            "improvement_suggestions": [
                {
                    "suggestion_type": "建议类型（add/modify/remove）",
                    "target_component": "目标组件",
                    "detailed_suggestion": "详细建议",
                    "justification": "建议理由",
                    "priority": 优先级（1-5），
                    "feasibility": 可行性（0-1）,
                    "expected_benefit": "预期收益",
                    "technology_level": "技术层级（基础/进阶/前沿）",
                    "industry_demand": "行业需求度"
                }
            ],
            "standards_compliance": "标准符合性评估（字符串）",
            "future_trends": "未来发展趋势（字符串）",
            "recommended_focus": {
                "core_technologies": ["核心技术重点"],
                "emerging_areas": ["新兴领域推荐"],
                "practical_skills": ["实践技能重点"],
                "certifications": ["推荐认证"]
            }
        }
        """

    def analyze(self, curriculum: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        分析培养方案并提出行业技术角度的建议
        
        Args:
            curriculum: 培养方案数据
            **kwargs: 其他参数（如目标岗位等）
            
        Returns:
            分析结果和改进建议
        """
        print(f"🔬 {self.agent_name} 开始分析培养方案...")
        
        # 提取培养方案摘要
        curriculum_summary = self._extract_curriculum_summary(curriculum)
        target_positions = kwargs.get("target_positions", [])
        
        # 构建分析提示词
        user_prompt = f"""
        请从行业技术专家角度分析以下培养方案：

        ## 培养方案概况：
        {curriculum_summary}

        ## 目标岗位群：
        {', '.join(target_positions) if target_positions else '未指定'}

        ## 详细培养方案数据：
        {curriculum}

        请重点分析：
        1. 技术内容的前沿性和创新性
        2. 与当前行业标准和最佳实践的匹配度
        3. 实际应用能力和工程化思维的培养
        4. 新兴技术趋势的跟进和覆盖
        5. 技术深度和广度的平衡性
        6. 创新能力和研发思维的培养
        7. 与国际先进水平的差距和改进方向

        请基于行业发展趋势和技术演进方向，提供具有前瞻性的优化建议。
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
                
                # 添加行业专家特有的字段
                suggestion.update({
                    "expected_benefit": raw_suggestion.get("expected_benefit", ""),
                    "technology_level": raw_suggestion.get("technology_level", ""),
                    "industry_demand": raw_suggestion.get("industry_demand", ""),
                    "innovation_impact": "技术创新提升"
                })
                
                suggestions.append(suggestion)

            return {
                "agent_type": self.agent_type,
                "agent_name": self.agent_name,
                "analysis_result": raw_result,
                "suggestions": suggestions,
                "summary": {
                    "innovation_rating": raw_result.get("innovation_rating", 3),
                    "technology_gaps": raw_result.get("technology_gaps", []),
                    "emerging_technologies": raw_result.get("emerging_technologies", []),
                    "recommended_focus": raw_result.get("recommended_focus", {})
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
                "overall_assessment": "由于技术问题，无法完成详细分析，建议手动审查技术前沿性",
                "innovation_rating": 3,
                "technology_gaps": ["需要进一步分析"],
                "emerging_technologies": ["需要进一步分析"],
                "recommended_focus": {}
            },
            "suggestions": [
                self.create_suggestion(
                    suggestion_type="modify",
                    target_component="technology_content",
                    detailed_suggestion="建议加强前沿技术的引入和应用能力培养",
                    justification="确保技术内容与行业发展同步",
                    priority=2,
                    feasibility=0.8
                )
            ],
            "summary": {
                "innovation_rating": 3,
                "technology_gaps": ["需要进一步分析"],
                "emerging_technologies": ["需要进一步分析"],
                "recommended_focus": {}
            }
        } 