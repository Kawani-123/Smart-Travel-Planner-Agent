/**
 * Smart Travel Planner — Frontend JavaScript
 * Connects to FastAPI backend for AI-powered travel planning.
 *
 * Fix: script.js was missing entirely from the original project.
 * This file implements all interactive functionality referenced in index.html.
 */

"use strict";

// ── Configuration ─────────────────────────────────────────────────────────────
const API_BASE = "http://localhost:8000/api";

// ── State ─────────────────────────────────────────────────────────────────────
let selectedInterests = [];

// ── On DOM ready ──────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  loadDestinations();
  setupBudgetIndicator();
  setupFormSubmit();
});

// ── Destination cards ─────────────────────────────────────────────────────────
async function loadDestinations() {
  const grid = document.getElementById("destGrid");
  if (!grid) return;

  try {
    const res  = await fetch(`${API_BASE}/travel/destinations`);
    const data = await res.json();

    grid.innerHTML = data.destinations
      .map(
        (d) => `
      <div class="dest-card" onclick="selectDestination('${d.name}')">
        <div class="dest-img" style="background-image: url('${d.image_url}')">
          <div class="dest-overlay">
            <span class="dest-region">${d.region}</span>
          </div>
        </div>
        <div class="dest-info">
          <h3 class="dest-name">${d.name}</h3>
          <p class="dest-desc">${d.description}</p>
          <div class="dest-tags">
            ${d.tags
              .slice(0, 3)
              .map((t) => `<span class="dest-tag">${t}</span>`)
              .join("")}
          </div>
          <div class="dest-season">🗓️ Best: ${d.best_season}</div>
        </div>
      </div>`
      )
      .join("");
  } catch (err) {
    grid.innerHTML = `<p class="error-msg">Could not load destinations. Is the backend running? (${err.message})</p>`;
  }
}

function selectDestination(name) {
  const select = document.getElementById("destination");
  if (select) {
    select.value = name;
    document.getElementById("planner")?.scrollIntoView({ behavior: "smooth" });
  }
}

// ── Stepper controls ──────────────────────────────────────────────────────────
function adjustStepper(field, delta) {
  const input = document.getElementById(field);
  if (!input) return;
  const min = parseInt(input.min) || 1;
  const max = parseInt(input.max) || 100;
  const val = parseInt(input.value) + delta;
  input.value = Math.min(max, Math.max(min, val));
}

// ── Option card selection (transport / hotel) ─────────────────────────────────
function selectOption(group, card) {
  const parent     = card.closest(".option-cards");
  const hiddenId   = group === "transport" ? "transport_type" : "hotel_type";
  parent.querySelectorAll(".option-card").forEach((c) => c.classList.remove("active"));
  card.classList.add("active");
  const hidden = document.getElementById(hiddenId);
  if (hidden) hidden.value = card.dataset.value;
}

// ── Interest tags ─────────────────────────────────────────────────────────────
function toggleInterest(btn) {
  const val = btn.dataset.value;
  btn.classList.toggle("active");
  if (selectedInterests.includes(val)) {
    selectedInterests = selectedInterests.filter((i) => i !== val);
  } else {
    selectedInterests.push(val);
  }
}

// ── Budget indicator ──────────────────────────────────────────────────────────
function setupBudgetIndicator() {
  const budgetInput = document.getElementById("budget");
  const indicator   = document.getElementById("budgetIndicator");
  if (!budgetInput || !indicator) return;

  budgetInput.addEventListener("input", () => {
    const val = parseInt(budgetInput.value) || 0;
    let label = "", cls = "";
    if (val < 10000)        { label = "🟡 Low Budget";      cls = "budget-low"; }
    else if (val < 30000)   { label = "🟢 Budget Trip";     cls = "budget-ok"; }
    else if (val < 80000)   { label = "🔵 Mid-range";       cls = "budget-mid"; }
    else                    { label = "💎 Luxury";           cls = "budget-lux"; }
    indicator.textContent  = label;
    indicator.className    = `budget-indicator ${cls}`;
  });
}

