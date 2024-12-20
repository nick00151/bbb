const userInput = document.getElementById("user_input");
const submitBtn = document.getElementById("submit_btn");
const outputDiv = document.getElementById("output");
const loadingDiv = document.getElementById("loading");

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

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || "伺服器錯誤");
        }

        const data = await response.json();
        if (data.error) {
            outputDiv.innerHTML = `<p>錯誤：${data.error}</p>`;
        } else if (data.response) {
            outputDiv.innerHTML = data.response; // 使用 innerHTML 渲染 HTML 分段
        } else {
            outputDiv.innerHTML = "<p>伺服器未返回有效回答，請稍後再試。</p>";
        }
    } catch (error) {
        if (error.message.includes("伺服器錯誤")) {
            outputDiv.innerHTML = "伺服器發生錯誤，請稍後再試。";
        } else {
            outputDiv.innerHTML = `<p>錯誤：${error.message}</p>`;
        }
    } finally {
        loadingDiv.style.display = "none";
        outputDiv.style.display = "block";
        submitBtn.disabled = false;
    }
});

