import fs from 'fs';
import path from 'path';
import os from 'os';

const GREEN = '\x1b[32m';
const RED = '\x1b[31m';
const YELLOW = '\x1b[33m';
const BLUE = '\x1b[34m';
const NC = '\x1b[0m';

const HOME_DIR = os.homedir();
const CLAUDE_DIR = path.join(HOME_DIR, '.claude');
const SETTINGS_FILE = path.join(CLAUDE_DIR, 'settings.json');
const HOOKS_DIR = path.join(CLAUDE_DIR, 'hooks');

let errorCount = 0;
let warningCount = 0;

console.log(`${BLUE}`);
console.log('╔═══════════════════════════════════════════════════════════════╗');
console.log('║         Hook Configuration Verifier v1.0                     ║');
console.log('╚═══════════════════════════════════════════════════════════════╝');
console.log(`${NC}\n`);

// Check if settings.json exists
if (!fs.existsSync(SETTINGS_FILE)) {
  console.log(`${RED}✗${NC} Settings file not found: ${SETTINGS_FILE}`);
  console.log(`${YELLOW}→${NC} Run 'pnpm install:config' first\n`);
  process.exit(1);
}

// Read settings.json
let settings;
try {
  const settingsContent = fs.readFileSync(SETTINGS_FILE, 'utf-8');
  settings = JSON.parse(settingsContent);
  console.log(`${GREEN}✓${NC} Settings file found and valid JSON\n`);
} catch (error) {
  console.log(`${RED}✗${NC} Failed to parse settings.json: ${error.message}\n`);
  process.exit(1);
}

// Expected hooks configuration
const expectedHooks = {
  PreToolUse: [
    { name: 'pre-bash.sh', matcher: 'Bash' },
    { name: 'pre-edit.sh', matcher: 'Edit' },
    { name: 'enhance-tool-call.sh', matcher: '*' },
    { name: 'vibecraft-hook.js', matcher: '*', optional: true },
  ],
  PostToolUse: [
    { name: 'post-bash.sh', matcher: 'Bash' },
    { name: 'post-edit.sh', matcher: 'Edit' },
    { name: 'vibecraft-hook.js', matcher: '*', optional: true },
  ],
  Stop: [
    { name: 'vibecraft-hook.js', optional: true },
  ],
  SubagentStop: [
    { name: 'vibecraft-hook.js', optional: true },
  ],
  SessionStart: [
    { name: 'learn-patterns.sh' },
    { name: 'vibecraft-hook.js', optional: true },
  ],
  SessionEnd: [
    { name: 'session-summary.sh' },
    { name: 'learn-patterns.sh' },
    { name: 'vibecraft-hook.js', optional: true },
  ],
};

// Verify hooks configuration
console.log(`${YELLOW}[1/3] Checking hooks configuration in settings.json...${NC}\n`);

const hooks = settings.hooks || {};
const hookTypes = Object.keys(expectedHooks);

for (const hookType of hookTypes) {
  const configuredHooks = hooks[hookType] || [];
  const expected = expectedHooks[hookType];

  console.log(`${BLUE}  ${hookType}:${NC}`);

  for (const expectedHook of expected) {
    // Handle nested hook structure: { matcher: "...", hooks: [{command: "..."}] }
    const found = Array.isArray(configuredHooks)
      ? configuredHooks.some(h => {
          if (typeof h === 'string') {
            return h.includes(expectedHook.name);
          }
          if (typeof h === 'object') {
            // Direct command
            if (h.command && h.command.includes(expectedHook.name)) {
              return true;
            }
            // Nested hooks array
            if (Array.isArray(h.hooks)) {
              return h.hooks.some(nestedHook =>
                nestedHook.command && nestedHook.command.includes(expectedHook.name)
              );
            }
          }
          return false;
        })
      : false;

    if (found) {
      console.log(`    ${GREEN}✓${NC} ${expectedHook.name}${expectedHook.matcher ? ` (${expectedHook.matcher})` : ''}`);
    } else if (expectedHook.optional) {
      console.log(`    ${YELLOW}⚠${NC} ${expectedHook.name} (optional, not configured)`);
      warningCount++;
    } else {
      console.log(`    ${RED}✗${NC} ${expectedHook.name} (missing)`);
      errorCount++;
    }
  }
  console.log();
}

