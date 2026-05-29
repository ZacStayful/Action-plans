// Serverless TTS proxy for ElevenLabs.
// Keeps the API key server-side (Vercel env vars) so it is never shipped to the browser.
// Env vars (set in Vercel): ELEVENLABS_API (the xi-api-key) and ELEVENLABS_VOICE_ID.

const ELEVENLABS_MODEL = 'eleven_turbo_v2_5';
const MAX_CHARS = 1500;

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  // Same-origin guard: block obvious off-site abuse of the proxy.
  const origin = req.headers.origin;
  if (origin) {
    try {
      if (new URL(origin).host !== req.headers.host) {
        res.status(403).json({ error: 'Forbidden' });
        return;
      }
    } catch {
      res.status(403).json({ error: 'Forbidden' });
      return;
    }
  }

  const apiKey = process.env.ELEVENLABS_API || process.env.ELEVENLABS_API_KEY;
  const voiceId = process.env.ELEVENLABS_VOICE_ID;
  if (!apiKey || !voiceId) {
    res.status(500).json({ error: 'TTS not configured' });
    return;
  }

  const text = req.body && typeof req.body.text === 'string' ? req.body.text.trim() : '';
  if (!text) {
    res.status(400).json({ error: 'Missing text' });
    return;
  }

  const upstream = await fetch(
    `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}?output_format=mp3_44100_128`,
    {
      method: 'POST',
      headers: {
        'xi-api-key': apiKey,
        'Content-Type': 'application/json',
        Accept: 'audio/mpeg',
      },
      body: JSON.stringify({
        text: text.slice(0, MAX_CHARS),
        model_id: ELEVENLABS_MODEL,
        voice_settings: {
          stability: 0.45,
          similarity_boost: 0.8,
          style: 0.0,
          use_speaker_boost: true,
        },
      }),
    }
  );

  if (!upstream.ok) {
    const detail = await upstream.text();
    res.status(502).json({ error: 'TTS upstream error', detail: detail.slice(0, 300) });
    return;
  }

  const audio = Buffer.from(await upstream.arrayBuffer());
  res.setHeader('Content-Type', 'audio/mpeg');
  res.setHeader('Cache-Control', 'public, max-age=86400');
  res.status(200).send(audio);
}
