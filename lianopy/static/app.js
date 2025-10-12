const state = {
  path: "",
  page: 1,
  pageSize: 50,
  total: 0,
  items: [],
  thumbCache: new Map(),
  selected: new Set(),
  filter: "all",
  search: "",
  sort: "name",
  group: "none",
  view: "tile" // or "list"
};



const titleToggle = document.getElementById("titleToggle");
const commands = document.getElementById("commands");

titleToggle.onclick = () => {
  commands.classList.toggle("hidden");
  // Optional: change arrow indicator
  if (commands.classList.contains("hidden")) {
    titleToggle.textContent = "Liana ▾";
  } else {
    titleToggle.textContent = "Liana ▴";
  }
};

async function loadPage() {
  const overlay = document.getElementById("loadingOverlay");
  let timer = setTimeout(() => overlay.classList.remove("hidden"), 200); // show if slow

  try {
    const url = `/api/list?path=${encodeURIComponent(state.path)}&page=${state.page}&page_size=${state.pageSize}&thumbnails=true`;
    const res = await fetch(url);
    const data = await res.json();
    state.total = data.total;
    state.items = data.items;
    state.path = data.path || "";

    // cache thumbs
    for (const item of state.items) {
      if (item.thumb) state.thumbCache.set(item.path, item.thumb);
    }

    render();
  } finally {
    clearTimeout(timer);
    overlay.classList.add("hidden");
  }
}

function passesFilter(item) {
  if (state.filter === "all" || item.is_dir) return true;
  const name = item.name.toLowerCase();
  if (state.filter === "images") return /\.(jpg|jpeg|png|gif|webp)$/i.test(name);
  if (state.filter === "videos") return /\.(mp4|mov|avi|mkv|webm)$/i.test(name);
  if (state.filter === "docs") return /\.(pdf|txt|docx?|xlsx?)$/i.test(name);
  return true;
}
function navigateTo(path) {
  state.path = path;
  state.page = 1;
  history.pushState({ path: state.path, page: state.page }, "", `?path=${encodeURIComponent(state.path)}&page=${state.page}`);
  loadPage();
}

function setPage(page) {
  state.page = page;
  history.pushState({ path: state.path, page: state.page }, "", `?path=${encodeURIComponent(state.path)}&page=${state.page}`);
  loadPage();
}


window.addEventListener("popstate", (event) => {
  if (event.state) {
    state.path = event.state.path || "";
    state.page = event.state.page || 1;
  } else {
    state.path = "";
    state.page = 1;
  }
  loadPage();
});

function render() {
  document.getElementById("pageInfo").textContent =
    `Page ${state.page} of ${Math.ceil(state.total / state.pageSize)} (${state.total} items)`;

  // --- breadcrumb ---
  const breadcrumb = document.getElementById("breadcrumb");
  breadcrumb.innerHTML = "";

  const parts = state.path.split("/").filter(Boolean);

  // Root link
  const rootLink = document.createElement("a");
  rootLink.href = "#";
  rootLink.textContent = "root";
  rootLink.onclick = (e) => { e.preventDefault(); navigateTo(""); };
  breadcrumb.appendChild(rootLink);

  // Each folder segment
  parts.forEach((part, idx) => {
    breadcrumb.append(" / ");
    const a = document.createElement("a");
    a.href = "#";
    a.textContent = part;

    const targetPath = parts.slice(0, idx + 1).join("/");

    if (idx === parts.length - 1) {
      a.style.fontWeight = "bold";
      a.style.pointerEvents = "none";
    } else {
      a.onclick = (e) => { e.preventDefault(); navigateTo(targetPath); };
    }
    breadcrumb.appendChild(a);
  });

  // --- grid ---
  const grid = document.getElementById("grid");
grid.innerHTML = "";
grid.className = state.view === "list" ? "list-view" : "tile-view";


  let items = state.items;

// filter
if (state.filter === "images") {
  items = items.filter(i => i.mime?.startsWith("image/"));
} else if (state.filter === "videos") {
  items = items.filter(i => i.mime?.startsWith("video/"));
} else if (state.filter === "docs") {
  items = items.filter(i => i.mime?.includes("pdf") || i.mime?.includes("word"));
}

// search
if (state.search) {
  items = items.filter(i => i.name.toLowerCase().includes(state.search));
}

// sort
if (state.sort === "name") {
  items.sort((a,b) => a.name.localeCompare(b.name));
} else if (state.sort === "date") {
  items.sort((a,b) => (a.mtime||0) - (b.mtime||0));
} else if (state.sort === "size") {
  items.sort((a,b) => (a.size||0) - (b.size||0));
}

if (state.group === "type") {
  // group by mime major type
  const groups = {};
  for (const item of items) {
    const key = item.is_dir ? "Folders" : (item.mime?.split("/")[0] || "Other");
    if (!groups[key]) groups[key] = [];
    groups[key].push(item);
  }
  items = Object.entries(groups).flatMap(([label, arr]) => {
    return [{ is_group_header: true, name: label }, ...arr];
  });
}


  for (const item of state.items.filter(passesFilter)) {
    const card = document.createElement("div");
    card.className = "card";

    const thumbDiv = document.createElement("div");
    thumbDiv.className = "thumb";
    if (item.is_dir) {
      thumbDiv.textContent = "📁";
      thumbDiv.style.fontSize = "2rem";
    } else {
      const img = document.createElement("img");
      const cached = state.thumbCache.get(item.path);
      if (cached) img.src = cached;
      else if (item.thumb) img.src = item.thumb;
      else {
        thumbDiv.textContent = "📄";
        thumbDiv.style.fontSize = "2rem";
      }
      if (img.src) thumbDiv.appendChild(img);
    }
    card.appendChild(thumbDiv);

    const name = document.createElement("div");
    name.className = "name";
    name.textContent = item.name;
    card.appendChild(name);

    const actions = document.createElement("div");
    actions.className = "actions hidden";
    if (!item.is_dir) {
      const dlBtn = document.createElement("button");
      dlBtn.textContent = "⬇";
      dlBtn.onclick = (e) => {
        e.stopPropagation();
        window.location = `/api/download?path=${encodeURIComponent(item.path)}`;
      };
      actions.appendChild(dlBtn);

      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.checked = state.selected.has(item.path);
      checkbox.onchange = (e) => {
        e.stopPropagation();
        if (e.target.checked) state.selected.add(item.path);
        else state.selected.delete(item.path);
      };
      actions.appendChild(checkbox);
    }
    card.appendChild(actions);

    // Card click
    if (item.is_dir) {
      card.onclick = () => { navigateTo(item.path); };
    } else {
      card.onclick = () => window.open(`/api/open?path=${encodeURIComponent(item.path)}`, "_blank");
    }
    card.style.cursor = "pointer";

    // Long press (mouse + touch)
    let pressTimer;
    const startPress = () => {
      pressTimer = setTimeout(() => { actions.classList.remove("hidden"); }, 600);
    };
    const cancelPress = () => clearTimeout(pressTimer);

    card.addEventListener("mousedown", startPress);
    card.addEventListener("mouseup", cancelPress);
    card.addEventListener("mouseleave", cancelPress);

    card.addEventListener("touchstart", startPress, { passive: true });
    card.addEventListener("touchend", cancelPress);
    card.addEventListener("touchmove", cancelPress);

    grid.appendChild(card);
  }
}



