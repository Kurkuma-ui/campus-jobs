import { useEffect, useState } from 'react'
import { ListGroup, Alert } from 'react-bootstrap'
import api from '../api/axios'

type Application = {
  id: number
  vacancy_id: number
  student_id: number
  status: string
  cover_letter?: string
}

export default function MyApplications() {
  const [apps, setApps] = useState<Application[]>([])
  const token = localStorage.getItem('token')

  useEffect(() => {
    if (!token) return
    api.get<Application[]>('/applications/me').then(r => setApps(r.data))
  }, [token])

  if (!token) {
    return <Alert variant="warning">Войдите, чтобы увидеть свои отклики</Alert>
  }

  return (
    <ListGroup>
      {apps.map(a => (
        <ListGroup.Item key={a.id}>
          Вакансия #{a.vacancy_id} — статус: <b>{a.status}</b>
          {a.cover_letter ? <> — «{a.cover_letter}»</> : null}
        </ListGroup.Item>
      ))}
      {apps.length === 0 && <div>Пока нет заявок.</div>}
    </ListGroup>
  )
}
