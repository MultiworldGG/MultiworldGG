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

      container.restoreValues = (values) => {
        selectedSet.clear();
        values.forEach((value) => selectedSet.add(String(value)));
        render(searchInput.value);
      };

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

      container.restoreValues = (values) => {
        allNames.forEach((name) => {
          const value = parseInt(values[name], 10);
          current[name] = isNaN(value) ? 0 : value;
        });
        render(searchInput.value);
      };

      render();
    });
  }

  function markPresetCustom() {
    const presetSelect = document.getElementById("game-options-preset");
    if (presetSelect) {
      presetSelect.value = "custom";
    }
  }

  function applyNumberBounds(input, container) {
    if (container.dataset.min !== "") {
      input.min = container.dataset.min;
    }
    if (container.dataset.max !== "") {
      input.max = container.dataset.max;
    }
  }

  function initFreeOptionLists() {
    document.querySelectorAll(".free-option-list").forEach((container) => {
      const optionName = container.dataset.optionName;
      const rowsContainer = container.querySelector(".free-form-rows");
      const newValueInput = container.querySelector(".free-form-new-value");
      const addButton = container.querySelector(".free-form-add");
      let nextRowId = 0;

      function addRow(value, markCustom = false) {
        const row = document.createElement("div");
        row.className = "option-entry free-form-row";

        const input = document.createElement("input");
        input.type = "text";
        input.name = `${optionName}||free-list`;
        input.value = String(value);
        input.id = `${optionName}-free-list-${nextRowId++}`;
        input.setAttribute("aria-label", `${optionName} value`);

        const moveUpButton = document.createElement("button");
        moveUpButton.type = "button";
        moveUpButton.className = "free-form-move-up js-required";
        moveUpButton.textContent = "\u2191";
        moveUpButton.setAttribute("aria-label", "Move value up");
        moveUpButton.title = "Move up";
        moveUpButton.addEventListener("click", () => {
          const previousRow = row.previousElementSibling;
          if (previousRow) {
            rowsContainer.insertBefore(row, previousRow);
            markPresetCustom();
          }
        });

        const moveDownButton = document.createElement("button");
        moveDownButton.type = "button";
        moveDownButton.className = "free-form-move-down js-required";
        moveDownButton.textContent = "\u2193";
        moveDownButton.setAttribute("aria-label", "Move value down");
        moveDownButton.title = "Move down";
        moveDownButton.addEventListener("click", () => {
          const nextRow = row.nextElementSibling;
          if (nextRow) {
            rowsContainer.insertBefore(nextRow, row);
            markPresetCustom();
          }
        });

        const removeButton = document.createElement("button");
        removeButton.type = "button";
        removeButton.className = "free-form-remove js-required";
        removeButton.textContent = "\u00d7";
        removeButton.setAttribute("aria-label", "Remove value");
        removeButton.title = "Remove";
        removeButton.addEventListener("click", () => {
          row.remove();
          markPresetCustom();
        });

        row.appendChild(input);
        row.appendChild(moveUpButton);
        row.appendChild(moveDownButton);
        row.appendChild(removeButton);
        rowsContainer.appendChild(row);
        if (markCustom) {
          markPresetCustom();
        }
      }

      function addNewValue() {
        if (!newValueInput.value) {
          return;
        }
        addRow(newValueInput.value, true);
        newValueInput.value = "";
        newValueInput.focus();
      }

      addButton.addEventListener("click", addNewValue);
      newValueInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          addNewValue();
        }
      });
      rowsContainer.addEventListener("input", markPresetCustom);

      container.getValues = () => Array.from(
        rowsContainer.querySelectorAll('input[type="text"]')
      ).map((input) => input.value).filter((value) => value !== "");

      container.restoreValues = (values) => {
        rowsContainer.innerHTML = "";
        values.forEach((value) => addRow(value));
      };

      container.restoreValues(JSON.parse(container.dataset.defaults || "[]"));
    });
  }

  function initFreeOptionCounters() {
    document.querySelectorAll(".free-option-counter").forEach((container) => {
      const optionName = container.dataset.optionName;
      const rowsContainer = container.querySelector(".free-form-rows");
      const newKeyInput = container.querySelector(".free-form-new-key");
      const newQuantityInput = container.querySelector(".free-form-new-quantity");
      const addButton = container.querySelector(".free-form-add");
      const keyListId = `${optionName}-keys`;
      const hasKeyList = document.getElementById(keyListId) !== null;
      let nextRowId = 0;

      applyNumberBounds(newQuantityInput, container);

      function addRow(key, value, markCustom = false) {
        const rowId = nextRowId++;
        const row = document.createElement("div");
        row.className = "option-entry free-form-row";

        const keyInput = document.createElement("input");
        keyInput.type = "text";
        keyInput.className = "free-form-key";
        keyInput.name = `${optionName}||counter-key||${rowId}`;
        keyInput.value = String(key);
        keyInput.id = `${optionName}-counter-key-${rowId}`;
        keyInput.setAttribute("aria-label", `${optionName} key`);
        if (hasKeyList) {
          keyInput.setAttribute("list", keyListId);
        }

        const valueInput = document.createElement("input");
        valueInput.type = "number";
        valueInput.className = "free-form-quantity";
        valueInput.name = `${optionName}||counter-value||${rowId}`;
        valueInput.value = String(value);
        valueInput.id = `${optionName}-counter-value-${rowId}`;
        valueInput.setAttribute("aria-label", `${optionName} quantity for ${key}`);
        applyNumberBounds(valueInput, container);

        const removeButton = document.createElement("button");
        removeButton.type = "button";
        removeButton.className = "free-form-remove js-required";
        removeButton.textContent = "\u00d7";
        removeButton.setAttribute("aria-label", "Remove entry");
        removeButton.title = "Remove";
        removeButton.addEventListener("click", () => {
          row.remove();
          markPresetCustom();
        });

        row.appendChild(keyInput);
        row.appendChild(valueInput);
        row.appendChild(removeButton);
        rowsContainer.appendChild(row);
        if (markCustom) {
          markPresetCustom();
        }
      }

      function addNewEntry() {
        const key = newKeyInput.value.trim();
        if (!key || newQuantityInput.value === "") {
          return;
        }
        addRow(key, newQuantityInput.value, true);
        newKeyInput.value = "";
        newQuantityInput.value = "1";
        newKeyInput.focus();
      }

      addButton.addEventListener("click", addNewEntry);
      [newKeyInput, newQuantityInput].forEach((input) => {
        input.addEventListener("keydown", (event) => {
          if (event.key === "Enter") {
            event.preventDefault();
            addNewEntry();
          }
        });
      });
      rowsContainer.addEventListener("input", markPresetCustom);

      container.getValues = () => {
        const values = {};
        rowsContainer.querySelectorAll(".free-form-row").forEach((row) => {
          const key = row.querySelector('input[type="text"]').value.trim();
          const value = row.querySelector('input[type="number"]').value;
          if (key && value !== "") {
            values[key] = Number.parseInt(value, 10);
          }
        });
        return values;
      };

      container.restoreValues = (values) => {
        rowsContainer.innerHTML = "";
        Object.entries(values).forEach(([key, value]) => addRow(key, value));
      };

      container.restoreValues(JSON.parse(container.dataset.defaults || "{}"));
    });
  }

  function initFreeOptionDicts() {
    document.querySelectorAll(".free-option-dict").forEach((container) => {
      const optionName = container.dataset.optionName;
      const schema = JSON.parse(container.dataset.schema || "{}");
      const fixedKeys = Object.keys(schema.keys || {});
      const allowsCustomKeys = schema.additional !== null;
      const rowsContainer = container.querySelector(".free-form-rows");
      const newKeyInput = container.querySelector(".free-form-new-key");
      const newValueContainer = container.querySelector(".free-form-new-value");
      const addButton = container.querySelector(".free-form-add");
      const keyListId = `${optionName}-dict-keys`;
      let newValueInput = null;
      let nextRowId = 0;

      function getValueSchema(key) {
        if (Object.prototype.hasOwnProperty.call(schema.keys || {}, key)) {
          return schema.keys[key];
        }
        return schema.additional;
      }

      function serializeValue(value, valueType) {
        if (valueType === "boolean") {
          return value === true || value === "true" ? "true" : "false";
        }
        return String(value);
      }

      function getDefaultValue(valueSchema) {
        if (Array.isArray(valueSchema.choices) && valueSchema.choices.length) {
          return valueSchema.choices[0];
        }
        if (valueSchema.type === "boolean") {
          return false;
        }
        if (valueSchema.type === "integer" || valueSchema.type === "number") {
          return 1;
        }
        return "";
      }

      function createValueInput(key, value, rowId = null) {
        const valueSchema = getValueSchema(key);
        if (!valueSchema) {
          return null;
        }

        const choices = Array.isArray(valueSchema.choices)
          ? valueSchema.choices
          : valueSchema.type === "boolean" ? [true, false] : null;
        let input;
        if (choices) {
          input = document.createElement("select");
          choices.forEach((choice) => {
            const option = document.createElement("option");
            option.value = serializeValue(choice, valueSchema.type);
            option.textContent = valueSchema.type === "boolean"
              ? (choice ? "True" : "False")
              : String(choice);
            input.appendChild(option);
          });
        } else {
          input = document.createElement("input");
          input.type = valueSchema.type === "integer" || valueSchema.type === "number"
            ? "number"
            : "text";
          if (valueSchema.type === "number") {
            input.step = "any";
          }
        }

        const resolvedValue = value === undefined ? getDefaultValue(valueSchema) : value;
        const serializedValue = serializeValue(resolvedValue, valueSchema.type);
        if (choices && !Array.from(input.options).some((option) => option.value === serializedValue)) {
          input.value = serializeValue(choices[0], valueSchema.type);
        } else {
          input.value = serializedValue;
        }

        input.className = "free-form-dict-value";
        input.dataset.valueType = valueSchema.type;
        input.setAttribute("aria-label", `${optionName} value for ${key}`);
        if (rowId !== null) {
          input.id = `${optionName}-dict-value-${rowId}`;
          input.name = `${optionName}||dict-value-${valueSchema.type}||${rowId}`;
        }
        return input;
      }

      function createKeyInput(key, rowId) {
        let input;
        if (allowsCustomKeys) {
          input = document.createElement("input");
          input.type = "text";
          input.value = key;
          if (fixedKeys.length) {
            input.setAttribute("list", keyListId);
          }
        } else {
          input = document.createElement("select");
          fixedKeys.forEach((fixedKey) => {
            const option = document.createElement("option");
            option.value = fixedKey;
            option.textContent = fixedKey;
            input.appendChild(option);
          });
          input.value = key;
        }
        input.className = "free-form-key";
        input.id = `${optionName}-dict-key-${rowId}`;
        input.name = `${optionName}||dict-key||${rowId}`;
        input.setAttribute("aria-label", `${optionName} key`);
        return input;
      }

      function readValue(input) {
        if (input.dataset.valueType === "integer") {
          return input.value === "" ? undefined : Number.parseInt(input.value, 10);
        }
        if (input.dataset.valueType === "number") {
          return input.value === "" ? undefined : Number.parseFloat(input.value);
        }
        if (input.dataset.valueType === "boolean") {
          return input.value === "true";
        }
        return input.value;
      }

      function usedKeys() {
        return new Set(Array.from(
          rowsContainer.querySelectorAll(".free-form-key")
        ).map((input) => input.value.trim()));
      }

      function updateNewEntry(preserveValue = false) {
        if (!allowsCustomKeys) {
          const used = usedKeys();
          const availableKey = fixedKeys.find((key) => !used.has(key));
          if (availableKey) {
            newKeyInput.value = availableKey;
            newKeyInput.disabled = false;
            addButton.disabled = false;
          } else {
            newKeyInput.disabled = true;
            addButton.disabled = true;
            newValueContainer.innerHTML = "";
            newValueInput = null;
            return;
          }
        }

        const previousValue = preserveValue && newValueInput ? readValue(newValueInput) : undefined;
        const replacement = createValueInput(newKeyInput.value.trim(), previousValue);
        newValueContainer.innerHTML = "";
        if (replacement) {
          newValueContainer.appendChild(replacement);
        }
        newValueInput = replacement;
      }

      function addRow(key, value, markCustom = false) {
        if (!getValueSchema(key)) {
          return;
        }

        const rowId = nextRowId++;
        const row = document.createElement("div");
        row.className = "option-entry free-form-row";
        const keyInput = createKeyInput(key, rowId);
        let valueInput = createValueInput(key, value, rowId);

        keyInput.addEventListener("change", () => {
          const replacement = createValueInput(keyInput.value.trim(), undefined, rowId);
          if (replacement) {
            valueInput.replaceWith(replacement);
            valueInput = replacement;
          }
          updateNewEntry();
        });

        const removeButton = document.createElement("button");
        removeButton.type = "button";
        removeButton.className = "free-form-remove js-required";
        removeButton.textContent = "\u00d7";
        removeButton.setAttribute("aria-label", "Remove entry");
        removeButton.title = "Remove";
        removeButton.addEventListener("click", () => {
          row.remove();
          updateNewEntry();
          markPresetCustom();
        });

        row.appendChild(keyInput);
        row.appendChild(valueInput);
        row.appendChild(removeButton);
        row.addEventListener("input", markPresetCustom);
        row.addEventListener("change", markPresetCustom);
        rowsContainer.appendChild(row);
        updateNewEntry();
        if (markCustom) {
          markPresetCustom();
        }
      }

      function addNewEntry() {
        const key = newKeyInput.value.trim();
        if (!key || !newValueInput || usedKeys().has(key)) {
          return;
        }
        const value = readValue(newValueInput);
        if (value === undefined) {
          return;
        }
        addRow(key, value, true);
        if (allowsCustomKeys) {
          newKeyInput.value = "";
          newKeyInput.focus();
        }
        updateNewEntry();
      }

      addButton.addEventListener("click", addNewEntry);
      newKeyInput.addEventListener("change", () => updateNewEntry(true));
      newKeyInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          addNewEntry();
        }
      });
      newValueContainer.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          addNewEntry();
        }
      });

      container.getValues = () => {
        const values = {};
        rowsContainer.querySelectorAll(".free-form-row").forEach((row) => {
          const key = row.querySelector(".free-form-key").value.trim();
          const input = row.querySelector(".free-form-dict-value");
          const value = readValue(input);
          if (key && value !== undefined) {
            values[key] = value;
          }
        });
        return values;
      };

      container.restoreValues = (values) => {
        rowsContainer.innerHTML = "";
        Object.entries(values).forEach(([key, value]) => addRow(key, value));
        updateNewEntry();
      };

      container.restoreValues(JSON.parse(container.dataset.defaults || "{}"));
    });
  }

  exports.initMultiSelectors = initMultiSelectors;
  exports.initMultiCounters = initMultiCounters;
  exports.initFreeOptionLists = initFreeOptionLists;
  exports.initFreeOptionCounters = initFreeOptionCounters;
  exports.initFreeOptionDicts = initFreeOptionDicts;
})((window.playerOptions = window.playerOptions || {}));

document.addEventListener("DOMContentLoaded", () => {
  window.playerOptions.initMultiSelectors?.();
  window.playerOptions.initMultiCounters?.();
  window.playerOptions.initFreeOptionLists?.();
  window.playerOptions.initFreeOptionCounters?.();
  window.playerOptions.initFreeOptionDicts?.();
});
