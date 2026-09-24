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
            .replace(/^[A-E]-/i, "")
            .replace(/_/g, " ")
            .trim()
            .replace(/\s+/g, " ");
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

    function isAnswerCorrect(answer, filename) {
        const answerTokens = getTokens(answer);
        const expectedTokens = getTokens(getFullName(filename));

        if (!answerTokens.length || !expectedTokens.length) {
            return false;
        }

        const remainingTokens = [...expectedTokens];

        return answerTokens.every(answerToken => {
            const matchingIndex = remainingTokens.indexOf(answerToken);

            if (matchingIndex === -1) {
                return false;
            }

            remainingTokens.splice(matchingIndex, 1);
            return true;
        });
    }

    return {
        getFullName,
        normalizeName,
        isAnswerCorrect
    };
}));
