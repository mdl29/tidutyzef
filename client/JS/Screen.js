function Screen( sec ){
		this.section = sec;
        this.load = function(file,id){
            $('body').append('<section id =' + id + '>'); 
            $('#' + id).load(file).hide();
        }
		this.open = function(){
			this.section.style.display = "block";
		};
		this.close = function(){
			this.section.style.display = "none";
		};
}
