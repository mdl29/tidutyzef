    var webSocket = false;
    var ws = new wsLib();
    var username;
    var markers={};
    
    function qs(s){
        return document.querySelector(s);
    }
    function setStatut (s){ //function permettant de définir le status
        qs("#status").innerHTML=s;
    }
    function addMessage(from, msg){ //function permettant d'envoyer un message
        qs("#msg").innerHTML=qs("#msg").innerHTML+"<br>"+from+" say : "+msg;
    }
    function getLocation(){ //function pour recupere la position
	
		
		if(navigator.geolocation){
		navigator.geolocation.watchPosition(showPosition);
		}
		
		
	}
	function showPosition(position){ //function permettant de montrer la position
	
		lat=position.coords.latitude;
		lon=position.coords.longitude;
		setPos(lat,lon);
		
	}
	function moveMarker(pos,username,team){ //function permettant de deplacer le marqueur
	
		if(!markers.hasOwnProperty(team)){  
			markers[team]={};
		}
		if(!markers.hasOwnProperty(username)){
		 markers[team][username] = L.marker(pos).setIcon(icons[team]).addTo(map).bindPopup(username);
		}
		else{	
			markers[team][username].setLatLng(pos);
		}
	}
    function onMessage (e){  //des qu'il y a un message
        rep = JSON.parse(e.data);
        console.log( rep );
        switch (rep.object){
            case "error":
                onError(rep);
                break;
            case "msg":
                if( rep.hasOwnProperty ("msg") && rep.hasOwnProperty("from")){
                    addMessage(rep.from, rep.msg);
                }
                break;
            case "login":
                setStatut("Connecté"); //définir le status en connecté
                username = rep.user;
                getLocation();
                sendToServ({object: "getParams",params:["map","zones","radius"]});
                break;
            case "updatePos":
                if( rep.hasOwnProperty ("pos") && rep.hasOwnProperty("from")){
					moveMarker(rep.pos,rep.from,rep.team);
					findOther(markers);
				}
				break
			case "params":
				if(rep.map==0){
					alert("Veuillez vous reconnecter plus tard: jeu non configuré")
					onClose();
				}else if(rep.map!=0){
					console.log("partie configurée");
					map.setView(rep.map,18, {animation: true});
					var zones=[rep.zones0,rep.zones1,rep.zones2,rep.zones3];
					modZone(zones);
				}
				break;
            case "logout":
                setStatut("Déconnecté");
                break;
        }

    }
    function onError (e){ //des qu'il y'a une erreur 
        switch(e.errorCode){
            case 0:
                alert("Pb de pseudo"); //crée un message 
                break;
            default:
                if (e.desc != ""){
                    alert(e.desc);
                }
                else{
                    alert("Erreur indéfinie");
                }
        }
    }
    function onClose(){ 	//des que la page est quittée		
        var data = {object :"logout"}; //déconnecte le joueur
        ws.msg(data);
        webSocket = false;
        setStatut("Déconnecté");   //définit le status en déconnecté
    }
    function openConnection (){ 
        if(!webSocket){
            ws.openSocket(qs('#ws_url').value,
                connectionOpened,
                onClose,
                onMessage,
                onError );
        }
    }
    function connectionOpened (){ //des que la connection est crée
        webSocket = true;
        setStatut('Veuillez entrer votre pseudo'); //demande de pseudo
    }
    function sendToServ (data){ //function permettant d'envoyer des donnés au serveur
        if(webSocket && ! ws.isClosed()){
            ws.msg(data);
        } 
        else{
            ws.close();
        }
    }
    function login (){	//fonction qui permet de se connecté
        var data = {object: "login",
                        username: qs('#pseudo').value,
                        team:qs('#team').value}
        sendToServ(data);
    }
    function sendMsg (){ //fonction pour envoyer un message
        var data = {object: "msg",
                        msg: qs('#sendMsg').value};
        sendToServ(data);
    }   
    function setPos(lat,lon){ //function qui permet définir la position 
        var data = {object: "updatePos",
                        lat: lat,
                        lng: lon};
        sendToServ(data);
    }
    function modZone(zones,radius){ //fonction qui permet ajouter des zones
		for(i=0;i<zones.length;i++){
			switch(zones[i].type){
				case "tidu":
					L.circle(zones[i].pos,zones[i].rad,{
							color: 'red'
					}).addTo(map);
					break
				case "tizef":
					L.circle(zones[i].pos,zones[i].rad,{
							color: 'blue'
					}).addTo(map);
					break
				case "neutre":
					L.circle(zones[i].pos,zones[i].rad,{
							color: '#ffffff'
					}).addTo(map);
					break
				case "regen":
					L.circle(zones[i].pos,zones[i].rad,{
							color: 'green'
					}).addTo(map);
					break
			}		
		}
	}
	function findOther(marker){
		console.log("function executeed");
		for(var row in marker){
		console.log(marker[row].id);
			for(var raw in marker[row]){
			console.log(marker[row][raw].id);
			}
		}
	}
