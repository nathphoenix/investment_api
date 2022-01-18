from typing import Dict, List, Union
from datetime import datetime

from db import db

# ItemJSON = Dict[str, Union[int, str, float]]


class InvestmentModel(db.Model):
    __tablename__ = "investment"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200), nullable=True, unique=False)
    email = db.Column(db.String(80), nullable=True, unique=False)
    username = db.Column(db.String(80), nullable=True, unique=False)
    amount = db.Column(db.Float(precision=2),  nullable=True)
    creator = db.Column(db.String(80), nullable=True, unique=False)
    status = db.Column(db.String(80), nullable=True, unique=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @classmethod
    def find_by_date(cls, created_at: datetime) -> "InvestmentModel":
        return cls.query.filter_by(created_at=created_at).first()
    
    
    @classmethod
    def find_all_name(cls, username: str) -> "InvestmentModel":
        return cls.query.filter_by(username=username)
      
    @classmethod
    def find_all_email(cls, email: str) -> "InvestmentModel":
        return cls.query.filter_by(username=email)

    @classmethod
    def find_by_name(cls, username: str) -> "InvestmentModel":
        return cls.query.filter_by(username=username).first()
      
    @classmethod
    def find_by_email(cls, email: str) -> "InvestmentModel":
        return cls.query.filter_by(username=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "InvestmentModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["InvestmentModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
