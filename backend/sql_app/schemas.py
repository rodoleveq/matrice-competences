from pydantic import BaseModel
from typing import List

# Schémas pour la lecture des données, afin de les reconstruire
class Value(BaseModel):
    content: str
    
class Item(BaseModel):
    type: str
    values: List[str]

class Pillar(BaseModel):
    name: str
    colorClasses: dict
    items: List[Item]

class MatrixData(BaseModel):
    ranks: List[str]
    pillars: List[Pillar]

# Schéma pour la sauvegarde (écriture des données)
class MatrixDataToSave(MatrixData):
    pass