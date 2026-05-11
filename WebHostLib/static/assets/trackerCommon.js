const TRACKER_TABLE_HEIGHT_COOKIE_PREFIX = 'trackerTableHeights_';
const TRACKER_TABLE_HEIGHT_COOKIE_MAX_AGE_SECONDS = 60 * 60 * 24 * 365;

const getCookie = (name) => {
    const cookie = document.cookie
        .split(';')
        .map((row) => row.trim())
        .find((row) => row.startsWith(`${name}=`));
    return cookie ? decodeURIComponent(cookie.split('=').slice(1).join('=')) : null;
};

const setCookie = (name, value) => {
    document.cookie = `${name}=${encodeURIComponent(value)};max-age=${TRACKER_TABLE_HEIGHT_COOKIE_MAX_AGE_SECONDS};path=/;SameSite=Lax`;
};

const getTrackerTableHeightCookieName = () => {
    let hash = 0;
    for (const character of location.pathname) {
        hash = ((hash << 5) - hash + character.charCodeAt(0)) >>> 0;
    }
    return `${TRACKER_TABLE_HEIGHT_COOKIE_PREFIX}${hash.toString(36)}`;
};

const getTableWrappers = () => Array.from(document.getElementsByClassName('table-wrapper'));

const loadTableHeightPreferences = () => {
    const cookieValue = getCookie(getTrackerTableHeightCookieName());
    if (!cookieValue)
        return [];

    try {
        const tableHeights = JSON.parse(cookieValue);
        if (Array.isArray(tableHeights))
            return tableHeights;
    } catch (error) {
        console.warn('Failed to load saved tracker table heights.', error);
    }
    return [];
};

const saveTableHeightPreferences = () => {
    const tableHeights = getTableWrappers().map((tableWrapper) =>
        Math.round(tableWrapper.getBoundingClientRect().height)
    );
    setCookie(getTrackerTableHeightCookieName(), JSON.stringify(tableHeights));
};

const applyTableHeightPreferences = () => {
    const tableHeights = loadTableHeightPreferences();
    if (!tableHeights.length)
        return;

    getTableWrappers().forEach((tableWrapper, index) => {
        const tableHeight = parseInt(tableHeights[index]);
        if (Number.isFinite(tableHeight) && tableHeight > 0) {
            tableWrapper.style.height = `${tableHeight}px`;
        }
    });
};

const watchTableHeightPreferenceChanges = () => {
    if (typeof ResizeObserver === 'undefined')
        return;

    let pointerDownOnTableWrapper = false;
    let tableWrapperSizeChanged = false;

    getTableWrappers().forEach((tableWrapper) => {
        tableWrapper.addEventListener('pointerdown', () => {
            pointerDownOnTableWrapper = true;
            tableWrapperSizeChanged = false;
        });

        new ResizeObserver(() => {
            if (pointerDownOnTableWrapper) {
                tableWrapperSizeChanged = true;
            }
        }).observe(tableWrapper);
    });

    window.addEventListener('pointerup', () => {
        if (pointerDownOnTableWrapper && tableWrapperSizeChanged) {
            saveTableHeightPreferences();
        }
        pointerDownOnTableWrapper = false;
        tableWrapperSizeChanged = false;
    });
};

const adjustTableHeight = () => {
    const tablesContainer = document.getElementById('tables-container');
    if (!tablesContainer)
        return;
    const upperDistance = tablesContainer.getBoundingClientRect().top;

    const tableWrappers = getTableWrappers();
    const availableHeight = window.innerHeight - upperDistance;
    const locationsTableWrapper = document.getElementById('locations-table-wrapper');
    const hasLocationsTable = locationsTableWrapper !== null;

    for (let i = 0; i < tableWrappers.length; i++) {
        // Ensure we are starting from maximum size prior to calculation.
        tableWrappers[i].style.height = null;
        tableWrappers[i].style.maxHeight = null;

        // Set as a reasonable height, but still allows the user to resize element if they desire.
        const currentHeight = tableWrappers[i].offsetHeight;
        let maxHeight;

        if (hasLocationsTable && tableWrappers[i].id === 'locations-table-wrapper') {
            maxHeight = availableHeight * 0.4;
        } else if (hasLocationsTable) {
            const otherTablesCount = tableWrappers.length - 1;
            maxHeight = (availableHeight * 0.6) / otherTablesCount;
        } else {
            maxHeight = availableHeight / Math.min(tableWrappers.length, 4);
        }

        if (currentHeight > maxHeight) {
            tableWrappers[i].style.height = `calc(${maxHeight}px - 1rem)`;
        }

        tableWrappers[i].style.maxHeight = `${currentHeight}px`;
    }
};

