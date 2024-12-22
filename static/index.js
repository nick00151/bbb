submitBtn.addEventListener("click", async function () {
    const question = userInput.value.trim();
    outputDiv.style.display = "none";
    loadingDiv.style.display = "block";
    submitBtn.disabled = true;

    if (!question) {
        loadingDiv.textContent = "請輸入問題，才能獲取回答。";
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

        const data = await response.json();
        if (data.error) {
            outputDiv.textContent = `錯誤：${data.error}`;
        } else if (data.response) {
            outputDiv.textContent = `回應：${data.response}`;
        } else {
            outputDiv.textContent = "伺服器未返回有效回答，請稍後再試。";
        }
    } catch (error) {
        outputDiv.textContent = `錯誤：${error.message}`;
    } finally {
        loadingDiv.style.display = "none";
        outputDiv.style.display = "block";
        submitBtn.disabled = false;
    }
});
