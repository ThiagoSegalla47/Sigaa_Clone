const router = require('express').Router();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { body, validationResult } = require('express-validator');
const usersDb = require('../utils/usersDb');

// Rota de registro
router.post(
  '/register',
  [
    body('email').isEmail().withMessage('O e-mail fornecido não é válido.'),
    body('password').isLength({ min: 6 }).withMessage('A senha deve ter no mínimo 6 caracteres.')
  ],
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty())
      return res.status(400).json({ errors: errors.array() });

    const { email, password } = req.body;

    const hash = await bcrypt.hash(password, 10);
    usersDb.push({
      id: usersDb.length + 1,
      email,
      password: hash,
    });

    res.status(201).json({ message: 'Usuário registrado com sucesso.' });
  }
);

// Rota de login
router.post('/login', async (req, res) => {
  const { email, password } = req.body;

  const user = usersDb.find((u) => u.email === email);
  if (!user)
    return res.status(401).json({ message: 'Credenciais inválidas.' });

  const isMatch = await bcrypt.compare(password, user.password);
  if (!isMatch)
    return res.status(401).json({ message: 'Credenciais inválidas.' });

  const token = jwt.sign(
    { id: user.id },
    process.env.JWT_SECRET,
    { expiresIn: '1h' }
  );

  res.cookie('jwt', token, {
    httpOnly: true,
    sameSite: 'Lax',
    maxAge: 3600000, // 1 hora
  });

  res.status(200).json({ message: 'Login bem-sucedido.' });
});

module.exports = router;
