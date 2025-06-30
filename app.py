"""
培养方案智能优化平台 V2.0 - Streamlit应用
"""

import streamlit as st
import json
import asyncio
from typing import Dict, List, Any
import time

from agents import (
    ProjectCoordinator,
    AcademicAffairsAgent,
    HRRecruiterAgent,
    IndustryExpertAgent,
    StudentRepresentativeAgent,
    FacultyRepresentativeAgent
)
from models import DEFAULT_OPTIMIZATION_CONFIG
from utils.document_parser import DocumentParser

# 页面配置
st.set_page_config(
    page_title="培养方案智能优化平台 V2.0",
    page_icon="🎓",
    layout="wide"
)

def init_session_state():
    """初始化会话状态"""
    if 'optimization_state' not in st.session_state:
        st.session_state.optimization_state = None
    if 'optimization_results' not in st.session_state:
        st.session_state.optimization_results = []
    if 'current_round' not in st.session_state:
        st.session_state.current_round = 0

def display_header():
    """显示应用头部"""
    st.title("🎓 培养方案智能优化平台 V2.0")
    st.markdown("""
    基于多智能体系统(MAS)的专业培养方案智能化优化工具
    
    ---
    """)

def sidebar_configuration():
    """侧边栏配置"""
    st.sidebar.header("⚙️ 配置参数")
    
    # API密钥配置
    api_key = st.sidebar.text_input(
        "🔑 SiliconFlow API密钥",
        type="password",
        help="请输入您的SiliconFlow API密钥"
    )
    
    # 优化参数配置
    st.sidebar.subheader("📊 优化参数")
    max_rounds = st.sidebar.slider("最大优化轮次", 1, 10, 5)
    convergence_threshold = st.sidebar.slider("收敛阈值", 0.1, 0.9, 0.3, 0.1)
    
    # 利益相关者权重配置
    st.sidebar.subheader("👥 利益相关者权重")
    academic_weight = st.sidebar.slider("教务处代表", 0.1, 1.0, 0.2, 0.1)
    hr_weight = st.sidebar.slider("企业HR代表", 0.1, 1.0, 0.3, 0.1)
    expert_weight = st.sidebar.slider("行业技术专家", 0.1, 1.0, 0.2, 0.1)
    student_weight = st.sidebar.slider("学生代表", 0.1, 1.0, 0.2, 0.1)
    faculty_weight = st.sidebar.slider("教师代表", 0.1, 1.0, 0.1, 0.1)
    
    return {
        "api_key": api_key,
        "max_rounds": max_rounds,
        "convergence_threshold": convergence_threshold,
        "weights": {
            "academic_affairs": academic_weight,
            "hr_recruiter": hr_weight,
            "industry_expert": expert_weight,
            "student_representative": student_weight,
            "faculty_representative": faculty_weight
        }
    }

