const task = document.getElementById("task");
const input = document.getElementById("inputText");
const inputLabel = document.getElementById("inputLabel");
const extraFields = document.getElementById("extraFields");
const submitBtn = document.getElementById("submitBtn");
const result = document.getElementById("result");
const statusEl = document.getElementById("status");

function updateForm() {
  extraFields.innerHTML = "";

  if (task.value === "qa") {
    inputLabel.textContent = "Your question";
    input.placeholder = "Example: Which is the largest ocean?";
  } else if (task.value === "explain") {
    inputLabel.textContent = "Topic";
    input.placeholder = "Example: Explain photosynthesis in simple terms.";
  } else if (task.value === "quiz") {
    inputLabel.textContent = "Topic or passage";
    input.placeholder = "Paste a passage or enter a topic to create MCQs.";

    extraFields.innerHTML = `
      <label for="count">Number of questions</label>
      <input id="count" type="number" min="1" max="10" value="3">
    `;
  } else if (task.value === "summarize") {
    inputLabel.textContent = "Educational passage";
    input.placeholder = "Paste the passage you want to summarize.";
  } else {
    inputLabel.textContent = "Learning topic";
    input.placeholder = "Example: SQL";
    extraFields.innerHTML = `
      <div class="extra-grid">
        <div>
          <label for="level">Current level</label>
          <select id="level">
            <option>beginner</option>
            <option>intermediate</option>
            <option>advanced</option>
          </select>
        </div>
        <div>
          <label for="hours">Hours per week</label>
          <input id="hours" type="number" min="1" max="40" value="5">
        </div>
      </div>
    `;
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderQuiz(items) {
  result.classList.remove("empty");
  result.innerHTML = items.map((item, i) => `
    <div class="quiz-item">
      <div class="quiz-question">${i + 1}. ${escapeHtml(item.question)}</div>
      ${item.options.map((option, index) => `
        <div class="option">${String.fromCharCode(65 + index)}. ${escapeHtml(option)}</div>
      `).join("")}
      <div><strong>Answer:</strong> ${escapeHtml(item.answer)}</div>
      ${item.explanation ? `<div><strong>Why:</strong> ${escapeHtml(item.explanation)}</div>` : ""}
    </div>
  `).join("");
}

async function submit() {
  const value = input.value.trim();
  if (!value) {
    result.classList.remove("empty");
    result.textContent = "Please enter some text first.";
    return;
  }

  let endpoint = "";
  let body = {};

  if (task.value === "qa") {
    endpoint = "/qa";
    body = { question: value };
  } else if (task.value === "explain") {
    endpoint = "/explain";
    body = { text: value };
  } else if (task.value === "quiz") {
    endpoint = "/quiz";
    body = {
      text: value,
      count: Number(document.getElementById("count").value || 3)
    };
  } else if (task.value === "summarize") {
    endpoint = "/summarize";
    body = { text: value };
  } else {
    endpoint = "/learn/recommendations";
    body = {
      topic: value,
      level: document.getElementById("level").value,
      weekly_hours: Number(document.getElementById("hours").value || 5)
    };
  }

  submitBtn.disabled = true;
  statusEl.textContent = "Thinking...";
  statusEl.classList.add("busy");
  result.classList.remove("empty");
  result.textContent = "EduGenie is generating your result...";

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(data.detail || "Request failed.");
    }

    if (task.value === "quiz") {
      renderQuiz(data.result);
    } else {
      result.textContent = data.result;
    }

    statusEl.textContent = "Complete";
  } catch (error) {
    result.textContent = `Error: ${error.message}`;
    statusEl.textContent = "Error";
  } finally {
    submitBtn.disabled = false;
    statusEl.classList.remove("busy");
  }
}

task.addEventListener("change", updateForm);
submitBtn.addEventListener("click", submit);
input.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    submit();
  }
});
updateForm();
