function ScreenCombat(){
		this.section = qs("#screen_combat");
		this.battle=function(against){
		
			qs('#pseudo').innerHTML=against;
			
		}
}
ScreenCombat.prototype= new Screen;
