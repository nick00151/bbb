// 取得 DOM 元素
const userInput = document.getElementById("user_input");
const submitBtn = document.getElementById("submit_btn");
const outputDiv = document.getElementById("output");
const loadingDiv = document.getElementById("loading");

// 綁定按鈕點擊事件
submitBtn.addEventListener("click", async function () {
    const question = userInput.value.trim(); // 獲取使用者輸入，並移除多餘空白

    // 隱藏輸出區域，顯示加載動畫
    outputDiv.style.display = "none";
    loadingDiv.style.display = "block";
    submitBtn.disabled = true; // 禁用按鈕，避免重複請求

    // 如果使用者未輸入內容
    if (!question) {
        loadingDiv.textContent = "請輸入問題，才能獲取回答。";
        submitBtn.disabled = false;
        return;
    }

    try {
        // 發送 API 請求
        const response = await fetch("/api/get_response", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ user_input: question }),
        });

        // 檢查伺服器回應狀態
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || "伺服器錯誤");
        }

        // 解析回應數據
        const data = await response.json();
        outputDiv.textContent = `回應：${data.response}`;
    } catch (error) {
        // 錯誤處理
        if (error.message.includes("伺服器錯誤")) {
            outputDiv.textContent = "伺服器發生錯誤，請稍後再試。";
        } else {
            outputDiv.textContent = `錯誤：${error.message}`;
        }
    } finally {
        // 恢復按鈕狀態，更新畫面
        loadingDiv.style.display = "none";
        outputDiv.style.display = "block";
        submitBtn.disabled = false;
    }
});

