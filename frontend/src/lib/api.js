// L'adresse de base de notre API. On pourra la changer facilement pour la production.
const BASE_URL = 'http://127.0.0.1:8000';

/**
 * Récupère les données complètes de la matrice depuis le backend.
 * @returns {Promise<object>} Les données de la matrice (ranks, pillars).
 */
export async function getMatrixData() {
    const response = await fetch(`${BASE_URL}/api/matrix`);
    if (!response.ok) {
        throw new Error('Failed to fetch matrix data');
    }
    return await response.json();
}

/**
 * Envoie les données mises à jour de la matrice au backend pour sauvegarde.
 * @param {object} matrixData - L'objet complet de la matrice.
 * @returns {Promise<object>} La réponse du serveur.
 */
export async function saveMatrixData(matrixData) {
    // CORRECTION ICI : `${BASE_URL}` au lieu de `${BASE-URL}`
    const response = await fetch(`${BASE_URL}/api/matrix`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(matrixData),
    });
    if (!response.ok) {
        throw new Error('Failed to save matrix data');
    }
    return await response.json();
}