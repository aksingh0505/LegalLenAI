function summarize() {
  let text = document.getElementById("documentText").value;
  document.getElementById("resultText").innerText = "📑 Summary:\n\nThis document covers rent, deposit, lock-in period, utilities, penalties, and termination terms.";
  saveHistory("Summary");
}

function checkRisks() {
  let text = document.getElementById("documentText").value;
  document.getElementById("resultText").innerText = "⚠️ Risks:\n\n- Security Deposit (2 months)\n- Lock-in Period (6 months)\n- Rent Escalation (8%)\n- Penalty for late payment\n- Arbitration clause";
  saveHistory("Risks");
}

function explainClause() {
  document.getElementById("resultText").innerText = "🔍 Clause Explanation:\n\nLock-in Period means you cannot leave the house before 6 months, or else you may lose your deposit.";
  saveHistory("Explain Clause");
}

function saveHistory(item) {
  let historyList = document.getElementById("history");
  let li = document.createElement("li");
  li.innerText = item + " checked";
  historyList.appendChild(li);
}
