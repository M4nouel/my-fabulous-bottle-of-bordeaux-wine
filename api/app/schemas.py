from typing import List
from pydantic import BaseModel


class Wine(BaseModel):
    id: int
    name: str
    millesime: int

    class Config:
        orm_mode = True


class Wines(BaseModel):
    totalCount: int
    wines: List[Wine]

    class Config:
        orm_mode = True

class SearchedWines(Wines):
    paramLikeName: str
    paramLikeMillesime: str
    skip: int
    count: int

    class Config:
        orm_mode = True


class Attribute(BaseModel):
    id: int
    tastes: List

    class Config:
        orm_mode = True

