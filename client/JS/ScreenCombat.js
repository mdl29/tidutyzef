function ScreenCombat(){
		this.section = qs("#screen_combat");

		var selection = false;
		var enemy;

		this.battle=function(against){
			enemy=against;
			selection=false;
			qs('#pseudo').innerHTML=enemy;
		}

		this.choice =function(choice){
			if(selection == false){
				var data ={"object":"choice",
							'choice':choice
				};
				client.send(data);
				console.log(data);
				$("#pour-centrage").hide();
				qs('#choice').innerHTML="Vous avez choisi "+choice;
				selection=true;
			}
		}

		this.showResult = function(win){
			console.log(win);
            if(win=="any"){
                alert("pas de gagnant, veuillez rejouer");
                switch_screen.show( screen_combat);
                this.battle(enemy);
                $("#pour-centrage").show();
                qs('#choice').innerHTML="Veuillez reselectionner quelque chose";
            }
			else if(win==player.user){
				qs('#result').innerHTML="Vous avez gagné";
				setTimeout(function(){switch_screen.show(screen_map)},9000);
				screen_map.notif(win+" a gagné contre "+enemy);
			}
			else{
				qs('#result').innerHTML="Vous avez perdu";
				setTimeout(function(){switch_screen.show(screen_map)},9000);
				screen_map.notif(enemy+" a perdu contre "+win);
			}
		}
}
ScreenCombat.prototype= new Screen;
