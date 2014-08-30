function ScreenWait(){
		this.section = qs("#screen_wait");
		this.newUser = function (username,team){
			console.log(username+"  "+team);
			if(team=="tidu"){
				$('#tiduUser').append(username+"<br>");
				console.log(username);
			}
			else if(team=="tizef"){
				$('#tizefUser').append(username+'<br>');
			}
		};
}
ScreenWait.prototype = new Screen;
