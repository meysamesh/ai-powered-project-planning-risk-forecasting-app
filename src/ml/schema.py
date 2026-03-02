from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


MODEL_FEATURE_COLUMNS = [
    "Task_Duration_Days",
    "Labor_Required",
    "Equipment_Units",
    "Material_Cost_USD",
    "Start_Constraint",
    "Resource_Constraint_Score",
    "Site_Constraint_Score",
    "Dependency_Count",
]

FEATURE_EDITOR_COLUMNS = [
    "Task_ID",
    *MODEL_FEATURE_COLUMNS,
]


class TaskRiskFeatures(BaseModel):
    Task_ID: str = Field(..., min_length=2)
    Task_Duration_Days: float = Field(..., ge=1.0)
    Labor_Required: int = Field(..., ge=0)
    Equipment_Units: int = Field(..., ge=0)
    Material_Cost_USD: float = Field(..., ge=0.0)
    Start_Constraint: float = Field(..., ge=0.0)
    Resource_Constraint_Score: float = Field(..., ge=0.0, le=1.0)
    Site_Constraint_Score: float = Field(..., ge=0.0, le=1.0)
    Dependency_Count: int = Field(..., ge=0)

    @field_validator("Task_ID")
    @classmethod
    def clean_task_id(cls, value: str) -> str:
        text = value.strip()
        if not text:
            raise ValueError("Task_ID cannot be empty.")
        return text
