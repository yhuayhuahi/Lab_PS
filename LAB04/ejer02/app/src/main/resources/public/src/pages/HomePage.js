import { defaultStyle } from "../utils/default.js"

const styles = /*css*/`
  ${defaultStyle}

  :host {
    --bg: #f7f1e3;
    --ink: #2b2a2f;
    --muted: #6b6772;
    --accent: #2a9d8f;
    --accent-dark: #1f7d72;
    --warn: #c44536;
    --paper: #fffdf7;
    --line: #e0d6c7;
    font-family: "Cascadia Code", "Fira Code", monospace;
    color: var(--ink);
  }

  .page {
    min-height: 100vh;
    background: radial-gradient(circle at 20% 20%, #fef6e4, #f7f1e3 55%, #efe7d8);
    padding: 32px 20px 60px;
  }

  .header {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 24px;
  }

  .title {
    font-size: clamp(24px, 4vw, 38px);
    letter-spacing: 1px;
  }

  .status {
    font-size: 14px;
    color: var(--muted);
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 18px;
  }

  .card {
    background: var(--paper);
    border: 2px solid var(--line);
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 10px 24px rgba(43, 42, 47, 0.08);
  }

  .card h2 {
    font-size: 18px;
    margin-bottom: 12px;
  }

  .form {
    display: grid;
    gap: 10px;
  }

  .row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }

  label {
    display: grid;
    gap: 6px;
    font-size: 13px;
    color: var(--muted);
    min-width: 0;
  }

  input {
    padding: 10px 12px;
    border-radius: 10px;
    border: 1px solid var(--line);
    background: #fff;
    font-size: 14px;
    width: 100%;
    min-width: 0;
  }

  input[type="checkbox"] {
    width: 18px;
    height: 18px;
    justify-self: start;
  }

  .actions {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }

  button {
    border: none;
    border-radius: 999px;
    padding: 10px 16px;
    font-weight: 600;
    cursor: pointer;
    background: var(--accent);
    color: #fff;
    transition: transform 0.15s ease, background 0.15s ease;
  }

  button:hover {
    transform: translateY(-1px);
    background: var(--accent-dark);
  }

  .ghost {
    background: transparent;
    color: var(--accent-dark);
    border: 2px solid var(--accent-dark);
  }

  .warn {
    background: var(--warn);
  }

  .list {
    display: grid;
    gap: 8px;
    font-size: 14px;
  }

  .scroll-list {
    max-height: 220px;
    overflow-y: auto;
    padding-right: 4px;
  }

  .pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 999px;
    background: #f1ede3;
    border: 1px dashed var(--line);
  }

  .meta {
    font-size: 13px;
    color: var(--muted);
  }

  .error {
    color: var(--warn);
    font-weight: 600;
  }

  .summary {
    white-space: pre-line;
    background: #fff9eb;
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 12px;
    font-size: 14px;
  }
`

const htmlRender = /*html*/`
  <section class="page">
    <header class="header">
      <div>
        <h1 class="title">Carrito de Compras</h1>
        <p class="meta">Interfaz simple para probar el API</p>
      </div>
      <div class="status" id="statusText">Listo</div>
    </header>

    <section class="grid">
      <article class="card">
        <h2>Agregar producto</h2>
        <form class="form" id="addForm">
          <div class="row">
            <label>
              ID
              <input type="number" id="addId" required />
            </label>
            <label>
              Cantidad
              <input type="number" id="addCantidad" required />
            </label>
          </div>
          <label>
            Nombre
            <input type="text" id="addNombre" required />
          </label>
          <div class="row">
            <label>
              Precio
              <input type="number" step="0.01" id="addPrecio" required />
            </label>
            <label>
              Disponible
              <input type="checkbox" id="addDisponible" checked />
            </label>
          </div>
          <div class="actions">
            <button type="submit">Agregar</button>
            <button type="button" class="ghost" id="refreshBtn">Refrescar</button>
          </div>
        </form>
      </article>

      <article class="card">
        <h2>Operaciones</h2>
        <div class="form">
          <label>
            ID a remover
            <input type="number" id="removeId" placeholder="Ej: 1" />
          </label>
          <div class="actions">
            <button type="button" class="warn" id="removeBtn">Remover</button>
            <button type="button" class="warn" id="clearBtn">Vaciar carrito</button>
          </div>
          <div class="pill">
            <span>Total:</span>
            <strong id="totalValue">0</strong>
          </div>
          <div class="pill">
            <span>Subtotal:</span>
            <strong id="subtotalValue">0</strong>
          </div>
        </div>
      </article>

      <article class="card">
        <h2>Items</h2>
        <div class="list" id="itemsList"></div>
      </article>

      <article class="card">
        <h2>Historial</h2>
        <div class="list scroll-list" id="historialList"></div>
      </article>

      <article class="card">
        <h2>Resumen</h2>
        <div class="summary" id="resumenText">Sin datos</div>
      </article>

      <article class="card">
        <h2>Errores</h2>
        <div class="error" id="errorText"></div>
      </article>
    </section>
  </section>
`

class HomePage extends HTMLElement {
  constructor() {
    super()
    this.attachShadow({ mode: "open" })
  }

