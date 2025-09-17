from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import json

# Crée les tables dans la base de données si elles n'existent pas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clarté API")

# Configuration CORS pour autoriser le frontend à communiquer avec le backend
origins = [
    "http://localhost:5173", # Adresse par défaut de SvelteKit en dev
    "http://localhost:3000", # Autre adresse commune
    "*",                     # Le symbole "*" autorise toutes les origines (tous les sites web)

]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    """Au démarrage, vérifie si la DB est vide. Si oui, la peuple avec les données initiales."""
    db = SessionLocal()
    if not db.query(models.Rank).first():
        print("Base de données vide, peuplement avec les données initiales...")
        with open('initial_data.json', 'r', encoding='utf-8') as f:
            initial_data = json.load(f)
        matrix_to_save = schemas.MatrixDataToSave(**initial_data)
        crud.save_matrix_data(db, matrix_to_save)
        print("Peuplement terminé.")
    db.close()


@app.get("/api/matrix", response_model=schemas.MatrixData)
def read_matrix_data(db: Session = Depends(get_db)):
    """Endpoint pour récupérer l'ensemble des données de la matrice."""
    matrix_data = crud.get_matrix_data(db)
    return matrix_data

@app.post("/api/matrix")
def update_matrix_data(matrix_data: schemas.MatrixDataToSave, db: Session = Depends(get_db)):
    """Endpoint pour sauvegarder l'ensemble des données de la matrice."""
    # Ici, nous ajouterons la logique d'authentification pour les managers
    try:
        crud.save_matrix_data(db, matrix_data)
        return {"message": "Matrice mise à jour avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))