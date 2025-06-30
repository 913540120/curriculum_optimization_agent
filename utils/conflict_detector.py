"""
利益相关者建议冲突检测器

识别和分析来自不同利益相关者的改进建议之间的冲突，
包括资源冲突、内容冲突、优先级冲突等类型
"""

from typing import List, Dict, Any, Tuple, Set
from collections import defaultdict
import textdistance
from datetime import datetime

from ..models import (
    ImprovementSuggestion, 
    ConflictAnalysis, 
    ConflictType,
    AgentType
)

class ConflictDetector:
    """冲突检测器"""
    
    def __init__(self):
        """初始化冲突检测器"""
        
        # 冲突类型权重（严重程度）
        self.conflict_weights = {
            ConflictType.RESOURCE.value: 0.9,    # 资源冲突最严重
            ConflictType.CONTENT.value: 0.7,     # 内容冲突较严重
            ConflictType.PRIORITY.value: 0.5,    # 优先级冲突中等
            ConflictType.TIMELINE.value: 0.6     # 时间冲突较严重
        }
        
        # 利益相关者立场特征
        self.stakeholder_profiles = {
            AgentType.ACADEMIC_AFFAIRS.value: {
                "focus": ["可行性", "资源", "成本", "管理"],
                "priorities": ["师资", "教室", "设备", "政策符合性"],
                "constraints": ["预算", "政策", "人力"]
            },
            AgentType.HR_RECRUITER.value: {
                "focus": ["就业", "技能匹配", "竞争力", "市场需求"],
                "priorities": ["实用技能", "项目经验", "软技能", "行业认证"],
                "constraints": ["招聘标准", "市场趋势"]
            },
            AgentType.INDUSTRY_EXPERT.value: {
                "focus": ["技术前沿", "行业标准", "实际应用", "创新能力"],
                "priorities": ["前沿技术", "工具使用", "实战经验", "行业认证"],
                "constraints": ["技术发展速度", "行业标准"]
            },
            AgentType.STUDENT_REP.value: {
                "focus": ["学习体验", "负担平衡", "兴趣培养", "个人发展"],
                "priorities": ["学习难度", "课程安排", "选择空间", "实践机会"],
                "constraints": ["学习能力", "时间安排", "兴趣偏好"]
            },
            AgentType.FACULTY_REP.value: {
                "focus": ["学术质量", "知识体系", "教学效果", "研究能力"],
                "priorities": ["理论基础", "知识完整性", "学术深度", "研究训练"],
                "constraints": ["教学质量", "学术标准", "课程逻辑"]
            }
        }
        
        print("🔍 冲突检测器已初始化")

    def detect_conflicts(self, suggestions: List[Dict]) -> List[Dict]:
        """检测建议之间的冲突"""
        print(f"🔍 开始冲突检测，共 {len(suggestions)} 个建议")
        
        if len(suggestions) < 2:
            return []
        
        conflicts = []
        
        # 简单的冲突检测逻辑
        for i in range(len(suggestions)):
            for j in range(i + 1, len(suggestions)):
                sug1, sug2 = suggestions[i], suggestions[j]
                
                if self._has_conflict(sug1, sug2):
                    conflict = {
                        "conflict_id": f"conflict_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}_{j}",
                        "conflict_type": "content_conflict",
                        "involved_suggestions": [sug1.get("suggestion_id", f"sug_{i}"), sug2.get("suggestion_id", f"sug_{j}")],
                        "conflict_description": f"建议之间存在冲突",
                        "severity_score": 0.7,
                        "affected_components": [sug1.get("target_component", "")],
                        "resolution_strategies": ["综合考虑各方意见", "寻求平衡方案"]
                    }
                    conflicts.append(conflict)
        
        print(f"✅ 冲突检测完成，发现 {len(conflicts)} 个冲突")
        return conflicts

    def _has_conflict(self, sug1: Dict, sug2: Dict) -> bool:
        """简单的冲突判断"""
        # 如果建议类型相反（添加 vs 删除）
        type1 = sug1.get("suggestion_type", "")
        type2 = sug2.get("suggestion_type", "")
        
        if (type1 == "add" and type2 == "remove") or (type1 == "remove" and type2 == "add"):
            return True
        
        # 检查建议者立场冲突（教务处 vs HR）
        agent1 = sug1.get("agent_type", "")
        agent2 = sug2.get("agent_type", "")
        
        if (agent1 == "academic_affairs" and agent2 == "hr_recruiter") or \
           (agent1 == "hr_recruiter" and agent2 == "academic_affairs"):
            return True
        
        return False

    def _group_by_component(self, suggestions: List[ImprovementSuggestion]) -> Dict[str, List[ImprovementSuggestion]]:
        """按目标组件分组建议"""
        groups = defaultdict(list)
        for suggestion in suggestions:
            component = suggestion.get("target_component", "unknown")
            groups[component].append(suggestion)
        return dict(groups)

    def _detect_resource_conflicts(self, suggestions: List[ImprovementSuggestion]) -> List[ConflictAnalysis]:
        """检测资源冲突"""
        conflicts = []
        
        # 检测同一组件的不同资源需求
        for i in range(len(suggestions)):
            for j in range(i + 1, len(suggestions)):
                suggestion1 = suggestions[i]
                suggestion2 = suggestions[j]
                
                # 检查是否存在资源竞争
                if self._has_resource_conflict(suggestion1, suggestion2):
                    conflict = self._create_conflict_analysis(
                        ConflictType.RESOURCE,
                        [suggestion1, suggestion2],
                        f"关于 {suggestion1['target_component']} 的资源分配存在冲突"
                    )
                    conflicts.append(conflict)
        
        return conflicts

    def _detect_content_conflicts(self, suggestions: List[ImprovementSuggestion]) -> List[ConflictAnalysis]:
        """检测内容冲突"""
        conflicts = []
        
        for i in range(len(suggestions)):
            for j in range(i + 1, len(suggestions)):
                suggestion1 = suggestions[i]
                suggestion2 = suggestions[j]
                
                # 检查建议类型是否冲突
                if self._has_content_conflict(suggestion1, suggestion2):
                    conflict = self._create_conflict_analysis(
                        ConflictType.CONTENT,
                        [suggestion1, suggestion2],
                        f"关于 {suggestion1['target_component']} 的内容建议存在矛盾"
                    )
                    conflicts.append(conflict)
        
        return conflicts

    def _detect_priority_conflicts(self, suggestions: List[ImprovementSuggestion]) -> List[ConflictAnalysis]:
        """检测优先级冲突"""
        conflicts = []
        
        # 按优先级分组
        priority_groups = defaultdict(list)
        for suggestion in suggestions:
            priority = suggestion.get("priority", 3)
            priority_groups[priority].append(suggestion)
        
        # 检测高优先级建议之间的冲突
        high_priority_suggestions = []
        for priority in [5, 4]:  # 高优先级
            high_priority_suggestions.extend(priority_groups.get(priority, []))
        
        if len(high_priority_suggestions) > 3:  # 如果高优先级建议过多
            conflict = self._create_conflict_analysis(
                ConflictType.PRIORITY,
                high_priority_suggestions,
                f"存在过多高优先级建议，可能导致资源分散"
            )
            conflicts.append(conflict)
        
        return conflicts

    def _detect_timeline_conflicts(self, suggestions: List[ImprovementSuggestion]) -> List[ConflictAnalysis]:
        """检测时间冲突"""
        conflicts = []
        
        # 检测实施时间线冲突（基于建议内容分析）
        for i in range(len(suggestions)):
            for j in range(i + 1, len(suggestions)):
                suggestion1 = suggestions[i]
                suggestion2 = suggestions[j]
                
                if self._has_timeline_conflict(suggestion1, suggestion2):
                    conflict = self._create_conflict_analysis(
                        ConflictType.TIMELINE,
                        [suggestion1, suggestion2],
                        f"关于 {suggestion1['target_component']} 的实施时间存在冲突"
                    )
                    conflicts.append(conflict)
        
        return conflicts

    def _detect_cross_component_conflicts(self, suggestions: List[ImprovementSuggestion]) -> List[ConflictAnalysis]:
        """检测跨组件冲突"""
        conflicts = []
        
        # 检测可能影响多个组件的建议
        component_suggestions = self._group_by_component(suggestions)
        components = list(component_suggestions.keys())
        
        for i in range(len(components)):
            for j in range(i + 1, len(components)):
                comp1, comp2 = components[i], components[j]
                
                # 检测相关组件之间的冲突
                if self._are_related_components(comp1, comp2):
                    sug1_list = component_suggestions[comp1]
                    sug2_list = component_suggestions[comp2]
                    
                    for sug1 in sug1_list:
                        for sug2 in sug2_list:
                            if self._has_cross_component_conflict(sug1, sug2):
                                conflict = self._create_conflict_analysis(
                                    ConflictType.CONTENT,
                                    [sug1, sug2],
                                    f"组件 {comp1} 和 {comp2} 之间存在关联冲突"
                                )
                                conflicts.append(conflict)
        
        return conflicts

    def _has_resource_conflict(self, sug1: ImprovementSuggestion, sug2: ImprovementSuggestion) -> bool:
        """判断是否存在资源冲突"""
        # 检查建议者立场是否天然存在资源竞争
        agent1 = sug1.get("agent_type", "")
        agent2 = sug2.get("agent_type", "")
        
        # 教务处 vs HR招聘者：资源分配冲突
        if (agent1 == AgentType.ACADEMIC_AFFAIRS.value and agent2 == AgentType.HR_RECRUITER.value) or \
           (agent1 == AgentType.HR_RECRUITER.value and agent2 == AgentType.ACADEMIC_AFFAIRS.value):
            return True
        
        # 检查具体建议内容
        content1 = sug1.get("detailed_suggestion", "").lower()
        content2 = sug2.get("detailed_suggestion", "").lower()
        
        resource_keywords = ["增加", "减少", "替换", "新增", "取消", "师资", "设备", "经费"]
        
        for keyword in resource_keywords:
            if keyword in content1 and keyword in content2:
                # 如果都涉及同样的资源操作，可能存在冲突
                return True
        
        return False

    def _has_content_conflict(self, sug1: ImprovementSuggestion, sug2: ImprovementSuggestion) -> bool:
        """判断是否存在内容冲突"""
        type1 = sug1.get("suggestion_type", "")
        type2 = sug2.get("suggestion_type", "")
        
        # 如果一个要添加，一个要删除同样的内容
        if (type1 == "add" and type2 == "remove") or (type1 == "remove" and type2 == "add"):
            return True
        
        # 检查建议内容的语义相似性但方向相反
        content1 = sug1.get("detailed_suggestion", "")
        content2 = sug2.get("detailed_suggestion", "")
        
        # 使用文本距离检测相似但冲突的建议
        similarity = textdistance.jaro_winkler(content1, content2)
        if similarity > 0.6:  # 内容相似
            # 检查是否方向相反
            if self._are_opposite_directions(content1, content2):
                return True
        
        return False

    def _has_timeline_conflict(self, sug1: ImprovementSuggestion, sug2: ImprovementSuggestion) -> bool:
        """判断是否存在时间冲突"""
        content1 = sug1.get("detailed_suggestion", "").lower()
        content2 = sug2.get("detailed_suggestion", "").lower()
        
        # 检查时间相关的关键词
        urgent_keywords = ["立即", "马上", "紧急", "优先", "第一学期"]
        gradual_keywords = ["逐步", "分阶段", "长期", "最后", "毕业前"]
        
        is_urgent1 = any(keyword in content1 for keyword in urgent_keywords)
        is_urgent2 = any(keyword in content2 for keyword in urgent_keywords)
        is_gradual1 = any(keyword in content1 for keyword in gradual_keywords)
        is_gradual2 = any(keyword in content2 for keyword in gradual_keywords)
        
        # 如果一个要求立即实施，一个要求逐步实施
        if (is_urgent1 and is_gradual2) or (is_urgent2 and is_gradual1):
            return True
        
        return False

    def _has_cross_component_conflict(self, sug1: ImprovementSuggestion, sug2: ImprovementSuggestion) -> bool:
        """判断是否存在跨组件冲突"""
        # 简化实现：检查建议是否可能互相影响
        content1 = sug1.get("detailed_suggestion", "").lower()
        content2 = sug2.get("detailed_suggestion", "").lower()
        
        # 检查是否涉及相同的概念但方向不同
        common_concepts = ["学分", "学时", "难度", "实践", "理论"]
        
        for concept in common_concepts:
            if concept in content1 and concept in content2:
                if self._are_opposite_directions(content1, content2):
                    return True
        
        return False

    def _are_related_components(self, comp1: str, comp2: str) -> bool:
        """判断两个组件是否相关"""
        # 定义相关组件关系
        related_pairs = [
            ("course", "credit"),
            ("course", "skill"),
            ("credit", "practical"),
            ("skill", "practical")
        ]
        
        for pair in related_pairs:
            if (pair[0] in comp1.lower() and pair[1] in comp2.lower()) or \
               (pair[1] in comp1.lower() and pair[0] in comp2.lower()):
                return True
        
        return False

    def _are_opposite_directions(self, content1: str, content2: str) -> bool:
        """判断两个建议是否方向相反"""
        positive_words = ["增加", "提高", "加强", "新增", "扩大", "提升"]
        negative_words = ["减少", "降低", "减弱", "删除", "缩小", "削减"]
        
        has_positive1 = any(word in content1 for word in positive_words)
        has_negative1 = any(word in content1 for word in negative_words)
        has_positive2 = any(word in content2 for word in positive_words)
        has_negative2 = any(word in content2 for word in negative_words)
        
        # 如果一个是正向建议，一个是负向建议
        return (has_positive1 and has_negative2) or (has_negative1 and has_positive2)

    def _create_conflict_analysis(
        self, 
        conflict_type: ConflictType, 
        involved_suggestions: List[ImprovementSuggestion],
        description: str
    ) -> ConflictAnalysis:
        """创建冲突分析结果"""
        
        # 计算冲突严重程度
        severity = self._calculate_conflict_severity(conflict_type, involved_suggestions)
        
        # 提取受影响的组件
        affected_components = list(set(
            sug.get("target_component", "") for sug in involved_suggestions
        ))
        
        # 生成解决策略
        resolution_strategies = self._generate_resolution_strategies(conflict_type, involved_suggestions)
        
        conflict_id = f"conflict_{conflict_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return ConflictAnalysis(
            conflict_id=conflict_id,
            conflict_type=conflict_type.value,
            involved_suggestions=[sug.get("suggestion_id", "") for sug in involved_suggestions],
            conflict_description=description,
            severity_score=severity,
            affected_components=affected_components,
            resolution_strategies=resolution_strategies
        )

    def _calculate_conflict_severity(
        self, 
        conflict_type: ConflictType, 
        suggestions: List[ImprovementSuggestion]
    ) -> float:
        """计算冲突严重程度"""
        
        base_severity = self.conflict_weights.get(conflict_type.value, 0.5)
        
        # 根据涉及的建议数量调整严重程度
        suggestion_factor = min(len(suggestions) / 5.0, 1.0)  # 最多5个建议
        
        # 根据建议优先级调整
        avg_priority = sum(sug.get("priority", 3) for sug in suggestions) / len(suggestions)
        priority_factor = avg_priority / 5.0  # 归一化到0-1
        
        # 根据可行性调整
        avg_feasibility = sum(sug.get("feasibility", 0.8) for sug in suggestions) / len(suggestions)
        feasibility_factor = 1.0 - avg_feasibility  # 可行性越低，冲突越严重
        
        # 综合计算
        total_severity = base_severity * 0.5 + \
                        suggestion_factor * 0.2 + \
                        priority_factor * 0.2 + \
                        feasibility_factor * 0.1
        
        return min(total_severity, 1.0)  # 确保不超过1.0

    def _generate_resolution_strategies(
        self, 
        conflict_type: ConflictType, 
        suggestions: List[ImprovementSuggestion]
    ) -> List[str]:
        """生成冲突解决策略"""
        
        strategies = []
        
        if conflict_type == ConflictType.RESOURCE:
            strategies.extend([
                "分阶段实施，避免资源竞争",
                "寻找共享资源的可能性",
                "调整实施优先级",
                "寻求额外资源支持"
            ])
        
        elif conflict_type == ConflictType.CONTENT:
            strategies.extend([
                "整合相似建议，形成综合方案",
                "选择最优建议，保留备选方案",
                "分别试点，比较效果",
                "征求专家意见进行裁决"
            ])
        
        elif conflict_type == ConflictType.PRIORITY:
            strategies.extend([
                "重新评估各建议的优先级",
                "按照整体目标重新排序",
                "平衡各方利益诉求",
                "制定优先级决策准则"
            ])
        
        elif conflict_type == ConflictType.TIMELINE:
            strategies.extend([
                "制定详细的实施时间表",
                "调整各建议的实施节奏",
                "预留缓冲时间",
                "分阶段验证和调整"
            ])
        
        return strategies

    def analyze_stakeholder_alignment(self, suggestions: List[ImprovementSuggestion]) -> Dict[str, Any]:
        """分析利益相关者的立场一致性"""
        
        alignment_analysis = {
            "overall_alignment": 0.0,
            "stakeholder_pairs": {},
            "consensus_areas": [],
            "divergent_areas": []
        }
        
        # 按利益相关者分组
        stakeholder_groups = defaultdict(list)
        for suggestion in suggestions:
            agent_type = suggestion.get("agent_type", "unknown")
            stakeholder_groups[agent_type].append(suggestion)
        
        stakeholders = list(stakeholder_groups.keys())
        total_alignments = []
        
        # 计算两两之间的一致性
        for i in range(len(stakeholders)):
            for j in range(i + 1, len(stakeholders)):
                stakeholder1, stakeholder2 = stakeholders[i], stakeholders[j]
                
                alignment_score = self._calculate_stakeholder_alignment(
                    stakeholder_groups[stakeholder1],
                    stakeholder_groups[stakeholder2]
                )
                
                pair_key = f"{stakeholder1}-{stakeholder2}"
                alignment_analysis["stakeholder_pairs"][pair_key] = alignment_score
                total_alignments.append(alignment_score)
        
        # 计算整体一致性
        if total_alignments:
            alignment_analysis["overall_alignment"] = sum(total_alignments) / len(total_alignments)
        
        return alignment_analysis

    def _calculate_stakeholder_alignment(
        self, 
        suggestions1: List[ImprovementSuggestion], 
        suggestions2: List[ImprovementSuggestion]
    ) -> float:
        """计算两个利益相关者之间的一致性"""
        
        if not suggestions1 or not suggestions2:
            return 0.0
        
        # 基于目标组件的重叠度
        components1 = set(sug.get("target_component", "") for sug in suggestions1)
        components2 = set(sug.get("target_component", "") for sug in suggestions2)
        
        component_overlap = len(components1 & components2) / len(components1 | components2) if components1 | components2 else 0
        
        # 基于建议类型的一致性
        types1 = [sug.get("suggestion_type", "") for sug in suggestions1]
        types2 = [sug.get("suggestion_type", "") for sug in suggestions2]
        
        type_consistency = len([t for t in types1 if t in types2]) / max(len(types1), len(types2)) if types1 or types2 else 0
        
        # 综合计算一致性
        alignment_score = (component_overlap * 0.6 + type_consistency * 0.4)
        
        return alignment_score 