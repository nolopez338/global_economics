const G11_HYPERLINKS = {
  G11_T1: {},
  G11_T2: {
    project: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQBXnxpZYDRmQbjMAdSqT17QAUMmHcxOwZjsldvt8rhqsQI?e=8dbMDd",
    worksheetC8C9: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQCow12zc_q1RrEttLaXBPNNAVZKYiSERhQUdvWO6nDtgf0?e=VKqRRj",
    homeworkC7: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQBhb_6xggQfRpGD5JLFMjLEAZ9NuxqfC6gluondjSdKYO0?e=YDLKv8",
    catchUpC1: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQBh41x19UO5RrQfIwr01-JCAXKluU43vMDQTdoBvIvOXv8?e=87jf7h",
    catchUpC2: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQA7CksEwywXQLhAyt2UWPGeAZqX5mn94zi0l1fCFmKNmok?e=RWs4BA",
    catchUpC3: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQDXLeKmmxDBQbI4tIK7GHbFAaKwM9IFvX2jrLOToJzrbZA?e=7djlp5",
    catchUpC4: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQBHkX5SEzmQSoRnp1E8mmydAbEQFXbQdWhEvDuWtaQavto?e=CYWHcx",
    catchUpC5: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQBMepcMIWrRSrTlOQ49_iXnAYRkDqSbsLmg9HXboQ0wQts?e=aCivUp",
    catchUpC6: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQD4ZmLN1oYAT49kuz43xTPxAV71w8MI4bTfUptAhXWVVCk?e=WivCy3",
    catchUpC7: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQCeSxXRzBwERI6-1WTFok_UAUkvK83-giVlI8TFk2jbo8k?e=3zJkN1",
    mockExam: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQBhE56uEJOYTLcPDY1FcMOiATmCTVD9K0p-ROhm6JVeWeo?e=lb1rVE",
    mockExamSolution: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQCWDVVZ1F-fTJQZMo40bzUIAZBwrZNBYl1yqoPau706FHE?e=KmDzTR"
  },
  G11_T3: {
    learningEvidenceC1C3: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQAl3TysrLTYSKqqAskJ46e9AbdE6UemZcAH9CxMpf7VaJQ?e=j5Pblg",
    learningEvidenceC4C5: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQCjO5zCLuWDSrWb1Ob7XsXTAVYVcE9QA9wR7z_0QZ_Ayd8?e=94J8Cj",
    learningEvidenceC6C7: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQBDjCronJl7SoBTAr8XZkOkAdnmRcmvHqIWYgeoLtOIEnE?e=TBGNWd",
    learningEvidenceC8C10: "https://correosanbartoloedu-my.sharepoint.com/:b:/g/personal/nicolas_lopez_sanbartolo_edu_co/IQADpDtcgulsQ4vd0wQcMdTYAfbzrAVJoID3Jjf2qQuf7gg?e=4lM3dQ"
  }
};

document.querySelectorAll("[data-g11-link]").forEach((element) => {
  const key = element.dataset.g11Link;
  const url = key
    ?.split(".")
    .reduce((value, segment) => value?.[segment], G11_HYPERLINKS);

  if (typeof url !== "string") {
    console.warn(`[G11 links] Invalid key: ${key || "(empty)"}`);
    return;
  }

  element.href = url;
});
