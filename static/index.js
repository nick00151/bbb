submitBtn.addEventListener("click", async function () {
    const question = userInput.value.trim(); // 取得使用者輸入的問題，並去除前後空白
    outputDiv.style.display = "none"; // 隱藏回應區域
    loadingDiv.style.display = "block"; // 顯示加載提示
    submitBtn.disabled = true; // 禁用按鈕，避免重複提交

    if (!question) { // 如果輸入框為空
        loadingDiv.textContent = "請輸入問題，才能獲取回答。"; // 顯示提示訊息
        submitBtn.disabled = false; // 恢復按鈕狀態
        return;
    }

    try {
        const response = await fetch("/api/get_response", { // 發送 POST 請求到伺服器
            method: "POST",
            headers: {
                "Content-Type": "application/json", // 設定請求的內容類型為 JSON
            },
            body: JSON.stringify({ user_input: question }), // 將使用者輸入的問題轉換為 JSON 格式
        });

        const data = await response.json(); // 解析伺服器返回的 JSON 數據
        if (data.error) { // 如果返回錯誤訊息
            outputDiv.innerHTML = `<p style="color: red;">錯誤：${data.error}</p>`;
        } else if (data.response) { // 如果返回有效回答
            const formattedResponse = data.response.replace(/\n/g, "<br>"); // 替換換行符為 <br>
            outputDiv.innerHTML = `<div>回應：<br>${formattedResponse}</div>`;
        } else { // 如果伺服器沒有返回有效回答
            outputDiv.innerHTML = "<p style='color: red;'>伺服器未返回有效回答，請稍後再試。</p>";
        }
    } catch (error) { // 捕獲任何錯誤
        outputDiv.innerHTML = `<p style="color: red;">錯誤：${error.message}</p>`;
    } finally {
        loadingDiv.style.display = "none"; // 隱藏加載提示
        outputDiv.style.display = "block"; // 顯示回應區域
        submitBtn.disabled = false; // 恢復按鈕狀態
    }
});
