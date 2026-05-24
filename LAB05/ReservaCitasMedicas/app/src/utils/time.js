export function toDateTime(fecha, hora) {
  // fecha: 'YYYY-MM-DD', hora: 'HH:MM'
  return new Date(`${fecha}T${hora}:00`)
}

export function minutesUntil(fecha, hora, now = new Date()) {
  const target = toDateTime(fecha, hora)
  return Math.max(0, Math.floor((target.getTime() - now.getTime()) / 60000))
}

export function formatRemaining(minutes) {
  if (minutes < 60) return `${minutes} min`
  const h = Math.floor(minutes / 60)
  const m = minutes % 60
  return m ? `${h} h ${m} min` : `${h} h`
}
