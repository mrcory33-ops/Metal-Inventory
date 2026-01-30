const fetch = require('node-fetch');

// This is a proxy endpoint to hide the Speechify API Key from the frontend
// You will need to host this on a small Node.js server (e.g. Vercel, Railway, or local)

const SPEECHIFY_API_KEY = process.env.SPEECHIFY_API_KEY || "YOUR_API_KEY_HERE";

// Supported Voices:
// english_us_male_1, english_us_female_1, spanish_mx_male_1, spanish_es_female_1
// See Speechify docs for full list

module.exports = async (req, res) => {
    const { text, lang } = req.body; // Expect JSON: { text: "Hello", lang: "en" }

    // Select voice based on language toggle
    const voiceId = lang === 'es' ? 'spanish_mexico_male' : 'english_us_male_2';

    try {
        const response = await fetch('https://api.speechify.com/v1/audio/speech', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${SPEECHIFY_API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                input: text,
                voice_id: voiceId,
                audio_format: 'mp3'
            })
        });

        if (!response.ok) {
            throw new Error(`Speechify API Error: ${response.statusText}`);
        }

        // Pipe the audio blob back to the frontend
        const audioBuffer = await response.buffer();
        res.setHeader('Content-Type', 'audio/mpeg');
        res.send(audioBuffer);

    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'TTS Failed' });
    }
};
