(function (exports) {
  const CHUNK_SIZE = 500;

  // Helpers
  function createDivider() {
    const divider = document.createElement("div");
    divider.className = "option-divider";
    divider.innerHTML = "&nbsp;";
    return divider;
  }

  function createAppendElement() {
    const moreDiv = document.createElement("div");
    moreDiv.className = "option-more";
    moreDiv.innerHTML = `<a href="#" class="load-more">
                       Show ${CHUNK_SIZE} more…
                     </a>`;
    return moreDiv;
  }

  // Multi‐Selector for ItemSet & LocationSet
  function initMultiSelectors() {
    document.querySelectorAll(".multi-selector").forEach((container) => {
      const optionName = container.dataset.optionName;
      const rawNames = container.dataset.names || container.dataset.locations;
      const allNames = rawNames ? JSON.parse(rawNames) : [];
      const defaults = JSON.parse(container.dataset.defaults || "[]");
      const selectedSet = new Set(defaults);

      let groups = null;
      if (container.dataset.groups) {
        const rawGroups = JSON.parse(container.dataset.groups);
        if (rawGroups && typeof rawGroups === "object" && !Array.isArray(rawGroups)) {
          groups = rawGroups;
        } else {
          console.log("initMultiSelectors: ignoring non-object data-groups", rawGroups);
        }
      }

      const searchInput = container.querySelector(".multi-search");
      const listContainer = container.querySelector(".multi-list");
      let currentLimit = CHUNK_SIZE;

      function createEntry(name, isChecked, isGroup) {
        const div = document.createElement("div");
        div.className = "option-entry" + (isGroup ? " group-entry" : "");

        const input = document.createElement("input");
        input.type = "checkbox";
        input.id = `${optionName}-${name}`;
        input.name = optionName;
        input.value = name;
        if (isChecked) {
          input.checked = true;
        }

        const label = document.createElement("label");
        label.htmlFor = `${optionName}-${name}`;
        label.textContent = name;

        div.appendChild(input);
        div.appendChild(label);
        return div;
      }

      listContainer.addEventListener("change", (e) => {
        const cb = e.target;
        if (cb.tagName === "INPUT" && cb.type === "checkbox") {
          cb.checked ? selectedSet.add(cb.value) : selectedSet.delete(cb.value);
          render(searchInput.value);
        }
      });

      listContainer.addEventListener("click", (e) => {
        if (e.target.matches(".load-more")) {
          e.preventDefault();
          currentLimit += CHUNK_SIZE;
          render(searchInput.value);
        }
      });

      searchInput.addEventListener("input", () => {
        currentLimit = CHUNK_SIZE;
        render(searchInput.value);
      });

      function render(filter = "") {
        listContainer.innerHTML = "";
        const searchInputValue = filter.toLowerCase();

        const allGroupNames = groups ? Object.keys(groups).filter((group) => group !== "Everything" && group !== "Everywhere") : [];

        const checkedGroups = allGroupNames.filter((group) => selectedSet.has(group)).sort((a, b) => a.localeCompare(b));

        const uncheckedGroups = allGroupNames.filter((group) => !selectedSet.has(group) && group.toLowerCase().includes(searchInputValue))
          .sort((a, b) => a.localeCompare(b));

        const matchedItems = allNames.filter((name) =>
          name.toLowerCase().includes(searchInputValue)
        );

        const checkedItems = Array.from(selectedSet)
          .filter((name) => allNames.includes(name))
          .sort((a, b) => a.localeCompare(b));

        const uncheckedItems = matchedItems
          .filter((name) => !selectedSet.has(name))
          .sort((a, b) => a.localeCompare(b));

        checkedGroups.forEach((group) =>
          listContainer.appendChild(createEntry(group, true, true))
        );

        checkedItems.forEach((item) =>
          listContainer.appendChild(createEntry(item, true, false))
        );

        if (uncheckedGroups.length || uncheckedItems.length) {
          listContainer.appendChild(createDivider());
        }

        uncheckedGroups.forEach((group) =>
          listContainer.appendChild(createEntry(group, false, true))
        );

        if (uncheckedGroups.length && uncheckedItems.length) {
          listContainer.appendChild(createDivider());
        }

        uncheckedItems
          .slice(0, currentLimit)
          .forEach((elem) =>
            listContainer.appendChild(createEntry(elem, false, false))
          );

        if (uncheckedItems.length > currentLimit) {
            listContainer.appendChild(createAppendElement());
        }
      }

      render();
    });
  }

  // Multi-Selector for OptionCounter
  function initMultiCounters() {
    document.querySelectorAll(".multi-counter").forEach((container) => {
      const allNames = JSON.parse(container.dataset.names || "[]");
      const defaults = JSON.parse(container.dataset.defaults || "{}");
      const current = {};
      allNames.forEach((name) => {
        const value = parseInt(defaults[name], 10);
        current[name] = isNaN(value) ? 0 : value;
      });

      const searchInput = container.querySelector(".multi-search");
      const listContainer = container.querySelector(".multi-list");
      let currentLimit = CHUNK_SIZE;

      function createEntry(name) {
        const val = current[name] || 0;
        const div = document.createElement("div");
        div.className = "option-entry" + (val > 0 ? " selected-entry" : "");

        const input = document.createElement("input");
        input.type = "number";
        input.id = `${container.dataset.optionName}-${name}-qty`;
        input.name = `${container.dataset.optionName}||${name}||qty`;
        input.value = val;
        input.setAttribute("data-name", name);

        const label = document.createElement("label");
        label.htmlFor = `${container.dataset.optionName}-${name}-qty`;
        label.textContent = name;

        div.appendChild(input);
        div.appendChild(label);
        return div;
      }

      listContainer.addEventListener("input", (e) => {
        if (e.target.matches("input[type=number]")) {
          const name = e.target.dataset.name;
          const value = parseInt(e.target.value, 10);
          current[name] = isNaN(value) ? 0 : value;
          render(searchInput.value);
        }
      });

      listContainer.addEventListener("click", (e) => {
        if (e.target.matches(".load-more")) {
          e.preventDefault();
          currentLimit += CHUNK_SIZE;
          render(searchInput.value);
        }
      });

      searchInput.addEventListener("input", () => {
        currentLimit = CHUNK_SIZE;
        render(searchInput.value);
      });

      function render(filter = "") {
        listContainer.innerHTML = "";
        const searchInputValue = filter.toLowerCase();

        const selected = allNames.filter((n) => current[n] > 0).sort((a, b) => a.localeCompare(b));

        const unselected = allNames.filter((name) => current[name] === 0 && name.toLowerCase().includes(searchInputValue))
          .sort((a, b) => a.localeCompare(b));

        selected.forEach((n) => listContainer.appendChild(createEntry(n)));

        if (selected.length && unselected.length) {
          listContainer.appendChild(createDivider());
        }

        unselected.slice(0, currentLimit).forEach((n) => listContainer.appendChild(createEntry(n)));

        if (unselected.length > currentLimit) {
            listContainer.appendChild(createAppendElement());
        }
      }
      render();
    });
  }

  exports.initMultiSelectors = initMultiSelectors;
  exports.initMultiCounters = initMultiCounters;
})((window.playerOptions = window.playerOptions || {}));

document.addEventListener("DOMContentLoaded", () => {
  window.playerOptions.initMultiSelectors?.();
  window.playerOptions.initMultiCounters?.();
});
