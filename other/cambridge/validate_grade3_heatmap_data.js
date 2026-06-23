#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const DATA_FILE = path.join(__dirname, 'grade3_heatmap_dashboard_data.js');
const DASHBOARD_FILE = path.join(__dirname, 'grade3_heatmap_dashboard.js');
const VALID_ANSWERS = new Set([null, -1, 0, 1, 2]);
const AGGREGATE_FIELDS = ['bien', 'mal', 'nr'];

function loadDatasets() {
  const source = fs.readFileSync(DATA_FILE, 'utf8');
  const context = vm.createContext({});
  return vm.runInContext(`${source}\nDATASETS;`, context, { filename: DATA_FILE });
}

function rowLabel(row, index) {
  const student = row && row.name ? ` (${row.name})` : '';
  return `row ${index + 1}${student}`;
}


function validateDashboardTooltipSafeguards(errors) {
  let source;

  try {
    source = fs.readFileSync(DASHBOARD_FILE, 'utf8');
  } catch (error) {
    errors.push(`Unable to load dashboard script from ${DASHBOARD_FILE}: ${error.message}`);
    return;
  }

  const requiredSnippets = [
    ['missing helper', 'function isMissingAnswer(value)'],
    ['missing heatmap branch documents omitted tooltip attributes', 'no data-tip, data-question-tip, or data-student-tip attributes'],
    ['non-missing heatmap cells expose question tooltip attribute', 'data-question-tip='],
    ['non-missing heatmap cells expose student tooltip attribute', 'data-student-tip='],
    ['histogram tooltip positive row', 'Positive units'],
    ['histogram tooltip non-response row', 'Non Responses'],
    ['histogram tooltip negative row', 'Negative units'],
    ['missing values still feed stacked histogram segments', 'responseParts(c)']
  ];

  requiredSnippets.forEach(([label, snippet]) => {
    if (!source.includes(snippet)) errors.push(`dashboard tooltip safeguard missing: ${label}.`);
  });

  const tooltipRowsMatch = source.match(/function tooltipRows\(c, total\) {[\s\S]*?const rows = \[([\s\S]*?)\];/);
  if (!tooltipRowsMatch) {
    errors.push('dashboard tooltip safeguard missing: tooltipRows rows could not be inspected.');
  } else if (tooltipRowsMatch[1].includes("'miss'")) {
    errors.push('dashboard tooltip safeguard failed: summary/histogram tooltipRows must not include a separate Missing row.');
  }
}

function validate() {
  const errors = [];
  let datasets;

  try {
    datasets = loadDatasets();
  } catch (error) {
    errors.push(`Unable to load DATASETS from ${DATA_FILE}: ${error.message}`);
    return errors;
  }

  if (!datasets || typeof datasets !== 'object' || Array.isArray(datasets)) {
    errors.push('DATASETS must exist and be an object.');
    return errors;
  }

  for (const [datasetKey, dataset] of Object.entries(datasets)) {
    if (!dataset || typeof dataset !== 'object' || Array.isArray(dataset)) {
      errors.push(`${datasetKey}: dataset must be an object.`);
      continue;
    }

    if (!Array.isArray(dataset.questions)) {
      errors.push(`${datasetKey}: questions must be an array.`);
    }

    if (!Array.isArray(dataset.rows)) {
      errors.push(`${datasetKey}: rows must be an array.`);
      continue;
    }

    const questionCount = Array.isArray(dataset.questions) ? dataset.questions.length : 0;

    dataset.rows.forEach((row, rowIndex) => {
      const label = `${datasetKey} ${rowLabel(row, rowIndex)}`;

      if (!row || typeof row !== 'object' || Array.isArray(row)) {
        errors.push(`${label}: row must be an object.`);
        return;
      }

      if (!Array.isArray(row.answers)) {
        errors.push(`${label}: answers must be an array.`);
        return;
      }

      if (row.answers.length !== questionCount) {
        errors.push(`${label}: answers length ${row.answers.length} does not match questions length ${questionCount}.`);
      }

      row.answers.forEach((answer, answerIndex) => {
        if (!VALID_ANSWERS.has(answer)) {
          errors.push(`${label}: answer ${answerIndex + 1} has invalid value ${JSON.stringify(answer)}.`);
        }
      });

      const computed = row.answers.reduce(
        (totals, answer) => {
          if (answer > 0) totals.bien += answer;
          else if (answer === -1) totals.mal += 1;
          else if (answer === 0 || answer === null) totals.nr += 1;
          return totals;
        },
        { bien: 0, mal: 0, nr: Math.max(questionCount - row.answers.length, 0) }
      );

      AGGREGATE_FIELDS.forEach((field) => {
        if (row[field] !== null && row[field] !== computed[field]) {
          errors.push(`${label}: ${field} is ${row[field]}, expected ${computed[field]}.`);
        }
      });
    });
  }

  validateDashboardTooltipSafeguards(errors);

  return errors;
}

const errors = validate();

if (errors.length > 0) {
  console.error(`Grade 3 heatmap data validation failed with ${errors.length} error(s):`);
  errors.forEach((error) => console.error(`- ${error}`));
  process.exit(1);
}

console.log('Grade 3 heatmap data validation passed.');
