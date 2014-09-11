function ScreenConnection(){
		this.section = qs("#screen_connection");
		qs('#modifIP').style.display = "none";
		this.modifIP=function(){
			qs('#modifIP').style.display = "block";
		};
		this.connectSuccess=function(){
			
			var user = $("#username").val();
			var team = $("input[type='radio'][name='team']:checked").val();
			
			if(user != null){

				player.user = user;
				player.team = team;
				
				
				var data ={
							"object": "login",
							"username": user,
							"team": team
							};
				client.send(data);
				
				screen_map.getLocation();
				switch_screen.show( screen_wait );
				
			}
			else{
				alert("Pseudo invalid")
			}
		};
		this.startCo=function(){
			client.openConnection(qs("#IP").value);
		};
}
ScreenConnection.prototype = new Screen();
