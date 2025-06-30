"""收敛性检查器 - 判断优化过程是否收敛"""

from typing import Dict, List, Any

class ConvergenceChecker:
    """收敛性检查器"""
    
    def __init__(self, convergence_threshold: float = 0.85):
        """
        初始化收敛检查器
        
        Args:
            convergence_threshold: 收敛阈值
        """
        self.convergence_threshold = convergence_threshold
        print(f"📊 收敛性检查器已初始化，阈值: {convergence_threshold}")

    def is_converged(self, optimization_state: Dict[str, Any]) -> bool:
        """
        检查优化是否收敛
        
        Args:
            optimization_state: 优化状态
            
        Returns:
            bool: 是否收敛
        """
        print("📊 正在检查收敛性...")
        
        # 获取收敛指标
        metrics = self._calculate_convergence_metrics(optimization_state)
        
        # 计算综合收敛分数
        convergence_score = self._calculate_convergence_score(metrics)
        
        print(f"📊 收敛分数: {convergence_score:.3f}, 阈值: {self.convergence_threshold}")
        
        is_converged = convergence_score >= self.convergence_threshold
        
        if is_converged:
            print("✅ 优化已收敛")
        else:
            print("🔄 优化尚未收敛")
        
        return is_converged

    def _calculate_convergence_metrics(self, state: Dict[str, Any]) -> Dict[str, float]:
        """计算收敛性指标"""
        metrics = {
            "suggestion_reduction_rate": 0.0,
            "conflict_severity_score": 1.0,
            "stakeholder_satisfaction_avg": 0.0,
            "curriculum_stability_score": 0.0,
            "consensus_degree": 0.0
        }
        
        # 建议减少率
        current_round = state.get("optimization_round", 1)
        if current_round > 1:
            # 比较当前轮次和前一轮次的建议数量
            current_suggestions = len(state.get("stakeholder_feedback", {}))
            if current_suggestions == 0:
                metrics["suggestion_reduction_rate"] = 1.0
            else:
                metrics["suggestion_reduction_rate"] = max(0, 1 - current_suggestions / 10)  # 假设初始有10个建议
        
        # 冲突严重度
        conflicts = state.get("conflict_analysis", [])
        if conflicts:
            avg_severity = sum(c.get("severity_score", 0.5) for c in conflicts) / len(conflicts)
            metrics["conflict_severity_score"] = 1.0 - avg_severity  # 冲突越少分数越高
        else:
            metrics["conflict_severity_score"] = 1.0
        
        # 利益相关者满意度
        satisfaction = state.get("stakeholder_satisfaction", {})
        if satisfaction:
            metrics["stakeholder_satisfaction_avg"] = sum(satisfaction.values()) / len(satisfaction)
        else:
            metrics["stakeholder_satisfaction_avg"] = 0.8  # 默认满意度
        
        # 培养方案稳定性（简化计算）
        versions = state.get("curriculum_versions", [])
        if len(versions) > 1:
            # 如果版本变化较少，说明趋于稳定
            metrics["curriculum_stability_score"] = min(1.0, 0.5 + 0.1 * len(versions))
        else:
            metrics["curriculum_stability_score"] = 0.7
        
        # 共识程度
        consensus_points = state.get("consensus_points", [])
        metrics["consensus_degree"] = min(1.0, len(consensus_points) / 5)  # 假设5个共识点为满分
        
        return metrics

    def _calculate_convergence_score(self, metrics: Dict[str, float]) -> float:
        """计算综合收敛分数"""
        
        # 各指标权重
        weights = {
            "suggestion_reduction_rate": 0.2,
            "conflict_severity_score": 0.3,
            "stakeholder_satisfaction_avg": 0.2,
            "curriculum_stability_score": 0.2,
            "consensus_degree": 0.1
        }
        
        # 加权平均
        score = sum(metrics[key] * weights[key] for key in weights if key in metrics)
        
        return min(score, 1.0)

    def get_convergence_report(self, optimization_state: Dict[str, Any]) -> Dict[str, Any]:
        """生成收敛性报告"""
        
        metrics = self._calculate_convergence_metrics(optimization_state)
        convergence_score = self._calculate_convergence_score(metrics)
        is_converged = convergence_score >= self.convergence_threshold
        
        report = {
            "is_converged": is_converged,
            "convergence_score": convergence_score,
            "threshold": self.convergence_threshold,
            "metrics": metrics,
            "recommendations": []
        }
        
        # 生成改进建议
        if not is_converged:
            if metrics["conflict_severity_score"] < 0.7:
                report["recommendations"].append("需要进一步解决利益相关者之间的冲突")
            
            if metrics["stakeholder_satisfaction_avg"] < 0.6:
                report["recommendations"].append("需要提高利益相关者的满意度")
            
            if metrics["consensus_degree"] < 0.5:
                report["recommendations"].append("需要形成更多共识点")
        
        return report