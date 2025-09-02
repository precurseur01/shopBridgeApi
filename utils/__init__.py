# Réexporte toutes les fonctions utiles d'auth_utils
from .auth_utils import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    oauth2_scheme  # si tu veux l’utiliser ailleurs
)
