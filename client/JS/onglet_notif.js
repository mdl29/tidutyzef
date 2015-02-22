var show = 0;
var showWid = 1;

function notifShow(){
  $('#alerte-notif').css('display','none');
  $('.barre_onglet').css('animation-timing-function','ease-out');
  $('.barre_onglet').css('animation-name','animation_barre-show');
  $('#zone-notif').css('transition-timing-function','ease-out');
  $('#zone-notif').css('height','75px');
  
}

function notifHide(){
  $('.barre_onglet').css('animation-timing-function','ease-in');
  $('.barre_onglet').css('animation-name','animation_barre-hide');
  $('#zone-notif').css('transition-timing-function','ease-in');
  $('#zone-notif').css('height','0px');
}

function check(){
  if (show == 0){
    show = 1;
    notifShow();
  }
  else {
    show = 0;
    notifHide();
  }
}

function widgetsShow(){
  $('#widgets').css('top','35px');  
}

function widgetsHide(){
  $('#widgets').css('top','-70px');
}

function checkWid(){
  if (showWid == 0){
    showWid = 1;
    widgetsShow();
  }
  else {
    showWid = 0;
    widgetsHide();
  }
}