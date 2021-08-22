from sqlalchemy.orm import Session

from . import crud


def kneighbors_of_wine_by_id(db: Session, KNN, wine_id: int, limit: int = 100):
    attributes = crud.get_attribute_by_id(db, wine_id)

    raw_nneighbhors = KNN.kneighbors(attributes.tastes)
    nneighbhors = [int(id) for id in raw_nneighbhors[1][0][:limit]]

    res = crud.get_wines_by_ids(db, nneighbhors)

    # Preserve distance ordering
    return [wine for id in nneighbhors for wine in res if wine.id == id]
