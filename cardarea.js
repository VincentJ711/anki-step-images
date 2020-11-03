var imgClsname = 'stepImagesImg';
var urlsAttr = 'urls';
var descriptionsAttr = 'descriptions';
var posAttr = 'pos';

if (window.gg) {
  window.removeEventListener('keyup', window.gg.glistener);
}

window.gg = {};

window.gg.onPrevClick = function(evt) {
  window.gg.step(evt.target.parentElement.nextElementSibling, -1);
}

window.gg.onNextClick = function(evt) {
  window.gg.step(evt.target.parentElement.nextElementSibling, 1);
}

window.gg.onKeyup = function(evt) {
  evt.stopPropagation();
  if (evt.key === '[') {
    window.gg.step(evt.target.parentElement.nextElementSibling, -1)
  } else if (evt.key === ']') {
    window.gg.step(evt.target.parentElement.nextElementSibling, 1)
  }
}

window.gg.glistener = function(evt) {
  const elts = document.getElementsByClassName(imgClsname);
  const elt = elts[0];

  if (elts.length !== 1) {
    return;
  } else if (evt.key === '[') {
    window.gg.step(elt, -1);
  } else if (evt.key === ']') {
    window.gg.step(elt, 1);
  }
}

window.gg.step = function(imgElt, delta) {
  const urls = imgElt.getAttribute(urlsAttr).split(';');
  const descs = imgElt.getAttribute(descriptionsAttr).split(';').map(atob)
  const pos = Number(imgElt.getAttribute(posAttr));
  var nextPos = Number(imgElt.getAttribute(posAttr)) + delta;

  if (nextPos == urls.length) {
    nextPos = 0;
  } else if (nextPos == -1) {
    nextPos = urls.length - 1;
  }

  imgElt.setAttribute(posAttr, nextPos + '');
  imgElt.setAttribute('src', urls[nextPos]);
  imgElt.previousElementSibling.firstElementChild.innerHTML =
      nextPos + 1 + ' / ' + urls.length;
  imgElt.nextElementSibling.innerHTML = descs[nextPos];
}

window.addEventListener('keyup', window.gg.glistener);