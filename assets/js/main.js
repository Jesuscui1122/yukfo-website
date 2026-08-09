function toggleMenu(){
  document.querySelector('.nav').classList.toggle('open');
}
document.addEventListener('click', function(e){
  var nav = document.querySelector('.nav');
  if(nav && !nav.contains(e.target) && !e.target.closest('.menu-toggle')) nav.classList.remove('open');
});
