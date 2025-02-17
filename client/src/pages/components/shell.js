/**
 * @param {HTMLElement} header 
 * @param {SVGAnimatedBoolean} isLoggedIn 
 */
export function initShell(header, isLoggedIn) {
  const accButtons = header.querySelector("#account-buttons");

  // TODO: rewrite into without string literals
  if (isLoggedIn) {
    accButtons.innerHTML += `
      <li><a href="/account/keys">[My Keys]</a></li>
      <li><a href="/favorites">[Favorites]</a></li>
      <li><a id="logout" href="/account/logout">[Logout]</a></li>
    `
    document.getElementById('logout').addEventListener('click', e => {
      e.preventDefault();
      localStorage.removeItem('logged_in');
      localStorage.removeItem('favs');
      localStorage.removeItem('post_favs');
      location.href = '/account/logout';
    })
  } else {
    accButtons.innerHTML += `
      <li><a href="/account/login">[Login]</a></li>
    `
  }
}
