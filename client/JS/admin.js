function Admin (){
	
	this.zonesTable=[];
	var that=this;
	this.defZone=function(){
					var index=0;
					
					map.on('click', function(e) {
						that.zonesTable.push(new Zone(index,[e.latlng.lat,e.latlng.lng],qs("#radius").value,qs('#team').value));
						console.log(that.zonesTable);
						index++;
					});
				};
	this.times=function(){
		var time =qs("#timer").value;
		var times =[time-1,60];
		return times;
	}
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
	this.sendParams=function(){
		var data={
			 "object": "setParams",
			 "map": map.getCenter(),
			 "zones":that.zonesTable,
			 "time":this.times()
		};
		this.send(data);
	}
}
Admin.prototype = new Client();

admin=new Admin();
