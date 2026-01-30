require('dotenv').config();
const express = require('express');
const cors = require('cors');
const speechifyRoute = require('./routes/speechify');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Routes
app.post('/api/speechify', speechifyRoute);

app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date() });
});

app.listen(PORT, () => {
    console.log(`Backend server running on http://localhost:${PORT}`);
});
