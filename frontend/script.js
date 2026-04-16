let quizData = [];
let username = "";
let user_id = null;

// ⏱️ TIME TRACKING
let startTime = Date.now();


// ================= LOGIN ================= //

async function login() {

let usernameInput = document.getElementById("username").value;
let password = document.getElementById("password").value;

try {

const response = await fetch("http://127.0.0.1:8000/login", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify({
username: usernameInput,
password: password
})
});

const data = await response.json();

if(response.ok){

user_id = data.user_id;
localStorage.setItem("user_id", user_id);

username = usernameInput;

document.getElementById("loginError").innerText = "";

document.getElementById("welcomeText").innerText =
"Hello " + username + "! What would you like to learn today?";

showPage(2);

} else {
document.getElementById("loginError").innerText =
data.detail || "Login failed";
}

} catch (err) {
console.log(err);
document.getElementById("loginError").innerText = "Server error";
}

}


// ================= SIGNUP ================= //

async function signup() {

let usernameInput = document.getElementById("username").value;
let password = document.getElementById("password").value;

try {

const response = await fetch("http://127.0.0.1:8000/signup", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify({
username: usernameInput,
password: password
})
});

const data = await response.json();

if(response.ok){
alert("Signup successful! Now login.");
} else {
alert(data.detail || "Signup failed");
}

} catch (err) {
console.log(err);
alert("Server error");
}

}


// ================= PAGE NAVIGATION ================= //

function nextPage(step){

if(step === 1){
login();
}

else if(step === 2){
showPage(3);
}

}


function showPage(page){

for(let i=1;i<=8;i++){
document.getElementById("page"+i).classList.add("hidden");
}

document.getElementById("page"+page).classList.remove("hidden");

}


// ================= LOAD QUIZ ================= //

async function loadQuiz(){

let topic = document.getElementById("topic").value;
let sector = document.getElementById("sector").value;

try {

const response = await fetch(
`http://127.0.0.1:8000/get_quiz?topic=${topic}&sector=${sector}`
);

const data = await response.json();

quizData = data || [];

if(quizData.length === 0){
alert("Quiz not generated");
return;
}

let quizHTML = "";

quizData.forEach((q,index)=>{

quizHTML += `<p><b>${index+1}. ${q.question}</b></p>`;

q.options.forEach(option=>{
quizHTML += `
<label>
<input type="radio" name="q${index}" value="${option}">
${option}
</label><br>`;
});

quizHTML += "<br>";

});

document.getElementById("quiz").innerHTML = quizHTML;

showPage(4);

} catch (err) {
console.log(err);
alert("Backend error");
}

}


// ================= SUBMIT QUIZ ================= //

async function submitQuiz(){

let score = 0;

quizData.forEach((q,index)=>{

let selected = document.querySelector(`input[name="q${index}"]:checked`);

if(selected && selected.value === q.answer){
score++;
}

});

// LEVEL
let accuracy = score / quizData.length;
let finalLevel = "beginner";

if(accuracy >= 0.8){
finalLevel = "advanced";
} else if(accuracy >= 0.5){
finalLevel = "intermediate";
}

localStorage.setItem("final_level", finalLevel);

let resultHTML = `
<h3>Your Score: ${score} / ${quizData.length}</h3>
<h3>🎯 Level: ${finalLevel}</h3>
`;

document.getElementById("result").innerHTML = resultHTML;

showPage(5);


// SAVE SCORE TO BACKEND
try {
await fetch("http://127.0.0.1:8000/save_score", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify({
user_id: parseInt(localStorage.getItem("user_id")),
topic: document.getElementById("topic").value,
score: score,
total: quizData.length,
level: finalLevel
})
});
} catch (err) {
console.log("Score not saved:", err);
}

}


// ================= EXPLANATION ================= //

async function showExplanation(){

let topic = document.getElementById("topic").value;
let level = localStorage.getItem("final_level") || "beginner";

const response = await fetch(
`http://127.0.0.1:8000/get_explanation?topic=${topic}&level=${level}`
);

const data = await response.json();

document.getElementById("explanation").innerText = data.explanation;

showPage(6);

}


// ================= VIDEOS ================= //

async function showVideos(){

let topic = document.getElementById("topic").value;
let level = localStorage.getItem("final_level") || "beginner";

const response = await fetch(
`http://127.0.0.1:8000/get_videos?topic=${topic}&level=${level}`
);

const data = await response.json();

let html = "";

data.videos.forEach(v=>{
html += `<p>📺 <a href="${v.url}" target="_blank">${v.title}</a></p>`;
});

html += `<br><button onclick="loadDashboard()">📊 Go to Dashboard</button>`;

document.getElementById("videos").innerHTML = html;

showPage(7);

}


// ================= DASHBOARD (FIXED) ================= //

async function loadDashboard(){

let user_id = localStorage.getItem("user_id");

if(!user_id){
alert("Please login first!");
return;
}

const response = await fetch(`http://127.0.0.1:8000/dashboard/${user_id}`);
const data = await response.json();

if(data.error){
alert(data.error);
return;
}

let html = `
<h3>👤 User: ${data.username}</h3>
<h3>🔐 Login Count: ${data.login_count}</h3>
<h3>⏱ Time Spent: ${(data.total_time_spent/60).toFixed(1)} mins</h3>
<h3>📊 Total Quizzes: ${data.total_quizzes}</h3>
<h3>📈 Average Score: ${data.average_score.toFixed(2)}</h3>
<hr>
`;

(data.progress || []).forEach(p=>{
html += `<p>📘 ${p.topic} → ${p.score} / ${p.total}</p>`;
});

document.getElementById("dashboard").innerHTML = html;

showPage(8);
}