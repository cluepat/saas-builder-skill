import { buildPrompt, resolveStackChoices } from "./prompt-builder.mjs?v=1.2.2";

const status = document.querySelector(".copy-status");
let clearStatus;
for (const button of document.querySelectorAll("[data-copy]")) {
  button.addEventListener("click", async () => {
    const source = document.getElementById(button.dataset.copy);
    try {
      await navigator.clipboard.writeText(source.textContent);
      status.textContent =
        button.dataset.copy === "stack-prompt"
          ? "Your stack prompt copied"
          : button.dataset.copy === "install-cursor"
            ? "Repository URL copied"
            : "Installation commands copied";
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

const tablist = document.querySelector(".client-tabs");
const tabs = [...tablist.querySelectorAll('[role="tab"]')];
function selectClient(selected) {
  for (const tab of tabs) {
    const active = tab === selected;
    tab.setAttribute("aria-selected", String(active));
    tab.tabIndex = active ? 0 : -1;
    const panel = document.getElementById(tab.getAttribute("aria-controls"));
    panel.setAttribute("role", "tabpanel");
    panel.hidden = !active;
  }
}
for (const [index, tab] of tabs.entries()) {
  tab.addEventListener("click", () => selectClient(tab));
  tab.addEventListener("keydown", (event) => {
    const targets = {
      ArrowRight: (index + 1) % tabs.length,
      ArrowLeft: (index + tabs.length - 1) % tabs.length,
      Home: 0,
      End: tabs.length - 1,
    };
    if (!(event.key in targets)) return;
    event.preventDefault();
    const next = tabs[targets[event.key]];
    selectClient(next);
    next.focus();
  });
}
selectClient(tabs[0]);
tablist.hidden = false;

const stackForm = document.getElementById("stack-form");
function updatePrompt() {
  for (const custom of stackForm.querySelectorAll("[data-custom-for]")) {
    const selected =
      stackForm.elements[custom.dataset.customFor].value === "__custom";
    custom.hidden = !selected;
    custom.querySelector("input").disabled = !selected;
  }
  const fields = resolveStackChoices(
    Object.fromEntries(new FormData(stackForm)),
  );
  fields.existing = stackForm.elements.existing.checked;
  document.getElementById("stack-prompt").textContent = buildPrompt(fields);
}
stackForm.addEventListener("input", updatePrompt);
stackForm.addEventListener("change", updatePrompt);
stackForm.addEventListener("submit", (event) => event.preventDefault());
updatePrompt();
document.querySelector(".prompt-builder").hidden = false;
