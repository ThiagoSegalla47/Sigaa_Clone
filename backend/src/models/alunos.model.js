const db = require('../config/db');

const Aluno = {
  async getAll() {
    const { rows } = await db.query('SELECT * FROM alunos ORDER BY id_aluno');
    return rows;
  },

  async getById(id) {
    const { rows } = await db.query('SELECT * FROM alunos WHERE id_aluno = $1', [id]);
    return rows[0];
  },

  async create(aluno) {
    const { matricula, cpf, nome_completo, email, telefone, data_nascimento, endereco, cidade, estado, cep, data_ingresso } = aluno;
    const { rows } = await db.query(
      `INSERT INTO alunos (matricula, cpf, nome_completo, email, telefone, data_nascimento, endereco, cidade, estado, cep, data_ingresso)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11) RETURNING *`,
      [matricula, cpf, nome_completo, email, telefone, data_nascimento, endereco, cidade, estado, cep, data_ingresso]
    );
    return rows[0];
  },

  async delete(id) {
    await db.query('DELETE FROM alunos WHERE id_aluno = $1', [id]);
  }
};

module.exports = Aluno;
