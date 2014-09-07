function ScreenMap(){
		this.section = qs("#screen_map");
		
		var that =this;
		
		this.markers={};
		
		var tidu = L.icon({
			iconUrl: 'img/marqueur_tidu.png',
			iconSize: [50,50],
			iconAnchor:[25,0]
		});
		var tizef = L.icon({
			iconUrl: 'img/marqueur_tizef.png',
			iconSize: [50,50],
			iconAnchor:[25,0]
		});
		
		var icons=[tidu,tizef];
		
		this.open = function(){
				Screen.prototype.open.call(this);
				this.getLocation();
					
			}
		this.showMap=function(center){
				var map = L.map('map').setView(center, 13);

				// add an OpenStreetMap tile layer
				L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
					attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
				}).addTo(map);
			};
			
		this.getLocation =function (){ 
			if(navigator.geolocation){
				navigator.geolocation.watchPosition(this.showPosition);
			}
		};
		
		this.showPosition = function (position){ 
			lat=position.coords.latitude;
			lon=position.coords.longitude;
			that.updatePos(lat,lon);
		};
		
		this.updatePos=function(lat,lon){
			
			var data ={'object':"updatePos",
				'lat':lat,
				'lng':lon
			};
			client.send(data);
			
		};
		
		this.moveMarkers=function(pos,user,team){
			console.log(pos+"  "+user+"   "+team);
			if(!this.markers.hasOwnProperty(team)){
				this.markers[team]={};
			}
			if(!this.markers.hasOwnProperty(user)){
				this.markers[team][username] = L.marker(pos).setIcon(icons[team]).addTo(map).bindPopup(username);
			}
			else{	
				this.markers[team][user].setLatLng(pos);
			}
			
		}
}
ScreenMap.prototype = new Screen;
