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
		
		this.icons={"tidu":this.tidu,"tizef":this.tizef};
		
		this.open = function(){
				Screen.prototype.open.call(this);
				this.getLocation();
					
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
			

			if(!this.markers.hasOwnProperty(team)){
				this.markers[team]={};
			}
			if(!this.markers.hasOwnProperty(user)){
				this.markers[team][username] = L.marker(pos,{icon: this.icons[team]}).addTo(this.map).bindPopup(user +" de la team " + team);
			}
			else{	
				this.markers[team][user].setLatLng(pos);
			}
			
		}
}
ScreenMap.prototype = new Screen;