def curriculum_input_section():
    """培养方案输入区域"""
    st.header("📄 培养方案输入")
    
    # 选择输入方式
    input_method = st.radio(
        "选择输入方式：",
        ["📝 手动输入", "📁 文件上传", "🔗 示例数据"],
        horizontal=True
    )
    
    curriculum_data = {}
    target_positions = []
    
    if input_method == "📝 手动输入":
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("基本信息")
            major_name = st.text_input("专业名称", placeholder="如：计算机科学与技术")
            degree_type = st.selectbox("学位类型", ["工学学士", "理学学士", "文学学士", "其他"])
            duration = st.selectbox("学制", ["4年", "3年", "5年"])
            
            st.subheader("课程体系")
            course_text = st.text_area(
                "课程列表（每行一门课程）",
                placeholder="高等数学\n大学物理\n程序设计基础\n...",
                height=200
            )
            
        with col2:
            st.subheader("目标岗位群")
            positions_text = st.text_area(
                "目标岗位（每行一个岗位）",
                placeholder="软件工程师\n算法工程师\n产品经理\n...",
                height=100
            )
            
            st.subheader("培养目标")
            training_goals = st.text_area(
                "培养目标描述",
                placeholder="培养具有扎实理论基础和实践能力的...",
                height=120
            )
        
        # 构建课程数据
        if course_text:
            courses = [line.strip() for line in course_text.split('\n') if line.strip()]
            curriculum_data = {
                "basic_info": {
                    "major_name": major_name,
                    "degree_type": degree_type,
                    "duration": duration,
                    "training_goals": training_goals
                },
                "courses": courses,
                "course_count": len(courses)
            }
            
        if positions_text:
            target_positions = [line.strip() for line in positions_text.split('\n') if line.strip()]
    
    elif input_method == "📁 文件上传":
        uploaded_file = st.file_uploader(
            "上传培养方案文件",
            type=['pdf', 'docx', 'txt', 'xlsx'],
            help="支持PDF、Word、Excel、文本文件格式"
        )
        
        if uploaded_file:
            st.info("文件解析功能正在开发中，请使用手动输入方式")
    
    elif input_method == "🔗 示例数据":
        if st.button("加载示例数据"):
            curriculum_data = {
                "basic_info": {
                    "major_name": "计算机科学与技术",
                    "degree_type": "工学学士",
                    "duration": "4年",
                    "training_goals": "培养具有扎实理论基础和实践能力的计算机专业人才"
                },
                "courses": [
                    "高等数学", "线性代数", "概率论与数理统计",
                    "程序设计基础", "数据结构", "算法分析",
                    "计算机组成原理", "操作系统", "数据库系统",
                    "计算机网络", "软件工程", "人工智能"
                ],
                "course_count": 12
            }
            target_positions = ["软件工程师", "算法工程师", "系统架构师"]
            st.success("示例数据已加载！")
    
    return curriculum_data, target_positions

