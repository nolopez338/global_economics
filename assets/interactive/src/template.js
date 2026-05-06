const practiceTopic = "[CERTIFICATE TOPIC]";
const targetQuestionCount = 5;

const questionDatabase = [
  { question: "[QUESTION 1 TEXT]", options: ["[OPTION A]", "[OPTION B]", "[OPTION C]", "[OPTION D]"], correctIndex: 0, explanation: "[QUESTION 1 FEEDBACK] [CORRECT ANSWER] explanation placeholder." },
  { question: "[QUESTION 2 TEXT]", options: ["[OPTION A]", "[OPTION B]", "[OPTION C]", "[OPTION D]"], correctIndex: 0, explanation: "[QUESTION 2 FEEDBACK] [CORRECT ANSWER] explanation placeholder." },
  { question: "[QUESTION 3 TEXT]", options: ["[OPTION A]", "[OPTION B]", "[OPTION C]", "[OPTION D]"], correctIndex: 0, explanation: "[QUESTION 3 FEEDBACK] [CORRECT ANSWER] explanation placeholder." },
  { question: "[QUESTION 4 TEXT]", options: ["[OPTION A]", "[OPTION B]", "[OPTION C]", "[OPTION D]"], correctIndex: 0, explanation: "[QUESTION 4 FEEDBACK] [CORRECT ANSWER] explanation placeholder." },
  { question: "[QUESTION 5 TEXT]", options: ["[OPTION A]", "[OPTION B]", "[OPTION C]", "[OPTION D]"], correctIndex: 0, explanation: "[QUESTION 5 FEEDBACK] [CORRECT ANSWER] explanation placeholder." },
  { question: "[QUESTION 6 TEXT]", options: ["[OPTION A]", "[OPTION B]", "[OPTION C]", "[OPTION D]"], correctIndex: 0, explanation: "[QUESTION 6 FEEDBACK] [CORRECT ANSWER] explanation placeholder." }
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

const templateSettings = window.InteractiveTemplateSettings || {};
const imageSettings = window.InteractiveImageQuestionSettings || {};
const subjects = templateSettings.subjects || {};
const selectedSubjectKey = templateSettings.selectedSubjectKey || "math";
const selectedSubject = subjects[selectedSubjectKey] || subjects.math || { label: "Math", paletteClass: "subject-math" };
const isQRCodeEnabled = templateSettings.enableQRCode === true;
const isFullscreenMonitoringEnabled = templateSettings.enableFullscreenMonitoring === true;
const isImageQuestionsEnabled = templateSettings.enableImageQuestions === true;

const qrButton = document.getElementById("qrButton");
const qrModalOverlay = document.getElementById("qrModalOverlay");
const qrCodeContainer = document.getElementById("qrCodeContainer");
const closeQrModalButton = document.getElementById("closeQrModalButton");
const monitoringNotice = document.getElementById("monitoringNotice");

let selectedQuestions = [];
let selectedAnswers = [];
let lastScore = 0;
let hasSubmitted = false;
let activityLog = [];
let attemptFlagged = false;
let suspiciousInterruptionCount = 0;
let isPracticeActive = false;
let hasGeneratedQrCode = false;
let imageQuestionStates = {};

function sanitizeImageQuestion(question) {
  if (!question || !question.goalRegion || question.goalRegion.type !== "normalized-mask") return null;
  const width = Number(question.goalRegion.width);
  const height = Number(question.goalRegion.height);
  const cells = Array.isArray(question.goalRegion.filledCells) ? question.goalRegion.filledCells : [];
  if (!Number.isInteger(width) || !Number.isInteger(height) || width <= 0 || height <= 0 || cells.length === 0) return null;
  const max = width * height;
  const dedup = [...new Set(cells.map(Number).filter(i => Number.isInteger(i) && i >= 0 && i < max))].sort((a,b)=>a-b);
  if (dedup.length === 0) return null;
  return { ...question, goalRegion: { type: "normalized-mask", width, height, filledCells: dedup } };
}

function buildSelectedQuestions() {
  const availableImageQuestions = Array.isArray(imageSettings.imageQuestions) ? imageSettings.imageQuestions.map(sanitizeImageQuestion).filter(Boolean) : [];
  let configured = Number(templateSettings.numberOfImageQuestions);
  if (!Number.isFinite(configured)) configured = 0;
  configured = Math.max(0, Math.floor(configured));
  const imageCount = isImageQuestionsEnabled ? Math.min(configured, targetQuestionCount, availableImageQuestions.length) : 0;
  const regularCount = Math.max(0, targetQuestionCount - imageCount);

  const regularQuestions = shuffleArray(questionDatabase).slice(0, regularCount).map(q => ({ type: "mcq", ...q }));
  const imageQuestions = shuffleArray(availableImageQuestions).slice(0, imageCount).map(q => ({ type: "image", ...q }));
  return shuffleArray([...regularQuestions, ...imageQuestions]);
}

function applySubjectPalette() { const body=document.body; if(!body)return; const classes=Object.values(subjects).map(s=>s&&s.paletteClass).filter(Boolean); if(classes.length) body.classList.remove(...classes); body.classList.add(selectedSubject.paletteClass||"subject-math"); }
function shuffleArray(array){const a=[...array];for(let i=a.length-1;i>0;i--){const r=Math.floor(Math.random()*(i+1));[a[i],a[r]]=[a[r],a[i]];}return a;}
function getTimestamp(){return new Date().toISOString();}
function formatTimestamp(t){return new Date(t).toLocaleString();}
function isFullscreenActive(){return Boolean(document.fullscreenElement);}
function addActivityLogEntry(eventType,description,extraData={}){activityLog.push({eventType,timestamp:getTimestamp(),description,...extraData});}
function recordSuspiciousInterruption(eventType,description,extraData={}){suspiciousInterruptionCount+=1;attemptFlagged=true;addActivityLogEntry(eventType,description,{suspiciousInterruption:true,...extraData});}

function resetPracticeState(){selectedQuestions=[];selectedAnswers=[];lastScore=0;hasSubmitted=false;activityLog=[];attemptFlagged=false;suspiciousInterruptionCount=0;isPracticeActive=false;imageQuestionStates={};resultContainer.innerHTML="";downloadButton.classList.add("hidden");submitButton.disabled=false;}

function startPractice(){const studentName=studentNameInput.value.trim();if(!studentName){alert("Please enter your name before starting the practice activity.");studentNameInput.focus();return;}resetPracticeState();selectedQuestions=buildSelectedQuestions();isPracticeActive=true;addActivityLogEntry("activity_started","The practice activity started.",{currentUrl:window.location.href,initialFullscreenStatus:isFullscreenActive(),initialVisibilityState:document.visibilityState});if(isFullscreenMonitoringEnabled){requestPracticeFullscreen();}resetButton.classList.remove("hidden");quizForm.classList.remove("hidden");renderQuestions();}
function requestPracticeFullscreen(){if(!practiceSection.requestFullscreen){recordSuspiciousInterruption("fullscreen_unavailable","Fullscreen mode was unavailable in this browser.");return;}if(isFullscreenActive()) return;practiceSection.requestFullscreen().catch(()=>{if(!isPracticeActive||hasSubmitted)return;recordSuspiciousInterruption("fullscreen_request_failed","Fullscreen mode did not start or was rejected by the browser.");});}

function renderImageQuestion(questionCard, questionItem, questionIndex) {
  const prompt = document.createElement("p"); prompt.textContent = questionItem.prompt || "Draw over the requested region in the image."; questionCard.appendChild(prompt);
  const status = document.createElement("div"); status.className = "image-question-status";
  const wrapper = document.createElement("div"); wrapper.className = "image-question-wrapper";
  const img = document.createElement("img"); img.className = "image-question-image"; img.src = questionItem.imageUrl || ""; img.alt = questionItem.title || "Image question";
  const canvas = document.createElement("canvas"); canvas.className = "image-question-canvas";
  const controls = document.createElement("div"); controls.className = "image-question-controls";
  const inkIndicator = document.createElement("div"); inkIndicator.className = "ink-indicator";
  const clearBtn = document.createElement("button"); clearBtn.type = "button"; clearBtn.textContent = "Clear Drawing"; clearBtn.className = "secondary-button";
  controls.append(inkIndicator, clearBtn); wrapper.append(img, canvas); questionCard.append(wrapper, status, controls);

  const goalSet = new Set(questionItem.goalRegion.filledCells);
  const budget = Math.floor(goalSet.size * 1.5);
  const state = imageQuestionStates[questionIndex] || { covered: new Set(), unavailable: false, loaded: false };
  imageQuestionStates[questionIndex] = state;
  const updateInk = () => { inkIndicator.textContent = `Ink remaining: ${Math.max(0, budget - state.covered.size)} / ${budget}`; };
  updateInk();

  function syncCanvas(){const rect=img.getBoundingClientRect();canvas.width=Math.max(1,Math.round(rect.width));canvas.height=Math.max(1,Math.round(rect.height));const ctx=canvas.getContext("2d");ctx.clearRect(0,0,canvas.width,canvas.height);ctx.fillStyle="rgba(37,99,235,0.35)";state.covered.forEach(index=>{const x=index%questionItem.goalRegion.width;const y=Math.floor(index/questionItem.goalRegion.width);ctx.fillRect(x*canvas.width/questionItem.goalRegion.width,y*canvas.height/questionItem.goalRegion.height,canvas.width/questionItem.goalRegion.width,canvas.height/questionItem.goalRegion.height);});}

  img.addEventListener("load", ()=>{state.loaded=true;status.textContent="";syncCanvas();});
  img.addEventListener("error", ()=>{state.unavailable=true;status.className="image-question-status unavailable";status.textContent="Image unavailable. This question will be graded as incorrect.";});
  window.addEventListener("resize", syncCanvas);

  let drawing=false;
  const brushRadius=2;
  function paint(ev){if(!drawing||hasSubmitted||state.unavailable||!state.loaded) return;const rect=canvas.getBoundingClientRect();const px=(ev.clientX-rect.left)/rect.width*questionItem.goalRegion.width;const py=(ev.clientY-rect.top)/rect.height*questionItem.goalRegion.height;for(let y=Math.floor(py-brushRadius);y<=Math.ceil(py+brushRadius);y++){for(let x=Math.floor(px-brushRadius);x<=Math.ceil(px+brushRadius);x++){if(x<0||y<0||x>=questionItem.goalRegion.width||y>=questionItem.goalRegion.height)continue;const dx=x+0.5-px,dy=y+0.5-py;if(dx*dx+dy*dy>brushRadius*brushRadius)continue;const idx=y*questionItem.goalRegion.width+x;if(!state.covered.has(idx)){if(state.covered.size>=budget)break;state.covered.add(idx);}}}syncCanvas();updateInk();}
  canvas.addEventListener("pointerdown",e=>{drawing=true;canvas.setPointerCapture(e.pointerId);paint(e);});
  canvas.addEventListener("pointermove",paint);
  canvas.addEventListener("pointerup",()=>drawing=false);
  canvas.addEventListener("pointerleave",()=>drawing=false);
  clearBtn.addEventListener("click",()=>{if(hasSubmitted) return;state.covered.clear();syncCanvas();updateInk();});

  if (hasSubmitted) {
    const missing = [...goalSet].some(i => !state.covered.has(i));
    const feedback = document.createElement("div");
    feedback.className = `feedback ${!state.unavailable && !missing ? "correct" : "incorrect"}`;
    feedback.innerHTML = `<strong>${!state.unavailable && !missing ? "Correct." : "Incorrect."}</strong> ${questionItem.explanation || "You must fully cover the goal region."}`;
    questionCard.appendChild(feedback);
    clearBtn.disabled = true;
  }
}

function renderQuestions(){questionsContainer.innerHTML="";selectedQuestions.forEach((questionItem,questionIndex)=>{const card=document.createElement("article");card.className="question-card";const title=document.createElement("div");title.className="question-title";title.textContent=`${questionIndex+1}. ${questionItem.type==="image" ? (questionItem.title||"Image Question") : questionItem.question}`;card.appendChild(title);
if(questionItem.type==="image"){renderImageQuestion(card,questionItem,questionIndex);}else{const options=document.createElement("div");options.className="options";questionItem.options.forEach((text,optionIndex)=>{const optionId=`question-${questionIndex}-option-${optionIndex}`;const label=document.createElement("label");label.className="option-label";label.setAttribute("for",optionId);const input=document.createElement("input");input.type="radio";input.id=optionId;input.name=`question-${questionIndex}`;input.value=String(optionIndex);input.disabled=hasSubmitted;if(selectedAnswers[questionIndex]===String(optionIndex))input.checked=true;if(hasSubmitted){const selected=Number(selectedAnswers[questionIndex]);if(optionIndex===questionItem.correctIndex)label.classList.add("correct-answer");if(optionIndex===selected&&selected!==questionItem.correctIndex)label.classList.add("incorrect-answer");}const span=document.createElement("span");span.textContent=text;label.append(input,span);options.appendChild(label);});card.appendChild(options);if(hasSubmitted){const ok=Number(selectedAnswers[questionIndex])===questionItem.correctIndex;const feedback=document.createElement("div");feedback.className=`feedback ${ok?"correct":"incorrect"}`;feedback.innerHTML=`<strong>${ok?"Correct.":"Incorrect."}</strong> Correct answer: ${questionItem.options[questionItem.correctIndex]}<br />${questionItem.explanation}`;card.appendChild(feedback);}}
questionsContainer.appendChild(card);});}

function submitAnswers(event){event.preventDefault();const formData=new FormData(quizForm);selectedAnswers=selectedQuestions.map((item,i)=>item.type==="image"?"image":formData.get(`question-${i}`));const unanswered=selectedQuestions.findIndex((item,i)=>item.type!=="image"&&selectedAnswers[i]===null);if(unanswered!==-1){alert(`Please answer question ${unanswered+1}.`);return;}lastScore=selectedQuestions.reduce((score,item,i)=>{if(item.type==="image"){const st=imageQuestionStates[i];if(!st||st.unavailable)return score;const goal=item.goalRegion.filledCells;const ok=goal.every(index=>st.covered.has(index));return ok?score+1:score;}return Number(selectedAnswers[i])===item.correctIndex?score+1:score;},0);hasSubmitted=true;isPracticeActive=false;submitButton.disabled=true;downloadButton.classList.remove("hidden");renderQuestions();renderSubmissionResult();}
function renderSubmissionResult(){const integrityMessage=isFullscreenMonitoringEnabled?(attemptFlagged?"Integrity status: Flagged. One or more focus, visibility, or fullscreen interruptions were detected.":"Integrity status: No focus or fullscreen interruptions detected."):"Integrity status: Monitoring disabled for fullscreen, focus, and visibility events.";const certificateMessage=isFullscreenMonitoringEnabled?(attemptFlagged?"A red flagged certificate will be generated for this attempt because an interruption was detected.":"A normal certificate will be generated for this attempt."):"A normal certificate will be generated for this attempt.";resultContainer.innerHTML=`<div class="score-box">Score: ${lastScore} / ${selectedQuestions.length}</div><div class="${attemptFlagged?"integrity-status flagged":"integrity-status"}">${integrityMessage}</div><div class="${attemptFlagged?"certificate-notice flagged":"certificate-notice"}">${certificateMessage}</div>`;}

function downloadCertificate(){/* unchanged behavior */const studentName=studentNameInput.value.trim();if(!studentName){alert("Please enter your name before downloading the certificate.");studentNameInput.focus();return;}if(!hasSubmitted){alert("Please submit the practice activity before downloading the certificate.");return;}if(!window.jspdf||!window.jspdf.jsPDF){alert("The PDF library could not be loaded. Please check your internet connection and try again.");return;}const {jsPDF}=window.jspdf;const doc=new jsPDF();if(attemptFlagged){generateFlaggedCertificate(doc,studentName);}else{generateNormalCertificate(doc,studentName);}doc.save(`${studentName.replace(/\s+/g,"_")}_${practiceTopic.replace(/[^a-z0-9]+/gi,"_")}_Certificate.pdf`);}
function generateNormalCertificate(doc,studentName){const completionDate=new Date().toLocaleDateString(undefined,{year:"numeric",month:"long",day:"numeric"});doc.setFont("helvetica","bold");doc.setFontSize(24);doc.text("Practice Certificate",105,30,{align:"center"});doc.setFontSize(14);doc.setFont("helvetica","normal");doc.text("This certificate confirms completion of the [SUBJECT OR TOPIC] practice activity.",105,48,{align:"center"});doc.setDrawColor(4,120,87);doc.setLineWidth(1.2);doc.line(25,58,185,58);doc.setFontSize(13);doc.text(`Topic: ${practiceTopic}`,30,78);doc.text(`Student name: ${studentName}`,30,93);doc.text(`Date: ${completionDate}`,30,108);doc.text(`Score: ${lastScore} / ${selectedQuestions.length}`,30,123);doc.text("Integrity status: No focus or fullscreen interruptions detected",30,138,{maxWidth:150});}
function generateFlaggedCertificate(doc,studentName){const completionDate=new Date().toLocaleDateString(undefined,{year:"numeric",month:"long",day:"numeric"});doc.setFillColor(185,28,28);doc.rect(20,18,170,32,"F");doc.setDrawColor(185,28,28);doc.setLineWidth(2);doc.roundedRect(20,18,170,245,5,5);doc.setFont("helvetica","bold");doc.setTextColor(255,255,255);doc.setFontSize(23);doc.text("Flagged Practice Certificate",105,38,{align:"center"});doc.setTextColor(31,41,51);doc.setFontSize(13);doc.text(`Topic: ${practiceTopic}`,30,108);doc.text(`Student name: ${studentName}`,30,123);doc.text(`Date: ${completionDate}`,30,138);doc.text(`Score: ${lastScore} / ${selectedQuestions.length}`,30,153);}
function hideQrFeatureUi(){if(qrButton)qrButton.classList.add("hidden");if(qrModalOverlay){qrModalOverlay.classList.add("hidden");qrModalOverlay.setAttribute("aria-hidden","true");}}
function loadQrLibrary(){return new Promise((resolve,reject)=>{if(typeof QRCode!=="undefined"){resolve();return;}const script=document.createElement("script");script.src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js";script.async=true;script.onload=()=>resolve();script.onerror=()=>reject(new Error("Failed to load QR code library."));document.head.appendChild(script);});}
function initializeQRCodeFeature(){if(!isQRCodeEnabled){hideQrFeatureUi();return;}if(!qrButton||!qrModalOverlay||!qrCodeContainer||!closeQrModalButton){hideQrFeatureUi();return;}qrButton.classList.remove("hidden");qrButton.addEventListener("click",openQrModal);closeQrModalButton.addEventListener("click",closeQrModal);loadQrLibrary().catch(()=>{qrCodeContainer.textContent="The QR code library could not be loaded.";});}
function openQrModal(){if(!isQRCodeEnabled||!qrModalOverlay||!qrCodeContainer||!closeQrModalButton)return;qrModalOverlay.classList.remove("hidden");qrModalOverlay.setAttribute("aria-hidden","false");if(!hasGeneratedQrCode){qrCodeContainer.innerHTML="";if(typeof QRCode==="undefined"){qrCodeContainer.textContent="The QR code library could not be loaded.";return;}new QRCode(qrCodeContainer,{text:window.location.href,width:220,height:220,correctLevel:QRCode.CorrectLevel.H});hasGeneratedQrCode=true;}closeQrModalButton.focus();}
function closeQrModal(){if(!isQRCodeEnabled||!qrModalOverlay||!qrButton)return;qrModalOverlay.classList.add("hidden");qrModalOverlay.setAttribute("aria-hidden","true");qrButton.focus();}
function initializeFullscreenMonitoringFeature(){if(!isFullscreenMonitoringEnabled)return;document.addEventListener("visibilitychange",()=>{if(!isPracticeActive||hasSubmitted)return; if(document.hidden){recordSuspiciousInterruption("page_hidden","The page became hidden during the practice attempt.");}else{addActivityLogEntry("page_visible","The page became visible again during the practice attempt.");}});window.addEventListener("blur",()=>{if(!isPracticeActive||hasSubmitted)return;recordSuspiciousInterruption("window_blur","The browser window lost focus during the practice attempt.");});window.addEventListener("focus",()=>{if(!isPracticeActive||hasSubmitted)return;addActivityLogEntry("window_focus","The browser window regained focus during the practice attempt.");});document.addEventListener("fullscreenchange",()=>{if(!isPracticeActive||hasSubmitted)return; if(document.fullscreenElement){addActivityLogEntry("fullscreen_entered","Fullscreen mode started for the practice attempt.");}else{recordSuspiciousInterruption("fullscreen_exited","Fullscreen mode ended during the practice attempt.");}});}

applySubjectPalette(); if (monitoringNotice && !isFullscreenMonitoringEnabled) monitoringNotice.classList.add("hidden");
startButton.addEventListener("click",startPractice); resetButton.addEventListener("click",startPractice); quizForm.addEventListener("submit",submitAnswers); downloadButton.addEventListener("click",downloadCertificate); initializeQRCodeFeature(); initializeFullscreenMonitoringFeature();
