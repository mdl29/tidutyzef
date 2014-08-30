function SwitchScreen(){
    this.screenOpen = null;
    this.show = function( screentoOpen ){
        if( this.screenOpen !== null ){
            this.screenOpen.close();
        }
        screentoOpen.open();
        this.screenOpen = screentoOpen;
    };
}