// controls
document.getElementById("prev").onclick = () => {
  if (state.page > 1) { setPage(state.page - 1); }
};
document.getElementById("next").onclick = () => {
  const maxPage = Math.ceil(state.total / state.pageSize);
  if (state.page < maxPage) { setPage(state.page + 1); }
};

document.getElementById("backBtn").onclick = () => {
  window.history.back();
};

document.getElementById("forwardBtn").onclick = () => {
  window.history.forward();
};
// Filter dropdown
document.getElementById("filterDropdown").onchange = (e) => {
  state.filter = e.target.value;
  render();
};

// Search box
document.getElementById("searchBox").oninput = (e) => {
  state.search = e.target.value.toLowerCase();
  render();
};

// Sort dropdown
document.getElementById("sortDropdown").onchange = (e) => {
  state.sort = e.target.value;
  render();
};

// Group dropdown (basic placeholder)
document.getElementById("groupDropdown").onchange = (e) => {
  state.group = e.target.value;
  render();
};

// View toggle
document.getElementById("tileViewBtn").onclick = () => {
  state.view = "tile";
  render();
};
document.getElementById("listViewBtn").onclick = () => {
  state.view = "list";
  render();
};



// Back/Forward buttons
const backBtn = document.getElementById("backBtn");
const forwardBtn = document.getElementById("forwardBtn");

backBtn.onclick = () => window.history.back();
forwardBtn.onclick = () => window.history.forward();

// Update button states (enable/disable)
function updateNavButtons() {
  // Unfortunately, browsers don’t expose “canGoBack/canGoForward”.
  // But we can approximate: disable Back at root, disable Forward unless user has gone back.
  backBtn.disabled = (state.path === "");
  // Forward button will re-enable automatically when user goes back and history has a forward entry.
}



document.getElementById("downloadSelected").onclick = async () => {
  const paths = Array.from(state.selected);
  if (paths.length === 0) return;
  const res = await fetch("/api/download-zip", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(paths),
  });
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = "selection.zip"; a.click();
  URL.revokeObjectURL(url);
};

// filter control
document.getElementById("filter").onchange = (e) => {
  state.filter = e.target.value;
  render();
};



// Initialize from URL and set initial history state
function initStateFromURL() {
  const urlParams = new URLSearchParams(window.location.search);
  state.path = urlParams.get("path") || "";
  state.page = parseInt(urlParams.get("page") || "1", 10);
  history.replaceState({ path: state.path, page: state.page }, "", `?path=${encodeURIComponent(state.path)}&page=${state.page}`);
}

initStateFromURL();
loadPage();

