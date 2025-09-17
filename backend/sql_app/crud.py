from sqlalchemy.orm import Session
from . import models, schemas

def get_matrix_data(db: Session) -> schemas.MatrixData:
    """Récupère et formate toutes les données de la matrice depuis la DB."""
    ranks_db = db.query(models.Rank).order_by(models.Rank.position).all()
    pillars_db = db.query(models.Pillar).order_by(models.Pillar.position).all()

    ranks = [rank.name for rank in ranks_db]
    pillars = []
    
    for pillar_db in pillars_db:
        items = []
        for item_db in sorted(pillar_db.items, key=lambda i: i.id):
            values_db = sorted(item_db.values, key=lambda v: v.rank.position)
            values = [val.content for val in values_db]
            items.append(schemas.Item(type=item_db.type, values=values))
        
        # MODIFICATION ICI : Reconstruire le dictionnaire complet de couleurs
        pillars.append(schemas.Pillar(
            name=pillar_db.name,
            colorClasses={
                "bg": pillar_db.color_bg, 
                "text": pillar_db.color_text,
                "accent": pillar_db.color_accent,
                "icon": pillar_db.color_icon,
                "border": pillar_db.color_border
            },
            items=items
        ))
        
    return schemas.MatrixData(ranks=ranks, pillars=pillars)

def save_matrix_data(db: Session, matrix_data: schemas.MatrixDataToSave):
    """Écrase toutes les données de la matrice avec les nouvelles données fournies."""
    db.query(models.Value).delete()
    db.query(models.Item).delete()
    db.query(models.Pillar).delete()
    db.query(models.Rank).delete()
    
    rank_models = []
    for i, rank_name in enumerate(matrix_data.ranks):
        rank = models.Rank(name=rank_name, position=i)
        db.add(rank)
        rank_models.append(rank)
    db.commit()

    for i, pillar_data in enumerate(matrix_data.pillars):
        # MODIFICATION ICI : Sauvegarder toutes les valeurs de couleur
        pillar_model = models.Pillar(
            name=pillar_data.name,
            position=i,
            color_bg=pillar_data.colorClasses.get("bg", ""),
            color_text=pillar_data.colorClasses.get("text", ""),
            color_accent=pillar_data.colorClasses.get("accent", ""),
            color_icon=pillar_data.colorClasses.get("icon", ""),
            color_border=pillar_data.colorClasses.get("border", "")
        )
        db.add(pillar_model)
        
        for item_data in pillar_data.items:
            item_model = models.Item(type=item_data.type, pillar=pillar_model)
            db.add(item_model)
            
            for j, value_content in enumerate(item_data.values):
                if j < len(rank_models): # Safety check
                    value_model = models.Value(
                        content=value_content,
                        item=item_model,
                        rank=rank_models[j]
                    )
                    db.add(value_model)
    
    db.commit()
    return {"status": "success"}
