(function () {
  const weeklyScheduleSectionMarkup = `    <section class="table-wrap" aria-label="Weekly schedule table">
      <div class="schedule-table-wrap">
        <table>
        <thead>
          <tr id="weekday-header">
            <th scope="col" aria-hidden="true"></th>
            <th scope="col">
              <button class="weekday-button" type="button" data-column="0" aria-controls="weekday-menu" aria-expanded="false">
                Monday
              </button>
            </th>
            <th scope="col">
              <button class="weekday-button" type="button" data-column="1" aria-controls="weekday-menu" aria-expanded="false">
                Tuesday
              </button>
            </th>
            <th scope="col">
              <button class="weekday-button" type="button" data-column="2" aria-controls="weekday-menu" aria-expanded="false">
                Wednesday
              </button>
            </th>
            <th scope="col">
              <button class="weekday-button" type="button" data-column="3" aria-controls="weekday-menu" aria-expanded="false">
                Thursday
              </button>
            </th>
            <th scope="col">
              <button class="weekday-button" type="button" data-column="4" aria-controls="weekday-menu" aria-expanded="false">
                Friday
              </button>
            </th>
          </tr>
          <tr>
            <th scope="col">Time</th>
            <th scope="col">Day 1</th>
            <th scope="col">Day 2</th>
            <th scope="col">Day 3</th>
            <th scope="col">Day 4</th>
            <th scope="col">Day 5</th>
          </tr>
        </thead>

        <tbody>
          <tr>
            <th scope="row">06:00 - 06:45</th>
            <td class="empty">—</td>
            <td class="empty">—</td>
            <td class="empty">—</td>
            <td class="empty">—</td>
            <td class="empty">—</td>
          </tr>

          <tr class="row-pause">
            <th scope="row">06:45 - 07:05</th>
            <td class="empty">—</td>
            <td class="empty">—</td>
            <td class="bar pause">Contact</td>
            <td class="empty">—</td>
            <td class="empty">—</td>
          </tr>

          <tr>
            <th scope="row">07:05 - 07:55</th>
            <td>
              <a class="class-link" href="pages/class_schedules/10B.html" aria-label="Open schedule page for class 10B">
                <span class="block warm">10B-1</span>
              </a>
            </td>
            <td class="empty">—</td>
            <td>
              <a class="class-link" href="pages/class_schedules/11E.html" aria-label="Open schedule page for class 11E">
                <span class="block cool">11E-2</span>
              </a>
            </td>
            <td>
              <a class="class-link" href="pages/class_schedules/10D.html" aria-label="Open schedule page for class 10D">
                <span class="block warm">10D-2</span>
              </a>
            </td>
            <td class="empty">—</td>
          </tr>

          <tr>
            <th scope="row">07:55 - 08:45</th>
            <td class="empty">—</td>
            <td class="empty">—</td>
            <td>
              <a class="class-link" href="pages/class_schedules/10A.html" aria-label="Open schedule page for class 10A">
                <span class="block warm-2">10A-2</span>
              </a>
            </td>
            <td class="empty">—</td>
            <td>
              <a class="class-link" href="pages/class_schedules/10C.html" aria-label="Open schedule page for class 10C">
                <span class="block warm">10C-2</span>
              </a>
            </td>
          </tr>

          <tr>
            <th scope="row">08:45 - 09:35</th>
            <td>
              <a class="class-link" href="pages/class_schedules/10A.html" aria-label="Open schedule page for class 10A">
                <span class="block warm-2">10A-1</span>
              </a>
            </td>
            <td class="empty">—</td>
            <td>
              <a class="class-link" href="pages/class_schedules/11A.html" aria-label="Open schedule page for class 11A">
                <span class="block cool-2">11A-2</span>
              </a>
            </td>
            <td class="empty">—</td>
            <td>
              <a class="class-link" href="pages/class_schedules/11B.html" aria-label="Open schedule page for class 11B">
                <span class="block cool">11B-2</span>
              </a>
            </td>
          </tr>

          <tr class="row-activity">
            <th scope="row">09:35 - 10:05</th>
            <td class="empty">—</td>
            <td class="bar activity">Rodaderos</td>
            <td class="empty">—</td>
            <td class="bar activity">Kilombera</td>
            <td class="empty">—</td>
          </tr>

          <tr>
            <th scope="row">10:05 - 11:00</th>
            <td class="empty">—</td>
            <td>
              <a class="class-link" href="pages/class_schedules/11E.html" aria-label="Open schedule page for class 11E">
                <span class="block cool">11E-1</span>
              </a>
            </td>
            <td>
              <a class="class-link" href="pages/magis.html" aria-label="Open schedule page for Teams">
                <span class="block" style="background: #d3b3f3;">Teams</span>
              </a>
            </td>
            <td class="empty">—</td>
            <td class="empty">—</td>
          </tr>

          <tr>
            <th scope="row">11:00 - 11:55</th>
            <td>
              <a class="class-link" href="pages/class_schedules/11A.html" aria-label="Open schedule page for class 11A">
                <span class="block cool-2">11A-1</span>
              </a>
            </td>
            <td>
              <a class="class-link" href="pages/magis.html" aria-label="Open schedule page for Magis">
                <span class="block" style="background: #e6d5f7;">Magis</span>
              </a>
            </td>
            <td>
              <a class="class-link" href="pages/class_schedules/10D.html" aria-label="Open schedule page for class 10D">
                <span class="block warm">10D-1</span>
              </a>
            </td>
            <td>
              <a class="class-link" href="pages/class_schedules/10E.html" aria-label="Open schedule page for class 10E">
                <span class="block warm">10E-2</span>
              </a>
            </td>
            <td class="empty">—</td>
          </tr>

          <tr>
            <th scope="row">11:55 - 12:50</th>
            <td>
              <a class="class-link" href="pages/class_schedules/11D.html" aria-label="Open schedule page for class 11D">
                <span class="block cool">11D-1</span>
              </a>
            </td>
            <td>
              <a class="class-link" href="pages/magis.html" aria-label="Open schedule page for Magis">
                <span class="block" style="background: #e6d5f7;">Magis</span>
              </a>
            </td>
            <td>
              <a class="class-link" href="pages/class_schedules/10E.html" aria-label="Open schedule page for class 10E">
                <span class="block warm">10E-1</span>
              </a>
            </td>
            <td>
              <a class="class-link" href="pages/class_schedules/11D.html" aria-label="Open schedule page for class 11D">
                <span class="block cool">11D-2</span>
              </a>
            </td>
            <td>
              <a class="class-link" href="pages/class_schedules/10B.html" aria-label="Open schedule page for class 10B">
                <span class="block warm">10B-2</span>
              </a>
            </td>
          </tr>

          <tr class="row-activity">
            <th scope="row">12:50 - 13:50</th>
            <td class="empty">—</td>
            <td class="empty">—</td>
            <td class="empty">—</td>
            <td class="empty">—</td>
            <td class="bar activity">Kilombera</td>
          </tr>

          <tr>
            <th scope="row">13:50 - 14:45</th>
            <td>
              <a class="class-link" href="pages/class_schedules/10C.html" aria-label="Open schedule page for class 10C">
                <span class="block warm">10C-1</span>
              </a>
            </td>
            <td>
              <a class="class-link" href="pages/class_schedules/11C.html" aria-label="Open schedule page for class 11C">
                <span class="block cool">11C-1</span>
              </a>
            </td>
            <td>
              <a class="class-link" href="pages/class_schedules/11B.html" aria-label="Open schedule page for class 11B">
                <span class="block cool">11B-1</span>
              </a>
            </td>
            <td>
              <a class="class-link" href="pages/class_schedules/11C.html" aria-label="Open schedule page for class 11C">
                <span class="block cool">11C-2</span>
              </a>
            </td>
            <td class="empty">—</td>
          </tr>

          <tr class="row-pause">
            <th scope="row">14:45 - 15:00</th>
            <td class="empty">—</td>
            <td class="empty">—</td>
            <td class="bar pause">Pause</td>
            <td class="empty">—</td>
            <td class="empty">—</td>
          </tr>

          <tr>
            <th scope="row">15:00 - 16:00</th>
            <td class="empty">—</td>
            <td class="empty">—</td>
            <td class="empty">—</td>
            <td class="empty">—</td>
            <td class="empty">—</td>
          </tr>
        </tbody>
        </table>
        <div class="current-time-overlay" aria-hidden="true" hidden>
          <div class="current-time-line">
            <span class="current-time-label"></span>
          </div>
        </div>
      </div>
      <div class="view-toggle">
        <span id="weekday-view-label">Weekday view</span>
        <button id="weekday-view-toggle" type="button" role="switch" aria-checked="false" aria-labelledby="weekday-view-label">
          <span class="view-toggle-indicator" aria-hidden="true"></span>
          <span class="view-toggle-text" aria-hidden="true">Off</span>
        </button>
        <span id="plain-style-label">Plain style</span>
        <button id="plain-style-toggle" type="button" role="switch" aria-checked="false" aria-labelledby="plain-style-label">
          <span class="view-toggle-indicator" aria-hidden="true"></span>
          <span class="view-toggle-text" aria-hidden="true">Off</span>
        </button>
        <span id="week-summary-label">Week summaries</span>
        <button id="week-summary-toggle" type="button" role="switch" aria-checked="false" aria-labelledby="week-summary-label">
          <span class="view-toggle-indicator" aria-hidden="true"></span>
          <span class="view-toggle-text" aria-hidden="true">Off</span>
        </button>
      </div>
    </section>
`;

  function renderWeeklyScheduleTable(target) {
    const targetElement = typeof target === "string" ? document.querySelector(target) : target;
    if (!targetElement) {
      return null;
    }

    targetElement.innerHTML = weeklyScheduleSectionMarkup;
    return targetElement.querySelector(".table-wrap");
  }

  window.renderWeeklyScheduleTable = renderWeeklyScheduleTable;
})();
