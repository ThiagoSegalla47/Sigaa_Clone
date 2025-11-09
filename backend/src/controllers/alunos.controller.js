const Aluno = require('../models/alunos.model');

exports.listar = async (req, res) => {
  try {
    const alunos = await Aluno.getAll();
    res.json(alunos);
  } catch (err) {
    res.status(500).json({ erro: 'Erro ao listar alunos', detalhes: err.message });
  }
};

exports.buscarPorId = async (req, res) => {
  try {
    const aluno = await Aluno.getById(req.params.id);
    if (!aluno) return res.status(404).json({ erro: 'Aluno não encontrado' });
    res.json(aluno);
  } catch (err) {
    res.status(500).json({ erro: 'Erro ao buscar aluno', detalhes: err.message });
  }
};

exports.cadastrar = async (req, res) => {
  try {
    const novo = await Aluno.create(req.body);
    res.status(201).json(novo);
  } catch (err) {
    res.status(500).json({ erro: 'Erro ao cadastrar aluno', detalhes: err.message });
  }
};

exports.deletar = async (req, res) => {
  try {
    await Aluno.delete(req.params.id);
    res.status(204).send();
  } catch (err) {
    res.status(500).json({ erro: 'Erro ao deletar aluno', detalhes: err.message });
  }
};
