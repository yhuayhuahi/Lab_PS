import "./pages/HomePage.js"

const app = document.querySelector("#app")

function render() {
  const path = window.location.hash || '#/'
  console.log("Current path:", path)

  app.innerHTML = ''

  if (path === '#/') {
    const homePage = document.createElement('home-page')
    app.appendChild(homePage)
  }
}

// Escuchar cambios en el hash (cuando cambia la URL)
window.addEventListener('hashchange', render);

// Configuración inicial
render();