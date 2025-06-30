"""项目协调官 - 培养方案优化流程总指挥"""

from typing import Dict, List, Any, Optional
import asyncio
from datetime import datetime

from .base_agent import BaseAgent
from ..utils.conflict_detector import ConflictDetector
from ..utils.convergence_checker import ConvergenceChecker
from ..models import CurriculumOptimizationState, OptimizationConfig, DEFAULT_OPTIMIZATION_CONFIG

class ProjectCoordinator(BaseAgent):
    """项目协调官 - 优化流程总指挥"""
    
    def __init__(self, openai_api_key: str, config: Optional[OptimizationConfig] = None):
        """
        初始化项目协调官
        
        Args:
            openai_api_key: OpenAI API密钥
            config: 优化配置
        """
        super().__init__(
            agent_name="项目协调官",
            agent_type="project_coordinator", 
            openai_api_key=openai_api_key
        )
        
        self.config = config or DEFAULT_OPTIMIZATION_CONFIG
        self.conflict_detector = ConflictDetector()
        self.convergence_checker = ConvergenceChecker(self.config["convergence_threshold"])
        
        # 初始化利益相关者智能体（延迟初始化）
        self.stakeholder_agents = {}
        self._initialize_stakeholder_agents(openai_api_key)
        
        print(f"🎩 {self.agent_name} 初始化完成，配置: {self.config}")

    def _initialize_stakeholder_agents(self, openai_api_key: str):
        """初始化利益相关者智能体"""
        try:
            from .academic_affairs_agent import AcademicAffairsAgent
            from .hr_recruiter_agent import HRRecruiterAgent
            from .industry_expert_agent import IndustryExpertAgent
            from .student_representative_agent import StudentRepresentativeAgent
            from .faculty_representative_agent import FacultyRepresentativeAgent
            
            self.stakeholder_agents = {
                "academic_affairs": AcademicAffairsAgent(openai_api_key),
                "hr_recruiter": HRRecruiterAgent(openai_api_key),
                "industry_expert": IndustryExpertAgent(openai_api_key),
                "student_representative": StudentRepresentativeAgent(openai_api_key),
                "faculty_representative": FacultyRepresentativeAgent(openai_api_key)
            }
        except ImportError:
            print("⚠️ 部分智能体模块尚未实现，使用模拟智能体")
            # 创建模拟智能体
            self.stakeholder_agents = {
                "academic_affairs": MockAgent("教务处代表", "academic_affairs"),
                "hr_recruiter": MockAgent("HR招聘代表", "hr_recruiter"),
                "industry_expert": MockAgent("行业专家", "industry_expert"),
                "student_representative": MockAgent("学生代表", "student_representative"),
                "faculty_representative": MockAgent("教师代表", "faculty_representative")
            }

    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """
        你是培养方案智能优化平台的项目协调官，负责管理整个优化流程。
        
        你的职责包括：
        1. 协调各利益相关者的分析工作
        2. 管理多轮优化循环
        3. 检测和处理冲突
        4. 判断收敛条件
        5. 生成最终优化报告
        
        请确保优化过程公平、高效、收敛。
        """

    def analyze(self, curriculum: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """协调整个优化分析过程"""
        # 项目协调官不直接分析，而是协调其他智能体
        return {"message": "项目协调官负责协调，请使用run_optimization方法"}

    def run_optimization(
        self, 
        initial_curriculum: Dict[str, Any],
        major_name: str,
        target_positions: List[str]
    ) -> CurriculumOptimizationState:
        """
        运行完整的优化流程
        
        Args:
            initial_curriculum: 初始培养方案
            major_name: 专业名称
            target_positions: 目标岗位群
            
        Returns:
            CurriculumOptimizationState: 最终优化状态
        """
        print(f"🚀 启动培养方案优化流程")
        print(f"📋 专业: {major_name}")
        print(f"🎯 目标岗位: {', '.join(target_positions)}")
        
        # 创建初始优化状态
        from ..models import create_optimization_state
        optimization_state = create_optimization_state(
            major_name=major_name,
            target_positions=target_positions,
            original_curriculum=initial_curriculum,
            config=self.config
        )
        
        optimization_state["status"] = "optimizing"
        start_time = datetime.now()
        
        try:
            # 多轮优化循环
            for round_num in range(1, self.config["max_rounds"] + 1):
                print(f"\n{'='*50}")
                print(f"🔄 第 {round_num}/{self.config['max_rounds']} 轮优化")
                print(f"{'='*50}")
                
                optimization_state["optimization_round"] = round_num
                optimization_state["updated_at"] = datetime.now().isoformat()
                
                # 执行单轮优化
                round_result = self._run_single_round(optimization_state)
                
                # 更新优化状态
                optimization_state.update(round_result)
                
                # 检查收敛条件
                if self.convergence_checker.is_converged(optimization_state):
                    print(f"✅ 第 {round_num} 轮达到收敛条件，优化完成")
                    optimization_state["is_consensus_reached"] = True
                    break
                
                # 检查是否达到最大轮数
                if round_num >= self.config["max_rounds"]:
                    print(f"⏰ 达到最大轮数 {self.config['max_rounds']}，结束优化")
                    break
            
            # 计算总耗时
            end_time = datetime.now()
            optimization_state["optimization_duration"] = (end_time - start_time).total_seconds()
            optimization_state["status"] = "converged" if optimization_state["is_consensus_reached"] else "completed"
            
            print(f"\n🎉 优化流程完成")
            print(f"⏱️ 总耗时: {optimization_state['optimization_duration']:.1f}秒")
            print(f"🔄 总轮数: {optimization_state['optimization_round']}")
            
            return optimization_state
            
        except Exception as e:
            print(f"❌ 优化过程出现错误: {str(e)}")
            optimization_state["status"] = "error"
            return optimization_state

    def _run_single_round(self, state: CurriculumOptimizationState) -> Dict[str, Any]:
        """运行单轮优化"""
        round_num = state["optimization_round"]
        current_curriculum = state["current_curriculum"]
        target_positions = state["target_positions"]
        
        print(f"📊 开始第 {round_num} 轮分析...")
        
        # Step 1: 并行收集各利益相关者的建议
        stakeholder_suggestions = self._collect_stakeholder_feedback(
            current_curriculum, target_positions
        )
        
        # Step 2: 冲突检测
        all_suggestions = []
        for agent_type, suggestions in stakeholder_suggestions.items():
            all_suggestions.extend(suggestions)
        
        conflicts = self.conflict_detector.detect_conflicts(all_suggestions)
        
        # Step 3: 冲突调解（简化实现）
        mediated_solutions = self._mediate_conflicts(conflicts, all_suggestions)
        
        # Step 4: 应用优化建议（简化实现）
        optimized_curriculum = self._apply_optimizations(
            current_curriculum, mediated_solutions
        )
        
        # Step 5: 评估满意度
        satisfaction_scores = self._evaluate_stakeholder_satisfaction(stakeholder_suggestions)
        
        # 更新结果
        round_result = {
            "stakeholder_feedback": stakeholder_suggestions,
            "conflict_analysis": conflicts,
            "mediated_solutions": mediated_solutions,
            "current_curriculum": optimized_curriculum,
            "stakeholder_satisfaction": satisfaction_scores,
            "optimization_log": state["optimization_log"] + [{
                "round": round_num,
                "suggestions_count": len(all_suggestions),
                "conflicts_count": len(conflicts),
                "timestamp": datetime.now().isoformat()
            }]
        }
        
        return round_result

    def _collect_stakeholder_feedback(
        self, 
        curriculum: Dict[str, Any], 
        target_positions: List[str]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """收集各利益相关者的反馈"""
        print("👥 收集利益相关者反馈...")
        
        feedback = {}
        
        for agent_type, agent in self.stakeholder_agents.items():
            try:
                print(f"  🤖 {agent.agent_name} 正在分析...")
                
                # 根据智能体类型传递不同参数
                if agent_type in ["hr_recruiter", "industry_expert"]:
                    result = agent.analyze(curriculum, target_positions=target_positions)
                else:
                    result = agent.analyze(curriculum)
                
                suggestions = result.get("suggestions", [])
                feedback[agent_type] = suggestions
                
                print(f"  ✅ {agent.agent_name} 完成，提出 {len(suggestions)} 个建议")
                
            except Exception as e:
                print(f"  ❌ {agent.agent_name} 分析失败: {str(e)}")
                feedback[agent_type] = []
        
        return feedback

    def _mediate_conflicts(
        self, 
        conflicts: List[Dict[str, Any]], 
        suggestions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """调解冲突（简化实现）"""
        print(f"⚖️ 调解 {len(conflicts)} 个冲突...")
        
        mediated_solutions = []
        
        for conflict in conflicts:
            # 简化的调解逻辑
            solution = {
                "solution_id": f"sol_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "resolved_conflicts": [conflict["conflict_id"]],
                "compromise_suggestions": conflict["involved_suggestions"],
                "implementation_plan": "综合考虑各方意见，寻求平衡方案",
                "stakeholder_acceptance": {
                    "academic_affairs": 0.8,
                    "hr_recruiter": 0.7,
                    "industry_expert": 0.8,
                    "student_representative": 0.6,
                    "faculty_representative": 0.7
                },
                "final_decision": "采用妥协方案"
            }
            mediated_solutions.append(solution)
        
        print(f"✅ 生成 {len(mediated_solutions)} 个调解方案")
        return mediated_solutions

    def _apply_optimizations(
        self, 
        current_curriculum: Dict[str, Any], 
        solutions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """应用优化方案（简化实现）"""
        print("🔧 应用优化方案...")
        
        # 简化实现：暂时返回原课程，后续可以根据调解方案实际修改
        optimized_curriculum = current_curriculum.copy()
        
        # 这里应该根据调解方案实际修改培养方案
        # 例如：添加/删除课程、调整学分、修改实践环节等
        
        print("✅ 优化方案应用完成")
        return optimized_curriculum

    def _evaluate_stakeholder_satisfaction(
        self, 
        stakeholder_suggestions: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, float]:
        """评估利益相关者满意度"""
        satisfaction = {}
        
        for agent_type, suggestions in stakeholder_suggestions.items():
            # 简化逻辑：根据建议数量和优先级评估满意度
            if not suggestions:
                satisfaction[agent_type] = 0.5  # 中性满意度
            else:
                avg_priority = sum(s.get("priority", 3) for s in suggestions) / len(suggestions)
                satisfaction[agent_type] = min(1.0, avg_priority / 5.0 + 0.3)
        
        return satisfaction

# 模拟智能体类（用于测试）
class MockAgent:
    """模拟智能体"""
    
    def __init__(self, agent_name: str, agent_type: str):
        self.agent_name = agent_name
        self.agent_type = agent_type
    
    def analyze(self, curriculum: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """模拟分析"""
        return {
            "suggestions": [
                {
                    "suggestion_id": f"mock_{self.agent_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "agent_type": self.agent_type,
                    "agent_name": self.agent_name,
                    "suggestion_type": "modify",
                    "target_component": "course",
                    "detailed_suggestion": f"{self.agent_name}的模拟建议",
                    "justification": "模拟理由",
                    "priority": 3,
                    "feasibility": 0.8,
                    "expected_benefit": "模拟收益",
                    "potential_risks": [],
                    "timestamp": datetime.now().isoformat()
                }
            ]
        } 