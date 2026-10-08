(() => {
  const buttons = [...document.querySelectorAll("[data-filter]")];
  const papers = [...document.querySelectorAll(".publication")];
  const headings = [...document.querySelectorAll(".pub-year")];
  const count = document.querySelector(".results-count");
  const empty = document.querySelector(".empty-message");
  if (!buttons.length) return;

  function applyFilter(tag) {
    let visible = 0;
    for (const paper of papers) {
      const tags = (paper.dataset.tags || "").split("|");
      const show = tag === "all" || tags.includes(tag);
      paper.hidden = !show;
      if (show) visible += 1;
    }
    for (const heading of headings) {
      let sibling = heading.nextElementSibling;
      let hasVisible = false;
      while (sibling && !sibling.classList.contains("pub-year")) {
        if (sibling.classList.contains("publication") && !sibling.hidden) hasVisible = true;
        sibling = sibling.nextElementSibling;
      }
      heading.hidden = !hasVisible;
    }
    for (const button of buttons) {
      const selected = button.dataset.filter === tag;
      button.classList.toggle("active", selected);
      button.setAttribute("aria-pressed", String(selected));
    }
    count.textContent = `Showing ${visible} publication${visible === 1 ? "" : "s"}`;
    empty.hidden = visible !== 0;
  }

  for (const button of buttons) {
    button.addEventListener("click", () => applyFilter(button.dataset.filter));
  }
})();
