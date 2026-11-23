// Loaded in <head> before the page draws: only hide sections for the scroll fade-in when the browser
// can bring them back (IntersectionObserver) and the visitor hasn't asked for reduced motion.
// Without this script (or with reduced motion), everything simply shows. Issue #49.
if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.documentElement.classList.add('js-anim');
}
