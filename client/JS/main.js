	var switch_screen = new SwitchScreen();
	var screen_wait= new ScreenWait();
	var screen_connection= new ScreenConnection();
	var screen_map= new ScreenMap();
	var screen_combat= new ScreenCombat();
	var player= new ClientJoueur();
	
	screen_combat.close();
	screen_map.close();
	screen_wait.close();
	screen_connection.close();
	
	switch_screen.show( screen_connection );
	
	window.onbeforeunload = function(){
		client.close();
		return false;
	};
	
	$("#formulaire_connexion").onclick(function(){
			screen_connection.startCo();
	});
	
	$("#formulaire_modIP").onclick(function(){
			screen_connection.modifIP();
	});
	
	$("#gps").onclick(function(){
			screen_map.gpsCenter();
	});
	
	$("#pierre").onclick(function(){
			screen_combat.choice('pierre');
	});
	
	$("#papier").onclick(function(){
			screen_combat.choice('papier');
	});
	
	$("#ciseaux").onclick(function(){
			screen_combat.choice('ciseaux');
	});
