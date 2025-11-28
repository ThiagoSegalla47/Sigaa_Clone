// GradesPage.jsx
import "./grades.css";

const subjects = [
  "Artes",
  "Banco de Dados",
  "Biologia",
  "Desenvolvimento Web I",
  "Educação Física",
  "Filosofia",
  "Física",
  "Geografia",
  "História",
  "Língua portuguesa e Literatura",
  "Matemática",
  "Projeto de Software",
  "Projeto Integrador I",
  "Química",
  "Sociologia",
  "Web Design",
];

export default function GradesPage() {
  return (
    <main className="grades-main">
      <header className="grades-header">
        <h1>Notas</h1>
        <div className="grades-header-right">
          <span>Turma 2G - 2º Ano</span>
        </div>
      </header>

      <section className="grades-top-bar">
        <button className="grades-top-button">Filtros</button>

        <div className="grades-top-card">
          <span>Média Geral</span>
          <strong>8.7</strong>
        </div>

        <button className="grades-top-button">Selecionar por ano</button>
      </section>

      <section className="grades-content">
        <h2 className="grades-section-title">Médias Particulares:</h2>

        <div className="grades-list">
          {subjects.map((subject) => (
            <article key={subject} className="grade-item">
              <header className="grade-item-header">
                <h3>{subject}</h3>
              </header>

              <div className="grade-item-bar">
                <div className="grade-term">
                  <span>T1</span>
                  <div className="grade-term-bar grade-t1" />
                </div>
                <div className="grade-term">
                  <span>T2</span>
                  <div className="grade-term-bar grade-t2" />
                </div>
                <div className="grade-term">
                  <span>T3</span>
                  <div className="grade-term-bar grade-t3" />
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>

      <aside className="grades-achievements">
        <h3>Conquistas dessa página:</h3>
        <ul>
          <li>Nota máxima em: Banco de Dados, Educação Física</li>
          <li>Maior nota da turma em: Matemática</li>
        </ul>
      </aside>
    </main>
  );
}
