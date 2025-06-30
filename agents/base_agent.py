"""基础智能体抽象类"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from openai import OpenAI
import json
import time

class BaseAgent(ABC):
    """智能体基类"""
    
    def __init__(self, agent_name: str, agent_type: str, openai_api_key: str):
        """
        初始化基础智能体
        
        Args:
            agent_name: 智能体名称
            agent_type: 智能体类型
            openai_api_key: OpenAI API密钥
        """
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.openai_client = OpenAI(
            base_url='https://api.siliconflow.cn/v1',
            api_key=openai_api_key
        )
        
        print(f"🤖 {self.agent_name} 已初始化")

    @abstractmethod
    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        pass

    @abstractmethod
    def analyze(self, curriculum: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """分析培养方案并提出建议"""
        pass

    def _call_ai_model(self, system_prompt: str, user_prompt: str, 
                      response_format: str = "json_object", timeout: int = 90) -> Dict[str, Any]:
        """
        调用AI模型
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            response_format: 响应格式
            timeout: 超时时间
            
        Returns:
            AI模型的响应结果
        """
        try:
            print(f"🔄 {self.agent_name} 正在调用AI模型...")
            
            response = self.openai_client.chat.completions.create(
                model="deepseek-ai/DeepSeek-R1",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": response_format} if response_format == "json_object" else None,
                timeout=timeout
            )
            
            content = response.choices[0].message.content
            
            if response_format == "json_object":
                result = json.loads(content)
            else:
                result = {"response": content}
            
            print(f"✅ {self.agent_name} AI调用成功")
            return result
            
        except Exception as e:
            print(f"❌ {self.agent_name} AI调用失败: {str(e)}")
            return {"error": str(e)}

    def _safe_execute(self, func, *args, **kwargs) -> Dict[str, Any]:
        """安全执行函数"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"❌ {self.agent_name} 执行失败: {str(e)}")
            return {"error": str(e)}

    def _extract_curriculum_summary(self, curriculum: Dict[str, Any]) -> str:
        """提取培养方案摘要用于AI分析"""
        summary_parts = []
        
        # 基本信息
        basic_info = curriculum.get("basic_info", {})
        if basic_info:
            summary_parts.append(f"专业：{basic_info.get('major_name', '未知')}")
            summary_parts.append(f"学制：{basic_info.get('duration', '四年')}")
            summary_parts.append(f"学位：{basic_info.get('degree_type', '学士')}")
        
        # 课程统计
        courses = curriculum.get("courses", [])
        if courses:
            total_credits = sum(course.get("credits", 0) for course in courses)
            summary_parts.append(f"总课程数：{len(courses)}门")
            summary_parts.append(f"总学分：{total_credits}分")
        
        # 学分分配
        credit_dist = curriculum.get("credit_distribution", {})
        if credit_dist:
            dist_str = ", ".join([f"{k}:{v}分" for k, v in credit_dist.items()])
            summary_parts.append(f"学分分配：{dist_str}")
        
        # 实践环节
        practical = curriculum.get("practical_training", [])
        if practical:
            summary_parts.append(f"实践环节：{len(practical)}个")
        
        return "\n".join(summary_parts)

    def create_suggestion(self, suggestion_type: str, target_component: str, 
                         detailed_suggestion: str, justification: str,
                         priority: int = 3, feasibility: float = 0.8) -> Dict[str, Any]:
        """创建改进建议"""
        from datetime import datetime
        
        suggestion_id = f"sug_{self.agent_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            "suggestion_id": suggestion_id,
            "agent_type": self.agent_type,
            "agent_name": self.agent_name,
            "suggestion_type": suggestion_type,
            "target_component": target_component,
            "detailed_suggestion": detailed_suggestion,
            "justification": justification,
            "priority": priority,
            "feasibility": feasibility,
            "expected_benefit": "",
            "potential_risks": [],
            "timestamp": datetime.now().isoformat()
        } 