#!/usr/bin/env node
"use strict";
const path = require('node:path');
const w = require('./lesson-workflow');
const assignment = m => ({ 'Lesson ID': m['Lesson ID'], Overrides: structuredClone(m.Overrides) });
const group = (a, b) => a.Grade === b.Grade && a.Section === b.Section && a.Term === b.Term;
function findMeeting(source, grade, section, date) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) throw new Error('Use an ISO date: YYYY-MM-DD');
  const matches = source.meetings.filter(m => m.Grade === Number(grade) && m.Section.toUpperCase() === section.toUpperCase() && m.Date.replaceAll(' / ', '-') === date);
  if (matches.length !== 1) throw new Error(`Expected one meeting for ${grade}${section} ${date}`);
  return matches[0];
}
function cancel(source, meetingKey, reason = '', options) {
  const byId = w.validateSource(source, options);
  const result = structuredClone(source);
  const target = result.meetings.find(m => w.key(m) === meetingKey);
  if (!target) throw new Error(`Unknown meeting: ${meetingKey}`);
  if (target.Status === 'canceled') return result;
  if (target.Status !== 'scheduled' || target.Term === null) throw new Error('Only an assigned in-term meeting can be canceled');
  const active = result.meetings.filter(m => group(m, target) && m.Status === 'scheduled' && m.Date >= target.Date).sort((a, b) => a.Date.localeCompare(b.Date));
  const extra = m => byId.get(m['Lesson ID']).kind === 'extra';
  // Only a trailing Extra slot may be consumed; no teaching/assessment is discarded.
  const capacity = active.findIndex((m, i) => extra(m) && active.slice(i).every(extra));
  if (capacity < 0) throw new Error(`Insufficient capacity in Grade ${target.Grade}${target.Section}, Term ${target.Term}: no trailing Extra Class slot`);
  for (let i = capacity; i > 0; i--) Object.assign(active[i], assignment(active[i - 1]));
  Object.assign(target, { Status: 'canceled', Reason: reason ? ` - ${reason}` : '', 'Canceled summary': '', 'Lesson ID': '', Overrides: {} });
  w.validateSource(result, options);
  return result;
}
function move(source, fromKey, toKey, options) {
  w.validateSource(source, options);
  const result = structuredClone(source);
  const from = result.meetings.find(m => w.key(m) === fromKey), to = result.meetings.find(m => w.key(m) === toKey);
  if (!from || !to || !group(from, to) || from.Status !== 'scheduled' || to.Status !== 'scheduled') throw new Error('Move requires two assigned meetings in the same section and term');
  const active = result.meetings.filter(m => group(m, from) && m.Status === 'scheduled').sort((a, b) => a.Date.localeCompare(b.Date));
  const assignments = active.map(assignment), fromIndex = active.indexOf(from), toIndex = active.indexOf(to);
  const [moved] = assignments.splice(fromIndex, 1); assignments.splice(toIndex, 0, moved);
  active.forEach((m, i) => Object.assign(m, assignments[i]));
  w.validateSource(result, options);
  return result;
}
if (require.main === module) {
  try {
    const [operation, grade, section, fromDate, ...rest] = process.argv.slice(2);
    if (!['cancel', 'move'].includes(operation) || !grade || !section || !fromDate || (operation === 'move' && rest.length !== 1)) throw new Error('Usage: reschedule.js cancel GRADE SECTION DATE [reason...] | move GRADE SECTION FROM_DATE TO_DATE');
    const source = w.readSource();
    const from = findMeeting(source, grade, section, fromDate);
    const result = operation === 'cancel' ? cancel(source, w.key(from), rest.join(' ')) : move(source, w.key(from), w.key(findMeeting(source, grade, section, rest[0])));
    w.generate(result, { sourcePath: path.join(__dirname, 'schedule.csv') });
    console.log(`${operation === 'cancel' && from.Status === 'canceled' ? 'Already canceled (no second shift)' : 'Updated assignments'}; validated and generated all four datasets.`);
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
module.exports = { cancel, move, findMeeting };
