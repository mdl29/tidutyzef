    var webSocket = false;
    var ws = new wsLib();
    var username;
    var markers={};
    var zone=["","","",""];
    
    function qs(s){
        return document.querySelector(s);
    }
    
    function setStatut (s){ //défini le statut
        qs("#status").innerHTML=s;
    }
    
    function addMessage(from, msg){ //ajoute un message (auteur, message)
        qs("#msg").innerHTML=qs("#msg").innerHTML+"<br>"+from+" say : "+msg;
    }
    
	function moveMarker(pos,username,team){ //déplace le marqueur
	
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
    function onMessage (e){   //des qu'il y a un message 
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
                setStatut("Connecté"); //définit le statut en Connecté
                username = rep.user;
                break;
            case "updatePos":
                if( rep.hasOwnProperty ("pos") && rep.hasOwnProperty("from")){
				moveMarker(rep.pos,rep.from,rep.team);
				}
            case "logout":
                setStatut("Déconnecté"); //définit le statut en Décconnecté
                break;
        }

    }
    
    function onError (e){ //des qu'il y a une erreur
        switch(e.errorCode){
            case 0:
                alert("Pb de pseudo");
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
    
    function onClose(){
        var data = {object :"logout"};
        ws.msg(data);
        webSocket = false;
        setStatut("Déconnecté");
    }
    
    function openConnection (){ //function pour ouvrir la connection
        if(!webSocket){
            ws.openSocket(qs('#ws_url').value,
                connectionOpened,
                onClose,
                onMessage,
                onError );
        }
    }
    
    function connectionOpened (){//function des que la connection est ouverte
        webSocket = true;
        setStatut('Veuillez entrer votre pseudo'); //demande de définir un pseudo
        login ();
    }
    
    function sendToServ (data){ //fonction pour envoyer des donné au serveur 
        if(webSocket && ! ws.isClosed()){
            ws.msg(data);
        } 
        else{
            ws.close();
        }
    
    }
    
    function login (){ //fonction pour se connecté
        var data = {object: "login",
                        username: "admin",
                        team:"admin"}
        sendToServ(data);
    }

    function sendMsg (){
        var data = {object: "msg",
                        msg: qs('#sendMsg').value};
        sendToServ(data);
    }   
    
    //INDEV
    function defZone(i){ //definit la/les zones
		var coord=["","","",""];
		
			map.on('click', function(e) {
				if(coord[i]== ""&&zone[i]==""){
					coord[i]=[[e.latlng.lat,e.latlng.lng],qs("#team").value];
					zone[i]=coord[i];
					console.log("zone "+i+" défini a "+coord[i] +"ou"+zone[i]);
				}
				else if(coord[i]!=""&&zone[i]!=""){
					console.log("zone"+i+" already defined to" + coord[i]);
				}
			});
		
		
	}
    
    //^^^INDEV^^^
    function selectParameters(){ //fonction pour définir les parametres 
	
		var center= map.getCenter();
		var coord=[center.lat,center.lng];
		console.log(coord);
		var rayon=qs('#zoneRayon').value;
		
		var data = {object:"setParams",
						map: coord,
						zone1:zone[0],
						zone2:zone[1],
						zone3:zone[2],
						zoneRegen:zone[3],
						rayon:rayon};
		console.log(data);
		sendToServ(data);
	}

