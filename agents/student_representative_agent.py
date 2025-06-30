"""学生代表智能体"""

from typing import Dict, List, Any
from .base_agent import BaseAgent
from ..models import ImprovementSuggestion

class StudentRepresentativeAgent(BaseAgent):
    """学生代表 - 关注学习体验、课业负担、个人发展"""
    
    def __init__(self, openai_api_key: str):
        """初始化学生代表智能体"""
        super().__init__(
            agent_name="学生代表",
            agent_type="student_representative",
            openai_api_key=openai_api_key
        )

    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """
        你是一名优秀的在校学生代表，具有丰富的学习经验和对学生需求的深刻理解。你的主要职责是从学生学习体验和个人发展角度评估培养方案。

        ## 你的关注重点：
        1. **学习体验与兴趣培养**
           - 课程内容的趣味性和吸引力
           - 学习方式的多样性和互动性
           - 实践环节的充实性和成就感
           - 个性化学习路径的可选择性

        2. **学习负担与时间管理**
           - 课程安排的合理性和可行性
           - 学习强度与难度的适中性
           - 考试评估的公平性和科学性
           - 课外活动和社会实践的平衡

        3. **个人发展与能力提升**
           - 专业技能与通用能力的平衡培养
           - 创新思维和批判性思考的培养
           - 团队合作和沟通能力的锻炼
           - 领导力和组织能力的培养机会

        4. **就业准备与职业规划**
           - 职业认知和规划指导的充分性
           - 实习机会的质量和多样性
           - 就业技能培训的实用性
           - 校友网络和师长指导的支持

        5. **身心健康与全面发展**
           - 学习压力的合理控制
           - 心理健康支持和指导
           - 体育锻炼和文娱活动的安排
           - 国际化视野和文化素养的培养

        ## 分析方法：
        - 基于学生真实学习体验和需求反馈
        - 关注学习效果和个人成长
        - 重视学习过程中的困难和挑战
        - 提供贴近学生实际的优化建议

        ## 输出要求：
        请以JSON格式返回分析结果，包含以下字段：
        {
            "overall_assessment": "总体评估（字符串）",
            "learning_experience": "学习体验分析（字符串）",
            "workload_analysis": "学习负担分析（字符串）",
            "satisfaction_rating": 满意度评分（1-5分），
            "main_benefits": ["主要优势列表"],
            "main_challenges": ["主要挑战列表"],
            "improvement_suggestions": [
                {
                    "suggestion_type": "建议类型（add/modify/remove）",
                    "target_component": "目标组件",
                    "detailed_suggestion": "详细建议",
                    "justification": "建议理由",
                    "priority": 优先级（1-5），
                    "feasibility": 可行性（0-1）,
                    "expected_benefit": "预期收益",
                    "student_impact": "对学生的影响",
                    "implementation_ease": "实施难易度"
                }
            ],
            "career_readiness": "就业准备度评估（字符串）",
            "personal_development": "个人发展机会（字符串）",
            "student_priorities": {
                "learning_preferences": ["学习偏好列表"],
                "skill_interests": ["技能兴趣列表"],
                "career_concerns": ["职业关切点列表"],
                "support_needs": ["支持需求列表"]
            }
        }
        """

    def analyze(self, curriculum: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        分析培养方案并提出学生角度的建议
        
        Args:
            curriculum: 培养方案数据
            **kwargs: 其他参数（如目标岗位等）
            
        Returns:
            分析结果和改进建议
        """
        print(f"🎓 {self.agent_name} 开始分析培养方案...")
        
        # 提取培养方案摘要
        curriculum_summary = self._extract_curriculum_summary(curriculum)
        target_positions = kwargs.get("target_positions", [])
        
        # 构建分析提示词
        user_prompt = f"""
        请从学生代表角度分析以下培养方案：

        ## 培养方案概况：
        {curriculum_summary}

        ## 目标岗位群：
        {', '.join(target_positions) if target_positions else '未指定'}

        ## 详细培养方案数据：
        {curriculum}

        请重点分析：
        1. 学习体验的质量和吸引力
        2. 课程负担的合理性和可承受性
        3. 个人兴趣发展和专业选择的空间
        4. 实践机会的充分性和成就感
        5. 就业准备和职业发展的支持
        6. 身心健康和全面发展的保障
        7. 学习过程中可能遇到的困难和挑战

        请站在学生的立场，提供真实、贴近学生需求的优化建议。
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
                
                # 添加学生代表特有的字段
                suggestion.update({
                    "expected_benefit": raw_suggestion.get("expected_benefit", ""),
                    "student_impact": raw_suggestion.get("student_impact", ""),
                    "implementation_ease": raw_suggestion.get("implementation_ease", ""),
                    "learning_enhancement": "学习体验提升"
                })
                
                suggestions.append(suggestion)

            return {
                "agent_type": self.agent_type,
                "agent_name": self.agent_name,
                "analysis_result": raw_result,
                "suggestions": suggestions,
                "summary": {
                    "satisfaction_rating": raw_result.get("satisfaction_rating", 3),
                    "main_benefits": raw_result.get("main_benefits", []),
                    "main_challenges": raw_result.get("main_challenges", []),
                    "student_priorities": raw_result.get("student_priorities", {})
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
                "overall_assessment": "由于技术问题，无法完成详细分析，建议收集学生反馈",
                "satisfaction_rating": 3,
                "main_benefits": ["需要进一步分析"],
                "main_challenges": ["需要进一步分析"],
                "student_priorities": {}
            },
            "suggestions": [
                self.create_suggestion(
                    suggestion_type="modify",
                    target_component="learning_experience",
                    detailed_suggestion="建议优化学习体验，平衡课业负担与个人发展",
                    justification="确保学生能够充分受益并健康发展",
                    priority=2,
                    feasibility=0.9
                )
            ],
            "summary": {
                "satisfaction_rating": 3,
                "main_benefits": ["需要进一步分析"],
                "main_challenges": ["需要进一步分析"],
                "student_priorities": {}
            }
        } 