async function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const status = document.getElementById("uploadStatus");

  if (!fileInput.files.length) {
    status.innerText = "Please select a file.";
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  status.innerText = "Uploading...";

  const res = await fetch("/upload", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  status.innerText = data.status || data.detail;
}

async function askQuestion() {
  const question = document.getElementById("question").value;
  const answerBox = document.getElementById("answerBox");

  if (!question.trim()) {
    answerBox.innerText = "Please enter a question.";
    return;
  }

  answerBox.innerText = "Thinking...";

  const res = await fetch("/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, top_k: 5 })
  });

  const data = await res.json();
  answerBox.innerText = data.answer || "No answer found.";
}