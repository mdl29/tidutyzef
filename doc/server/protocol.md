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
    "pos": (48.370652522533, -4.5949385672784),
    "status" : "playing"
}
```

# Réception des positions des autres joueurs

Serveur --> Client 
Le serveur va également transmettre la position des autres joueurs, par exemple si titi de l'équipe tidu est à la position [48.40618, -4.46730] ([lat, longitude]), le serveur va vous envoyer le message suivant :

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
L'admin défini la localisation de la map ainsi que les zones sur cette map avec les positions latitudes et longitudes ainsi que le rayon des zones en mètres ensuite geré par leaflet directement ainsi que le temps du timer.

```json
{
    "object": "setParams",
    "map": {"lat":48.408365900017856,"lng":-4.480619430541992},
    "zone":[ { id=0, pos=[], radius="10", type="tidu"}, { id=1, pos=[], radius="10", type="tizef"}, { id=2, pos=[], radius="10", type="neutre"}],
    "time":600
}
```

#Récupération des données defini par l'administrateur(non uttilisé)

Serveur --> client  
Les joueurs doivent pouvoir, normalement, récupérer les options que l'administrateur a envoyé.Pour cela, l'objet getParams est là. les paramètres à récupérer sont transmis dans un tableau par le champ params.
Les paramètres peuvent être map pour récupérer le centre de la carte, zones pour récupérer les zones ou rayon pour connaitre le rayon d'action des zones et des joueurs.

```json
{
    "object": "getParams",
    "params": ["map","zones","rayon","timer"]
}
```

#Début de la partie

Serveur --> client
Les joueurs recuperent le signal de lancement de partie ansi que les différents paramétres.

```json
{
    'object': 'startGame',
    'map': [48.408365900017856, -4.480619430541992],
    "zones": [{'team': 'tidu', 'id': 0, 'pos': [48.408807461106136, -4.480319023132324],'time2chgTeam': {'tizef': 10, 'tidu': 10}},{'team': 'tizef', 'id': 1, 'pos': [48.40333753077148, -4.492807388305664],'time2chgTeam': {'tizef': 10, 'tidu': 10}},{'team': 'neutre', 'id': 2, 'pos': [48.40949116103341, -4.479374885559082],'time2chgTeam': {'tizef': 10, 'tidu': 10}}, {'team': 'neutre', 'id': 3, 'pos': [48.40949116103341, -4.479374885559082], 'time2chgTeam': {'tizef': 10, 'tidu': 10}}], 'time': 60000, 'radius': 10
} 

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

#Fin d'une battle

Serveur-->Client
```json
{
    'object': 'battle',
    'winner': 'tata'
}
```
```json
{
    'object':"endBattle"
}
```

#Fin du jeu

Serveur-->Client

{
    'object': 'endGame',
    'cause': ''
}
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

