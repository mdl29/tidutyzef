    var webSocket = false;
    var ws = new wsLib();
    var username;
    
    function qs(s){
        return document.querySelector(s);
    }
    
    function setStatut (s){
        qs("#status").innerHTML=s;
    }
    
    function addMessage(from, msg){
        qs("#msg").innerHTML=qs("#msg").innerHTML+"<br>"+from+" say : "+msg;
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
                        username: qs('#pseudo').value}
        sendToServ(data);
    }

    function sendMsg (){
        var data = {object: "msg",
                        msg: qs('#sendMsg').value};
        sendToServ(data);
    }   
    function setPos(){
        var data = {object: "updatePos",
                        lat: qs('#lat').value,
                        lng: qs('#lng').value};
        sendToServ(data);

    }