/**
 * Convert an integer number of seconds into a human readable HH:MM format
 * @param {Number} seconds
 * @returns {string}
 */
const secondsToHours = (seconds) => {
    let hours = Math.floor(seconds / 3600);
    let minutes = Math.floor((seconds - (hours * 3600)) / 60).toString().padStart(2, '0');
    return `${hours}:${minutes}`;
};

window.addEventListener('load', () => {
    const tables = $(".table").DataTable({
        paging: false,
        info: false,
        dom: "t",
        stateSave: true,
        stateSaveCallback: function (settings, data) {
            delete data.search;
            localStorage.setItem(`DataTables_${settings.sInstance}_/tracker`, JSON.stringify(data));
        },
        stateLoadCallback: function (settings) {
            return JSON.parse(localStorage.getItem(`DataTables_${settings.sInstance}_/tracker`));
        },
        rowCallback: function (row, data) {
            // Add data attributes for filtering
            if ($(row).attr('data-checked')) {
                return;
            }
            const checkedCell = $(row).find('td').eq(1).text().trim();
            if (checkedCell === '✔') {
                $(row).attr('data-checked', 'true');
            } else {
                $(row).attr('data-checked', 'false');
            }
        },
        footerCallback: function (tfoot, data, start, end, display) {
            if (tfoot) {
                const activityData = this.api().column('lastActivity:name').data().toArray().filter(x => !isNaN(x));
                Array.from(tfoot?.children).find(td => td.classList.contains('last-activity')).innerText =
                    (activityData.length) ? secondsToHours(Math.min(...activityData)) : 'None';
            }
        },
        columnDefs: [
            {
                targets: 'last-activity',
                name: 'lastActivity'
            },
            {
                targets: 'hours',
                render: function (data, type, row) {
                    if (type === "sort" || type === 'type') {
                        if (data === "None")
                            return Number.MAX_VALUE;

                        return parseInt(data);
                    }
                    if (data === "None")
                        return data;

                    return secondsToHours(data);
                }
            },
            {
                targets: 'number',
                render: function (data, type, row) {
                    if (type === "sort" || type === 'type') {
                        return parseFloat(data);
                    }
                    return data;
                }
            },
            {
                targets: 'fraction',
                render: function (data, type, row) {
                    let splitted = data.split("/", 1);
                    let current = splitted[0]
                    if (type === "sort" || type === 'type') {
                        return parseInt(current);
                    }
                    return data;
                }
            },
        ],

        // DO NOT use the scrollX or scrollY options. They cause DataTables to split the thead from
        // the tbody and render two separate tables.
    });

    const searchBox = document.getElementById("search");
    searchBox.value = tables.search();
    searchBox.focus();
    searchBox.select();
    const doSearch = () => {
        tables.search(searchBox.value);
        tables.draw();
    };
    searchBox.addEventListener("keyup", doSearch);
    window.addEventListener("keydown", (event) => {
        if (!event.ctrlKey && !event.altKey && event.key.length === 1 && document.activeElement !== searchBox) {
            searchBox.focus();
            searchBox.select();
        }
        if (!event.ctrlKey && !event.altKey && !event.shiftKey && event.key === "Escape") {
            if (searchBox.value !== "") {
                searchBox.value = "";
                doSearch();
            }
            searchBox.blur();
            if (!document.getElementById("tables-container"))
                window.scroll(0, 0);
            event.preventDefault();
        }
    });
    const target_second = parseInt(document.getElementById('tracker-wrapper').getAttribute('data-second')) + 3;
    console.log("Target second of refresh: " + target_second);

    function getSleepTimeSeconds() {
        // -40 % 60 is -40, which is absolutely wrong and should burn
        var sleepSeconds = (((target_second - new Date().getSeconds()) % 60) + 60) % 60;
        return sleepSeconds || 60;
    }

    let update_on_view = false;
    const update = () => {
        if (document.hidden) {
            console.log("Document reporting as not visible, not updating Tracker...");
            update_on_view = true;
        } else {
            update_on_view = false;
            const target = $("<div></div>");
            console.log("Updating Tracker...");
            target.load(location.href, function (response, status) {
                if (status === "success") {
                    target.find(".table").each(function (i, new_table) {
                        const new_trs = $(new_table).find("tbody>tr");
                        const footer_tr = $(new_table).find("tfoot>tr");
                        const old_table = tables.eq(i);
                        const topscroll = $(old_table.settings()[0].nScrollBody).scrollTop();
                        const leftscroll = $(old_table.settings()[0].nScrollBody).scrollLeft();
                        old_table.clear();
                        if (footer_tr.length) {
                            $(old_table.table).find("tfoot").html(footer_tr);
                        }
                        old_table.rows.add(new_trs);
                        old_table.draw();
                        $(old_table.settings()[0].nScrollBody).scrollTop(topscroll);
                        $(old_table.settings()[0].nScrollBody).scrollLeft(leftscroll);
                    });
                    $("#multi-stream-link").replaceWith(target.find("#multi-stream-link"));
                } else {
                    console.log("Failed to connect to Server, in order to update Table Data.");
                    console.log(response);
                }
            })
        }
        updater = setTimeout(update, getSleepTimeSeconds() * 1000);
    }
    let updater = setTimeout(update, getSleepTimeSeconds() * 1000);

    window.addEventListener('resize', () => {
        adjustTableHeight();
        applyTableHeightPreferences();
        tables.draw();
    });

    window.addEventListener('visibilitychange', () => {
        if (!document.hidden && update_on_view) {
            console.log("Page became visible, tracker should be refreshed.");
            clearTimeout(updater);
            update();
        }
    });

    adjustTableHeight();
    applyTableHeightPreferences();
    watchTableHeightPreferenceChanges();

    // Persistent filter for hiding checked locations and found hints
    $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
        const row = $(settings.aoData[dataIndex].nTr);
        if (settings.nTable.id === 'locations-table') {
            const hideChecked = document.getElementById('hide-checked-locations')?.checked;
            if (hideChecked && row.attr('data-checked') === 'true') {
                return false;
            }
        }
        if (settings.nTable.id === 'hints-table') {
            const hideFound = document.getElementById('hide-found-hints')?.checked;
            if (hideFound && row.attr('data-found') === 'true') {
                return false;
            }
        }
        return true;
    });

    const hideCheckedCheckbox = document.getElementById('hide-checked-locations');
    if (hideCheckedCheckbox) {
        hideCheckedCheckbox.checked = localStorage.getItem('hideCheckedLocations') === 'true';
        const onCheckedChange = () => {
            localStorage.setItem('hideCheckedLocations', hideCheckedCheckbox.checked);
            tables.table('#locations-table').draw();
        };
        onCheckedChange();
        hideCheckedCheckbox.addEventListener('change', onCheckedChange);
    }

    const hideFoundCheckbox = document.getElementById('hide-found-hints');
    if (hideFoundCheckbox) {
        hideFoundCheckbox.checked = localStorage.getItem('hideFoundHints') === 'true';
        const onFoundChange = () => {
            localStorage.setItem('hideFoundHints', hideFoundCheckbox.checked);
            tables.table('#hints-table').draw();
        };
        onFoundChange();
        hideFoundCheckbox.addEventListener('change', onFoundChange);
    }
});
