const status = document.querySelector(".copy-status");
let clearStatus;
for (const button of document.querySelectorAll("[data-copy]")) {
  button.addEventListener("click", async () => {
    const source = document.getElementById(button.dataset.copy);
    try {
      await navigator.clipboard.writeText(source.textContent);
      status.textContent = "Installation commands copied";
    } catch {
      const range = document.createRange();
      range.selectNodeContents(source);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = "Commands selected. Copy with your keyboard.";
    }
    clearTimeout(clearStatus);
    clearStatus = setTimeout(() => {
      status.textContent = "";
    }, 4000);
  });
}
