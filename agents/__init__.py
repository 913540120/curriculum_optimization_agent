"""
培养方案智能优化平台 V2.0 - 智能体包

包含所有利益相关者智能体和协调机制
"""

from .base_agent import BaseAgent
from .project_coordinator import ProjectCoordinator
from .curriculum_analyst import CurriculumAnalyst
from .academic_affairs_agent import AcademicAffairsAgent
from .hr_recruiter_agent import HRRecruiterAgent
from .industry_expert_agent import IndustryExpertAgent
from .student_representative_agent import StudentRepresentativeAgent
from .faculty_representative_agent import FacultyRepresentativeAgent
from .conflict_mediator_agent import ConflictMediatorAgent
from .curriculum_optimizer_agent import CurriculumOptimizerAgent

__all__ = [
    "BaseAgent",
    "ProjectCoordinator",
    "CurriculumAnalyst",
    "AcademicAffairsAgent",
    "HRRecruiterAgent",
    "IndustryExpertAgent",
    "StudentRepresentativeAgent",
    "FacultyRepresentativeAgent", 
    "ConflictMediatorAgent",
    "CurriculumOptimizerAgent"
] 