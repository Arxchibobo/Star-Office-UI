import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_DIR = path.resolve(__dirname, '..');

const GREEN = '\x1b[32m';
const RED = '\x1b[31m';
const YELLOW = '\x1b[33m';
const NC = '\x1b[0m'; // No Color

const HOME_DIR = os.homedir();
const CLAUDE_DIR = path.join(HOME_DIR, '.claude');

console.log(`${GREEN}`);
console.log('╔═══════════════════════════════════════════════════════════════╗');
console.log('║         Claude Reconstruction v5.0                           ║');
console.log('║         Claude Code Engineering Config (Node.js)             ║');
console.log('╚═══════════════════════════════════════════════════════════════╝');
console.log(`${NC}`);

console.log(`${YELLOW}OS: ${os.platform()} ${os.release()}${NC}`);
console.log('');
console.log(`${YELLOW}Source: ${PROJECT_DIR}${NC}`);
console.log(`${YELLOW}Target: ${CLAUDE_DIR}${NC}`);
console.log('');

// Helper to copy directory recursively
function copyDir(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (let entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

try {
  // Create directory structure
  console.log(`${GREEN}[1/5] Creating directories...${NC}`);
  [
    'rules/core',
    'rules/domain',
    'rules/delegator',
    'index',
    'capabilities',
    'errors',
    'design',
    'vibe-marketing'
  ].forEach(dir => {
    const fullPath = path.join(CLAUDE_DIR, dir);
    if (!fs.existsSync(fullPath)) {
      fs.mkdirSync(fullPath, { recursive: true });
    }
  });

  // Backup existing config
  const claudeMdPath = path.join(CLAUDE_DIR, 'CLAUDE.md');
  if (fs.existsSync(claudeMdPath)) {
    console.log(`${YELLOW}[Backup] Backing up existing CLAUDE.md...${NC}`);
    const backupName = `CLAUDE.md.backup.${new Date().toISOString().replace(/[:.]/g, '-').split('T')[0]}`;
    fs.copyFileSync(claudeMdPath, path.join(CLAUDE_DIR, backupName));
  }

  // Install core config
  console.log(`${GREEN}[2/5] Installing core config...${NC}`);
  fs.copyFileSync(path.join(PROJECT_DIR, 'CLAUDE.md'), path.join(CLAUDE_DIR, 'CLAUDE.md'));
  fs.copyFileSync(path.join(PROJECT_DIR, 'CONTEXT_MANAGER.md'), path.join(CLAUDE_DIR, 'CONTEXT_MANAGER.md'));

  // Install rules
  console.log(`${GREEN}[3/5] Installing rules...${NC}`);
  if (fs.existsSync(path.join(PROJECT_DIR, 'rules'))) {
      copyDir(path.join(PROJECT_DIR, 'rules'), path.join(CLAUDE_DIR, 'rules'));
  }

  // Install index & capabilities
  console.log(`${GREEN}[4/5] Installing index, capabilities, errors...${NC}`);
  if (fs.existsSync(path.join(PROJECT_DIR, 'index'))) {
      copyDir(path.join(PROJECT_DIR, 'index'), path.join(CLAUDE_DIR, 'index'));
  }
  if (fs.existsSync(path.join(PROJECT_DIR, 'capabilities'))) {
      copyDir(path.join(PROJECT_DIR, 'capabilities'), path.join(CLAUDE_DIR, 'capabilities'));
  }
  if (fs.existsSync(path.join(PROJECT_DIR, 'errors'))) {
      copyDir(path.join(PROJECT_DIR, 'errors'), path.join(CLAUDE_DIR, 'errors'));
  }

  // Install optional resources
  console.log(`${GREEN}[5/5] Installing design & marketing docs...${NC}`);
  if (fs.existsSync(path.join(PROJECT_DIR, 'design'))) {
    copyDir(path.join(PROJECT_DIR, 'design'), path.join(CLAUDE_DIR, 'design'));
  }
  if (fs.existsSync(path.join(PROJECT_DIR, 'vibe-marketing'))) {
    copyDir(path.join(PROJECT_DIR, 'vibe-marketing'), path.join(CLAUDE_DIR, 'vibe-marketing'));
  }

  console.log('');
  console.log(`${GREEN}═══════════════════════════════════════════════════════════════${NC}`);
  console.log(`${GREEN}Install complete!${NC}`);
  console.log(`${GREEN}═══════════════════════════════════════════════════════════════${NC}`);
  console.log('');
  console.log(`${YELLOW}Installed:${NC}`);
  console.log(`  - ${path.join(CLAUDE_DIR, 'CLAUDE.md')} (entry point)`);
  console.log(`  - ${path.join(CLAUDE_DIR, 'CONTEXT_MANAGER.md')} (smart loading)`);
  console.log(`  - ${path.join(CLAUDE_DIR, 'rules')} (rules engine)`);
  console.log('');

} catch (err) {
  console.error(`${RED}Error during installation:${NC}`, err);
  process.exit(1);
}
