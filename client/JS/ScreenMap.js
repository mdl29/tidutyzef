function ScreenMap(){
		this.section = qs("#screen_map");
		
		this.open = function(){
				Screen.prototype.open.call(this);
					
			}
		this.showMap=function(center){
				var map = L.map('map').setView(center, 13);

				// add an OpenStreetMap tile layer
				L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
					attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
				}).addTo(map);
			};
}
ScreenMap.prototype = new Screen;
