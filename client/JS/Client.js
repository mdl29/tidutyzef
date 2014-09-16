 function Client()
{
    var webSocket = false;
    var ws = new wsLib();
	var that=this;
    
    this.onMessage = function(rep){
		console.log(rep.object);
        switch (rep.object){
            case "error":
                that.onError(rep);
                break;
            case "newUser":
                this.send({"object":"getAllUsers"});
				break;
			case "startGame":
				switch_screen.show( screen_map );
				screen_map.showMap(rep.map);
				screen_map.startCountDown(rep.time);
				screen_map.setZone(rep.zones);
				console.log(rep.zones);
				
				break;
			case "usersConnected":
				if(rep.hasOwnProperty("tidu")){
					screen_wait.newTidu(rep.tidu);
				}
				if(rep.hasOwnProperty("tizef")){
					screen_wait.newTizef(rep.tizef);
				}
				break;
			case "updatePos":
				screen_map.moveMarkers(rep.pos,rep.from,rep.team,rep.status);
				break;
			case "startBattle":
				switch_screen.show( screen_combat);
				screen_combat.battle(rep.against);
				break;
			case "battle":
				console.log('Result');
				screen_combat.showResult(rep.winner);
				break;
			case "endBattle":
				console.log('fin de la battle');
				break
			case "endGame":
				switch(rep.cause){
					case "tiduWin":
						screen_map.winner("tidu");
						break;
					case "tizefWin":
						screen_map.winner("tizef");
						break;
					case "noEnoughPlayer":
						alert("Il n'y a pas assez de joueurs \n veuillez resoudre le probleme ou contacter l'administrateur");
						switch_screen.show(screen_connection);
						that.onClose();
						break;
				}
				break;
		}
    };
    this._onmessage = function(e){ 
        var rep = JSON.parse(e.data);
        console.log(rep);
        that.onMessage(rep);
    };

    this.onError = function(e){
		if(e.errorCode==2){
			switch_screen.show( screen_connection );
			alert(e.desc);
		}
		this.onClose();
    };
    
    this.onClose = function(){
        var data = {object :"logout"};
        this.send(data);
        webSocket = false;
    };
    
    this.openConnection = function (ip){
        if(!webSocket){
            ws.openSocket(ip,
                this.onConnection,
                this.onClose,
                this._onmessage,
                this.onError );
        }
    };
    
    this.onConnection = function(){
        webSocket = true;
        screen_connection.connectSuccess();
    }

    this.send = function (data){
        if(webSocket && ! ws.isClosed()){
            ws.msg(data);
        }
        else{
            ws.close();
        }
    };
    
}

client = new Client();
