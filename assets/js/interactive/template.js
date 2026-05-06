const practiceTopic = "[CERTIFICATE TOPIC]";

    const questionDatabase = [
      {
        question: "[QUESTION 1 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 1 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 2 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 2 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 3 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 3 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 4 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 4 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 5 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 5 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 6 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 6 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 7 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 7 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 8 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 8 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 9 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 9 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 10 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 10 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 11 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 11 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 12 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 12 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 13 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 13 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 14 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 14 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 15 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 15 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 16 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 16 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 17 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 17 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 18 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 18 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 19 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 19 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      },
      {
        question: "[QUESTION 20 TEXT]",
        options: [
          "[OPTION A]",
          "[OPTION B]",
          "[OPTION C]",
          "[OPTION D]"
        ],
        correctIndex: 0,
        explanation:
          "[QUESTION 20 FEEDBACK] [CORRECT ANSWER] explanation placeholder."
      }
    
    ];

    const practiceSection = document.getElementById("practiceSection");
    const startButton = document.getElementById("startButton");
    const resetButton = document.getElementById("resetButton");
    const submitButton = document.getElementById("submitButton");
    const downloadButton = document.getElementById("downloadButton");
    const quizForm = document.getElementById("quizForm");
    const questionsContainer = document.getElementById("questionsContainer");
    const resultContainer = document.getElementById("resultContainer");
    const studentNameInput = document.getElementById("studentName");

    const qrButton = document.getElementById("qrButton");
    const qrModalOverlay = document.getElementById("qrModalOverlay");
    const qrCodeContainer = document.getElementById("qrCodeContainer");
    const closeQrModalButton = document.getElementById("closeQrModalButton");

    let selectedQuestions = [];
    let selectedAnswers = [];
    let lastScore = 0;
    let hasSubmitted = false;

    let activityLog = [];
    let attemptFlagged = false;
    let suspiciousInterruptionCount = 0;
    let isPracticeActive = false;
    let hasGeneratedQrCode = false;

    function shuffleArray(array) {
      const copiedArray = [...array];

      for (let i = copiedArray.length - 1; i > 0; i--) {
        const randomIndex = Math.floor(Math.random() * (i + 1));
        [copiedArray[i], copiedArray[randomIndex]] = [
          copiedArray[randomIndex],
          copiedArray[i]
        ];
      }

      return copiedArray;
    }

    function getTimestamp() {
      return new Date().toISOString();
    }

    function formatTimestamp(timestamp) {
      return new Date(timestamp).toLocaleString();
    }

    function isFullscreenActive() {
      return Boolean(document.fullscreenElement);
    }

    function addActivityLogEntry(eventType, description, extraData = {}) {
      activityLog.push({
        eventType,
        timestamp: getTimestamp(),
        description,
        ...extraData
      });
    }

    function recordSuspiciousInterruption(eventType, description, extraData = {}) {
      suspiciousInterruptionCount += 1;
      attemptFlagged = true;
      addActivityLogEntry(eventType, description, {
        suspiciousInterruption: true,
        ...extraData
      });
    }

    function resetPracticeState() {
      selectedQuestions = [];
      selectedAnswers = [];
      lastScore = 0;
      hasSubmitted = false;
      activityLog = [];
      attemptFlagged = false;
      suspiciousInterruptionCount = 0;
      isPracticeActive = false;

      resultContainer.innerHTML = "";
      downloadButton.classList.add("hidden");
      submitButton.disabled = false;
    }

    function startPractice() {
      const studentName = studentNameInput.value.trim();

      if (!studentName) {
        alert("Please enter your name before starting the practice activity.");
        studentNameInput.focus();
        return;
      }

      resetPracticeState();

      selectedQuestions = shuffleArray(questionDatabase).slice(0, 5);
      isPracticeActive = true;

      addActivityLogEntry(
        "activity_started",
        "The practice activity started.",
        {
          currentUrl: window.location.href,
          initialFullscreenStatus: isFullscreenActive(),
          initialVisibilityState: document.visibilityState
        }
      );

      requestPracticeFullscreen();

      resetButton.classList.remove("hidden");
      quizForm.classList.remove("hidden");

      renderQuestions();
    }

    function requestPracticeFullscreen() {
      if (!practiceSection.requestFullscreen) {
        recordSuspiciousInterruption(
          "fullscreen_unavailable",
          "Fullscreen mode was unavailable in this browser."
        );
        return;
      }

      if (isFullscreenActive()) {
        return;
      }

      practiceSection.requestFullscreen().catch(() => {
        if (!isPracticeActive || hasSubmitted) {
          return;
        }

        recordSuspiciousInterruption(
          "fullscreen_request_failed",
          "Fullscreen mode did not start or was rejected by the browser."
        );
      });
    }

    function renderQuestions() {
      questionsContainer.innerHTML = "";

      selectedQuestions.forEach((questionItem, questionIndex) => {
        const questionCard = document.createElement("article");
        questionCard.className = "question-card";

        const questionTitle = document.createElement("div");
        questionTitle.className = "question-title";
        questionTitle.textContent = `${questionIndex + 1}. ${questionItem.question}`;
        questionCard.appendChild(questionTitle);

        const optionsContainer = document.createElement("div");
        optionsContainer.className = "options";

        questionItem.options.forEach((optionText, optionIndex) => {
          const optionId = `question-${questionIndex}-option-${optionIndex}`;

          const optionLabel = document.createElement("label");
          optionLabel.className = "option-label";
          optionLabel.setAttribute("for", optionId);

          const radioInput = document.createElement("input");
          radioInput.type = "radio";
          radioInput.id = optionId;
          radioInput.name = `question-${questionIndex}`;
          radioInput.value = String(optionIndex);
          radioInput.disabled = hasSubmitted;

          if (selectedAnswers[questionIndex] === String(optionIndex)) {
            radioInput.checked = true;
          }

          if (hasSubmitted) {
            const selectedAnswer = Number(selectedAnswers[questionIndex]);
            const correctAnswer = questionItem.correctIndex;

            if (optionIndex === correctAnswer) {
              optionLabel.classList.add("correct-answer");
            }

            if (
              optionIndex === selectedAnswer &&
              selectedAnswer !== correctAnswer
            ) {
              optionLabel.classList.add("incorrect-answer");
            }
          }

          const optionSpan = document.createElement("span");
          optionSpan.textContent = optionText;

          optionLabel.appendChild(radioInput);
          optionLabel.appendChild(optionSpan);
          optionsContainer.appendChild(optionLabel);
        });

        questionCard.appendChild(optionsContainer);

        if (hasSubmitted) {
          const isCorrect =
            Number(selectedAnswers[questionIndex]) === questionItem.correctIndex;

          const feedback = document.createElement("div");
          feedback.className = `feedback ${isCorrect ? "correct" : "incorrect"}`;

          const correctAnswerText =
            questionItem.options[questionItem.correctIndex];

          feedback.innerHTML = `
            <strong>${isCorrect ? "Correct." : "Incorrect."}</strong>
            Correct answer: ${correctAnswerText}<br />
            ${questionItem.explanation}
          `;

          questionCard.appendChild(feedback);
        }

        questionsContainer.appendChild(questionCard);
      });
    }

    function submitAnswers(event) {
      event.preventDefault();

      const formData = new FormData(quizForm);

      selectedAnswers = selectedQuestions.map((_, questionIndex) =>
        formData.get(`question-${questionIndex}`)
      );

      const unansweredQuestionIndex = selectedAnswers.findIndex(
        answer => answer === null
      );

      if (unansweredQuestionIndex !== -1) {
        alert(`Please answer question ${unansweredQuestionIndex + 1}.`);
        return;
      }

      lastScore = selectedQuestions.reduce((score, questionItem, questionIndex) => {
        return Number(selectedAnswers[questionIndex]) === questionItem.correctIndex
          ? score + 1
          : score;
      }, 0);

      hasSubmitted = true;
      isPracticeActive = false;
      submitButton.disabled = true;
      downloadButton.classList.remove("hidden");

      renderQuestions();
      renderSubmissionResult();
    }

    function renderSubmissionResult() {
      const integrityMessage = attemptFlagged
        ? "Integrity status: Flagged. One or more focus, visibility, or fullscreen interruptions were detected."
        : "Integrity status: No focus or fullscreen interruptions detected.";

      const certificateMessage = attemptFlagged
        ? "A red flagged certificate will be generated for this attempt because an interruption was detected."
        : "A normal certificate will be generated for this attempt.";

      const integrityClass = attemptFlagged
        ? "integrity-status flagged"
        : "integrity-status";

      const certificateNoticeClass = attemptFlagged
        ? "certificate-notice flagged"
        : "certificate-notice";

      resultContainer.innerHTML = `
        <div class="score-box">
          Score: ${lastScore} / 5
        </div>

        <div class="${integrityClass}">
          ${integrityMessage}
        </div>

        <div class="${certificateNoticeClass}">
          ${certificateMessage}
        </div>
      `;
    }

    function downloadCertificate() {
      const studentName = studentNameInput.value.trim();

      if (!studentName) {
        alert("Please enter your name before downloading the certificate.");
        studentNameInput.focus();
        return;
      }

      if (!hasSubmitted) {
        alert("Please submit the practice activity before downloading the certificate.");
        return;
      }

      if (!window.jspdf || !window.jspdf.jsPDF) {
        alert("The PDF library could not be loaded. Please check your internet connection and try again.");
        return;
      }

      const { jsPDF } = window.jspdf;
      const doc = new jsPDF();

      if (attemptFlagged) {
        generateFlaggedCertificate(doc, studentName);
      } else {
        generateNormalCertificate(doc, studentName);
      }

      doc.save(`${studentName.replace(/\s+/g, "_")}_${practiceTopic.replace(/[^a-z0-9]+/gi, "_")}_Certificate.pdf`);
    }

    function generateNormalCertificate(doc, studentName) {
      const completionDate = new Date().toLocaleDateString(undefined, {
        year: "numeric",
        month: "long",
        day: "numeric"
      });

      doc.setFont("helvetica", "bold");
      doc.setFontSize(24);
      doc.text("Practice Certificate", 105, 30, { align: "center" });

      doc.setFontSize(14);
      doc.setFont("helvetica", "normal");
      doc.text("This certificate confirms completion of the [SUBJECT OR TOPIC] practice activity.", 105, 48, {
        align: "center"
      });

      doc.setDrawColor(4, 120, 87);
      doc.setLineWidth(1.2);
      doc.line(25, 58, 185, 58);

      doc.setFontSize(13);
      doc.text(`Topic: ${practiceTopic}`, 30, 78);
      doc.text(`Student name: ${studentName}`, 30, 93);
      doc.text(`Date: ${completionDate}`, 30, 108);
      doc.text(`Score: ${lastScore} / 5`, 30, 123);
      doc.text("Integrity status: No focus or fullscreen interruptions detected", 30, 138, {
        maxWidth: 150
      });

      doc.setFont("helvetica", "bold");
      doc.setFontSize(12);
      doc.text("Activity note", 30, 165);

      doc.setFont("helvetica", "normal");
      doc.setFontSize(11);
      doc.text(
        "This certificate records completion and basic browser activity during the practice attempt. It is not a secure proctoring report.",
        30,
        177,
        { maxWidth: 150 }
      );

      doc.setDrawColor(180, 190, 200);
      doc.roundedRect(20, 18, 170, 245, 5, 5);
    }

    function generateFlaggedCertificate(doc, studentName) {
      const completionDate = new Date().toLocaleDateString(undefined, {
        year: "numeric",
        month: "long",
        day: "numeric"
      });

      doc.setFillColor(185, 28, 28);
      doc.rect(20, 18, 170, 32, "F");

      doc.setDrawColor(185, 28, 28);
      doc.setLineWidth(2);
      doc.roundedRect(20, 18, 170, 245, 5, 5);

      doc.setFont("helvetica", "bold");
      doc.setTextColor(255, 255, 255);
      doc.setFontSize(23);
      doc.text("Flagged Practice Certificate", 105, 38, {
        align: "center"
      });

      doc.setTextColor(185, 28, 28);
      doc.setFontSize(16);
      doc.text("FLAGGED ATTEMPT", 105, 68, {
        align: "center"
      });

      doc.setFont("helvetica", "normal");
      doc.setFontSize(12);
      doc.text(
        "One or more focus, visibility, or fullscreen interruptions were detected during the practice attempt.",
        30,
        82,
        { maxWidth: 150 }
      );

      doc.setFont("helvetica", "normal");
      doc.setTextColor(31, 41, 51);
      doc.setFontSize(13);
      doc.text(`Topic: ${practiceTopic}`, 30, 108);
      doc.text(`Student name: ${studentName}`, 30, 123);
      doc.text(`Date: ${completionDate}`, 30, 138);
      doc.text(`Score: ${lastScore} / 5`, 30, 153);
      doc.text(`Recorded monitoring events: ${activityLog.length}`, 30, 168);
      doc.text(`Suspicious interruptions: ${suspiciousInterruptionCount}`, 30, 183);

      doc.setTextColor(185, 28, 28);
      doc.setFont("helvetica", "bold");
      doc.text(
        "Integrity status: Flagged: focus, visibility, or fullscreen interruption detected",
        30,
        198,
        { maxWidth: 150 }
      );

      doc.setTextColor(31, 41, 51);
      doc.setFont("helvetica", "bold");
      doc.setFontSize(12);
      doc.text("Activity note", 30, 225);

      doc.setFont("helvetica", "normal");
      doc.setFontSize(11);
      doc.text(
        "This certificate records completion and basic browser activity during the practice attempt. It is not a secure proctoring report.",
        30,
        237,
        { maxWidth: 150 }
      );
    }

    function openQrModal() {
      qrModalOverlay.classList.remove("hidden");
      qrModalOverlay.setAttribute("aria-hidden", "false");

      if (!hasGeneratedQrCode) {
        qrCodeContainer.innerHTML = "";

        if (typeof QRCode === "undefined") {
          qrCodeContainer.textContent =
            "The QR code library could not be loaded.";
          return;
        }

        new QRCode(qrCodeContainer, {
          text: window.location.href,
          width: 220,
          height: 220,
          correctLevel: QRCode.CorrectLevel.H
        });

        hasGeneratedQrCode = true;
      }

      closeQrModalButton.focus();
    }

    function closeQrModal() {
      qrModalOverlay.classList.add("hidden");
      qrModalOverlay.setAttribute("aria-hidden", "true");
      qrButton.focus();
    }

    document.addEventListener("visibilitychange", () => {
      if (!isPracticeActive || hasSubmitted) {
        return;
      }

      if (document.hidden) {
        recordSuspiciousInterruption(
          "page_hidden",
          "The page became hidden during the practice attempt."
        );
      } else {
        addActivityLogEntry(
          "page_visible",
          "The page became visible again during the practice attempt."
        );
      }
    });

    window.addEventListener("blur", () => {
      if (!isPracticeActive || hasSubmitted) {
        return;
      }

      recordSuspiciousInterruption(
        "window_blur",
        "The browser window lost focus during the practice attempt."
      );
    });

    window.addEventListener("focus", () => {
      if (!isPracticeActive || hasSubmitted) {
        return;
      }

      addActivityLogEntry(
        "window_focus",
        "The browser window regained focus during the practice attempt."
      );
    });

    document.addEventListener("fullscreenchange", () => {
      if (!isPracticeActive || hasSubmitted) {
        return;
      }

      if (document.fullscreenElement) {
        addActivityLogEntry(
          "fullscreen_entered",
          "Fullscreen mode started for the practice attempt."
        );
      } else {
        recordSuspiciousInterruption(
          "fullscreen_exited",
          "Fullscreen mode ended during the practice attempt."
        );
      }
    });

    startButton.addEventListener("click", startPractice);
    resetButton.addEventListener("click", startPractice);
    quizForm.addEventListener("submit", submitAnswers);
    downloadButton.addEventListener("click", downloadCertificate);

    qrButton.addEventListener("click", openQrModal);
    closeQrModalButton.addEventListener("click", closeQrModal);
