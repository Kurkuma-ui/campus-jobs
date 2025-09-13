import { Routes, Route, NavLink, Link } from "react-router-dom";
import VacanciesList from "./pages/VacanciesList";
import VacancyView from "./pages/VacancyView";
import Login from "./pages/Login";
import MyApplications from "./pages/MyApplications";

function App() {
  return (
    <div>
      {/* навигация */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark px-3">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">
            Campus Jobs
          </Link>

          <div className="navbar-nav">
            <NavLink className="nav-link" to="/vacancies">
              Вакансии
            </NavLink>
            <NavLink className="nav-link" to="/applications">
              Мои отклики
            </NavLink>
          </div>

          <div className="ms-auto navbar-nav">
            <NavLink className="nav-link" to="/login">
              Войти
            </NavLink>
          </div>
        </div>
      </nav>

      {/* маршруты */}
      <Routes>
        <Route path="/" element={<VacanciesList />} />
        <Route path="/vacancies" element={<VacanciesList />} />
        <Route path="/vacancies/:id" element={<VacancyView />} />
        <Route path="/login" element={<Login />} />
        <Route path="/applications" element={<MyApplications />} />
      </Routes>
    </div>
  );
}

export default App;
