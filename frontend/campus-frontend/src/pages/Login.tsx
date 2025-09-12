import { useState } from 'react'
import { Button, Card, Form } from 'react-bootstrap'
import { useLocation, useNavigate } from 'react-router-dom'
import api from '../api/axios'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const location = useLocation() as any
  const backTo: string = location?.state?.from ?? '/'

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      const r = await api.post('/auth/login', { email, password })
      localStorage.setItem('token', r.data.access_token)
      navigate(backTo)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="mx-auto" style={{ maxWidth: 420 }}>
      <Card.Body>
        <Card.Title>Вход</Card.Title>
        <Form onSubmit={submit}>
          <Form.Group className="mb-3">
            <Form.Label>Email</Form.Label>
            <Form.Control value={email} onChange={e => setEmail(e.target.value)} type="email" required />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Пароль</Form.Label>
            <Form.Control value={password} onChange={e => setPassword(e.target.value)} type="password" required />
          </Form.Group>
          <Button type="submit" disabled={loading}>Войти</Button>
        </Form>
      </Card.Body>
    </Card>
  )
}
