#!/usr/bin/env node
"use strict";
const { generate } = require('./lesson-workflow');
try {
  const args = process.argv.slice(2);
  if (args.some(arg => arg !== '--check')) throw new Error('Usage: node teacher/authoring/generate-schedule-data.js [--check]');
  console.log(`${args.includes('--check') ? 'Verified' : 'Generated'} ${generate(undefined, { check: args.includes('--check') })} linked datasets.`);
} catch (error) { console.error(error.message); process.exitCode = 1; }
