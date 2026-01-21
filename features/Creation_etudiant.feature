Feature: Creation de compte Campus France

Scenario: Creation d un compte Etudiant
  Given je suis sur la page de creation de compte
  When je saisi les informations utilisateur
  Then le bouton creer affiche un message "votre compte est cree"
