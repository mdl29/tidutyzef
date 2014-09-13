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
		this.marker = L.icon({
			iconUrl:'img/marqueur_mort.png',
			iconSize:[34,64],
			inconAnchor:[25,0]
		});
		
		this.icons={'none':{"tidu":this.marker,"tizef":this.marker},'playing':{"tidu":this.tidu,"tizef":this.tizef},"2":{"tidu":this.marker,"tizef":this.marker}};
		
		this.open = function(){
				Screen.prototype.open.call(this);
				//this.getLocation();
					
			}
		this.showMap=function(center){
				this.map = L.map('map').setView(center, 13);

				// add an OpenStreetMap tile layer
				L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
					attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
				}).addTo(this.map);
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
				this.markers[team][username] = L.marker(pos,{icon: this.icons[status][team]}).addTo(this.map).bindPopup(user +" de la team " + team);
			}
			else{	
				this.markers[team][user].setLatLng(pos).setIcon( this.icons[status][team]);
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
		}
		
		this.setZone=function(zones){
		
			for(var i=0;i<zones.length;i++){
			
				switch(zones[i].team){
					case 'tidu':
						L.circle(zones[i].pos,zones[i].radius).setStyle('color':'red').addTo(map);
						break;
					case 'tizef':
						L.circle(zones[i].pos,zones[i].radius).setStyle('color':'blue').addTo(map);
						break;
					case 'neutre':
						L.circle(zones[i].pos,zones[i].radius).setStyle('color':'grey').addTo(map);
						break
					
				}
			}
			
		}
}
ScreenMap.prototype = new Screen;
