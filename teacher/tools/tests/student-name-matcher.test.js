"use strict";

const assert = require("node:assert/strict");
const matcher = require("../assets/js/student-name-matcher.js");

const filename = "A-Andrade García Nicolas.png";

assert.equal(matcher.getFullName(filename), "Andrade García Nicolas");
assert.equal(matcher.isAnswerCorrect("Nicolas", filename), true);
assert.equal(matcher.isAnswerCorrect("Andrade García Nicolas", filename), true);
assert.equal(matcher.isAnswerCorrect("Nicolas Andrade Garcia", filename), true);
assert.equal(matcher.isAnswerCorrect("  NICOLÁS   ", filename), true);
assert.equal(matcher.isAnswerCorrect("Gar", filename), false);
assert.equal(matcher.isAnswerCorrect("", filename), false);
assert.equal(matcher.isAnswerCorrect("Nicolas Smith", filename), false);
assert.equal(
    matcher.isAnswerCorrect("Ana Ana", "B-Ana Maria.png"),
    false
);

console.log("student-name-matcher tests passed");
