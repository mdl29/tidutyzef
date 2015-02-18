var show = 0;

function notifShow(){
  $('#zone-notif').css('height','75px');
  $('#label').css('bottom','78px');
  $('.barre_onglet').css('bottom','75px');
}

function notifHide(){
  $('#zone-notif').css('height','0px');
  $('#label').css('bottom','3px');
  $('.barre_onglet').css('bottom','0px');
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
