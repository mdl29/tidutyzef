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
}
ScreenCombat.prototype= new Screen;
