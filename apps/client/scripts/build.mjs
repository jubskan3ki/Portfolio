import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import { setTimeout as sleep } from 'node:timers/promises';

const ARTIFACT = '.output/server/index.mjs';
const POLL_INTERVAL_MS = 1000;
const POLL_TIMEOUT_MS = 2 * 60 * 1000;
const FLUSH_GRACE_MS = 5000;

const nuxtBin = './node_modules/nuxt/bin/nuxt.mjs';

const child = spawn(process.execPath, [nuxtBin, 'build'], {
    stdio: 'inherit',
    env: process.env,
});

let childExited = false;
let childExitCode = null;
child.on('exit', (code) => {
    childExited = true;
    childExitCode = code;
});

const start = Date.now();
while (!existsSync(ARTIFACT) && !childExited) {
    if (Date.now() - start > POLL_TIMEOUT_MS) {
        console.error(`[build.mjs] timeout: ${ARTIFACT} non cree apres ${POLL_TIMEOUT_MS / 1000}s`);
        child.kill('SIGKILL');
        process.exit(1);
    }
    await sleep(POLL_INTERVAL_MS);
}

if (childExited && !existsSync(ARTIFACT)) {
    console.error(`[build.mjs] nuxt build a quitte (code=${childExitCode}) sans produire ${ARTIFACT}`);
    process.exit(childExitCode ?? 1);
}

await sleep(FLUSH_GRACE_MS);

if (!childExited) {
    child.kill('SIGKILL');
}

console.log('[build.mjs] build artifact present, exit clean');
process.exit(0);
