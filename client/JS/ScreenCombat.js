function ScreenCombat(){
		this.section = qs("#screen_combat");

		this.battle=function(against){
			qs('#pseudo').innerHTML=against;
		}

		this.choice =function(choice){
			var data ={"object":"choice",
						'choice':choice
			};
			client.send(data);
		}

		this.showResult = function(win){
			$("#pour-centrage").hide();
			console.log(player.name);
            if(win=="any"){
                alert("pas de gagnant, veuillez rejouer");
            }
			if(win==player.name){
				qs('#result').innerHTML="Vous avez gagné";
				setTimeout(function(){switch_screen.show(screen_map)},1);
			}
			else{
				qs('#result').innerHTML="Vous avez perdu";
				setTimeout(function(){switch_screen.show(screen_map)},1);
			}
		}
}
ScreenCombat.prototype= new Screen;
