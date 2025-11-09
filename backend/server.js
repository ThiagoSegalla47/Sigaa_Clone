// Configurações básicas
require('dotenv').config();
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const cookieParser = require('cookie-parser');

// Import das rotas
const authRoutes = require('./src/routes/auth.routes');
const privateRoutes = require('./src/routes/private.routes');
const alunosRoutes = require('./src/routes/alunos.routes'); // novas rotas do banco

// Inicialização do app
const app = express();
const PORT = process.env.PORT || 5000;

// Configurações de segurança e limite
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 100, // máximo de 100 requisições por IP
  message: "Muitas requisições deste IP. Tente novamente mais tarde."
});

const corsOptions = {
  origin: ["http://localhost:5173"], // domínios permitidos
  methods: "GET,POST,PUT,DELETE",
  credentials: true
};

// Middlewares globais
app.use(express.json());
app.use(cookieParser());
app.use(helmet());
app.use(limiter);
app.use(cors(corsOptions));

// Rotas principais
app.use('/api/auth', authRoutes);
app.use('/api', privateRoutes);
app.use('/api/alunos', alunosRoutes);

// Rota inicial (teste rápido)
app.get('/', (req, res) => {
  res.send('🚀 Servidor acadêmico rodando perfeitamente!');
});

// Inicialização do servidor
app.listen(PORT, () => {
  console.log(`✅ Servidor rodando na porta ${PORT}`);
});
