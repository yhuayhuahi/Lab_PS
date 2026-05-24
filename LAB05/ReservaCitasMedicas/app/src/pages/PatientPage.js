import { defaultStyle } from '../default/default.js'

const styles = /*css*/`
  ${defaultStyle}
`

const htmlRender = /*html*/`
  <h1>Patient Panel</h1>
`

class PatientPage extends HTMLElement {
  constructor() {
    super()
    this.attachShadow({ mode: 'open' })
  }

  connectedCallback() {
    this.shadowRoot.innerHTML = /*html*/`
      <style>${styles}</style>
      ${htmlRender}
    `
  }
}

customElements.define('patient-page', PatientPage)