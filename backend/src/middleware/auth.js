const jwt = require('jsonwebtoken');
const verifyToken = (req, res, next) => {
 const token = req.cookies?.jwt;
 if (!token) return res.status(401).json({ message: 'Token ausente' });
 try {
 req.user = jwt.verify(token, process.env.JWT_SECRET);
 next();
 } catch {
 res.status(403).json({ message: 'Token inválido' });
 }
};
module.exports = verifyToken;