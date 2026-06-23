#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const DATA_FILE = path.join(__dirname, 'grade3_heatmap_dashboard_data.js');
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

  return errors;
}

const errors = validate();

if (errors.length > 0) {
  console.error(`Grade 3 heatmap data validation failed with ${errors.length} error(s):`);
  errors.forEach((error) => console.error(`- ${error}`));
  process.exit(1);
}

console.log('Grade 3 heatmap data validation passed.');
