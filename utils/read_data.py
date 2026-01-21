import json
from models.etudiant import Etudiant

class ReadData:

    def read_data_from_json(self):
        filename = "C:\\Users\\User\\Desktop\\Campus_Python\\data\\etudiant.json"

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
