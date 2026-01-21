class Etudiant:
    def __init__(
        self,
        email,
        motDePasse,
        confirmationMotDePasse,
        civilite,
        nom,
        prenom,
        paysResidence,
        paysNationalite,
        codePostal,
        ville,
        telephone,
        profil,
        domaineActivite,
        niveauEtude
    ):
        self.email = email
        self.motDePasse = motDePasse
        self.confirmationMotDePasse = confirmationMotDePasse
        self.civilite = civilite
        self.nom = nom
        self.prenom = prenom
        self.paysResidence = paysResidence
        self.paysNationalite = paysNationalite
        self.codePostal = codePostal
        self.ville = ville
        self.telephone = telephone
        self.profil = profil
        self.domaineActivite = domaineActivite
        self.niveauEtude = niveauEtude
