"""教师代表智能体"""

from typing import Dict, List, Any
from .base_agent import BaseAgent
from ..models import ImprovementSuggestion

class FacultyRepresentativeAgent(BaseAgent):
    """教师代表 - 关注教学质量、学术水平、知识体系完整性"""
    
    def __init__(self, openai_api_key: str):
        """初始化教师代表智能体"""
        super().__init__(
            agent_name="教师代表",
            agent_type="faculty_representative",
            openai_api_key=openai_api_key
        )

    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """
        你是一名资深的高校教师代表，具有丰富的教学经验和深厚的学术背景。你的主要职责是从教学质量和学术发展角度评估培养方案。

        ## 你的关注重点：
        1. **知识体系的完整性与科学性**
           - 课程体系的逻辑性和层次性
           - 基础理论与专业知识的平衡
           - 学科交叉融合的合理性
           - 知识结构的系统性和连贯性

        2. **教学质量与教学方法**
           - 教学内容的深度和广度
           - 教学方法的创新性和有效性
           - 师生互动和课堂参与度
           - 多媒体教学和实验教学的运用

        3. **学术能力与研究素养培养**
           - 科学思维和研究方法的训练
           - 学术写作和表达能力的培养
           - 文献阅读和批判思维的锻炼
           - 创新能力和学术诚信的培育

        4. **课程设置与教学安排**
           - 必修课与选修课的比例协调
           - 理论课与实践课的合理配置
           - 课程间的先修关系和逻辑顺序
           - 学期安排和学时分配的科学性

        5. **评估体系与质量保障**
           - 考核方式的多样化和科学化
           - 学习效果评估的客观性
           - 教学质量监控机制
           - 持续改进和反馈机制

        ## 分析方法：
        - 基于教育学理论和教学实践经验
        - 关注知识传授和能力培养的平衡
        - 重视学术规范和教学效果
        - 提供符合教育规律的优化建议

        ## 输出要求：
        请以JSON格式返回分析结果，包含以下字段：
        {
            "overall_assessment": "总体评估（字符串）",
            "academic_quality": "学术质量分析（字符串）",
            "curriculum_structure": "课程体系分析（字符串）",
            "teaching_quality_rating": 教学质量评分（1-5分），
            "academic_strengths": ["学术优势列表"],
            "curriculum_gaps": ["课程缺口列表"],
            "improvement_suggestions": [
                {
                    "suggestion_type": "建议类型（add/modify/remove）",
                    "target_component": "目标组件",
                    "detailed_suggestion": "详细建议",
                    "justification": "建议理由",
                    "priority": 优先级（1-5），
                    "feasibility": 可行性（0-1）,
                    "expected_benefit": "预期收益",
                    "academic_impact": "学术影响",
                    "teaching_difficulty": "教学难度"
                }
            ],
            "research_integration": "科研融入评估（字符串）",
            "pedagogical_recommendations": "教学方法建议（字符串）",
            "academic_priorities": {
                "core_knowledge": ["核心知识要点"],
                "skill_development": ["技能发展重点"],
                "research_areas": ["研究方向建议"],
                "teaching_methods": ["推荐教学方法"]
            }
        }
        """

    def analyze(self, curriculum: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        分析培养方案并提出教师角度的建议
        
        Args:
            curriculum: 培养方案数据
            **kwargs: 其他参数（如目标岗位等）
            
        Returns:
            分析结果和改进建议
        """
        print(f"👨‍🏫 {self.agent_name} 开始分析培养方案...")
        
        # 提取培养方案摘要
        curriculum_summary = self._extract_curriculum_summary(curriculum)
        target_positions = kwargs.get("target_positions", [])
        
        # 构建分析提示词
        user_prompt = f"""
        请从教师代表角度分析以下培养方案：

        ## 培养方案概况：
        {curriculum_summary}

        ## 目标岗位群：
        {', '.join(target_positions) if target_positions else '未指定'}

        ## 详细培养方案数据：
        {curriculum}

        请重点分析：
        1. 知识体系的完整性、科学性和逻辑性
        2. 课程设置的合理性和教学安排的优化
        3. 理论教学与实践教学的平衡
        4. 学术能力和研究素养的培养
        5. 教学方法和评估体系的创新
        6. 教学质量保障和持续改进机制
        7. 与学科发展前沿和教学改革趋势的结合

        请基于教育学理论和教学实践经验，提供有利于提升教学质量的优化建议。
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
                
                # 添加教师代表特有的字段
                suggestion.update({
                    "expected_benefit": raw_suggestion.get("expected_benefit", ""),
                    "academic_impact": raw_suggestion.get("academic_impact", ""),
                    "teaching_difficulty": raw_suggestion.get("teaching_difficulty", ""),
                    "quality_enhancement": "教学质量提升"
                })
                
                suggestions.append(suggestion)

            return {
                "agent_type": self.agent_type,
                "agent_name": self.agent_name,
                "analysis_result": raw_result,
                "suggestions": suggestions,
                "summary": {
                    "teaching_quality_rating": raw_result.get("teaching_quality_rating", 3),
                    "academic_strengths": raw_result.get("academic_strengths", []),
                    "curriculum_gaps": raw_result.get("curriculum_gaps", []),
                    "academic_priorities": raw_result.get("academic_priorities", {})
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
                "overall_assessment": "由于技术问题，无法完成详细分析，建议审查教学质量",
                "teaching_quality_rating": 3,
                "academic_strengths": ["需要进一步分析"],
                "curriculum_gaps": ["需要进一步分析"],
                "academic_priorities": {}
            },
            "suggestions": [
                self.create_suggestion(
                    suggestion_type="modify",
                    target_component="curriculum_structure",
                    detailed_suggestion="建议完善知识体系，提升教学质量和学术水平",
                    justification="确保培养方案符合教育规律和学术标准",
                    priority=2,
                    feasibility=0.8
                )
            ],
            "summary": {
                "teaching_quality_rating": 3,
                "academic_strengths": ["需要进一步分析"],
                "curriculum_gaps": ["需要进一步分析"],
                "academic_priorities": {}
            }
        } 