from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import cast, Column
from sqlalchemy.sql.sqltypes import String

from . import models


def get_ten_wines(db: Session):
    return db.query(models.Wines).limit(10).all()

def get_wine_by_id(db: Session, wine_id: int):
    return db.query(models.Wines).filter(models.Wines.id == wine_id).first()

def get_wines_by_ids(db: Session,
                    wine_ids: List[int],
                    skip: int = 0,
                    limit: int = 100):
    return (db.query(models.Wines)
            .filter(models.Wines.id.in_(wine_ids))
            .offset(skip)
            .limit(limit)
            .all())

def get_wine_by_name_and_millesime(db: Session, name: str, millesime: str):
    return (db.query(models.Wines)
            .filter(models.Wines.name == name, models.Wines.millesime == millesime)
            .first())

def get_wines_like_name_and_millesime(db: Session,
                                    name: str,
                                    millesime: str,
                                    skip: int = 0,
                                    limit: int = 10):
    totalCount = (db.query(models.Wines)
                .filter(
                    models.Wines.name.ilike("%" + name + "%"),
                    cast(models.Wines.millesime, String).ilike("%" + millesime + "%"))
                .count())
    wines = (db.query(models.Wines)
            .filter(
                models.Wines.name.ilike("%" + name + "%"),
                cast(models.Wines.millesime, String).ilike("%" + millesime + "%"))
            .offset(skip)
            .limit(limit)
            .all())

    return {'paramLikeName': name,
            'paramLikeMillesime': millesime,
            'skip': skip,
            'count': len(wines),
            'totalCount': totalCount,
            'wines': wines}


def get_attribute_by_id(db: Session, attribute_id: int):
    return db.query(models.Attributes).filter(models.Attributes.id == attribute_id).first()

def get_attribute_by_name_and_millesime(db: Session, name: str, millesime: str):
    return (db.query(models.Attributes)
            .filter(models.Wines.name == name, models.Wines.millesime == millesime)
            .first())



# def get_wines_by_id(db: Session, wine_ids: List[int], skip: int = 0, limit: int = 100):
#     return db.query(models.Wines).filter(models.Wines.id.in_(wine_ids)).offset(skip).limit(limit).all()

