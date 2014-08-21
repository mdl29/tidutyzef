    var webSocket = false;
    var ws = new wsLib();
    var username;
    var markers={};
    
    function qs(s){
        return document.querySelector(s);
    }
    
    function setStatut (s){
        qs("#status").innerHTML=s;
    }
    
    function addMessage(from, msg){
        qs("#msg").innerHTML=qs("#msg").innerHTML+"<br>"+from+" say : "+msg;
    }
    function getLocation(){
	
		
		if(navigator.geolocation){
		navigator.geolocation.watchPosition(showPosition);
		}
		
		
	}
	
	function showPosition(position){
	
		lat=position.coords.latitude;
		lon=position.coords.longitude;
		setPos(lat,lon);
		
	}
	function moveMarker(pos,username,team){
	
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
	
    function onMessage (e){   
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
                setStatut("Connecté");
                username = rep.user;
                getLocation();
                sendToServ({object: "getParams",params:["map","zones","radius"]});
                break;
            case "updatePos":
                if( rep.hasOwnProperty ("pos") && rep.hasOwnProperty("from")){
					moveMarker(rep.pos,rep.from,rep.team);
				}
				break
			case "params":
				console.log("params");
				map.setView(rep.map,18, {animation: true});
				//addZone(rep.zones1,rep.zones2,rep.zones3,rep.zones4,rep.radius);
				console.log("params recu"+rep.map);
				break;
            case "logout":
                setStatut("Déconnecté");
                break;
        }

    }
    
    function onError (e){
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
    
    function openConnection (){
        if(!webSocket){
            ws.openSocket(qs('#ws_url').value,
                connectionOpened,
                onClose,
                onMessage,
                onError );
        }
    }
    
    function connectionOpened (){
        webSocket = true;
        setStatut('Veuillez entrer votre pseudo');
    }
    
    function sendToServ (data){
        if(webSocket && ! ws.isClosed()){
            ws.msg(data);
        } 
        else{
            ws.close();
        }
    
    }
    
    function login (){
        var data = {object: "login",
                        username: qs('#pseudo').value,
                        team:qs('#team').value}
        sendToServ(data);
    }

    function sendMsg (){
        var data = {object: "msg",
                        msg: qs('#sendMsg').value};
        sendToServ(data);
    }   
    function setPos(lat,lon){
        var data = {object: "updatePos",
                        lat: lat,
                        lng: lon};
        sendToServ(data);

    }


