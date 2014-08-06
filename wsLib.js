var wsLib = new function(){
    var that = this;
    var onopen = null;
    var onmessage = null;
    var onclose = null;
	this.openSocket = function(serveur,onOpen,onClose,onMessage){
        this.onopen=onOpen;
        this.onmessage=onMessage;
        this.onclose=onClose;
        console.log(serveur);
		this.ws = new WebSocket(serveur, "protocolOne");
        
		this.ws.onopen = function(e){
			console.log("WebSocket opened, event :");
			console.log(e);
            that.onopen();
		};
        
		window.onbeforeunload = function(){
            that.close();
            return false;
		};
        
		this.ws.onmessage = onMessage;
	};

    this.msg = function(data){
        var data = JSON.stringify(data);
        console.log("send data : "+data);
        this.ws.send(data);
    };
    this.close = function(){
        this.onclose();
        this.ws.close();
    };
}();
	
	