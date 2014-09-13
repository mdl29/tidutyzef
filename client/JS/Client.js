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
                screen_wait.newUser(rep.username,rep.team);
				break;
			case "startGame":
				console.log('startGame');
				switch_screen.show( screen_map );
				screen_map.showMap(rep.mapCenter);
				screen_map.startCountDown(rep.time);
				screen_map.setZone(rep.zones);
				break;
			case "updatePos":
				screen_map.moveMarkers(rep.pos,rep.from,rep.team,rep.status);
				break;
			case "startBattle":
				switch_screen.show( screen_combat);
				console.log(rep.against);
				screen_combat.battle(rep.against);
				break;
			case "battle":
				console.log(rep);
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
		this.close();
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
