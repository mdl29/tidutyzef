# Protocol du jeu

Ce document décrit le protocol de communication utilisé pour le jeu.

Les requêtes et réponses sont au format JSON.

---

* Authentification :
   * [ Connexion ](#connexion) 
   * [ Déconnexion ](#déconnexion)
* Positionnement des joueurs :
   * [Envoi de sa position](#envoi-de-sa-position)
   * [Réception des positions des autres joueurs](#réception-des-positions-des-autres-joueurs)
* Gestion des zones :

TODO

* Gestion des combats :

TODO

* [Envoi des données defini par l'administrateur](#envoi-des-données-defini-par-l-administrateur)

* Codes d'erreur :
    * [ 0 ](#erreur-0)
    * [ 1 ](#erreur-1)
    * [ 2 ](#erreur-2)
    * [ 3 ](#erreur-3)
    * [ 4 ](#erreur-4)
    * [ 5 ](#erreur-5)

And more will come XD

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
#Envoi des données defini par l'administrateur
L'admin defini la localisation de la map ainsi que les zones sur cette map avec les positions latitudes et longitudes ainsi que le le rayon des zones en metres ensuite gerer par leaflet directement.

```json
{
    "object": "setParams",
    "map": [48.40618, -4.46730],
    "zone1":  [48.40618, -4.4670],
    "zone2": [48.4068, -4.46730],
    "zone3":[48.4061, -4.4670],
    "rayon" :10
}
```

# Erreur 0
*usernameNotSet* -> un username doit etre transmis ainsi que la team

# Erreur 1
*teamError* -> la team spécifié n'existe pas

# Erreur 2
*usernameAlreadyUse* -> l'username est déjà utilisé par un autre joueur dans la team demandée

# Erreur 3 
*JSONError* -> le Json n'a pas pu être correctement lu (il faut peut être renvoyer le dernier message

# Erreur 4
*unknowObject* -> l'objet spécifié dans je JSON ne correspond à aucun objet pouvant être traité

#Erreur 5
*usernameAlreadySet* -> le client ne peut pas demander à changer son username ou son équipe en cours de partie
