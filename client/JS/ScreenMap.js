function ScreenMap(){
		this.section = qs("#screen_map");
		
		var that =this;
		this.map;
		
		this.markers={};
		
		this.tidu = L.icon({
			iconUrl: 'img/marqueur_tidu.png',
			iconSize: [34,64],
			iconAnchor:[25,0]
		});
		this.tizef = L.icon({
			iconUrl: 'img/marqueur_tizef.png',
			iconSize: [34,64],
			iconAnchor:[25,0]
		});
		this.tizefMort = L.icon({
			iconUrl: 'img/marqueur_tizef_mort.png',
			iconSize: [34,64],
			iconAnchor:[25,0]
		});
		this.tiduMort = L.icon({
			iconUrl: 'img/marqueur_tizef_mort.png',
			iconSize: [34,64],
			iconAnchor:[25,0]
		});
		this.marker = L.icon({
			iconUrl:'img/marqueur_mort.png',
			iconSize:[34,64],
			inconAnchor:[25,0]
		});
		
		this.icons={'playing':{"tidu":this.tidu,"tizef":this.tizef},
					"none":{"tidu":this.marker,"tizef":this.marker},
					"fighting":{"tidu":this.tidu,"tizef":this.tizef},
					"kill":{"tidu":this.tiduMort,"tizef":this.tizefMort}};
		
		this.open = function(){
				Screen.prototype.open.call(this);
				//this.getLocation();
					
			}
		this.showMap=function(center){
				this.map = L.map('map').setView([0,0], 18);

				// add an OpenStreetMap tile layer
				L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
					attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
				}).addTo(this.map);
				this.map.setView(center,18);
			};
			
		this.getLocation =function (){ 
			if(navigator.geolocation){
				navigator.geolocation.watchPosition(that.showPosition);
			}
		};
		
		this.showPosition = function (position){ 
			lat=position.coords.latitude;
			lon=position.coords.longitude;
			that.updatePos(lat,lon);
			player.pos=[lat,lon];
		};
		
		this.updatePos=function(lat,lon){
			
			var data ={'object':"updatePos",
				'lat':lat,
				'lng':lon
			};
			client.send(data);
			
		};
		
		this.moveMarkers=function(pos,user,team, status){
			
			if(!this.markers.hasOwnProperty(team)){
				this.markers[team]={};
			}
			if(!this.markers.hasOwnProperty(user)){
				this.markers[team][user] = L.marker(pos,{icon: this.icons[status][team]}).addTo(this.map).bindPopup(user +" de la team " + team);
			}
			else{	
				this.markers[team][user].setIcon( this.icons[status][team]).setLatLng(pos);
			}
			
		};
		
		this.gpsCenter =function(){
			
			this.map.setView(player.pos);
			
		};
		
		this.startCountDown=function(time){
		
			var min=time[0],sec=time[1];
			setInterval(function(){
				sec--;
				if(sec==0){
					min--;
					sec=60;
				}
				qs('#time').innerHTML=min+":"+sec;
				},1000);
		};
		
		this.setZone=function(zones){
		console.log('new');
		for(var i=0;i<zones.length;i++){
			var zone =JSON.stringify(zones[i]);
			console.log(zone);
			var zoneObj=JSON.parse(zone);
			console.log(zoneObj);
			that.zoneStyle(zoneObj);
		}
		
		};
		this.zoneStyle=function(zone){
			console.log(zone);
			
			switch(zone.type){
					case 'tidu':
					console.log('newTiduZone');
						L.circle(zone.pos,zone.radius).setStyle({'color':'red'}).addTo(map);
						break;
					case 'tizef':
					console.log('newtizefZone');
						L.circle(zone.pos,zone.radius).setStyle({'color':'blue'}).addTo(map);
						break;
					case 'neutre':
					console.log('newNEutreZone');
						L.circle(zone.pos,zone.radius).setStyle({'color':'grey'}).addTo(map);
						break
					default :
						console.log("newZone");
						L.circle(zone.pos,zone.radius).addTo(map);
			}
		};
		
		this.notif=function(cause){
			qs('#notif').innerHTML=cause;
		};
		this.winner=function(team){
			
			if(team==player.team){
				alert("Les "+player.team+" ont gagnés :D");
				var r=confirm("Rejouer");
				if(r==true){
					location.reload(true);
					client.onClose();
				}
				else if(r==false){
					alert("Veuiller vous deconnecter");	
				}
			}
			if (team!=player.team){
				alert("Les "+player.team+" ont perdus :'(");
				var r=confirm("Rejouer");
				if(r==true){
					location.reload(true);
					client.onClose();
				}
				else if(r==false){
					alert("Veuiller vous deconnecter");	
				}
			}
		};
}
ScreenMap.prototype = new Screen;
