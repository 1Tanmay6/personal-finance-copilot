from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_date = Column(String, nullable=False)  # 'YYYY-MM-DD'
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)  # positive=credit, negative=debit
    type = Column(String, nullable=False)  # 'CREDIT' or 'DEBIT'
    closing_balance = Column(Float, nullable=True)
    account = Column(String, nullable=True)
    ref_no = Column(String, nullable=True)
    category = Column(String, nullable=True)  # filled by agent
    source = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class Goal(Base):
    __tablename__ = "goals"

    goal_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    goal_type = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    target_date = Column(String, nullable=True)  # 'YYYY-MM-DD'
    monthly_target = Column(Float, nullable=True)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    suggestions = relationship("Suggestion", back_populates="goal")
    


class UserSetting(Base):
    __tablename__ = "user_settings"

    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    goal_id = Column(Integer, ForeignKey("goals.goal_id"), nullable=True)
    suggestion_type = Column(String, nullable=False)
    content = Column(String, nullable=False)
    reason = Column(String, nullable=True)
    impact_description = Column(String, nullable=True)
    impact_numeric = Column(Float, nullable=True)
    priority = Column(Integer, default=0)
    status = Column(String, default="active")
    created_at = Column(DateTime, server_default=func.now())
    implemented_at = Column(DateTime, nullable=True)

    goal = relationship("Goal", back_populates="suggestions")
    