  connectedCallback() {
    this.shadowRoot.innerHTML = /*html*/`
    <style>
      ${styles}
    </style>
    ${htmlRender}
    `

    this.bindUI()
    this.refreshAll()
  }

  bindUI() {
    this.statusText = this.shadowRoot.getElementById("statusText")
    this.errorText = this.shadowRoot.getElementById("errorText")
    this.itemsList = this.shadowRoot.getElementById("itemsList")
    this.historialList = this.shadowRoot.getElementById("historialList")
    this.totalValue = this.shadowRoot.getElementById("totalValue")
    this.subtotalValue = this.shadowRoot.getElementById("subtotalValue")
    this.resumenText = this.shadowRoot.getElementById("resumenText")

    this.shadowRoot.getElementById("addForm").addEventListener("submit", (event) => {
      event.preventDefault()
      this.agregarProducto()
    })

    this.shadowRoot.getElementById("refreshBtn").addEventListener("click", () => {
      this.refreshAll()
    })

    this.shadowRoot.getElementById("removeBtn").addEventListener("click", () => {
      this.removerProducto()
    })

    this.shadowRoot.getElementById("clearBtn").addEventListener("click", () => {
      this.vaciarCarrito()
    })
  }

  async apiFetch(path, options = {}) {
    this.setStatus("Cargando...")
    this.setError("")

    const response = await fetch(path, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers
      },
      ...options
    })

    if (!response.ok) {
      const payload = await response.json().catch(() => ({ error: "Error" }))
      const message = payload?.error || `Error ${response.status}`
      throw new Error(message)
    }

    return response.json().catch(() => ({}))
  }

  async refreshAll() {
    try {
      const [items, historial, total, resumen] = await Promise.all([
        this.apiFetch("/api/carrito/items"),
        this.apiFetch("/api/carrito/historial"),
        this.apiFetch("/api/carrito/total"),
        this.apiFetch("/api/carrito/resumen")
      ])

      this.renderItems(items)
      this.renderHistorial(historial)
      this.renderTotal(total)
      this.renderResumen(resumen)
      this.setStatus("Actualizado")
    } catch (error) {
      this.setError(error.message)
      this.setStatus("Error")
    }
  }

  renderItems(items = []) {
    if (!items.length) {
      this.itemsList.innerHTML = "<span class='meta'>Sin items</span>"
      this.subtotalValue.textContent = "0"
      return
    }

    const subtotal = items.reduce((acc, item) => acc + (item.subtotal ?? (item.producto?.precio || 0) * item.cantidad), 0)

    this.itemsList.innerHTML = items.map((item) => {
      const producto = item.producto || {}
      return `
        <div class="pill">
          <strong>${producto.nombre || "Producto"}</strong>
          <span>#${producto.id ?? "?"}</span>
          <span>x ${item.cantidad}</span>
          <span>$${(producto.precio ?? 0).toFixed(2)}</span>
        </div>
      `
    }).join("")

    this.subtotalValue.textContent = subtotal.toFixed(2)
  }

  renderHistorial(historial = []) {
    if (!historial.length) {
      this.historialList.innerHTML = "<span class='meta'>Sin historial</span>"
      return
    }

    this.historialList.innerHTML = historial.map((item) => {
      return `<div class="pill">${item.operacion}</div>`
    }).join("")
  }

  renderTotal(totalPayload = {}) {
    const total = totalPayload.total ?? 0
    this.totalValue.textContent = total.toFixed(2)
  }

  renderResumen(resumenPayload = {}) {
    this.resumenText.textContent = resumenPayload.resumen || "Sin resumen"
  }

  setStatus(message) {
    this.statusText.textContent = message
  }

  setError(message) {
    this.errorText.textContent = message
  }

  async agregarProducto() {
    try {
      const producto = {
        id: Number(this.shadowRoot.getElementById("addId").value),
        nombre: this.shadowRoot.getElementById("addNombre").value.trim(),
        precio: Number(this.shadowRoot.getElementById("addPrecio").value),
        disponible: this.shadowRoot.getElementById("addDisponible").checked
      }

      const cantidad = Number(this.shadowRoot.getElementById("addCantidad").value)

      await this.apiFetch("/api/carrito/items", {
        method: "POST",
        body: JSON.stringify({ producto, cantidad })
      })

      this.setStatus("Producto agregado")
      await this.refreshAll()
    } catch (error) {
      this.setError(error.message)
      this.setStatus("Error")
    }
  }

  async removerProducto() {
    try {
      const id = Number(this.shadowRoot.getElementById("removeId").value)

      if (!id) {
        this.setError("Ingresa un ID valido")
        return
      }

      await this.apiFetch(`/api/carrito/items/${id}`, {
        method: "DELETE"
      })

      this.setStatus("Producto removido")
      await this.refreshAll()
    } catch (error) {
      this.setError(error.message)
      this.setStatus("Error")
    }
  }

  async vaciarCarrito() {
    try {
      await this.apiFetch("/api/carrito/vaciar", {
        method: "POST"
      })

      this.setStatus("Carrito vaciado")
      await this.refreshAll()
    } catch (error) {
      this.setError(error.message)
      this.setStatus("Error")
    }
  }
}

customElements.define('home-page', HomePage)