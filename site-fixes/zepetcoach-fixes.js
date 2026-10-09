/* Script de secours pour le menu mobile (Services / Blog).
   À ajouter via WPCode : type "JavaScript", emplacement "Pied de page du site".
   IMPORTANT : l'exclure du "Delay JS" / "Defer JS" de l'extension de cache. */
(function () {
  function isOpen(li) {
    var sub = li.querySelector(':scope > .sub-menu');
    return sub && getComputedStyle(sub).display !== 'none';
  }

  document.addEventListener('click', function (e) {
    var link = e.target.closest('.elementor-nav-menu--dropdown .menu-item-has-children > a');
    if (!link) return;
    var li = link.parentElement;
    var wasOpen = isOpen(li);
    // Laisse Elementor agir d'abord ; s'il n'a rien ouvert, on le fait.
    setTimeout(function () {
      if (isOpen(li) !== wasOpen) return;
      if (!wasOpen) {
        li.parentElement.querySelectorAll(':scope > .zpc-open').forEach(function (o) {
          if (o !== li) o.classList.remove('zpc-open');
        });
      }
      li.classList.toggle('zpc-open', !wasOpen);
      link.setAttribute('aria-expanded', String(!wasOpen));
    }, 80);
    e.preventDefault();
  }, true);
})();
