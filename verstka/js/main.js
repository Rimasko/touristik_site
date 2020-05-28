/* Set the width of the side navigation to 250px */
function openNav() {
  if(document.getElementById("mySidenav").style.width == "0px") {
    console.log("WDD");
    document.getElementById("mySidenav").style.width = "250px";
  }
  else {
    closeNav();
  }
}

/* Set the width of the side navigation to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

$('.dropdown-toggle').dropdown()