const container = document.querySelector(".container");
const userInput = document.getElementById("user_input");
const submitBtn = document.getElementById("submit_btn");
const outputDiv = document.getElementById("output");
const loadingDiv = document.getElementById("loading");

// 設置按鈕的事件監聽器
submitBtn.addEventListener("click", async function() {
    const question = userInput.value.trim(); // 取得用戶輸入
    outputDiv.style.display = "none"; // 隱藏舊的結果
    loadingDiv.style.display = "block"; // 顯示處理中提示

    if (!question) {
        loadingDiv.textContent = "Please enter a question."; // 用戶未輸入內容
        return;
    }

    try {
        // 向後端發送請求
        const response = await fetch('/api/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: question })
        });

        if (!response.ok) {
            throw new Error("Failed to get a response from the server.");
        }

        const data = await response.json(); // 解析後端返回的 JSON
        if (data.error) {
            outputDiv.textContent = `Error: ${data.error}`;
        } else {
            outputDiv.textContent = `Response: ${data.response}`;
        }
    } catch (error) {
        outputDiv.textContent = `Error: ${error.message}`;
    } finally {
        loadingDiv.style.display = "none"; // 隱藏處理中提示
        outputDiv.style.display = "block"; // 顯示結果
    }
});
