import { useEffect, useState } from 'react'
import { Button, Card } from 'react-bootstrap'
import { useNavigate, useParams } from 'react-router-dom'
import api from '../api/axios'

type Vacancy = {
  id: number
  org_id: number
  title: string
  description: string
  employment_type?: string
  location?: string
  is_active: boolean
}

export default function VacancyView() {
  const { id } = useParams()
  const [vac, setVac] = useState<Vacancy | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    api.get<Vacancy>(`/vacancies/${id}`).then(r => setVac(r.data))
  }, [id])

  const apply = async () => {
    const token = localStorage.getItem('token')
    if (!token) {
      navigate('/login', { state: { from: `/vacancies/${id}` } })
      return
    }
    await api.post('/applications', { vacancy_id: Number(id), cover_letter: 'Отклик через UI' })
    alert('Отклик отправлен!')
    navigate('/me')
  }

  if (!vac) return null

  return (
    <Card>
      <Card.Body>
        <Card.Title>{vac.title}</Card.Title>
        <Card.Subtitle className="mb-2 text-muted">
          {vac.location ?? '—'} · {vac.employment_type ?? '—'}
        </Card.Subtitle>
        <Card.Text>{vac.description}</Card.Text>
        <Button onClick={apply}>Откликнуться</Button>
      </Card.Body>
    </Card>
  )
}
