function ScreenMap(){
		this.section = qs("#screen_map");
		
		this.open = function(){
				Screen.prototype.open.call(this);
				var map = L.map('map').setView([51.505, -0.09], 13);

				// add an OpenStreetMap tile layer
				L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
					attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
				}).addTo(map);	
			}
}
ScreenMap.prototype = new Screen;
