const userInput = document.getElementById("user_input");
const submitBtn = document.getElementById("submit_btn");
const outputDiv = document.getElementById("output");
const loadingDiv = document.getElementById("loading");

submitBtn.addEventListener("click", async function () {
    const question = userInput.value.trim();
    outputDiv.style.display = "none"; // 隱藏輸出區
    loadingDiv.style.display = "block"; // 顯示載入動畫
    submitBtn.disabled = true; // 禁用按鈕，避免重複請求

    if (!question) {
        loadingDiv.textContent = "請輸入問題，才能獲取回答。";
        submitBtn.disabled = false;
        return;
    }

    try {
        console.log("發送請求中..."); // 調試訊息
        const response = await fetch("http://127.0.0.1:5000/api/get_response", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ user_input: question }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.response || "伺服器錯誤");
        }

        const data = await response.json();
        console.log("收到回應：", data); // 調試訊息
        outputDiv.innerHTML = `回應：<br>${data.response.replace(/\n/g, "<br>")}`;
    } catch (error) {
        outputDiv.textContent = `錯誤：${error.message}`;
    } finally {
        loadingDiv.style.display = "none"; // 隱藏載入動畫
        outputDiv.style.display = "block"; // 顯示輸出
        submitBtn.disabled = false; // 恢復按鈕狀態
    }
});

