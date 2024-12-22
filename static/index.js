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
            outputDiv.innerHTML = `<p style="color: red;">錯誤：${data.error}</p>`;
        } else if (data.response) {
            // 將換行符替換為 <br>
            const formattedResponse = data.response.replace(/\n/g, "<br>");
            outputDiv.innerHTML = `<div>回應：<br>${formattedResponse}</div>`;
        } else {
            outputDiv.innerHTML = "<p style='color: red;'>伺服器未返回有效回答，請稍後再試。</p>";
        }
    } catch (error) {
        outputDiv.innerHTML = `<p style="color: red;">錯誤：${error.message}</p>`;
    } finally {
        loadingDiv.style.display = "none";
        outputDiv.style.display = "block";
        submitBtn.disabled = false;
    }
});
