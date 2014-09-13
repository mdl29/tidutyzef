function ScreenWait(){
		this.section = qs("#screen_wait");
		this.newTidu = function (tidu){
			qs('#players-tidu').innerHTML="";
			console.log(tidu);
			for(var i=0;i<tidu.length;i++){
				$( "#players-tidu" ).append(tidu[i]+"<br>");
			}			
		};
		this.newTizef = function(tizef){
			qs('#players-tizef').innerHTML="";
			console.log(tizef);
			for(var i=0;i<tizef.length;i++){
				$( "#players-tizef" ).append(tizef[i]+"<br>");
			}
		};
}
ScreenWait.prototype = new Screen;
