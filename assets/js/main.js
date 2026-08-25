function toggleMenu(){
  document.querySelector('.nav').classList.toggle('open');
}
document.addEventListener('click', function(e){
  var nav = document.querySelector('.nav');
  if(nav && !nav.contains(e.target) && !e.target.closest('.menu-toggle')) nav.classList.remove('open');
});

/* lightbox for Work page */
document.addEventListener('click', function(e){
  var card = e.target.closest('.case-card[data-img]');
  if(!card) return;
  var box = document.getElementById('lightbox');
  if(!box){
    box = document.createElement('div');
    box.id = 'lightbox';
    box.className = 'lightbox';
    box.innerHTML = '<img alt=""><button class="lb-close" aria-label="Close">&times;</button>';
    document.body.appendChild(box);
    box.addEventListener('click', function(){ box.classList.remove('open'); });
    box.querySelector('.lb-close').addEventListener('click', function(){ box.classList.remove('open'); });
  }
  box.querySelector('img').src = card.getAttribute('data-img');
  box.querySelector('img').alt = card.querySelector('img').alt;
  box.classList.add('open');
});
document.addEventListener('keydown', function(e){
  if(e.key === 'Escape'){ var box = document.getElementById('lightbox'); if(box) box.classList.remove('open'); }
});
