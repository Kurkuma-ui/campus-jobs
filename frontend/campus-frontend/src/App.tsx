import { Container, Nav, Navbar } from 'react-bootstrap'
import { Routes, Route, Link, useNavigate } from 'react-router-dom'
import VacanciesList from './pages/VacanciesList'
import VacancyView from './pages/VacancyView'
import Login from './pages/Login'
import MyApplications from './pages/MyApplications'

function App() {
  const navigate = useNavigate()
  const token = localStorage.getItem('token')

  const logout = () => {
    localStorage.removeItem('token')
    navigate('/')
  }

  return (
    <>
      <Navbar bg="dark" data-bs-theme="dark" expand="sm">
        <Container>
          <Navbar.Brand as={Link} to="/">Campus Jobs</Navbar.Brand>
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">Вакансии</Nav.Link>
            <Nav.Link as={Link} to="/me">Мои отклики</Nav.Link>
          </Nav>
          <Nav>
            {!token ? (
              <Nav.Link as={Link} to="/login">Войти</Nav.Link>
            ) : (
              <Nav.Link onClick={logout}>Выйти</Nav.Link>
            )}
          </Nav>
        </Container>
      </Navbar>

      <Container className="py-3">
        <Routes>
          <Route path="/" element={<VacanciesList />} />
          <Route path="/vacancies/:id" element={<VacancyView />} />
          <Route path="/login" element={<Login />} />
          <Route path="/me" element={<MyApplications />} />
        </Routes>
      </Container>
    </>
  )
}

export default App
