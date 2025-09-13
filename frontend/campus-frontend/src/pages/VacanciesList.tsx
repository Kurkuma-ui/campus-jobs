import { useEffect, useState } from 'react'
import { Card, Button, Row, Col, Form } from 'react-bootstrap'
import { Link, useSearchParams } from 'react-router-dom'
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

type Page = {
  items: Vacancy[]
  total: number
  limit: number
  offset: number
}

export default function VacanciesList() {
  const [params, setParams] = useSearchParams()
  const [page, setPage] = useState<Page | null>(null)
  const [q, setQ] = useState(params.get('q') ?? '')

  const limit = 10
  const offset = Number(params.get('offset') ?? 0)

  useEffect(() => {
    api.get<Page>('/vacancies', { params: { q, limit, offset } })
      .then(r => setPage(r.data))
  }, [q, offset])

  const next = () => setParams({ q, offset: String(offset + limit) })
  const prev = () => setParams({ q, offset: String(Math.max(0, offset - limit)) })

  return (
    <>
      <Form className="mb-3" onSubmit={(e) => { e.preventDefault(); setParams({ q, offset: '0' }) }}>
        <Form.Control
          placeholder="Поиск по вакансиям…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
      </Form>

      <Row xs={1} md={2} lg={3} className="g-3">
        {page?.items.map(v => (
          <Col key={v.id}>
            <Card className="h-100">
              <Card.Body>
                <Card.Title>{v.title}</Card.Title>
                <Card.Subtitle className="mb-2 text-muted">
                  {v.location ?? '—'} · {v.employment_type ?? '—'}
                </Card.Subtitle>
                <Card.Text>{v.description.slice(0, 120)}…</Card.Text>
                <Link to={`/vacancies/${v.id}`} className="btn btn-primary">
				Подробнее
				</Link>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      <div className="d-flex gap-2 justify-content-center mt-3">
        <Button onClick={prev} disabled={offset === 0}>Назад</Button>
        <Button onClick={next} disabled={(offset + limit) >= (page?.total ?? 0)}>Вперёд</Button>
      </div>
    </>
  )
}
