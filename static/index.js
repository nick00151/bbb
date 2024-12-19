const container = document.querySelector(".container");
const userInput = document.getElementById("user_input");
const submitBtn = document.getElementById("submit_btn");
const outputDiv = document.getElementById("output");
const loadingDiv = document.getElementById("loading");

submitBtn.addEventListener("click", async function () {
    const question = userInput.value.trim();
    outputDiv.style.display = "none";
    loadingDiv.style.display = "block";
    submitBtn.disabled = true; // 禁用按鈕，避免重複請求

    if (!question) {
        loadingDiv.textContent = "Please enter a question.";
        submitBtn.disabled = false;
        return;
    }

    try {
        const response = await fetch("/api/get_response", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ user_input: question }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || "Server error");
        }

        const data = await response.json();
        outputDiv.textContent = `Response: ${data.response}`;
    } catch (error) {
        outputDiv.textContent = `Error: ${error.message}`;
    } finally {
        loadingDiv.style.display = "none";
        outputDiv.style.display = "block";
        submitBtn.disabled = false; // 恢復按鈕狀態
    }
});

