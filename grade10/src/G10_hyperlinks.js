// SharePoint document URLs are grouped by Grade 10 term, then by resource purpose.
window.TERM_HYPERLINKS = {
  G10_T1: {
    project: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQDH9kA9sZWtS6hAj3AyeZRXAXSbKDKlG8BKgUjXs-NP_6A?e=Cpg1VI",
    worksheetC8C9: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQBBCtjU-jmiTKaC7FAUC9RUATq4CEyClb1c_G7zE4o0CIY?e=bLGfTB",
    homeworkC7: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQD17lynHTt3To6m_B7wkBd6AYP5aUcuAP7tfcKV8pt-4-o?e=iAGVPF",
    catchUpC1: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQA2T5rM2OepTIiTLHuyDGvbAbV3gmltSEwddl7oqDUy9UM?e=PnXZFZ",
    catchUpC2: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQAVJhusxrUdSKZH9ZHKWls2AX1tE2-MQSPoSwcmefOTgYY?e=kG7opR",
    catchUpC3: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQCHwKFrq9X5Qp5-0LYBURtqAYDY98lT_nuD-GXQmaLGHEg?e=zhK0Ae",
    catchUpC4: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQCfuHJSdyGWRJHGRWwxclfdAQ4b_bw5RCtEzyNyn_lNipQ?e=bV9XD6",
    catchUpC5: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQBWAv0PwifxTavZepXEj2jqAcA7_ebKp3WFRCrBQUAP-4w?e=nRaaui",
    catchUpC6: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQCEreVRirj4RYt7vF9ruSgEAcYvmY2LJtBMrlNFUwMJntc?e=m1bsVv",
    catchUpC7: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQAvnuzpB5DzTbDU9BSxZJvwAZq8NPCLPVl3f1T86nV_zbM?e=3kbzuz",
    mockExamC1C5: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQC55Ww5jPgqSb3ZMFMd6d1MAZYM7YrNRjlmo79zpuo5tro?e=Jn5kiR",
    midtermSolution: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQBJDaB81exKSbvxrIV9Lh4QAcxUaZRPUaV_ob3uz1NkxpQ?e=VYAAuj"
  },
  G10_T2: {},
  G10_T3: {
    learningEvidenceC1C3: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQCDJe_EI83tQIsYlDlwLYWoAfLkf_JTGErnUcaldKVg2a4?e=SdTWbT",
    learningEvidenceC4: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQAQvrOgrcbFSrC-AE5tldJrAZCt7S-vvyilDn-TVyXKI98?e=ZVIaht",
    learningEvidenceC5C7: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQCMq2SUZi_kTKtWAWMc4onLAZ5HE_nKhN8A4ha77d98DUU?e=KjUlcN",
    learningEvidenceC8C10: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQA5t-04kjmBSa8hHMokaLS1ARFEpywjsPIcn8SxtFggfOA?e=VJL7Yh"
  }
};

// Compatibility for existing Grade 10 pages that still use the legacy attribute.
document.querySelectorAll("[data-g10-link]").forEach((element) => {
  const key = element.dataset.g10Link;
  const segments = key ? key.split(".") : [];
  let resolved = window.TERM_HYPERLINKS;

  for (const segment of segments) {
    if (!segment || typeof resolved !== "object" || resolved === null ||
        !Object.prototype.hasOwnProperty.call(resolved, segment)) {
      resolved = undefined;
      break;
    }
    resolved = resolved[segment];
  }

  if (segments.length < 2 || typeof resolved !== "string" || !resolved) {
    console.warn(`[G10 hyperlinks] Missing or invalid link key: ${key || "(empty)"}`);
    element.removeAttribute("href");
    element.setAttribute("aria-disabled", "true");
    return;
  }

  element.href = resolved;
});
