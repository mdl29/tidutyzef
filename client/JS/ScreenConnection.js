function ScreenConnection(){
		this.section = qs("#screen_connection");
		qs('#modifIP').style.display = "none";
		this.modifIP=function(){
			qs('#modifIP').style.display = "block";
		}
		this.connectSuccess=function(){
			
			var user = qs("#username").value;
			var team = $("input[type='radio'][name='team']:checked").val();
			
			var player = new ClientJoueur();
			player.user = user;
			player.team = team;
			
			var client = new Client();
			
			var data ={
						"object": "login",
						"username": user,
						"team": team
						};
			client.send(data);
		}
}
ScreenConnection.prototype = new Screen();
