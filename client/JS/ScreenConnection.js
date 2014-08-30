function ScreenConnection(){
		this.section = qs("#screen_connection");
		qs('#modifIP').style.display = "none";
		this.modifIP=function(){
			qs('#modifIP').style.display = "block";
		}
}
ScreenConnection.prototype = new Screen;
