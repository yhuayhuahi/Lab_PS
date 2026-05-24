import { defaultStyle } from '../default/default.js'
import { AuthService } from '../model/authService.js'
import { MedicoRepository } from '../model/MedicoRepository.js'
import { PacienteRepository } from '../model/PacienteRepository.js'
import { CitaRepository } from '../model/CitaRepository.js'
import { CitaService } from '../model/citaService.js'
import '../components/ConfirmDialog.js'
import '../components/AvailabilityGrid.js'
import '../components/AppointmentsList.js'

const styles = /*css*/`
  ${defaultStyle}
  .page {
    max-width: 1100px;
    margin: 0 auto;
    padding: 32px 18px 40px 18px;
  }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
  }
  .title {
    font-size: 2rem;
    color: #1976d2;
    font-weight: 700;
    letter-spacing: -0.02em;
  }
  .subtitle {
    color: #4a4a4a;
    font-size: 1rem;
  }
  .row {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 24px;
  }
  .card {
    background: #fff;
    border-radius: 14px;
    box-shadow: 0 4px 16px #1976d214, 0 1.5px 8px #0002;
    padding: 20px 22px;
  }
  .card h2 {
    font-size: 1.35rem;
    margin-bottom: 8px;
    color: #1a237e;
  }
  .alert {
    padding: 10px 12px;
    border-radius: 8px;
    background: #fff3e0;
    color: #ef6c00;
    border: 1px solid #ffcc80;
    margin-bottom: 10px;
  }
  @media (max-width: 900px) {
    .row { grid-template-columns: 1fr; }
  }
`

class DoctorPage extends HTMLElement {
  constructor() {
    super()
    this.attachShadow({ mode: 'open' })
    this.selectedDate = this._getFechaHoy()
    this.pendingAdd = new Set()
    this.pendingRemove = new Set()
  }

  connectedCallback() {
    this.render()
  }

  render() {
    const session = AuthService.getSession()
    if (!session || session.rol !== 'medico') {
      this.shadowRoot.innerHTML = `<style>${styles}</style><div class="page"><div class="alert">Necesitas iniciar sesión como médico.</div></div>`
      return
    }

    const medico = MedicoRepository.getById(session.id)
    const date = this.selectedDate
    const bloques = CitaService.getBloquesHorario()
    const estadoSlots = this._mapEstadoSlots(session.id, date)
    const nowDate = this._getFechaHoy()
    const nowTime = this._getHoraActual()

    const slotsHtml = bloques.map(hora => {
      const estado = estadoSlots[hora] || 'empty'
      const isPast = date < nowDate || (date === nowDate && hora <= nowTime)
      let cls = `slot ${estado}`
      if (isPast) cls += ' disabled'
      if (estado === 'empty' && this.pendingAdd.has(hora)) cls = 'slot add'
      if (estado === 'available' && this.pendingRemove.has(hora)) cls = 'slot remove'
      return `<div class="${cls}" data-hora="${hora}" data-estado="${estado}">${hora}</div>`
    }).join('')

    const citas = this._getCitasFuturas(session.id)
    const citasHtml = citas.length ? citas.map(c => {
      const paciente = PacienteRepository.getById(c.pacienteId)
      const nombre = paciente ? paciente.nombre : c.pacienteId
      return `<div class="list-item">
        <div><strong>${c.fecha}</strong> ${c.hora} - ${nombre}</div>
        <span class="pill">Reservada</span>
      </div>`
    }).join('') : `<div class="alert">No tienes citas próximas.</div>`

    this.shadowRoot.innerHTML = `
      <style>${styles}</style>
      <div class="page">
        <div class="header">
          <div>
            <div class="title">Panel del médico</div>
            <div class="subtitle">${medico ? medico.nombre : 'Médico'} • ${medico ? medico.especialidad : ''}</div>
          </div>
          <div class="subtitle">Agenda y disponibilidad</div>
        </div>
        <div class="row">
          <div class="card">
            <h2>Disponibilidad por día</h2>
            <availability-grid id="availability-grid"></availability-grid>
          </div>
          <div class="card">
            <h2>Próximas citas</h2>
            <appointments-list id="appointments-list"></appointments-list>
          </div>
        </div>
      </div>
      <confirm-dialog id="confirm-dialog"></confirm-dialog>
    `

    const grid = this.shadowRoot.getElementById('availability-grid')
    if (grid) grid.data = { date, slotsHtml }
    const list = this.shadowRoot.getElementById('appointments-list')
    if (list) list.data = { html: citasHtml }

    this._bindEvents(session.id)
  }

