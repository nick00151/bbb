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

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || "伺服器錯誤");
        }

        const data = await response.json();
        // 將回答內容分段排版
        outputDiv.innerHTML = `回應：<br>${data.response.replace(/\n/g, "<br>")}`;
    } catch (error) {
        if (error.message.includes("伺服器錯誤")) {
            outputDiv.textContent = "伺服器發生錯誤，請稍後再試。";
        } else {
            outputDiv.textContent = `錯誤：${error.message}`;
        }
    } finally {
        loadingDiv.style.display = "none";
        outputDiv.style.display = "block";
        submitBtn.disabled = false; // 恢復按鈕狀態
    }
});

