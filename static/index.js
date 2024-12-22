// 取得 DOM 元素
const userInput = document.getElementById("user_input");
const submitBtn = document.getElementById("submit_btn");
const outputDiv = document.getElementById("output");
const loadingDiv = document.getElementById("loading");

// 監聽按鈕點擊事件
submitBtn.addEventListener("click", async function () {
    console.log("按鈕被點擊了"); // 確認按鈕事件是否觸發
    const question = userInput.value.trim(); // 去除多餘空白

    // 清理並初始化狀態
    outputDiv.style.display = "none";
    loadingDiv.style.display = "block";
    submitBtn.disabled = true; // 禁用按鈕，避免重複請求
    loadingDiv.textContent = "正在處理請求...";

    // 檢查輸入是否為空
    if (!question) {
        loadingDiv.textContent = "請輸入問題，才能獲取回答。";
        submitBtn.disabled = false;
        return;
    }

    try {
        console.log("正在發送請求到後端 API...");
        // 發送 POST 請求到後端
        const response = await fetch("/api/get_response", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ user_input: question }),
        });

        // 檢查伺服器是否返回成功
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.response || "伺服器錯誤");
        }

        // 解析伺服器返回的 JSON 數據
        const data = await response.json();
        console.log("伺服器返回成功：", data);

        // 顯示結果並格式化換行
        outputDiv.innerHTML = `回應：<br>${data.response.replace(/\n/g, "<br>")}`;
    } catch (error) {
        console.error("發生錯誤：", error); // 在控制台中記錄錯誤
        outputDiv.textContent = `錯誤：${error.message}`;
    } finally {
        // 恢復界面狀態
        loadingDiv.style.display = "none";
        outputDiv.style.display = "block";
        submitBtn.disabled = false;
    }
});
