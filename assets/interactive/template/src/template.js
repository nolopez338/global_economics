const practiceTopic = "[CERTIFICATE TOPIC]";

const practiceSection = document.getElementById("practiceSection");
const startButton = document.getElementById("startButton");
const resetButton = document.getElementById("resetButton");
const submitButton = document.getElementById("submitButton");
const downloadButton = document.getElementById("downloadButton");
const quizForm = document.getElementById("quizForm");
const questionsContainer = document.getElementById("questionsContainer");
const resultContainer = document.getElementById("resultContainer");
const studentNameInput = document.getElementById("studentName");
const templateSettings = window.InteractiveTemplateSettings || {};
const multipleChoiceSettings = window.InteractiveMultipleChoiceQuestionSettings || {};
const imageSettings = window.InteractiveImageQuestionSettings || {};
const isImageQuestionsEnabled = templateSettings.enableImageQuestions !== false;
const isMultipleChoiceEnabled = templateSettings.enableMultipleChoiceQuestions !== false;

let selectedQuestions = [];
let selectedAnswers = [];
let imageQuestionStates = {};
let hasSubmitted = false;

function shuffleArray(array){const a=[...array];for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function sanitizePercent(value,min,max,def){const n=Number(value);if(!Number.isFinite(n))return def;return Math.min(max,Math.max(min,Math.round(n)));}
function toNonNegativeInt(value, fallback){const n = Number(value); if (!Number.isFinite(n)) return fallback; return Math.max(0, Math.floor(n));}

function sanitizeMcqQuestion(question, index) {
  if (!question || !question.id || !question.prompt || !Array.isArray(question.options) || question.options.length < 2 || !question.correctOptionId) return null;
  const options = question.options
    .map((opt) => ({ id: String(opt && opt.id ? opt.id : "").trim().toUpperCase(), text: String(opt && opt.text ? opt.text : "").trim() }))
    .filter((opt) => opt.id && opt.text);
  if (options.length < 2) return null;
  const ids = new Set(options.map((o) => o.id));
  const correctOptionId = String(question.correctOptionId).trim().toUpperCase();
  if (!ids.has(correctOptionId)) return null;
  return { type: "multiple-choice", id: String(question.id), title: String(question.title || `Question ${index + 1}`), prompt: String(question.prompt), options, correctOptionId, feedback: String(question.feedback || "") };
}

function sanitizeImageQuestion(question) {
  if (!question || !question.imageUrl || !question.goalRegion || question.goalRegion.type !== "normalized-mask") return null;
  const width = Number(question.goalRegion.width);
  const height = Number(question.goalRegion.height);
  const cells = Array.isArray(question.goalRegion.filledCells) ? question.goalRegion.filledCells : [];
  if (!Number.isInteger(width) || !Number.isInteger(height) || width <= 0 || height <= 0 || cells.length === 0) return null;
  const max = width * height;
  const dedup = [...new Set(cells.map(Number).filter(i => Number.isInteger(i) && i >= 0 && i < max))].sort((a,b)=>a-b);
  if (!dedup.length) return null;
  return { ...question, type: "image", studentInkPercent: sanitizePercent(question.studentInkPercent,100,200,150), coverGoalPercent: sanitizePercent(question.coverGoalPercent,30,100,90), goalRegion: { type: "normalized-mask", width, height, filledCells: dedup } };
}

function buildSelectedQuestions() {
  const totalQuestions = toNonNegativeInt(templateSettings.totalQuestions, 5);
  const mcqPool = (Array.isArray(multipleChoiceSettings.questions) ? multipleChoiceSettings.questions : []).map(sanitizeMcqQuestion).filter(Boolean);
  const imagePool = (Array.isArray(imageSettings.imageQuestions) ? imageSettings.imageQuestions : []).map(sanitizeImageQuestion).filter(Boolean);
  if (!isImageQuestionsEnabled && !isMultipleChoiceEnabled) return [];

  let desiredImageCount = isImageQuestionsEnabled ? toNonNegativeInt(templateSettings.numberOfImageQuestions, 0) : 0;
  desiredImageCount = Math.min(desiredImageCount, totalQuestions, imagePool.length);

  let desiredMcqCount = isMultipleChoiceEnabled ? Math.max(0, totalQuestions - desiredImageCount) : 0;
  desiredMcqCount = Math.min(desiredMcqCount, mcqPool.length);

  if (!isMultipleChoiceEnabled) desiredImageCount = Math.min(totalQuestions, imagePool.length);
  if (!isImageQuestionsEnabled) desiredImageCount = 0;

  const chosenImages = shuffleArray(imagePool).slice(0, desiredImageCount);
  const chosenMcqs = shuffleArray(mcqPool).slice(0, desiredMcqCount);
  return shuffleArray([...chosenImages, ...chosenMcqs]);
}

function renderQuestions() {
  questionsContainer.innerHTML = "";
  selectedQuestions.forEach((q, i) => {
    const card = document.createElement("article"); card.className = "question-card";
    const title = document.createElement("div"); title.className = "question-title"; title.textContent = `${i + 1}. ${q.title || q.prompt}`; card.appendChild(title);
    if (q.type === "image") {
      const p = document.createElement("p"); p.textContent = q.prompt; card.appendChild(p);
    } else {
      const prompt = document.createElement("p"); prompt.textContent = q.prompt; card.appendChild(prompt);
      const options = document.createElement("div"); options.className = "options";
      q.options.forEach((opt) => {
        const id = `q-${i}-${opt.id}`; const label = document.createElement("label"); label.className = "option-label"; label.setAttribute("for", id);
        const input = document.createElement("input"); input.type = "radio"; input.name = `question-${i}`; input.id = id; input.value = opt.id; input.disabled = hasSubmitted;
        if (selectedAnswers[i] === opt.id) input.checked = true;
        const span = document.createElement("span"); span.textContent = `${opt.id}. ${opt.text}`;
        label.append(input, span); options.appendChild(label);
      });
      card.appendChild(options);
    }
    questionsContainer.appendChild(card);
  });
}

function startPractice(){
  if(!studentNameInput.value.trim()){alert("Please enter your name before starting the practice activity.");return;}
  selectedQuestions = buildSelectedQuestions(); selectedAnswers = []; hasSubmitted = false;
  if (!selectedQuestions.length) { resultContainer.innerHTML = '<div class="error-message">No valid questions are available. Please check the question database files.</div>'; quizForm.classList.add("hidden"); return; }
  resultContainer.innerHTML = ""; quizForm.classList.remove("hidden"); resetButton.classList.remove("hidden"); renderQuestions();
}

function submitAnswers(e){
  e.preventDefault();
  hasSubmitted = true;
  let score = 0;
  selectedQuestions.forEach((q, i) => {
    if (q.type === "multiple-choice") {
      const selected = document.querySelector(`input[name=question-${i}]:checked`);
      if (selected && selected.value === q.correctOptionId) score += 1;
    }
  });
  resultContainer.innerHTML = `<div class="result-box">Score: ${score} / ${selectedQuestions.length}</div>`;
}

startButton.addEventListener("click", startPractice);
resetButton.addEventListener("click", startPractice);
quizForm.addEventListener("submit", submitAnswers);
