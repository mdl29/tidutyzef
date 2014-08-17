# Protocol du jeu

Ce document décrit le protocol de communication utilisé pour le jeu.

Les requêtes et réponses sont au format JSON.

---

* Authentification :
   * [ Connexion ](#-connexion) 
   * [ Déconnexion ](#-déconnexion)
* Positionnement des joueurs :
   * [Envoi de sa position](#-envoi-de-sa-position)
   * [Réception des positions des autres joueurs](#-réception-des-positions-des-autres-joueurs)
* Gestion des zones :

TODO

* Gestion des combats :

TODO

* Codes d'erreur :

TODO

# Connexion

Pour se connecter en tant que toto avec l'équipe tidu, envoier le message suivant :

```json
{
    "object": "login",
    "username": "toto",
    "team": "tidu"
}
```

# Déconnexion
Pour se déconnecter, envoyer le message :

```json
{
    "object": "logout"
}
```

# Envoi de sa position
Pour transmettre sa position GPS, par exemple [48.40618, -4.46730], envoyer le message :

```json
{
    "object": "updatePos",
    "lat": 48.40618,
    "lng":  -4.46730 
}
```

# Réception des positions des autres joueurs
Le serveur va également transmettre la position des autres joueurs, par exemple si titi de l'équipe tidu est à le position [48.40618, -4.46730] ([lat, longitude]), le serveur va vous envoyer le message suivant :

```json
{
    "object": "updatePos",
    "from": "titi",
    "team":  tidu,
    "pos": [48.40618, -4.46730]
}
```
