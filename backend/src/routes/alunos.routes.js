const express = require('express');
const router = express.Router();
const controller = require('../controllers/alunos.controller');

router.get('/', controller.listar);
router.get('/:id', controller.buscarPorId);
router.post('/', controller.cadastrar);
router.delete('/:id', controller.deletar);

module.exports = router;