// Verify hook files exist
console.log(`${YELLOW}[2/3] Checking hook files in ${HOOKS_DIR}...${NC}\n`);

if (!fs.existsSync(HOOKS_DIR)) {
  console.log(`${RED}✗${NC} Hooks directory not found: ${HOOKS_DIR}\n`);
  errorCount++;
} else {
  const allHookNames = new Set();
  for (const expected of Object.values(expectedHooks)) {
    expected.forEach(h => allHookNames.add(h.name));
  }

  for (const hookName of allHookNames) {
    const hookPath = path.join(HOOKS_DIR, hookName);
    if (fs.existsSync(hookPath)) {
      // Check if file is executable (Unix-like systems)
      if (process.platform !== 'win32' && hookName.endsWith('.sh')) {
        try {
          const stats = fs.statSync(hookPath);
          const isExecutable = !!(stats.mode & fs.constants.S_IXUSR);
          if (isExecutable) {
            console.log(`  ${GREEN}✓${NC} ${hookName} (exists and executable)`);
          } else {
            console.log(`  ${YELLOW}⚠${NC} ${hookName} (exists but not executable)`);
            console.log(`    ${YELLOW}→${NC} Run: chmod +x ${hookPath}`);
            warningCount++;
          }
        } catch (error) {
          console.log(`  ${YELLOW}⚠${NC} ${hookName} (exists, cannot check permissions)`);
          warningCount++;
        }
      } else {
        console.log(`  ${GREEN}✓${NC} ${hookName}`);
      }
    } else {
      // Check if it's optional
      let isOptional = false;
      for (const expected of Object.values(expectedHooks)) {
        const hook = expected.find(h => h.name === hookName);
        if (hook && hook.optional) {
          isOptional = true;
          break;
        }
      }

      if (isOptional) {
        console.log(`  ${YELLOW}⚠${NC} ${hookName} (optional, not found)`);
        warningCount++;
      } else {
        console.log(`  ${RED}✗${NC} ${hookName} (missing)`);
        errorCount++;
      }
    }
  }
  console.log();
}

// Check for additional unexpected hooks
console.log(`${YELLOW}[3/3] Checking for unexpected hook files...${NC}\n`);

if (fs.existsSync(HOOKS_DIR)) {
  const actualFiles = fs.readdirSync(HOOKS_DIR);
  const expectedFiles = new Set();
  for (const expected of Object.values(expectedHooks)) {
    expected.forEach(h => expectedFiles.add(h.name));
  }

  const unexpectedFiles = actualFiles.filter(f => !expectedFiles.has(f) && !f.startsWith('.'));

  if (unexpectedFiles.length > 0) {
    console.log(`  ${YELLOW}⚠${NC} Found ${unexpectedFiles.length} unexpected hook file(s):`);
    unexpectedFiles.forEach(f => console.log(`    - ${f}`));
    console.log();
  } else {
    console.log(`  ${GREEN}✓${NC} No unexpected hook files found\n`);
  }
}

// Summary
console.log(`${BLUE}═══════════════════════════════════════════════════════════════${NC}\n`);

if (errorCount === 0 && warningCount === 0) {
  console.log(`${GREEN}✓ All hooks configured correctly!${NC}\n`);
  process.exit(0);
} else if (errorCount === 0) {
  console.log(`${YELLOW}⚠ Configuration complete with ${warningCount} warning(s)${NC}`);
  console.log(`${YELLOW}  Warnings are typically optional components or permissions${NC}\n`);
  process.exit(0);
} else {
  console.log(`${RED}✗ Found ${errorCount} error(s) and ${warningCount} warning(s)${NC}`);
  console.log(`${RED}  Please fix errors before continuing${NC}\n`);

  console.log(`${YELLOW}Suggested fixes:${NC}`);
  console.log(`  1. Run: pnpm install:config`);
  console.log(`  2. Check hooks documentation: rules/hooks.md`);
  console.log(`  3. Verify ~/.claude/settings.json manually\n`);

  process.exit(1);
}
