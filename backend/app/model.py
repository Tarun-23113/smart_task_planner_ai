from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    goal = Column(String(255), nullable=False)

    tasks = relationship("TaskModel", back_populates="plan", cascade="all, delete-orphan")


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_code = Column(String(10), nullable=False)  # T1, T2 ...
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    depends_on = Column(String(255), nullable=True)
    estimated_days = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(50), default="Not Started")

    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    plan = relationship("Plan", back_populates="tasks")
