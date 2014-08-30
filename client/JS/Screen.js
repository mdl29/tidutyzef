function Screen( sec ){
		this.section = sec;
		this.open = function(){
			this.section.style.display = "block";
		};
		this.close = function(){
			this.section.style.display = "none";
		};
}
