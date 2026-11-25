(function(){
 var $=function(s,c){return(c||document).querySelector(s)},$$=function(s,c){return[].slice.call((c||document).querySelectorAll(s))};
 var b=$('.menu'),n=$('#nav');
 function set(o){if(!n)return;n.classList.toggle('open',o);b.setAttribute('aria-expanded',o);b.querySelector('span').textContent=o?'Close':'Menu';document.body.classList.toggle('menu-open',o)}
 if(b&&n){b.addEventListener('click',function(){set(!n.classList.contains('open'))});n.addEventListener('click',function(e){if(e.target.closest('a'))set(false)});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&n.classList.contains('open')){set(false);b.focus()}});
  matchMedia('(min-width:961px)').addEventListener('change',function(m){if(m.matches)set(false)})}
 var p=$('#prog');if(p)addEventListener('scroll',function(){var h=document.documentElement;p.style.width=(h.scrollTop/Math.max(1,h.scrollHeight-h.clientHeight)*100)+'%'},{passive:true});
 var tabs=$$('[role=tab]');
 function show(id,scroll){var t=tabs.filter(function(x){return x.getAttribute('aria-controls')===id})[0];if(!t)return false;
  tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;$('#'+x.getAttribute('aria-controls')).hidden=!on});
  if(scroll){var ix=$('#intelligence');if(ix)ix.scrollIntoView()}return true}
 if(tabs.length){tabs.forEach(function(t){t.addEventListener('click',function(){show(t.getAttribute('aria-controls'))});
  t.addEventListener('keydown',function(e){var i=tabs.indexOf(t),k=e.key;if(k==='ArrowRight'||k==='ArrowDown')i=(i+1)%tabs.length;else if(k==='ArrowLeft'||k==='ArrowUp')i=(i+tabs.length-1)%tabs.length;else if(k==='Home')i=0;else if(k==='End')i=tabs.length-1;else return;e.preventDefault();tabs[i].focus();show(tabs[i].getAttribute('aria-controls'))})});
  show('sector-explorer');var h=function(){var id=location.hash.slice(1);if(id)show(id,true)};addEventListener('hashchange',h);h();}
  $$('.seg button').forEach(function(x){x.addEventListener('click',function(){$$('.seg button').forEach(function(y){y.setAttribute('aria-pressed',y===x)});$$('.sector').forEach(function(s){s.hidden=s.id!==x.getAttribute('aria-controls')})})});
 var q=$('#q'),L=$('#latest');
 if(q&&L){var orig=L.innerHTML,data=null,esc=function(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML};
  var run=function(){var t=q.value.trim().toLowerCase();if(!t){L.innerHTML=orig;return}var r=data.filter(function(x){return(x.t+' '+x.s+' '+x.c).toLowerCase().indexOf(t)>-1}).slice(0,25);
   L.innerHTML=r.length?'<div class="rows">'+r.map(function(x){return'<a class="row" href="'+x.u+'"><span class="rd">'+esc(x.d)+'</span><span class="rt"><strong>'+esc(x.t)+'</strong><small>'+esc(x.s)+'</small></span><span class="rc">'+esc(x.c)+'</span></a>'}).join('')+'</div>':'<p class="empty">No matches.</p>'};
  q.addEventListener('input',function(){if(data)return run();fetch('/search.json').then(function(r){return r.json()}).then(function(j){data=j;run()}).catch(function(){})})}
})();