  _bindEvents(medicoId) {
    const grid = this.shadowRoot.getElementById('availability-grid')
    if (!grid) return
    const dateInput = grid.shadowRoot.getElementById('date-input')
    const clearBtn = grid.shadowRoot.getElementById('clear-selection')
    const saveBtn = grid.shadowRoot.getElementById('save-availability')
    const confirmDialog = this.shadowRoot.getElementById('confirm-dialog')

    if (dateInput) {
      dateInput.addEventListener('change', (e) => {
        this.selectedDate = e.target.value
        this.pendingAdd.clear()
        this.pendingRemove.clear()
        this.render()
      })
    }

    grid.addEventListener('slot-toggle', (e) => {
      const { hora, action, selected } = e.detail
      if (action === 'add') {
        if (selected) this.pendingAdd.add(hora)
        else this.pendingAdd.delete(hora)
      } else if (action === 'remove') {
        if (selected) this.pendingRemove.add(hora)
        else this.pendingRemove.delete(hora)
      }
    })

    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        this.pendingAdd.clear()
        this.pendingRemove.clear()
        grid.clearSelection()
      })
    }

    if (saveBtn) {
      saveBtn.addEventListener('click', async () => {
        const horasAdd = Array.from(this.pendingAdd)
        const horasRemove = Array.from(this.pendingRemove)
        if (!horasAdd.length && !horasRemove.length) return

        const message = `Vas a agregar ${horasAdd.length} bloque(s) y quitar ${horasRemove.length} bloque(s). ¿Deseas continuar?`
        const ok = await confirmDialog.open({
          title: 'Confirmar cambios',
          message
        })
        if (!ok) return

        if (horasAdd.length) {
          CitaService.medicoDeclaraDisponibilidad({
            medicoId,
            fecha: this.selectedDate,
            horas: horasAdd
          })
        }
        horasRemove.forEach(hora => {
          CitaService.medicoDeshabilitaBloque({
            medicoId,
            fecha: this.selectedDate,
            hora
          })
        })
        this.pendingAdd.clear()
        this.pendingRemove.clear()
        this.render()
      })
    }
  }

  _mapEstadoSlots(medicoId, fecha) {
    const slots = {}
    const citas = CitaRepository.getAll().filter(c => c.medicoId === medicoId && c.fecha === fecha && c.activa)
    citas.forEach(c => {
      if (c.tipo === 'paciente') slots[c.hora] = 'reserved'
      if (c.tipo === 'medico' && !slots[c.hora]) slots[c.hora] = 'available'
    })
    return slots
  }

  _getCitasFuturas(medicoId) {
    const hoy = this._getFechaHoy()
    const ahora = this._getHoraActual()
    return CitaRepository.getAll()
      .filter(c => c.medicoId === medicoId && c.tipo === 'paciente' && c.activa)
      .filter(c => c.fecha > hoy || (c.fecha === hoy && c.hora > ahora))
      .sort((a, b) => (a.fecha + a.hora).localeCompare(b.fecha + b.hora))
  }

  _getFechaHoy() {
    return new Date().toISOString().slice(0, 10)
  }

  _getHoraActual() {
    const d = new Date()
    return d.toTimeString().slice(0, 5)
  }
}

customElements.define('doctor-page', DoctorPage)
