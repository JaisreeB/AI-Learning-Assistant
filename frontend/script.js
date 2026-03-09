let quizData = [];
let username = "";


function nextPage(step){

if(step === 1){

username = document.getElementById("username").value;

document.getElementById("welcomeText").innerText =
"Hello " + username + "! What would you like to learn today?";

showPage(2);

}

else if(step === 2){

showPage(3);

}

}


function showPage(page){

for(let i=1;i<=7;i++){
document.getElementById("page"+i).classList.add("hidden");
}

document.getElementById("page"+page).classList.remove("hidden");

}



async function loadQuiz(){

let topic = document.getElementById("topic").value;
let sector = document.getElementById("sector").value;

const response = await fetch(`http://127.0.0.1:8000/get_quiz?topic=${topic}&sector=${sector}`);
const data = await response.json();

quizData = data.quiz;

let quizHTML="";

quizData.forEach((q,index)=>{

quizHTML += `<p><b>${index+1}. ${q.question}</b></p>`;

q.options.forEach(option=>{

quizHTML += `<input type="radio" name="q${index}" value="${option}">
${option}<br>`;

});

quizHTML+="<br>";

});

document.getElementById("quiz").innerHTML=quizHTML;

showPage(4);

}



function submitQuiz(){

let score=0;
let resultHTML="";

quizData.forEach((q,index)=>{

let selected=document.querySelector(`input[name="q${index}"]:checked`);

if(selected && selected.value===q.answer){

score++;
resultHTML+=`<p>Q${index+1}: ✅ Correct</p>`;

}else{

resultHTML+=`<p>Q${index+1}: ❌ Correct Answer: <b>${q.answer}</b></p>`;

}

});


resultHTML+=`<h3>Your Score: ${score} / ${quizData.length}</h3>`;

document.getElementById("result").innerHTML=resultHTML;

showPage(5);

}



async function showExplanation(){

let topic=document.getElementById("topic").value;

const response=await fetch(`http://127.0.0.1:8000/get_explanation?topic=${topic}&level=general`);
const data=await response.json();

document.getElementById("explanation").innerText=data.explanation;

showPage(6);

}



async function showVideos(){

let topic=document.getElementById("topic").value;

const response=await fetch(`http://127.0.0.1:8000/get_videos?topic=${topic}`);
const data=await response.json();

let html="";

data.videos.forEach(v=>{

html+=`<p><a href="${v.url}" target="_blank">${v.title}</a></p>`;

});

document.getElementById("videos").innerHTML=html;

showPage(7);

}