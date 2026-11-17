import { setTimeout } from 'node:timers/promises';

const url = process.env.RENDER_EXTERNAL_URL || 'https://codelens-ai-frontend.onrender.com';
let healthy = false;
for (let attempt = 1; attempt <= 5; attempt++) {
  try {
    const response = await fetch(url, { signal: AbortSignal.timeout(10_000) });
    await response.body?.cancel();
    if (response.status === 200) { healthy = true; break; }
    console.error(`Attempt ${attempt}: HTTP ${response.status}`);
  } catch (error) { console.error(`Attempt ${attempt}: ${error.message}`); }
  if (attempt < 5) await setTimeout(5000);
}
console.log(healthy ? 'Health check successful' : 'Health check failed');
process.exitCode = healthy ? 0 : 1;
