// Overlays: the drawer and the theme card. Both need the same three things beyond being shown — the
// keyboard has to move into them, the page behind them has to stop scrolling, and focus has to come
// back to whatever opened them on close. Keeping that in one place is what stops the two drifting.

let lastFocus = null;

export function openOverlay(overlay, inner) {
  lastFocus = document.activeElement;
  overlay.hidden = false;
  document.body.classList.add("no-scroll");
  if (inner) inner.focus();         // the panel, not the first control: it reads from the top
}

export function closeOverlay(overlay) {
  if (overlay.hidden) return;
  const focusWasInside = overlay.contains(document.activeElement);
  overlay.hidden = true;
  document.body.classList.remove("no-scroll");
  if (focusWasInside && lastFocus && document.contains(lastFocus)) lastFocus.focus();
  lastFocus = null;
}
