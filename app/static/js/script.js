//Side navigation menu
function openNav() {
  document.getElementById("mySidenav").style.width = "60%";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}
const menuToggle = document.getElementById("menuToggle");
const navMenu = document.getElementById("navMenu");

menuToggle.addEventListener("click", () => {
  navMenu.classList.toggle("active");
});
