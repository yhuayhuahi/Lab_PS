import { defaultStyle } from '../default/default.js'
import { AuthService } from '../model/authService.js'
import { MedicoRepository } from '../model/MedicoRepository.js'
import { PacienteRepository } from '../model/PacienteRepository.js'
import { CitaRepository } from '../model/CitaRepository.js'
import { CitaService } from '../model/citaService.js'

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
  .date-row {
    display: flex;
    gap: 12px;
    align-items: center;
    margin-bottom: 14px;
  }
  input[type="date"] {
    border: 1.4px solid #b3c6e4;
    border-radius: 8px;
    padding: 8px 10px;
    font-size: 1rem;
    background: #f8faff;
  }
  .slot-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
    gap: 10px;
  }
  .slot {
    padding: 9px 10px;
    border-radius: 8px;
    border: 1.4px solid #c8d4f0;
    background: #f6f9ff;
    color: #223;
    font-weight: 600;
    cursor: pointer;
    text-align: center;
    transition: all .15s;
    user-select: none;
  }
  .slot.available { background: #e8f5ff; color: #1976d2; border-color: #90caf9; }
  .slot.reserved { background: #ffe8e8; color: #c62828; border-color: #ef9a9a; cursor: not-allowed; }
  .slot.empty { background: #f6f9ff; color: #37474f; }
  .slot.add { background: #e0f7fa; color: #00796b; border-color: #4dd0e1; }
  .slot.remove { background: #fff3e0; color: #ef6c00; border-color: #ffcc80; }
  .slot.disabled { background: #f0f0f0; color: #9e9e9e; border-color: #ddd; cursor: not-allowed; }
  .actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 14px;
  }
  .btn {
    padding: 10px 16px;
    border-radius: 8px;
    border: none;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
  }
  .btn.primary {
    background: #1976d2;
    color: #fff;
    box-shadow: 0 2px 10px #1976d225;
  }
  .btn.ghost {
    background: #f5f5f5;
    color: #333;
  }
  .list {
    margin-top: 12px;
    display: grid;
    gap: 8px;
  }
  .list-item {
    padding: 10px 12px;
    border-radius: 8px;
    background: #f7f9ff;
    border: 1px solid #dde6f5;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .pill {
    font-size: 0.85rem;
    background: #e3f2fd;
    color: #1565c0;
    padding: 4px 10px;
    border-radius: 999px;
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
            <div class="date-row">
              <label>Fecha:</label>
              <input type="date" id="date-input" value="${date}" />
            </div>
            <div class="slot-grid" id="slot-grid">${slotsHtml}</div>
            <div class="actions">
              <button class="btn ghost" id="clear-selection">Limpiar selección</button>
              <button class="btn primary" id="save-availability">Guardar cambios</button>
            </div>
          </div>
          <div class="card">
            <h2>Próximas citas</h2>
            <div class="list">${citasHtml}</div>
          </div>
        </div>
      </div>
    `

    this._bindEvents(session.id)
  }

  _bindEvents(medicoId) {
    const dateInput = this.shadowRoot.getElementById('date-input')
    const slotGrid = this.shadowRoot.getElementById('slot-grid')
    const clearBtn = this.shadowRoot.getElementById('clear-selection')
    const saveBtn = this.shadowRoot.getElementById('save-availability')

    if (dateInput) {
      dateInput.addEventListener('change', (e) => {
        this.selectedDate = e.target.value
        this.pendingAdd.clear()
        this.pendingRemove.clear()
        this.render()
      })
    }

    if (slotGrid) {
      slotGrid.addEventListener('click', (e) => {
        const target = e.target.closest('.slot')
        if (!target || target.classList.contains('reserved') || target.classList.contains('disabled')) return
        const hora = target.dataset.hora
        const estado = target.dataset.estado
        if (estado === 'empty') {
          if (this.pendingAdd.has(hora)) this.pendingAdd.delete(hora)
          else this.pendingAdd.add(hora)
        } else if (estado === 'available') {
          if (this.pendingRemove.has(hora)) this.pendingRemove.delete(hora)
          else this.pendingRemove.add(hora)
        }
        this.render()
      })
    }

    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        this.pendingAdd.clear()
        this.pendingRemove.clear()
        this.render()
      })
    }

    if (saveBtn) {
      saveBtn.addEventListener('click', () => {
        const horasAdd = Array.from(this.pendingAdd)
        if (horasAdd.length) {
          CitaService.medicoDeclaraDisponibilidad({
            medicoId,
            fecha: this.selectedDate,
            horas: horasAdd
          })
        }
        const horasRemove = Array.from(this.pendingRemove)
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
