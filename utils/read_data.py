import os
import json
from models.etudiant import Etudiant

class ReadData:

    def read_data_from_json(self):
        # Chemin relatif au projet, peu importe où il est cloné
        base_dir = os.path.dirname(os.path.dirname(__file__))  # remonte de utils/ à la racine du repo
        filename = os.path.join(base_dir, "data", "etudiant.json")

        # Vérifier que le fichier existe
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Le fichier {filename} est introuvable !")

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        return Etudiant(
            email=data["email"],
            motDePasse=data["motDePasse"],
            confirmationMotDePasse=data["confirmationMotDePasse"],
            civilite=data["civilite"],
            nom=data["nom"],
            prenom=data["prenom"],
            paysResidence=data["paysResidence"],
            paysNationalite=data["paysNationalite"],
            codePostal=data["codePostal"],
            ville=data["ville"],
            telephone=data["telephone"],
            profil=data["profil"],
            domaineActivite=data["domaineActivite"],
            niveauEtude=data["niveauEtude"]
        )
