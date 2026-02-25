import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const GREEN = '\x1b[32m';
const RED = '\x1b[31m';
const YELLOW = '\x1b[33m';
const NC = '\x1b[0m'; // No Color

const HOME_DIR = os.homedir();
const CLAUDE_DIR = path.join(HOME_DIR, '.claude');
let errorCount = 0;

console.log(`${GREEN}`);
console.log('╔═══════════════════════════════════════════════════════════════╗');
console.log('║         Claude Reconstruction v5.0 - Verify (Node.js)         ║');
console.log('╚═══════════════════════════════════════════════════════════════╝');
console.log(`${NC}`);

function verifyFile(filePath, description) {
  if (fs.existsSync(filePath) && fs.lstatSync(filePath).isFile()) {
    console.log(`${GREEN}✓${NC} ${description}`);
    return true;
  } else {
    console.log(`${RED}✗${NC} ${description} (missing: ${filePath})`);
    errorCount++;
    return false;
  }
}

function verifyDir(dirPath, description) {
  if (fs.existsSync(dirPath) && fs.lstatSync(dirPath).isDirectory()) {
    console.log(`${GREEN}✓${NC} ${description}`);
    return true;
  } else {
    console.log(`${RED}✗${NC} ${description} (missing: ${dirPath})`);
    errorCount++;
    return false;
  }
}

console.log(`${YELLOW}[1/4] Core config files...${NC}`);
verifyFile(path.join(CLAUDE_DIR, 'CLAUDE.md'), 'CLAUDE.md (entry point)');
verifyFile(path.join(CLAUDE_DIR, 'CONTEXT_MANAGER.md'), 'CONTEXT_MANAGER.md (smart loading)');
console.log('');

console.log(`${YELLOW}[2/4] Rules engine...${NC}`);
verifyDir(path.join(CLAUDE_DIR, 'rules'), 'rules/');
verifyDir(path.join(CLAUDE_DIR, 'rules', 'core'), 'rules/core/');
verifyDir(path.join(CLAUDE_DIR, 'rules', 'domain'), 'rules/domain/');
verifyDir(path.join(CLAUDE_DIR, 'rules', 'delegator'), 'rules/delegator/');
verifyFile(path.join(CLAUDE_DIR, 'rules', 'core', 'work-mode.md'), 'core/work-mode.md');
verifyFile(path.join(CLAUDE_DIR, 'rules', 'core', 'blocking-rules.md'), 'core/blocking-rules.md');
verifyFile(path.join(CLAUDE_DIR, 'rules', 'domain', 'coding.md'), 'domain/coding.md');
verifyFile(path.join(CLAUDE_DIR, 'rules', 'domain', 'security.md'), 'domain/security.md');
console.log('');

console.log(`${YELLOW}[3/4] Index & capabilities...${NC}`);
verifyDir(path.join(CLAUDE_DIR, 'index'), 'index/');
verifyFile(path.join(CLAUDE_DIR, 'index', 'task-router.md'), 'task-router.md');
verifyDir(path.join(CLAUDE_DIR, 'capabilities'), 'capabilities/');
verifyFile(path.join(CLAUDE_DIR, 'capabilities', 'mcp-servers.md'), 'mcp-servers.md');
verifyFile(path.join(CLAUDE_DIR, 'capabilities', 'skills-guide.md'), 'skills-guide.md');
console.log('');

console.log(`${YELLOW}[4/4] Error library...${NC}`);
verifyDir(path.join(CLAUDE_DIR, 'errors'), 'errors/');
verifyFile(path.join(CLAUDE_DIR, 'errors', 'ERROR_CATALOG.md'), 'ERROR_CATALOG.md');
verifyFile(path.join(CLAUDE_DIR, 'errors', 'top-5-errors.md'), 'top-5-errors.md');
console.log('');

// Results
console.log(`${GREEN}═══════════════════════════════════════════════════════════════${NC}`);
if (errorCount === 0) {
  console.log(`${GREEN}✓ All checks passed!${NC}`);
  console.log('');
  console.log(`${YELLOW}Config location:${NC} ${CLAUDE_DIR}`);
  console.log(`${YELLOW}Version:${NC} 5.0 (Context Engineering)`);
  process.exit(0);
} else {
  console.log(`${RED}✗ ${errorCount} check(s) failed.${NC}`);
  console.log('');
  console.log('Run: npm run install:config');
  process.exit(1);
}
