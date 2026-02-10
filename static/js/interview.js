let currentQuestion = "";
  let recognition = null;
  let stream = null;
  let isSpeaking = false;
  let sessionId = null;

  async function loadQuestion() {
    const res = await fetch("/question");
    const data = await res.json();

    sessionId = data.session_id;
    currentQuestion = data.question;

    document.getElementById("questionText").innerText = currentQuestion;
    speakQuestion(currentQuestion);
    startBorderTimer();
  }


  function speakQuestion(text) {
    if (!("speechSynthesis" in window) || !text) return;

    const panel = document.getElementById("aiPanel");
    const speakBtn = document.getElementById("speakBtn");

    window.speechSynthesis.cancel();

    const utter = new SpeechSynthesisUtterance(text);
    
    utter.lang = "en-US";

    utter.onstart = () => {
      isSpeaking = true;
      panel.classList.add("ai-speaking");
      speakBtn.disabled = true;
    };

    utter.onend = () => {
      isSpeaking = false;
      panel.classList.remove("ai-speaking");
      speakBtn.disabled = false;
    };

    window.speechSynthesis.speak(utter);
  }

  function speakAgain() {
    if (!isSpeaking) speakQuestion(currentQuestion);
  }

  function startListening() {
    if (!("webkitSpeechRecognition" in window)) return;

    recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.onresult = e => {
      document.getElementById("answerInput").value = e.results[0][0].transcript;
    };
    recognition.start();
  }
const TOTAL_QUESTIONS = 5;
let answeredCount = 0;
function updateProgress() {
  const percent = Math.min(
    Math.round((answeredCount / TOTAL_QUESTIONS) * 100),
    100
  );

  document.getElementById("progressFill").style.width = percent + "%";
  document.getElementById("progressText").innerText = `${percent}% completed`;
}

  async function submitAnswer(isAuto = false) {
    
    const input = document.getElementById("answerInput");
    const answer = isAuto ? "" : input.value.trim();
    
    if (!isAuto && !answer) return;
    stopBorderTimer();

    const resDiv = document.getElementById("response");
    answeredCount++;
    updateProgress();

    if (answeredCount === TOTAL_QUESTIONS) {
      hideBorderTimer();
      const outro = `
          That concludes the interview.
          Please wait patiently while we evaluate your responses.
            `;
      speakQuestion(outro); 
      await delay(6000);
      resDiv.style.display = "block";
      resDiv.innerText = "Evaluating your interview...";
    } else {
      resDiv.innerText = "Processing answer...";
    }
    const res = await fetch("/next-question", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: sessionId,
        answer: answer
      })
    });

    const data = await res.json();
    if (data.done) {
      hideBorderTimer();
      speakQuestion("Here Is your Evaluation");
      resDiv.style.display = "block";
      resDiv.innerHTML = `
      <h3>Evaluation</h3>

        <div class="evaluation-text">
            ${data.evaluation}
        </div>

      <div>Time Taken: ${data.time_taken}s</div>`;
      return;
    }

    currentQuestion = data.question;
    document.getElementById("answerInput").value = "";
    document.getElementById("questionText").innerText = currentQuestion;
  
    speakQuestion(currentQuestion);
    startBorderTimer();
    await delay(3000);
    startListening()
  }


  const video = document.getElementById("cam");
  const startCam = document.getElementById("startCam");
  const stopCam = document.getElementById("stopCam");

  startCam.onclick = startCamera;

  async function startCamera() {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    startCam.disabled = true;
    stopCam.disabled = false;
  }

  stopCam.onclick = () => {
    stream.getTracks().forEach(t => t.stop());
    video.srcObject = null;
    stream = null;
    startCam.disabled = false;
    stopCam.disabled = true;
  };

  function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async function initInterview() {
    hideBorderTimer();
    startCamera();
    await delay(1000);
    const userName = document.body.dataset.username;
    const intro = `
          Hello ${userName} , and welcome to Evalynx.
          I’ll be your AI interviewer today.
          This interview is designed to understand your skills, thinking process, and communication ability.
          Please answer each question honestly and clearly.
          note that you have 1 minute for each question.
          let’s begin.
          Here is your First Question.
            `;

    speakQuestion(intro);
    await delay(20000);
    loadQuestion();
    await delay(2000);
    startListening(); 
    
  }


let borderTimer = null;
const QUESTION_TIME = 60;
let borderTimeLeft = QUESTION_TIME;
let hasSpokenTenSecWarning = false;
function startBorderTimer() {
  stopBorderTimer();
  showBorderTimer();

  const path = document.querySelector(".border-path");
  borderTimeLeft = QUESTION_TIME;
  path.style.strokeDashoffset = "0";

  borderTimer = setInterval(() => {
    borderTimeLeft--;

    const progress = 1 - (borderTimeLeft / QUESTION_TIME);
    path.style.strokeDashoffset = progress.toString();
    if (borderTimeLeft === 10 && !hasSpokenTenSecWarning) {
      speakQuestion("You have 10 seconds left.");
      hasSpokenTenSecWarning = true;
    }
    if (borderTimeLeft <= 0) {
      stopBorderTimer();
      autoSubmitNoAnswer();
      hasSpokenTenSecWarning = false;
    }
  }, 1000);
}


function stopBorderTimer() {
  if (borderTimer) {
    clearInterval(borderTimer);
    borderTimer = null;
  }
}

function resetBorderTimer() {
  stopBorderTimer();
  const path = document.querySelector(".border-path");
  path.style.strokeDashoffset = "0";
}
function autoSubmitNoAnswer() {
  document.getElementById("answerInput").value = "";
  submitAnswer(true);
}
function showBorderTimer() {
  document.querySelector(".border-path").style.opacity = "1";
}

function hideBorderTimer() {
  stopBorderTimer();
  const path = document.querySelector(".border-path");
  path.style.opacity = "0";
  path.style.strokeDashoffset = "0";
}

    initInterview();