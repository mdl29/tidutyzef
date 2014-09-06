function Admin (){
	this.defZone=function(){
					var index=0;
					map.on('click', function(e) {
						zones.push(new zone(index,[e.latlng.lat,e.latlng.lng],qs("#radius").value,qs('#team').value));
						L.circle([e.latlng.lat,e.latlng.lng],qs("#radius").value).addTo(map);
						console.log(zones);
						index++;
					});
				};
	this.startGame=function(){
		this.send({"object":"startGame"});
	};
	this.open=function (){
		var data ={
						"object": "login",
						"username": "admin",
						"team": "admin"
						};
		console.log(qs('#ip').value);
		this.openConnection(qs('#ip').value);
		this.send(data);
	};
}
Admin.prototype = new Client();

admin=new Admin();
