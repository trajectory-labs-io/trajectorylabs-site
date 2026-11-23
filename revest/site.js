// Marketing page behavior, in a file (not inline) so the Content Security Policy can allow only
// scripts from this site (security review M3, issue #59).

// Screenshot images that fail to load show a soft placeholder with the emoji in data-fallback
(function () {
  function showPlaceholder(img) {
    var screen = img.closest('.screenshot-screen, .hero__phone-screen');
    if (!screen || screen.dataset.placeholder) return;
    screen.dataset.placeholder = '1';
    screen.classList.add(screen.classList.contains('hero__phone-screen') ? 'hero__phone-screen--placeholder' : 'screenshot-screen--placeholder');
    var icon = document.createElement('div');
    icon.className = 'screenshot-placeholder-icon';
    icon.setAttribute('aria-hidden', 'true');
    icon.textContent = img.dataset.fallback || '';
    img.remove();
    screen.appendChild(icon);
  }

  var images = document.querySelectorAll('img[data-fallback]');
  images.forEach(function (img) {
    // Already failed before this script ran
    if (img.complete && img.naturalWidth === 0) showPlaceholder(img);
    else img.addEventListener('error', function () { showPlaceholder(img); });
  });
})();

// Sections fade in as they scroll into view
(function () {
  var items = document.querySelectorAll('.fade-in');
  if (!('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('visible'); });
    return;
  }
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  items.forEach(function (el) { observer.observe(el); });
})();
