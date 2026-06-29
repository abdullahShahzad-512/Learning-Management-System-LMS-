window.GeneratedQuiz = null;

const QuizRenderer = {

    render(quiz) {

        window.GeneratedQuiz = quiz;

        const container = document.getElementById("generatedQuestionsContainer");

        container.innerHTML = "";

        quiz.questions.forEach((question, index) => {

            const card = document.createElement("div");
            card.className = "generated-question-card generated-question";

            card.innerHTML = `
        <div class="question-number">Question ${index + 1}</div>

        <textarea class="field-input question-text mb-1" rows="2">${question.question}</textarea>

        <div class="mt-3 space-y-1">
          ${question.options.map((option) => `
            <input class="field-input option" value="${option}">
          `).join("")}
        </div>

        <div class="mt-4">
          <label class="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">
            Correct Answer
          </label>
          <input class="field-input answer" value="${question.answer}">
        </div>

        <div class="card-actions">
          <button type="button" class="btn-action delete-question">
            <span class="material-symbols-outlined" style="font-size:15px;">delete</span>
            Remove
          </button>
        </div>
      `;

            /* Remove button */
            card.querySelector(".delete-question").addEventListener("click", () => {
                card.remove();
                /* Hide Save All if no cards left */
                if (!document.querySelector(".generated-question")) {
                    document.getElementById("saveAllContainer").classList.add("hidden");
                }
            });

            container.appendChild(card);

        });

    }

};

/* ── Save All ── */
document
    .getElementById("saveAllQuestions")
    .addEventListener("click", async () => {

        const quizId = document.getElementById("quizId").value;
        const questions = collectQuestions();

        const response = await fetch(`/quiz/${quizId}/import`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ questions })
        });

        const result = await response.json();

        if (result.success) {
            alert("Questions imported successfully.");
            location.reload();
        }

    });

function collectQuestions() {

    const questions = [];

    document.querySelectorAll(".generated-question").forEach(card => {
        questions.push({
            question: card.querySelector(".question-text").value,
            options: [...card.querySelectorAll(".option")].map(x => x.value),
            answer: card.querySelector(".answer").value
        });
    });

    return questions;

}