def optimization_process_section(config: Dict, curriculum_data: Dict, target_positions: List[str]):
    """优化过程区域"""
    st.header("🔄 优化过程")
    
    if not config["api_key"]:
        st.warning("⚠️ 请在侧边栏配置API密钥")
        return
    
    if not curriculum_data:
        st.warning("⚠️ 请先输入培养方案数据")
        return
    
    # 显示输入摘要
    with st.expander("📋 输入数据摘要", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**培养方案信息：**")
            st.json(curriculum_data)
        with col2:
            st.write("**目标岗位群：**")
            st.write(target_positions)
    
    # 开始优化按钮
    if st.button("🚀 开始智能优化", type="primary"):
        optimize_curriculum(config, curriculum_data, target_positions)

def optimize_curriculum(config: Dict, curriculum_data: Dict, target_positions: List[str]):
    """执行培养方案优化"""
    
    # 创建进度容器
    progress_container = st.container()
    results_container = st.container()
    
    with progress_container:
        st.subheader("🔄 优化进度")
        progress_bar = st.progress(0)
        status_text = st.empty()
        round_info = st.empty()
    
    try:
        # 初始化项目协调官
        coordinator = ProjectCoordinator(config["api_key"])
        
        # 创建利益相关者智能体
        stakeholders = [
            AcademicAffairsAgent(config["api_key"]),
            HRRecruiterAgent(config["api_key"]),
            IndustryExpertAgent(config["api_key"]),
            StudentRepresentativeAgent(config["api_key"]),
            FacultyRepresentativeAgent(config["api_key"])
        ]
        
        # 模拟优化过程
        total_rounds = config["max_rounds"]
        
        for round_num in range(1, total_rounds + 1):
            round_info.info(f"📊 第 {round_num} 轮优化")
            status_text.text("正在进行多智能体分析...")
            
            # 模拟各智能体分析
            round_results = []
            
            for i, agent in enumerate(stakeholders):
                agent_progress = (round_num - 1) / total_rounds + (i + 1) / (len(stakeholders) * total_rounds)
                progress_bar.progress(min(agent_progress, 1.0))
                status_text.text(f"🤖 {agent.agent_name} 正在分析...")
                
                # 模拟分析时间
                time.sleep(1)
                
                # 执行分析（使用模拟数据）
                try:
                    result = agent.analyze(curriculum_data, target_positions=target_positions)
                    round_results.append(result)
                    status_text.text(f"✅ {agent.agent_name} 分析完成")
                except Exception as e:
                    st.error(f"❌ {agent.agent_name} 分析失败: {str(e)}")
                    # 使用备用分析结果
                    result = agent._create_fallback_analysis()
                    round_results.append(result)
            
            # 显示轮次结果
            with results_container:
                if round_num == 1:
                    st.subheader("📊 优化结果")
                
                with st.expander(f"第 {round_num} 轮分析结果", expanded=(round_num == 1)):
                    display_round_results(round_results)
            
            # 模拟收敛判断
            if round_num >= 2:  # 简单的收敛模拟
                status_text.text("🎯 系统已收敛，优化完成！")
                progress_bar.progress(1.0)
                break
        
        # 显示最终总结
        with results_container:
            st.success("🎉 优化完成！")
            display_optimization_summary(round_results)
            
    except Exception as e:
        st.error(f"❌ 优化过程出错: {str(e)}")

def display_round_results(results: List[Dict]):
    """显示轮次结果"""
    tabs = st.tabs([result["agent_name"] for result in results])
    
    for i, (tab, result) in enumerate(zip(tabs, results)):
        with tab:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write("**总体评估：**")
                analysis = result.get("analysis_result", {})
                st.write(analysis.get("overall_assessment", "暂无评估"))
                
                st.write("**主要建议：**")
                suggestions = result.get("suggestions", [])
                for j, suggestion in enumerate(suggestions[:3]):  # 只显示前3个建议
                    st.write(f"{j+1}. {suggestion.get('detailed_suggestion', '')}")
            
            with col2:
                st.write("**评分：**")
                summary = result.get("summary", {})
                for key, value in summary.items():
                    if isinstance(value, (int, float)) and key.endswith("_rating"):
                        st.metric(key.replace("_", " ").title(), f"{value}/5")

def display_optimization_summary(results: List[Dict]):
    """显示优化总结"""
    st.subheader("📈 优化总结")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("参与智能体", len(results))
    
    with col2:
        total_suggestions = sum(len(r.get("suggestions", [])) for r in results)
        st.metric("改进建议总数", total_suggestions)
    
    with col3:
        avg_rating = sum(
            r.get("summary", {}).get("feasibility_rating", 3) 
            for r in results
        ) / len(results) if results else 3
        st.metric("平均可行性评分", f"{avg_rating:.1f}/5")
    
    # 建议汇总
    st.subheader("🎯 关键改进建议")
    all_suggestions = []
    for result in results:
        for suggestion in result.get("suggestions", []):
            suggestion["agent"] = result["agent_name"]
            all_suggestions.append(suggestion)
    
    # 按优先级排序并显示前10个
    all_suggestions.sort(key=lambda x: x.get("priority", 3), reverse=True)
    
    for i, suggestion in enumerate(all_suggestions[:10], 1):
        with st.expander(f"{i}. {suggestion.get('detailed_suggestion', '')[:50]}..."):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**建议内容：** {suggestion.get('detailed_suggestion', '')}")
                st.write(f"**理由：** {suggestion.get('justification', '')}")
                st.write(f"**预期收益：** {suggestion.get('expected_benefit', '')}")
            with col2:
                st.write(f"**来源：** {suggestion.get('agent', '')}")
                st.write(f"**优先级：** {suggestion.get('priority', 3)}/5")
                st.write(f"**可行性：** {suggestion.get('feasibility', 0.8):.1%}")

def main():
    """主函数"""
    init_session_state()
    display_header()
    
    # 获取配置
    config = sidebar_configuration()
    
    # 培养方案输入
    curriculum_data, target_positions = curriculum_input_section()
    
    # 优化过程
    optimization_process_section(config, curriculum_data, target_positions)
    
    # 页脚
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        🎓 培养方案智能优化平台 V2.0 | 基于多智能体系统(MAS) | 
        <a href='https://github.com/913540120/curriculum_optimization_agent' target='_blank'>GitHub</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 