import { existsSync } from 'node:fs';
import { loadEnvFile } from 'node:process';
import { fileURLToPath } from 'node:url';
import { createApp } from './app.js';

// Backend settings take precedence over the shared root environment file.
for (const path of ['.env', '../.env']) {
  const file = fileURLToPath(new URL(path, import.meta.url));
  if (existsSync(file)) loadEnvFile(file);
}
const port = Number(process.env.PORT || 5000);
createApp().listen(port, '0.0.0.0', () => console.log(`CodeLens AI listening on port ${port}`));
