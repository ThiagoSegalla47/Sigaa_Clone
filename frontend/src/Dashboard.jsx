// Dashboard.jsx
import { useState } from "react";
import "./Dashboard.css";

export default function Dashboard() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => setIsSidebarOpen((prev) => !prev);

  return (
    <div className={`app ${isSidebarOpen ? "app--sidebar-open" : ""}`}>
      {/* Sidebar (fixa no desktop, sobreposta no mobile) */}
      <aside className={`sidebar ${isSidebarOpen ? "sidebar--open" : ""}`}>
        <div className="sidebar-logo">
          <div className="logo-icon">EM</div>
          <div className="logo-text">
            <h1>Dashboard</h1>
            <span>Bem vindo Moysés!</span>
          </div>
        </div>

        <nav className="sidebar-menu">
          <button className="menu-item active">Dashboard</button>
          <button className="menu-item">Notas</button>
          <button className="menu-item">Frequência</button>
          <button className="menu-item">Mensagens</button>
          <button className="menu-item">Atividades</button>
          <button className="menu-item">Agenda</button>
          <button className="menu-item">Ranking</button>
        </nav>

        <div className="sidebar-footer">
          <div className="user-avatar" />
          <div className="user-info">
            <span className="user-name">Moysés Voss</span>
            <span className="user-role">Estudante</span>
          </div>
        </div>
      </aside>

      {/* backdrop quando o menu estiver aberto no mobile */}
      {isSidebarOpen && <div className="sidebar-backdrop" onClick={toggleSidebar} />}

      {/* Main content */}
      <main className="main">
        <header className="topbar">
          <div className="topbar-left">
            {/* botão azul EM: abre/fecha menu no mobile */}
            <button className="mobile-logo-icon" onClick={toggleSidebar}>
              EM
            </button>
          </div>
          <div className="topbar-right">
            <span className="topbar-user-name">Moysés - 2G</span>
            <div className="topbar-user-avatar" />
          </div>
        </header>

        <section className="summary-cards">
          <div className="card card-average">
            <span className="card-label">Média Geral</span>
            <h2>8.7</h2>
            <span className="card-sub">↑ 0.8 este trimestre</span>
          </div>
          <div className="card card-frequency">
            <span className="card-label">Frequência</span>
            <h2>94%</h2>
            <span className="card-sub">4 faltas esse mês</span>
          </div>
          <div className="card card-tasks">
            <span className="card-label">Tarefas</span>
            <div className="card-tasks-values">
              <span>5 pendentes</span>
              <span>1 atrasadas</span>
            </div>
          </div>
          <div className="card card-ranking">
            <span className="card-label">Ranking</span>
            <h2>3º</h2>
            <span className="card-sub">na turma</span>
          </div>
        </section>

        <section className="content-grid">
          {/* Notas por disciplina */}
          <div className="card full card-grades">
            <div className="card-header">
              <h3>Notas por disciplina</h3>
              <button className="link-button">Ver todas</button>
            </div>

            <div className="grade-row">
              <div className="grade-info">
                <span className="grade-title">Matemática</span>
                <span className="grade-teacher">Prof. Bernardo</span>
              </div>
              <div className="grade-bar">
                <div className="grade-bar-fill green" style={{ width: "92%" }} />
              </div>
              <span className="grade-value">9.2</span>
            </div>

            <div className="grade-row">
              <div className="grade-info">
                <span className="grade-title">Banco de Dados</span>
                <span className="grade-teacher">Prof. Danimar</span>
              </div>
              <div className="grade-bar">
                <div className="grade-bar-fill blue" style={{ width: "100%" }} />
              </div>
              <span className="grade-value">10.0</span>
            </div>

            <div className="grade-row">
              <div className="grade-info">
                <span className="grade-title">Web Design</span>
                <span className="grade-teacher">Prof. Danimar</span>
              </div>
              <div className="grade-bar">
                <div className="grade-bar-fill yellow" style={{ width: "75%" }} />
              </div>
              <span className="grade-value">7.5</span>
            </div>

            <div className="grade-row">
              <div className="grade-info">
                <span className="grade-title">PI I</span>
                <span className="grade-teacher">Prof. Guilherme, Danimar</span>
              </div>
              <div className="grade-bar">
                <div className="grade-bar-fill red" style={{ width: "59%" }} />
              </div>
              <span className="grade-value">5.9</span>
            </div>
          </div>

          {/* Próximas atividades + Mensagens + Conquistas */}
          <div className="right-column">
            <div className="card card-activities">
              <div className="card-header">
                <h3>Próximas atividades</h3>
              </div>
              <div className="activity activity-red">
                <div>
                  <h4>Prova de química</h4>
                  <span>Amanhã 14:30</span>
                </div>
                <span className="badge badge-danger">Urgente</span>
              </div>
              <div className="activity activity-yellow">
                <div>
                  <h4>Entrega de PI</h4>
                  <span>4 de Novembro, 18:00</span>
                </div>
                <span className="badge">7 dias</span>
              </div>
              <div className="activity activity-purple">
                <div>
                  <h4>Lista de Matemática</h4>
                  <span>19 de Novembro, 15:00</span>
                </div>
                <span className="badge">15 dias</span>
              </div>
            </div>

            <div className="card card-messages">
              <div className="card-header">
                <h3>Mensagens</h3>
              </div>
              <div className="message-item">
                <div className="message-avatar" />
                <div className="message-text">
                  <span className="message-title">Prof. H. Romeu Pinto</span>
                  <span className="message-preview">
                    Novo aviso sobre a avaliação de recuperação...
                  </span>
                </div>
              </div>
            </div>

            <div className="card card-achievements">
              <div className="card-header">
                <h3>Conquistas</h3>
                <button className="link-button">Ver todas</button>
              </div>
              <div className="achievement achievement-gold">
                <span>Nota máxima</span>
                <span>Matemática - prova 1</span>
              </div>
              <div className="achievement achievement-blue">
                <span>Frequência perfeita</span>
                <span>Outubro 2025</span>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