// ── Form submission ────────────────────────────────────────────────────────────
function setupFormSubmit() {
  const form = document.getElementById("travelForm");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    await planTrip();
  });
}

async function planTrip() {
  const source        = document.getElementById("source")?.value.trim();
  const destination   = document.getElementById("destination")?.value;
  const budget        = parseInt(document.getElementById("budget")?.value);
  const days          = parseInt(document.getElementById("days")?.value);
  const travelers     = parseInt(document.getElementById("travelers")?.value);
  const transport_type = document.getElementById("transport_type")?.value || "flight";
  const hotel_type    = document.getElementById("hotel_type")?.value || "standard";

  if (!source || !destination || !budget || !days || !travelers) {
    alert("Please fill in all required fields.");
    return;
  }

  // Show loading
  showLoading(true);
  animateLoadingSteps();

  try {
    // Parallel API calls
    const [weatherRes, costRes, itineraryRes, destRes] = await Promise.allSettled([
      fetch(`${API_BASE}/weather/current?city=${encodeURIComponent(destination)}`),
      fetch(`${API_BASE}/predict/cost`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ destination, days, travelers, transport_type, hotel_type }),
      }),
      fetch(`${API_BASE}/itinerary/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          source, destination, budget, days, travelers,
          interests: selectedInterests, transport_type, hotel_type,
        }),
      }),
      fetch(`${API_BASE}/travel/destination/${encodeURIComponent(destination)}`),
    ]);

    const weather     = weatherRes.status === "fulfilled"   ? await weatherRes.value.json()     : null;
    const cost        = costRes.status === "fulfilled"       ? await costRes.value.json()         : null;
    const itinerary   = itineraryRes.status === "fulfilled"  ? await itineraryRes.value.json()   : null;
    const destDetail  = destRes.status === "fulfilled"       ? await destRes.value.json()         : null;

    // Render dashboard
    renderDashboard({ destination, days, travelers, budget, weather, cost, itinerary, destDetail });

  } catch (err) {
    alert(`Error: ${err.message}\n\nMake sure the backend is running on ${API_BASE.replace("/api", "")}`);
  } finally {
    showLoading(false);
  }
}

// ── Dashboard rendering ───────────────────────────────────────────────────────
function renderDashboard({ destination, days, travelers, budget, weather, cost, itinerary, destDetail }) {
  // Summary cards
  setText("sumDestination", destination);
  setText("sumDays", `${days} Day${days > 1 ? "s" : ""}`);
  setText("sumTravelers", `${travelers} traveler${travelers > 1 ? "s" : ""}`);

  if (cost) {
    setText("sumCost", `₹${cost.estimated_cost?.toLocaleString("en-IN") ?? "—"}`);
    setText("sumCostPer", `₹${cost.per_person_cost?.toLocaleString("en-IN")} per person`);
  } else {
    setText("sumCost", `₹${budget.toLocaleString("en-IN")}`);
    setText("sumCostPer", "Budget provided");
  }

  if (weather && !weather.error) {
    setText("sumTemp", `${weather.temperature}°C`);
    setText("sumWeatherDesc", weather.description);
    const iconEl = document.getElementById("weatherIcon");
    if (iconEl && weather.icon_url) {
      iconEl.innerHTML = `<img src="${weather.icon_url}" alt="weather" style="width:40px;height:40px">`;
    }
  } else {
    setText("sumTemp", "—");
    setText("sumWeatherDesc", "Unavailable");
  }

  // Tabs content
  renderItinerary(itinerary);
  renderWeather(weather, destination);
  renderCost(cost, budget, days, travelers);
  renderDestination(destDetail);

  // Show dashboard, activate first tab
  const dash = document.getElementById("dashboard");
  if (dash) {
    dash.classList.remove("hidden");
    dash.scrollIntoView({ behavior: "smooth" });
  }
  switchTab("itinerary", document.querySelector(".tab-btn.active"));
}

function renderItinerary(data) {
  const el = document.getElementById("itineraryContent");
  if (!el) return;

  if (!data) {
    el.innerHTML = `<p class="error-msg">Could not generate itinerary. Is the backend running?</p>`;
    return;
  }

  // Update model badge
  const badge = document.getElementById("modelBadge");
  if (badge) {
    const src = data.model_source || "demo_mock";
    badge.textContent = src.includes("watsonx") ? "IBM watsonx.ai ✅" : "Demo Mode";
    badge.style.background = src.includes("watsonx") ? "rgba(0,200,80,0.15)" : "rgba(200,100,0,0.15)";
  }

  // Convert markdown-like text to HTML
  const html = markdownToHtml(data.itinerary || "No itinerary generated.");
  el.innerHTML = html;
}

function renderWeather(weather, destination) {
  const currentEl  = document.getElementById("weatherCurrentContent");
  const forecastEl = document.getElementById("weatherForecastContent");

  if (!weather || weather.error) {
    if (currentEl)  currentEl.innerHTML  = `<p class="error-msg">Weather data unavailable. Add OPENWEATHER_API_KEY to .env</p>`;
    if (forecastEl) forecastEl.innerHTML = "";
    loadForecast(destination);
    return;
  }

  if (currentEl) {
    currentEl.innerHTML = `
      <div class="weather-big">
        <img src="${weather.icon_url}" alt="weather icon" class="weather-icon-big"/>
        <div class="weather-temp-big">${weather.temperature}°C</div>
      </div>
      <div class="weather-details-grid">
        <div class="wd-item"><span>Feels Like</span><strong>${weather.feels_like}°C</strong></div>
        <div class="wd-item"><span>Humidity</span><strong>${weather.humidity}%</strong></div>
        <div class="wd-item"><span>Wind</span><strong>${weather.wind_speed} m/s</strong></div>
        <div class="wd-item"><span>Visibility</span><strong>${weather.visibility} km</strong></div>
        <div class="wd-item"><span>Condition</span><strong>${weather.description}</strong></div>
        <div class="wd-item"><span>Country</span><strong>${weather.country ?? "IN"}</strong></div>
      </div>
      ${weather.note ? `<p class="weather-note">ℹ️ ${weather.note}</p>` : ""}
    `;
  }

  loadForecast(destination, forecastEl);
}

async function loadForecast(destination, el) {
  const forecastEl = el || document.getElementById("weatherForecastContent");
  if (!forecastEl) return;
  try {
    const res  = await fetch(`${API_BASE}/weather/forecast?city=${encodeURIComponent(destination)}&days=5`);
    const data = await res.json();
    if (data.error) throw new Error(data.error);

    forecastEl.innerHTML = `
      <div class="forecast-grid">
        ${data.forecast.map((d) => `
          <div class="forecast-day">
            <div class="fc-date">${formatDate(d.date)}</div>
            <img src="${d.icon_url}" alt="icon" class="fc-icon"/>
            <div class="fc-range">${d.temp_min}° – ${d.temp_max}°C</div>
            <div class="fc-desc">${d.description}</div>
            <div class="fc-hum">💧 ${d.humidity}%</div>
          </div>`).join("")}
      </div>
      ${data.note ? `<p class="weather-note">ℹ️ ${data.note}</p>` : ""}
    `;
  } catch (err) {
    forecastEl.innerHTML = `<p class="error-msg">Forecast unavailable: ${err.message}</p>`;
  }
}

function renderCost(cost, budget, days, travelers) {
  const summaryEl   = document.getElementById("costSummaryContent");
  const breakdownEl = document.getElementById("costBreakdownContent");

  if (!cost || cost.detail) {
    // ML error or model not ready
    if (summaryEl) summaryEl.innerHTML = `
      <div class="cost-hero">
        <div class="cost-amount">₹${budget.toLocaleString("en-IN")}</div>
        <div class="cost-label">Your Budget</div>
        <p class="cost-note">⚠️ ML model not ready. Run <code>python ml/train.py</code> to enable predictions.</p>
      </div>`;
    if (breakdownEl) breakdownEl.innerHTML = "";
    return;
  }

  if (summaryEl) {
    summaryEl.innerHTML = `
      <div class="cost-hero">
        <div class="cost-amount">₹${cost.estimated_cost.toLocaleString("en-IN")}</div>
        <div class="cost-label">Estimated Total</div>
        <div class="cost-per">₹${cost.per_person_cost.toLocaleString("en-IN")} per person</div>
        <div class="cost-range">
          Range: ₹${cost.confidence_range.low.toLocaleString("en-IN")} –
                 ₹${cost.confidence_range.high.toLocaleString("en-IN")}
        </div>
        <div class="cost-vs-budget ${cost.estimated_cost <= budget ? "within" : "over"}">
          ${cost.estimated_cost <= budget
            ? `✅ Within budget (saves ₹${(budget - cost.estimated_cost).toLocaleString("en-IN")})`
            : `⚠️ Exceeds budget by ₹${(cost.estimated_cost - budget).toLocaleString("en-IN")}`}
        </div>
      </div>`;
  }

  if (breakdownEl && cost.breakdown) {
    const total = Object.values(cost.breakdown).reduce((a, b) => a + b, 0) || 1;
    const items = [
      { label: "✈️ Transport",  key: "transport" },
      { label: "🏨 Hotel",      key: "hotel" },
      { label: "🍽️ Food",       key: "food" },
      { label: "🎯 Activities", key: "activities" },
    ];
    breakdownEl.innerHTML = `
      <div class="breakdown-bars">
        ${items.map(({ label, key }) => {
          const val = cost.breakdown[key] || 0;
          const pct = Math.round((val / total) * 100);
          return `
            <div class="breakdown-row">
              <div class="breakdown-label">${label}</div>
              <div class="breakdown-bar-wrap">
                <div class="breakdown-bar" style="width:${pct}%"></div>
              </div>
              <div class="breakdown-value">₹${val.toLocaleString("en-IN")} (${pct}%)</div>
            </div>`;
        }).join("")}
      </div>`;
  }
}

function renderDestination(dest) {
  const el = document.getElementById("destinationDetailContent");
  if (!el) return;

  if (!dest) {
    el.innerHTML = `<p class="error-msg">Destination details unavailable.</p>`;
    return;
  }

  el.innerHTML = `
    <div class="dest-detail-card">
      <div class="dest-detail-hero" style="background-image: url('${dest.image_url}')">
        <div class="dest-detail-title">${dest.name}</div>
        <div class="dest-detail-state">${dest.state} · ${dest.region}</div>
      </div>
      <div class="dest-detail-body">
        <p class="dest-full-desc">${dest.description}</p>
        <div class="dest-detail-grid">
          <div class="dest-info-block">
            <h4>🏛️ Highlights</h4>
            <ul>${(dest.highlights || []).map((h) => `<li>${h}</li>`).join("")}</ul>
          </div>
          <div class="dest-info-block">
            <h4>📋 Quick Info</h4>
            <ul>
              <li>🗣️ Language: ${dest.language}</li>
              <li>🗓️ Best Season: ${dest.best_season}</li>
              <li>💰 Budget/day: ₹${dest.avg_budget_per_day?.budget?.toLocaleString("en-IN")}–₹${dest.avg_budget_per_day?.luxury?.toLocaleString("en-IN")}</li>
            </ul>
          </div>
        </div>
        <div class="dest-tags-row">
          ${(dest.tags || []).map((t) => `<span class="dest-tag">${t}</span>`).join("")}
        </div>
      </div>
    </div>`;
}

// ── Tab switching ─────────────────────────────────────────────────────────────
function switchTab(name, btn) {
  document.querySelectorAll(".tab-content").forEach((el) => el.classList.add("hidden"));
  document.querySelectorAll(".tab-btn").forEach((b)  => b.classList.remove("active"));

  const tab = document.getElementById(`tab-${name}`);
  if (tab) tab.classList.remove("hidden");
  if (btn) btn.classList.add("active");
}

// ── Loading overlay ───────────────────────────────────────────────────────────
function showLoading(show) {
  const overlay = document.getElementById("loadingOverlay");
  if (!overlay) return;
  overlay.classList.toggle("hidden", !show);
  const dash = document.getElementById("dashboard");
  if (dash) dash.classList.add("hidden");
}

function animateLoadingSteps() {
  const steps = ["step1", "step2", "step3", "step4", "step5", "step6"];
  steps.forEach((id, i) => {
    const el = document.getElementById(id);
    if (el) el.classList.remove("active", "done");
  });

  let i = 0;
  const interval = setInterval(() => {
    if (i > 0) {
      const prev = document.getElementById(steps[i - 1]);
      if (prev) { prev.classList.remove("active"); prev.classList.add("done"); }
    }
    if (i < steps.length) {
      const cur = document.getElementById(steps[i]);
      if (cur) cur.classList.add("active");
      i++;
    } else {
      clearInterval(interval);
    }
  }, 1800);
}

// ── Utilities ─────────────────────────────────────────────────────────────────
function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function formatDate(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-IN", { weekday: "short", month: "short", day: "numeric" });
}

function markdownToHtml(md) {
  return md
    // Headers
    .replace(/^### (.+)$/gm, "<h3>$1</h3>")
    .replace(/^## (.+)$/gm, "<h2>$1</h2>")
    .replace(/^# (.+)$/gm, "<h1>$1</h1>")
    // Bold
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    // Italic
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    // Markdown table rows
    .replace(/^\|(.+)\|$/gm, (line) => {
      if (/^[\|\s\-:]+$/.test(line)) return "";  // separator row
      const cells = line.split("|").filter((_, i, a) => i > 0 && i < a.length - 1);
      return `<tr>${cells.map((c) => `<td>${c.trim()}</td>`).join("")}</tr>`;
    })
    // List items
    .replace(/^\d+\.\s(.+)$/gm, "<li>$1</li>")
    .replace(/^[-*]\s(.+)$/gm, "<li>$1</li>")
    // Code
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    // Paragraphs
    .replace(/\n\n+/g, "</p><p>")
    // Wrap in <p>
    .replace(/^(?!<)(.+)$/gm, (line) =>
      line.startsWith("<") ? line : `<span>${line}</span>`
    )
    .replace(/<\/li>\n?<li>/g, "</li><li>")
    .replace(/(<li>.+<\/li>)/gs, "<ul>$1</ul>");
}

function resetForm() {
  const form = document.getElementById("travelForm");
  if (form) form.reset();
  selectedInterests = [];
  document.querySelectorAll(".interest-tag").forEach((b) => b.classList.remove("active"));
  document.querySelectorAll(".option-card").forEach((c) => c.classList.remove("active"));

  // Reset defaults
  const defTransport = document.querySelector('.option-card[data-value="flight"]');
  const defHotel     = document.querySelector('.option-card[data-value="standard"]');
  if (defTransport) defTransport.classList.add("active");
  if (defHotel) defHotel.classList.add("active");

  const dashboard = document.getElementById("dashboard");
  if (dashboard) dashboard.classList.add("hidden");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function copyItinerary() {
  const el = document.getElementById("itineraryContent");
  if (!el) return;
  const text = el.innerText;
  navigator.clipboard.writeText(text).then(
    () => alert("✅ Itinerary copied to clipboard!"),
    () => {
      // Fallback
      const ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      alert("✅ Itinerary copied!");
    }
  );
}
