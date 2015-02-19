function Admin (){
	this.zonesTable=[];
	var that=this;
	
	this.defZone=function(){
		var index=0;

		map.on('click', function(e) {
			that.zonesTable.push(zone.zoneCreate(index,[e.latlng.lat,e.latlng.lng],qs("#radius").value,qs('#team').value));
			console.log(that.zonesTable);

		switch(that.zonesTable[index].team){
		case 'tidu':
			L.circle(that.zonesTable[index].pos,that.zonesTable[index].radius,{color:'red'}).addTo(map);
			break;
		case 'tizef':
			L.circle(that.zonesTable[index].pos,that.zonesTable[index].radius).setStyle({color:'blue'}).addTo(map);
			break;
		case 'neutre':
			L.circle(that.zonesTable[index].pos,that.zonesTable[index].radius).setStyle({color:'grey'}).addTo(map);
			break;
		}
		index++;
		});
	};
	this.time=function(){
		var time =qs("#timer").value;
		time = time*60;
		return time;
	}
	this.startGame=function(){
		this.send({"object":"startGame"});
	};
	this.open=function (){
		console.log(qs('#ip').value);
		this.openConnection(qs('#ip').value, function(){ console.log("Admin connected"); } );
	};
	this.sendParams=function(){
		var data={
			 "object": "setParams",
			 "map": map.getCenter(),
			 "zones":that.zonesTable,
			 "time":this.time()
		};
		this.send(data);
	}
}
Admin.prototype = new Client();

admin=new Admin();
