async function sendQuestion() {
  const input = document.getElementById("question");
  const responseDiv = document.getElementById("response");
  const question = input.value;

  if (!question) return;

  // ユーザーの質問を表示
  const userMessage = document.createElement("div");
  userMessage.className = "message user";
  userMessage.textContent = question;
  responseDiv.appendChild(userMessage);

  // API に送信
  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: question })
  });

  const data = await res.json();

  // Botの回答をMarkdownでHTML表示
  const botMessage = document.createElement("div");
  botMessage.className = "message bot";
  botMessage.innerHTML = `<strong>[${data.source}]</strong><br>` + marked.parse(data.answer || "(エラー)");
  responseDiv.appendChild(botMessage);

  // 入力をクリアし、スクロール
  input.value = "";
  responseDiv.scrollTop = responseDiv.scrollHeight;
}
