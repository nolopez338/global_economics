(function (root, factory) {
    const matcher = factory();

    if (typeof module === "object" && module.exports) {
        module.exports = matcher;
    }

    root.StudentNameMatcher = matcher;
}(typeof globalThis !== "undefined" ? globalThis : this, function () {
    "use strict";

    function getFullName(filename) {
        return String(filename || "")
            .replace(/\.png$/i, "")
            .replace(/^[^-]*-/, "");
    }

    function normalizeName(name) {
        return String(name || "")
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLocaleLowerCase()
            .replace(/[^\p{L}\p{N}]+/gu, " ")
            .trim()
            .replace(/\s+/g, " ");
    }

    function getTokens(name) {
        const normalized = normalizeName(name);
        return normalized ? normalized.split(" ") : [];
    }

    function getNameComponents(name) {
        return Array.from(
            String(name || "").matchAll(/[\p{L}\p{M}\p{N}]+/gu),
            match => ({
                text: match[0],
                start: match.index,
                end: match.index + match[0].length,
                normalized: normalizeName(match[0])
            })
        );
    }

    function matchAnswer(answer, filename) {
        const answerTokens = getTokens(answer);
        const components = getNameComponents(getFullName(filename));
        const remainingComponentIndexes = components.map(
            (component, index) => index
        );
        const matchedComponentIndexes = [];

        if (!answerTokens.length || !components.length) {
            return {
                correct: false,
                matchedComponentIndexes
            };
        }

        let correct = true;

        answerTokens.forEach(answerToken => {
            const remainingIndex = remainingComponentIndexes.findIndex(
                componentIndex =>
                    components[componentIndex].normalized === answerToken
            );

            if (remainingIndex === -1) {
                correct = false;
                return;
            }

            matchedComponentIndexes.push(
                remainingComponentIndexes[remainingIndex]
            );
            remainingComponentIndexes.splice(remainingIndex, 1);
        });

        return {
            correct,
            matchedComponentIndexes
        };
    }

    function isAnswerCorrect(answer, filename) {
        return matchAnswer(answer, filename).correct;
    }

    return {
        getFullName,
        getNameComponents,
        matchAnswer,
        normalizeName,
        isAnswerCorrect
    };
}));
