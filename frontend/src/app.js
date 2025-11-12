const express = require('express');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware to parse JSON requests
app.use(express.json());

// API endpoint to get batch information
app.get('/api/batch/:id', async (req, res) => {
    try {
        const response = await axios.get(`http://localhost:5000/api/batch/${req.params.id}`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching batch information' });
    }
});

// API endpoint to create a new batch
app.post('/api/batch', async (req, res) => {
    try {
        const response = await axios.post('http://localhost:5000/api/batch', req.body);
        res.status(201).json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Error creating batch' });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Frontend app listening at http://localhost:${PORT}`);
});