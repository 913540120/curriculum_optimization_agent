"""企业HR代表智能体"""

from typing import Dict, List, Any
from .base_agent import BaseAgent
from ..models import ImprovementSuggestion

class HRRecruiterAgent(BaseAgent):
    """企业HR代表 - 关注就业匹配度、市场需求、技能实用性"""
    
    def __init__(self, openai_api_key: str):
        """初始化HR代表智能体"""
        super().__init__(
            agent_name="企业HR代表",
            agent_type="hr_recruiter", 
            openai_api_key=openai_api_key
        )

    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """
        你是一名资深的企业HR招聘专家，具有丰富的校园招聘和人才评估经验。你的主要职责是从企业用人需求角度评估培养方案。

        ## 你的关注重点：
        1. **岗位技能匹配度**
           - 核心技能与目标岗位的匹配程度
           - 技术技能的前沿性和实用性
           - 跨领域技能的培养（如数据分析、项目管理）
           - 专业认证和证书的含金量

        2. **就业竞争力分析**
           - 毕业生在就业市场的竞争优势
           - 与同类院校同专业的差异化特色
           - 薪资水平预期和职业发展潜力
           - 行业认可度和雇主满意度

        3. **软技能培养**
           - 沟通表达和团队协作能力
           - 问题解决和创新思维能力
           - 适应性和学习能力
           - 领导力和项目管理能力

        4. **实践经验积累**
           - 实习机会的充分性和质量
           - 项目实践的真实性和挑战性
           - 行业接触和职业认知水平
           - 作品集和实战案例积累

        5. **市场趋势适应性**
           - 对行业发展趋势的敏感度
           - 新兴技术和工具的掌握
           - 跨行业就业的可能性
           - 持续学习和自我提升能力

        ## 分析方法：
        - 基于真实招聘经验评估人才培养效果
        - 对比行业标准和企业实际需求
        - 关注就业数据和市场反馈
        - 提供贴近企业需求的优化建议

        ## 输出要求：
        请以JSON格式返回分析结果，包含以下字段：
        {
            "overall_assessment": "总体评估（字符串）",
            "market_analysis": "市场需求分析（字符串）",
            "skill_gap_analysis": "技能缺口分析（字符串）",
            "employability_rating": 就业能力评分（1-5分），
            "main_strengths": ["主要优势列表"],
            "main_weaknesses": ["主要不足列表"],
            "improvement_suggestions": [
                {
                    "suggestion_type": "建议类型（add/modify/remove）",
                    "target_component": "目标组件",
                    "detailed_suggestion": "详细建议",
                    "justification": "建议理由",
                    "priority": 优先级（1-5），
                    "feasibility": 可行性（0-1）,
                    "expected_benefit": "预期收益",
                    "market_demand": "市场需求度",
                    "industry_trends": "行业趋势匹配度"
                }
            ],
            "career_prospects": "职业发展前景（字符串）",
            "salary_expectations": "薪资水平预期（字符串）",
            "skill_priorities": {
                "technical_skills": ["技术技能优先级列表"],
                "soft_skills": ["软技能优先级列表"],
                "certifications": ["推荐认证列表"]
            }
        }
        """

    def analyze(self, curriculum: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        分析培养方案并提出企业招聘角度的建议
        
        Args:
            curriculum: 培养方案数据
            **kwargs: 其他参数（如目标岗位等）
            
        Returns:
            分析结果和改进建议
        """
        print(f"💼 {self.agent_name} 开始分析培养方案...")
        
        # 提取培养方案摘要
        curriculum_summary = self._extract_curriculum_summary(curriculum)
        target_positions = kwargs.get("target_positions", [])
        
        # 构建分析提示词
        user_prompt = f"""
        请从企业HR招聘角度分析以下培养方案：

        ## 培养方案概况：
        {curriculum_summary}

        ## 目标岗位群：
        {', '.join(target_positions) if target_positions else '未指定'}

        ## 详细培养方案数据：
        {curriculum}

        请重点分析：
        1. 毕业生的技能结构与目标岗位需求的匹配度
        2. 相对于市场上其他候选人的竞争优势和劣势
        3. 实践能力培养的充分性（实习、项目、实战）
        4. 软技能培养（沟通、协作、创新、领导力）
        5. 适应行业发展趋势和技术变革的能力
        6. 毕业生的就业前景和职业发展潜力

        请基于真实的企业招聘需求和市场情况，提供具体的优化建议。
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
                
                # 添加HR特有的字段
                suggestion.update({
                    "expected_benefit": raw_suggestion.get("expected_benefit", ""),
                    "market_demand": raw_suggestion.get("market_demand", ""),
                    "industry_trends": raw_suggestion.get("industry_trends", ""),
                    "employment_impact": "就业能力提升"
                })
                
                suggestions.append(suggestion)

            return {
                "agent_type": self.agent_type,
                "agent_name": self.agent_name,
                "analysis_result": raw_result,
                "suggestions": suggestions,
                "summary": {
                    "employability_rating": raw_result.get("employability_rating", 3),
                    "main_strengths": raw_result.get("main_strengths", []),
                    "main_weaknesses": raw_result.get("main_weaknesses", []),
                    "skill_priorities": raw_result.get("skill_priorities", {})
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
                "overall_assessment": "由于技术问题，无法完成详细分析，建议手动审查就业匹配度",
                "employability_rating": 3,
                "main_strengths": ["需要进一步分析"],
                "main_weaknesses": ["需要进一步分析"],
                "skill_priorities": {}
            },
            "suggestions": [
                self.create_suggestion(
                    suggestion_type="modify",
                    target_component="skill_training",
                    detailed_suggestion="建议加强与企业需求的对接，提升就业竞争力",
                    justification="确保毕业生满足市场需求",
                    priority=2,
                    feasibility=0.9
                )
            ],
            "summary": {
                "employability_rating": 3,
                "main_strengths": ["需要进一步分析"],
                "main_weaknesses": ["需要进一步分析"],
                "skill_priorities": {}
            }
        }