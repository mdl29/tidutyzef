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
   *[Debut d'un combat](#Debut-d'une-battle)
   *[Choix lors d'un combat](#Choix-lors-d'une-battle)
   

* Administration
    * [Envoi des données defini par l'administrateur](#envoi-des-données-defini-par-ladministrateur)
    * [Récupération des données defini par l'administrateur](#récupération-des-données-defini-par-ladministrateur)
* Codes d'erreur :
    * [ 0 ](#erreur-0)
    * [ 1 ](#erreur-1)
    * [ 2 ](#erreur-2)
    * [ 3 ](#erreur-3)
    * [ 4 ](#erreur-4)
    * [ 5 ](#erreur-5)

And more will come XD

# Connexion

Client --> Serveur
Pour se connecter en tant que toto avec l'équipe tidu, envoier le message suivant :

```json
{
    "object": "login",
    "username": "toto",
    "team": "tidu"
}
```

#Notification de connection d'un nouvel utilisateur

Serveur --> Client
Utiliser sur l'ecran d'attente pour voir la connection des joueurs

```json
{
    "object": "newUser",
    "user": "toto",
    "team":"tidu"
}
```

# Déconnexion

Client --> Serveur 
Pour se déconnecter, envoyer le message :

```json
{
    "object": "logout"
}
```

# Envoi de sa position

Client --> Serveur
Pour transmettre sa position GPS, par exemple [48.40618, -4.46730], envoyer le message :

```json
{
    "object": "updatePos",
    "lat": 48.40618,
    "lng":  -4.46730,
    "status" : "playing"
}
```

# Réception des positions des autres joueurs

Serveur --> Client 
Le serveur va également transmettre la position des autres joueurs, par exemple si titi de l'équipe tidu est à le position [48.40618, -4.46730] ([lat, longitude]), le serveur va vous envoyer le message suivant :

```json
{
    "object": "updatePos",
    "from": "titi",
    "team":  "tidu",
    "pos": [48.40618, -4.46730]
}
```
#Envoi des données defini par l'administrateur

Admin --> Serveur
L'admin defini la localisation de la map ainsi que les zones sur cette map avec les positions latitudes et longitudes ainsi que le le rayon des zones en metres ensuite gerer par leaflet directement.

```json
{
    "object": "setParams",
    "map": [48.40618, -4.46730],
    "zone":[ { id=0, pos=[2], radius="20", type="tidu"}, { id=1, pos=[2], radius="10", type="tizef"}, { id=2, pos=[2], radius="10", type="neutre"}]
}
```
#Récupération des données defini par l'administrateur

Serveur --> client  
Les joueurs doivent pouvoir, normalement, récupérer les options que l'administrateur a envoyé.Pour cela, l'objet getParams est là. les paramètres à récupérer sont transmis dans un tableau par le champ params.
Les paramètres peuvent être map pour récupérer le centre de la carte, zones pour récupérer les zones ou rayon pour connaitre le rayon d'action des zones et des joueurs.

```json
{
    "object": "getParams",
    "params": ["map","zones","rayon","timer"]
}
```
#notification Start Régéneration.

Serveur --> Client  
```json
{
	"objet": "StartRégéne"
}
```
#notification End Régéneration.

Serveur --> Client  
```json
{
	"objet": "EndRégéne"
}
```

#notification capture d'une zonne.

Serveur --> Client  
```json
{
	"objet": "startCapture",
	"team": "tidu",
	"user": "toto",
	"index": "5"
}
```

#fin de capture de la zonne.

Serveur --> Client
```json
{
	"object":"enCapture"
	"team":"tyzef"
	"user":"tot"
	"index":"3"
}
```
#Debut d'une battle

Server --> Client

```json
{
	"object":"startBattle"
	"against":"toto"
}
```

#Choix lors d'une battle

Client --> Serveur

```json
{
	"object":"choice"
	"choice":"papier"
}
```

# Erreur 0

Serveur --> Client
*usernameNotSet* -> un username doit etre transmis ainsi que la team

# Erreur 1

Serveur --> Client
*teamError* -> la team spécifié n'existe pas

# Erreur 2

Serveur --> Client
*usernameAlreadyUse* -> l'username est déjà utilisé par un autre joueur dans la team demandée

# Erreur 3 

Serveur --> Client
*JSONError* -> le Json n'a pas pu être correctement lu (il faut peut être renvoyer le dernier message

# Erreur 4

Serveur --> Client
*unknowObject* -> l'objet spécifié dans je JSON ne correspond à aucun objet pouvant être traité

#Erreur 5

Serveur --> Client
*usernameAlreadySet* -> le client ne peut pas demander à changer son username ou son équipe en cours de partie

