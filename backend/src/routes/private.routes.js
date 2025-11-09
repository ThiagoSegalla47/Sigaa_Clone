const router = require('express').Router();
const verifyToken = require('../middleware/auth');
router.get('/protected', verifyToken, (req, res) => {
 res.json({ message: 'Acesso autorizado.' });
});
module.exports = router;
