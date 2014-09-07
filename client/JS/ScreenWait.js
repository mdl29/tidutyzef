function ScreenWait(){
		this.section = qs("#screen_wait");
		this.newUser = function (username,team){
			if(team=="tidu"){
				$('#players-tidu').append(username+"<br>");
				console.log(username);
			}
			else if(team=="tizef"){
				$('#players-tizef').append(username+'<br>');
			}
			else if(team=='admin'){
				console.log('admin connected');
			}
		};
}
ScreenWait.prototype = new Screen;
