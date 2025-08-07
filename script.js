// frontend/script.js

const BACKEND = "https://huggingface.co/spaces/chanaivibe/college1helpbot-backend?logs=container"; // Replace when deployed

async function uploadPDF() {
  const fileInput = document.getElementById("pdfInput");
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const res = await fetch(`${BACKEND}/upload_pdf/`, {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  alert(data.msg);
}

async function askQuestion() {
  const question = document.getElementById("question").value;
  const formData = new FormData();
  formData.append("question", question);

  const res = await fetch(`${BACKEND}/ask/`, {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  document.getElementById("answer").innerText = data.answer;
}
