const sampleOpportunities = [
  {
    id: 101,
    sam_notice_id: "DOE-ZT-2026-001",
    title: "Zero Trust Cloud Modernization Support",
    solicitation_number: "RFQ-2026-001",
    notice_type: "RFQ",
    agency: "Department of Energy",
    naics_code: "541512",
    set_aside: "8(a)",
    status: "reviewing",
    posted_date: "2026-07-01",
    due_date: "2026-08-14",
    summary:
      "DOE needs zero trust cloud modernization support, including cybersecurity engineering, architecture alignment, and migration readiness.",
    description:
      "Seeking cybersecurity engineering and cloud modernization support for zero trust architecture.",
    qualification_score: 10,
    qualification_recommendation: "pursue",
    qualification_rationale:
      "Recommendation: Pursue. The opportunity shows strong alignment with the company's capabilities and supporting evidence, resulting in a GovCaptureAI fit score of 10/10.\n\nStrengths: NAICS match on 541512; agency match with Department of Energy; set-aside alignment found for 8(a); capability overlap found in cloud, cybersecurity, engineering, modernization, support; past performance evidence is available.\n\nGaps to Review: confirm incumbent and pricing history before committing capture resources.",
  },
  {
    id: 102,
    sam_notice_id: "GSA-ADMIN-2026-022",
    title: "Administrative Program Support Services",
    solicitation_number: "RFP-2026-022",
    notice_type: "RFP",
    agency: "General Services Administration",
    naics_code: "561110",
    set_aside: "Small Business",
    status: "new",
    posted_date: "2026-07-08",
    due_date: "2026-08-22",
    summary:
      "GSA is seeking administrative program support for acquisition operations, reporting workflows, and program coordination.",
    description:
      "Administrative and program support services for acquisition operations and reporting workflows.",
    qualification_score: 6,
    qualification_recommendation: "consider",
    qualification_rationale:
      "Recommendation: Consider. The opportunity has partial alignment, but it needs a quick capture review before committing, with a GovCaptureAI fit score of 6/10.\n\nStrengths: agency match with General Services Administration; small business eligibility appears aligned.\n\nGaps to Review: technical capability overlap is limited; past performance evidence needs to be checked.",
  },
  {
    id: 103,
    sam_notice_id: "NASA-SSE-2026-041",
    title: "Space Systems Engineering Support",
    solicitation_number: "RFI-2026-041",
    notice_type: "Sources Sought",
    agency: "NASA",
    naics_code: "541330",
    set_aside: "HUBZone",
    status: "no_bid",
    posted_date: "2026-07-15",
    due_date: "2026-09-03",
    summary:
      "NASA is collecting sources for engineering support tied to mission systems integration and spaceflight testing.",
    description:
      "Engineering support for mission systems integration and spaceflight system testing.",
    qualification_score: 2,
    qualification_recommendation: "no_bid",
    qualification_rationale:
      "Recommendation: No-bid. Current qualification evidence is too limited or misaligned to justify pursuit confidently, resulting in a GovCaptureAI fit score of 2/10.\n\nGaps to Review: no target NAICS match was found for 541330; target agency coverage is not yet clear for NASA; set-aside evidence is not clearly aligned for HUBZone.",
  },
];

const sampleCompanies = [
  {
    id: 201,
    name: "Illustris Enterprise LLC",
  },
  {
    id: 202,
    name: "Apex Capture Group",
  },
];

const sampleDocuments = {
  201: [
    {
      id: 301,
      company_id: 201,
      document_type: "capability_statement",
      title: "Zero Trust Capability Statement",
      filename: "Illustris-Zero-Trust-Capabilities.pdf",
      content_text:
        "Cloud modernization, cybersecurity engineering, zero trust architecture, migration planning, and operations support.",
      notes: "Use for DOE, GSA, and civilian agency cloud security opportunities.",
      created_at: "2026-07-01T00:00:00Z",
    },
    {
      id: 302,
      company_id: 201,
      document_type: "past_performance",
      title: "DOE Cloud Security Modernization",
      filename: "DOE-Cloud-Security-Past-Performance.docx",
      content_text:
        "Delivered zero trust implementation planning, identity controls, and secure cloud migration support for a federal energy mission environment.",
      notes: "Strong match for Department of Energy cybersecurity and modernization work.",
      created_at: "2026-07-02T00:00:00Z",
    },
    {
      id: 303,
      company_id: 201,
      document_type: "certification",
      title: "8(a) and Small Business Eligibility",
      filename: "certifications-summary.pdf",
      content_text: "8(a), Small Business, and cybersecurity delivery qualifications.",
      notes: "Verify set-aside eligibility before final bid decision.",
      created_at: "2026-07-03T00:00:00Z",
    },
  ],
};

const workflowStatuses = [
  "new",
  "reviewing",
  "pursuing",
  "no_bid",
  "drafting",
  "submitted",
  "won",
  "lost",
  "closed",
];

const defaultNoticeTypes = [
  "RFI",
  "RFQ",
  "RFP",
  "Sources Sought",
];

const proposalReviewStatuses = [
  "draft_generated",
  "in_review",
  "revisions_needed",
  "ready_for_final",
  "final_review",
  "submitted",
];

const documentTypes = [
  ["capability_statement", "Capability statement"],
  ["past_performance", "Past performance"],
  ["certification", "Certification"],
  ["key_personnel", "Key personnel"],
  ["other", "Other evidence"],
];

const APP_VERSION = "13c-company-award";

const state = {
  companies: [],
  documentsByCompany: {},
  opportunities: [],
  samSearchResults: [],
  samSearchSource: "dashboard",
  selectedId: null,
  activeTab: "overview",
  activeNav: "opportunities",
  dataMode: "sample",
  samApiMode: "unknown",
  samSearchMessage: "Preview up to 3 results",
  companyMessage: "",
  preferredCompanyId: null,
  workflowMessage: "",
  evidenceMessage: "",
  proposalDraft: null,
  proposalMessage: "",
};

const elements = {
  apiBase: document.querySelector("#api-base"),
  refreshButton: document.querySelector("#refresh-button"),
  apiStatus: document.querySelector("#api-status"),
  frontendVersion: document.querySelector("#frontend-version"),
  frontendSource: document.querySelector("#frontend-source"),
  dashboardUrl: document.querySelector("#dashboard-url"),
  apiTarget: document.querySelector("#api-target"),
  dataMode: document.querySelector("#data-mode"),
  demoNote: document.querySelector("#demo-note"),
  searchInput: document.querySelector("#search-input"),
  statusFilter: document.querySelector("#status-filter"),
  recommendationFilter: document.querySelector("#recommendation-filter"),
  noticeTypeFilter: document.querySelector("#notice-type-filter"),
  sortSelect: document.querySelector("#sort-select"),
  samKeyword: document.querySelector("#sam-keyword"),
  samNaics: document.querySelector("#sam-naics"),
  samAgency: document.querySelector("#sam-agency"),
  samNoticeType: document.querySelector("#sam-notice-type"),
  samSearchButton: document.querySelector("#sam-search-button"),
  samClearButton: document.querySelector("#sam-clear-button"),
  samSaveButton: document.querySelector("#sam-save-button"),
  resetDemoQueueButton: document.querySelector("#reset-demo-queue-button"),
  samSearchStatus: document.querySelector("#sam-search-status"),
  samSearchResults: document.querySelector("#sam-search-results"),
  opportunitySearchPanel: document.querySelector("#opportunity-search-panel"),
  companyPanel: document.querySelector("#company-panel"),
  companyForm: document.querySelector("#company-form"),
  companyName: document.querySelector("#company-name"),
  companyWebsite: document.querySelector("#company-website"),
  companyDescription: document.querySelector("#company-description"),
  companyCapabilities: document.querySelector("#company-capabilities"),
  companyNaics: document.querySelector("#company-naics"),
  companyAgencies: document.querySelector("#company-agencies"),
  companyCertifications: document.querySelector("#company-certifications"),
  companySubmitButton: document.querySelector("#company-submit-button"),
  companyMessage: document.querySelector("#company-message"),
  total: document.querySelector("#metric-total"),
  average: document.querySelector("#metric-average"),
  pursue: document.querySelector("#metric-pursue"),
  review: document.querySelector("#metric-review"),
  visibleCount: document.querySelector("#visible-count"),
  table: document.querySelector("#opportunity-table"),
  selectedId: document.querySelector("#selected-id"),
  decisionContent: document.querySelector("#decision-content"),
  decisionPanel: document.querySelector(".decision-panel"),
  workspace: document.querySelector(".workspace"),
  navLinks: document.querySelectorAll(".nav a"),
  tabs: document.querySelectorAll(".detail-tabs button"),
};

function defaultApiBase() {
  if (window.location.protocol === "http:" || window.location.protocol === "https:") {
    return `${window.location.protocol}//${window.location.hostname}:8000`;
  }

  return elements.apiBase.value;
}

elements.apiBase.value = defaultApiBase();

function isLocalHost(hostname) {
  return hostname === "localhost" || hostname === "127.0.0.1" || hostname === "::1";
}

function frontendSourceLabel() {
  if (window.location.protocol === "file:") {
    return "Mac local file";
  }

  if (isLocalHost(window.location.hostname)) {
    return "Local web server";
  }

  if (window.location.hostname === "192.168.1.51") {
    return "Raspberry Pi demo";
  }

  return "Remote demo host";
}

function dashboardLocationLabel() {
  if (window.location.protocol === "file:") {
    return "file:// dashboard";
  }

  return `${window.location.protocol}//${window.location.host}`;
}

function demoNoteText() {
  if (window.location.protocol === "file:") {
    return "Local file view. The Raspberry Pi demo updates only after sync and deploy.";
  }

  if (window.location.hostname === "192.168.1.51") {
    return "Raspberry Pi demo view. If the version looks old, sync and redeploy the Pi.";
  }

  if (isLocalHost(window.location.hostname)) {
    return "Local web view. Use the Pi URL when rehearsing the shared buyer demo.";
  }

  return "Remote demo view. Confirm the API target before a buyer walkthrough.";
}

function updateDemoEnvironment() {
  elements.frontendVersion.textContent = `v${APP_VERSION}`;
  elements.frontendSource.textContent = frontendSourceLabel();
  elements.dashboardUrl.textContent = dashboardLocationLabel();
  elements.apiTarget.textContent = elements.apiBase.value || "Not set";
  elements.dataMode.textContent = state.dataMode === "live" ? "Live API data" : "Sample data";
  elements.demoNote.textContent = demoNoteText();
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function shortOpportunitySummary(opportunity) {
  const existing = opportunity.summary || opportunity.description;
  if (existing) {
    const normalized = String(existing).replace(/\s+/g, " ").trim();
    return normalized.length > 220 ? `${normalized.slice(0, 217)}...` : normalized;
  }

  const title = opportunity.title || "this opportunity";
  const agency = opportunity.agency ? ` from ${opportunity.agency}` : "";
  return `Short summary not available yet. Review ${title}${agency} before capture action.`;
}

function recommendationLabel(value) {
  const labels = {
    pursue: "Pursue",
    consider: "Consider",
    no_bid: "No bid",
    unscored: "Unscored",
  };
  return labels[value || "unscored"] || value;
}

function formatStatus(value) {
  return (value || "new").replace(/_/g, " ");
}

function inferNoticeType(opportunity) {
  const text = [
    opportunity.solicitation_number,
    opportunity.title,
    opportunity.description,
    opportunity.sam_notice_id,
  ]
    .filter(Boolean)
    .join(" ")
    .toUpperCase();

  if (/SOURCE[S]?\s+SOUGHT/.test(text)) {
    return "Sources Sought";
  }

  const match = text.match(/(^|[^A-Z0-9])(RFI|RFQ|RFP)([^A-Z0-9]|$)/);
  return match ? match[2] : null;
}

function formatNoticeType(opportunity) {
  if (typeof opportunity === "string") {
    return opportunity || "Unspecified";
  }

  return opportunity?.notice_type || inferNoticeType(opportunity || {}) || "Unspecified";
}

function isAwardNotice(opportunity) {
  return formatNoticeType(opportunity).toLowerCase().includes("award");
}

function defaultCompanyId() {
  return (
    state.preferredCompanyId ||
    state.companies.find((company) => company.name === "Illustris Enterprise LLC")?.id ||
    state.companies[0]?.id
  );
}

function formatDate(value) {
  if (!value) {
    return "No date";
  }

  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(new Date(`${value}T00:00:00`));
}

function getRecommendation(opportunity) {
  return opportunity.qualification_recommendation || "unscored";
}

function searchableText(opportunity) {
  return [
    opportunity.title,
    opportunity.agency,
    formatNoticeType(opportunity),
    opportunity.naics_code,
    opportunity.set_aside,
    opportunity.solicitation_number,
    opportunity.sam_notice_id,
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

function filteredOpportunities() {
  const status = elements.statusFilter.value;
  const recommendation = elements.recommendationFilter.value;
  const noticeType = elements.noticeTypeFilter.value;
  const query = elements.searchInput.value.trim().toLowerCase();

  const filtered = state.opportunities.filter((opportunity) => {
    const statusMatches = status === "all" || opportunity.status === status;
    const recommendationMatches =
      recommendation === "all" || getRecommendation(opportunity) === recommendation;
    const noticeTypeMatches =
      noticeType === "all" || formatNoticeType(opportunity) === noticeType;
    const queryMatches = !query || searchableText(opportunity).includes(query);
    return statusMatches && recommendationMatches && noticeTypeMatches && queryMatches;
  });

  return filtered.sort((left, right) => {
    switch (elements.sortSelect.value) {
      case "due-asc":
        return dateValue(left.due_date) - dateValue(right.due_date);
      case "agency-asc":
        return textValue(left.agency).localeCompare(textValue(right.agency));
      case "title-asc":
        return textValue(left.title).localeCompare(textValue(right.title));
      case "score-desc":
      default:
        return scoreValue(right) - scoreValue(left);
    }
  });
}

function dateValue(value) {
  return value ? new Date(`${value}T00:00:00`).getTime() : Number.MAX_SAFE_INTEGER;
}

function scoreValue(opportunity) {
  return typeof opportunity.qualification_score === "number"
    ? opportunity.qualification_score
    : -1;
}

function textValue(value) {
  return (value || "").toLowerCase();
}

function renderMetrics() {
  const scored = state.opportunities.filter(
    (opportunity) => typeof opportunity.qualification_score === "number",
  );
  const totalScore = scored.reduce(
    (sum, opportunity) => sum + opportunity.qualification_score,
    0,
  );

  elements.total.textContent = String(state.opportunities.length);
  elements.average.textContent = scored.length
    ? (totalScore / scored.length).toFixed(1)
    : "-";
  elements.pursue.textContent = String(
    state.opportunities.filter((opportunity) => getRecommendation(opportunity) === "pursue")
      .length,
  );
  elements.review.textContent = String(
    state.opportunities.filter((opportunity) =>
      ["consider", "unscored"].includes(getRecommendation(opportunity)),
    ).length,
  );
}

function samSearchPayload() {
  return {
    keyword: elements.samKeyword.value.trim() || null,
    naics_code: elements.samNaics.value.trim() || null,
    agency: elements.samAgency.value.trim() || null,
    set_aside: null,
    notice_type: elements.samNoticeType.value || null,
    posted_from: null,
    posted_to: null,
    limit: 3,
  };
}

function samResultId(result, index = 0) {
  return result.sam_notice_id || result.solicitation_number || `dashboard-search-${index + 1}`;
}

function resultToOpportunity(result, index = 0) {
  return {
    id: Date.now() + index,
    sam_notice_id: samResultId(result, index),
    title: result.title || "Untitled opportunity",
    solicitation_number: result.solicitation_number || samResultId(result, index),
    notice_type: result.notice_type || inferNoticeType(result) || "Unspecified",
    agency: result.agency || "Unassigned",
    naics_code: result.naics_code || null,
    set_aside: result.set_aside || null,
    posted_date: normalizeApiDate(result.posted_date),
    due_date: normalizeApiDate(result.due_date),
    status: "new",
    summary: shortOpportunitySummary(result),
    description: result.description || "No description returned from search preview.",
    qualification_score: null,
    qualification_recommendation: "unscored",
    qualification_rationale: null,
  };
}

function normalizeApiDate(value) {
  if (!value) {
    return null;
  }

  const parsed = new Date(value);
  if (!Number.isNaN(parsed.getTime())) {
    return parsed.toISOString().slice(0, 10);
  }

  const match = String(value).match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})/);
  if (!match) {
    return null;
  }

  const [, month, day, year] = match;
  return `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;
}

function sampleSamSearchResults(payload) {
  return sampleOpportunities
    .filter((opportunity) => {
      const keywordText = [
        opportunity.title,
        opportunity.description,
        opportunity.solicitation_number,
        opportunity.sam_notice_id,
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      const keywordMatches =
        !payload.keyword || keywordText.includes(payload.keyword.toLowerCase());
      const naicsMatches =
        !payload.naics_code || opportunity.naics_code === payload.naics_code;
      const agencyMatches =
        !payload.agency || textValue(opportunity.agency).includes(payload.agency.toLowerCase());
      const noticeTypeMatches =
        !payload.notice_type || formatNoticeType(opportunity) === payload.notice_type;
      return keywordMatches && naicsMatches && agencyMatches && noticeTypeMatches;
    })
    .slice(0, 3)
    .map((opportunity) => ({
      sam_notice_id: opportunity.sam_notice_id,
      title: opportunity.title,
      solicitation_number: opportunity.solicitation_number,
      notice_type: formatNoticeType(opportunity),
      agency: opportunity.agency,
      naics_code: opportunity.naics_code,
      set_aside: opportunity.set_aside,
      posted_date: opportunity.posted_date,
      due_date: opportunity.due_date,
      summary: opportunity.summary || shortOpportunitySummary(opportunity),
      description: opportunity.description,
    }));
}

function renderSamSearch() {
  const modeLabel =
    state.samApiMode === "live"
      ? "SAM.gov live mode"
      : state.samApiMode === "mock"
        ? "Mock mode - not live SAM.gov"
        : "SAM.gov mode unknown";
  elements.samSearchStatus.textContent = `${modeLabel} · ${state.samSearchMessage}`;
  elements.samSaveButton.disabled = !state.samSearchResults.some((result) => !isAwardNotice(result));

  if (!state.samSearchResults.length) {
    elements.samSearchResults.innerHTML =
      '<p class="empty">Run a search to preview opportunities before adding them to the review queue.</p>';
    return;
  }

  elements.samSearchResults.innerHTML = state.samSearchResults
    .map(
      (result, index) => `
        <article class="search-result-card">
          <div>
            <span class="pill ${isAwardNotice(result) ? "informational" : "unscored"}">${escapeHtml(
              isAwardNotice(result) ? "Informational - Award Notice" : result.notice_type || "Opportunity",
            )}</span>
            <h3>${escapeHtml(result.title || "Untitled opportunity")}</h3>
            <p>${escapeHtml(shortOpportunitySummary(result))}</p>
            <span class="summary-note">Short summary for capture triage</span>
          </div>
          <dl>
            <div>
              <dt>Agency</dt>
              <dd>${escapeHtml(result.agency || "Unassigned")}</dd>
            </div>
            <div>
              <dt>NAICS</dt>
              <dd>${escapeHtml(result.naics_code || "No NAICS")}</dd>
            </div>
            <div>
              <dt>Due</dt>
              <dd>${escapeHtml(formatDate(normalizeApiDate(result.due_date)))}</dd>
            </div>
            <div>
              <dt>Solicitation</dt>
              <dd>${escapeHtml(result.solicitation_number || samResultId(result, index))}</dd>
            </div>
          </dl>
        </article>
      `,
    )
    .join("");
}

function renderTable() {
  const visible = filteredOpportunities();
  elements.visibleCount.textContent = `${visible.length} shown`;

  if (!visible.length) {
    elements.table.innerHTML = `
      <tr>
        <td colspan="7" class="empty">No opportunities match the current filters.</td>
      </tr>
    `;
    renderDecisionPanel(null);
    return;
  }

  if (!visible.some((opportunity) => opportunity.id === state.selectedId)) {
    state.selectedId = visible[0].id;
  }

  elements.table.innerHTML = visible
    .map((opportunity) => {
      const recommendation = getRecommendation(opportunity);
      const selected = opportunity.id === state.selectedId ? "selected" : "";
      const score = opportunity.qualification_score ?? "-";

      return `
        <tr class="${selected}" data-id="${opportunity.id}">
          <td class="title-cell">
            <strong>${escapeHtml(opportunity.title)}</strong>
            <span>${escapeHtml(opportunity.solicitation_number || opportunity.sam_notice_id || "No solicitation")}</span>
          </td>
          <td>${escapeHtml(formatNoticeType(opportunity))}</td>
          <td>${escapeHtml(opportunity.agency || "Unassigned")}</td>
          <td>${escapeHtml(formatDate(opportunity.due_date))}</td>
          <td><span class="score">${escapeHtml(score)}</span></td>
          <td><span class="pill ${recommendation}">${escapeHtml(recommendationLabel(recommendation))}</span></td>
          <td>${escapeHtml(formatStatus(opportunity.status))}</td>
        </tr>
      `;
    })
    .join("");

  for (const row of elements.table.querySelectorAll("tr[data-id]")) {
    row.addEventListener("click", () => {
      state.selectedId = Number(row.dataset.id);
      state.activeTab = "overview";
      state.activeNav = "opportunities";
      render();
    });
  }
}

function renderDecisionPanel(opportunity) {
  updateTabs();

  if (!opportunity) {
    elements.selectedId.textContent = "No selection";
    elements.decisionContent.innerHTML =
      '<p class="empty">Select an opportunity to review its detail record.</p>';
    return;
  }

  elements.selectedId.textContent = `Opportunity #${opportunity.id}`;

  if (state.activeTab === "qualification") {
    elements.decisionContent.innerHTML = renderQualificationTab(opportunity);
    return;
  }

  if (state.activeTab === "workflow") {
    elements.decisionContent.innerHTML = renderWorkflowTab(opportunity);
    bindWorkflowControls(opportunity);
    return;
  }

  if (state.activeTab === "evidence") {
    elements.decisionContent.innerHTML = renderEvidenceTab();
    bindEvidenceControls();
    return;
  }

  if (state.activeTab === "proposal") {
    elements.decisionContent.innerHTML = renderProposalTab(opportunity);
    bindProposalControls(opportunity);
    return;
  }

  if (state.activeTab === "source") {
    elements.decisionContent.innerHTML = renderSourceTab(opportunity);
    return;
  }

  elements.decisionContent.innerHTML = renderOverviewTab(opportunity);
}

function renderOverviewTab(opportunity) {
  const recommendation = getRecommendation(opportunity);

  return `
    <div class="detail-hero">
      <span class="pill ${recommendation}">${escapeHtml(recommendationLabel(recommendation))}</span>
      <h3>${escapeHtml(opportunity.title)}</h3>
      <p>${escapeHtml(shortOpportunitySummary(opportunity))}</p>
    </div>
    <div class="field-grid">
      ${fieldItem("Agency", opportunity.agency || "Unassigned")}
      ${fieldItem("Notice type", formatNoticeType(opportunity))}
      ${fieldItem("Due date", formatDate(opportunity.due_date))}
      ${fieldItem("Posted", formatDate(opportunity.posted_date))}
      ${fieldItem("Status", formatStatus(opportunity.status))}
      ${fieldItem("NAICS", opportunity.naics_code || "No NAICS")}
      ${fieldItem("Set-aside", opportunity.set_aside || "No set-aside")}
    </div>
  `;
}

function renderQualificationTab(opportunity) {
  const rationaleParts = parseRationale(opportunity.qualification_rationale);
  const recommendation = getRecommendation(opportunity);

  if (isAwardNotice(opportunity)) {
    return `
      <div class="score-method-card informational-card">
        <h3>Informational notice</h3>
        <p>Award Notices describe an award that has already been made. They are not scored for bid/no-bid pursuit.</p>
      </div>
    `;
  }

  return `
    <div class="qualification-scoreline">
      <div>
        <span class="small">GovCaptureAI Fit Score</span>
        <strong>${escapeHtml(opportunity.qualification_score ?? "-")}/10</strong>
      </div>
      <span class="pill ${recommendation}">${escapeHtml(recommendationLabel(recommendation))}</span>
    </div>
    <div class="score-method-card">
      <h3>How this score is determined</h3>
      <p>
        This is GovCaptureAI's internal bid/no-bid prioritization score, not a government score
        and not a random percentage. It helps decide whether an opportunity deserves capture effort.
      </p>
      <ul>
        <li>NAICS alignment with the company profile</li>
        <li>Agency fit against target customers</li>
        <li>Set-aside and certification alignment</li>
        <li>Capability keyword overlap with uploaded evidence</li>
        <li>Past performance and capability-statement support</li>
      </ul>
    </div>
    <div class="rationale">
      ${rationaleParts.map((part) => `<p>${escapeHtml(part)}</p>`).join("")}
    </div>
  `;
}

function renderWorkflowTab(opportunity) {
  const companyOptions = state.companies.length
    ? state.companies
        .map(
          (company) =>
            `<option value="${escapeHtml(company.id)}" ${Number(company.id) === Number(defaultCompanyId()) ? "selected" : ""}>${escapeHtml(company.name)}</option>`,
        )
        .join("")
    : '<option value="">No company profiles available</option>';

  const statusOptions = workflowStatuses
    .map((status) => {
      const selected = status === opportunity.status ? "selected" : "";
      return `<option value="${status}" ${selected}>${escapeHtml(formatStatus(status))}</option>`;
    })
    .join("");

  return `
    <div class="workflow-stack">
      <section class="workflow-section">
        <h3>Status</h3>
        <div class="workflow-row">
          <select id="workflow-status" aria-label="Set opportunity status">
            ${statusOptions}
          </select>
          <button id="save-status-button" type="button">Save status</button>
        </div>
      </section>
      <section class="workflow-section">
        <h3>Qualification</h3>
        <div class="workflow-row">
          <select id="workflow-company" aria-label="Select company profile">
            ${companyOptions}
          </select>
          <button id="auto-score-button" type="button" ${state.companies.length && !isAwardNotice(opportunity) ? "" : "disabled"}>
            Auto score
          </button>
        </div>
      </section>
      <p id="workflow-message" class="status muted">${escapeHtml(
        state.workflowMessage || (isAwardNotice(opportunity) ? "Award Notices remain informational and are not scored." : workflowModeLabel()),
      )}</p>
    </div>
  `;
}

function workflowModeLabel() {
  if (state.dataMode === "live") {
    return "Connected to live API data.";
  }
  return "Demo data is active; workflow actions update the local dashboard preview.";
}

function renderCompanyOptions(selectedCompanyId = state.companies[0]?.id) {
  if (!state.companies.length) {
    return '<option value="">No company profiles available</option>';
  }

  return state.companies
    .map((company) => {
      const selected = Number(company.id) === Number(selectedCompanyId) ? "selected" : "";
      return `<option value="${escapeHtml(company.id)}" ${selected}>${escapeHtml(company.name)}</option>`;
    })
    .join("");
}

function documentTypeLabel(type) {
  const match = documentTypes.find(([value]) => value === type);
  return match ? match[1] : formatStatus(type || "other");
}

function renderEvidenceTab() {
  const selectedCompanyId = Number(document.querySelector("#evidence-company")?.value) || defaultCompanyId();
  const documents = state.documentsByCompany[selectedCompanyId] || [];
  const typeOptions = documentTypes
    .map(([value, label]) => `<option value="${value}">${escapeHtml(label)}</option>`)
    .join("");

  return `
    <div class="workflow-stack">
      <section class="workflow-section evidence-intro">
        <h3>Company Evidence Library</h3>
        <p>
          Capture the artifacts that support qualification and proposal drafting:
          capability statements, past performance, certifications, key personnel, and other reusable evidence.
        </p>
        <p class="status muted">
          Demo note: this MVP stores evidence metadata and text. Full binary file storage can be added during a pilot.
        </p>
      </section>
      <section class="workflow-section">
        <h3>Add Evidence Artifact</h3>
        <div class="evidence-form-grid">
          <label>
            Company
            <select id="evidence-company">
              ${renderCompanyOptions(selectedCompanyId)}
            </select>
          </label>
          <label>
            Evidence type
            <select id="evidence-type">
              ${typeOptions}
            </select>
          </label>
          <label>
            Title
            <input id="evidence-title" type="text" placeholder="Example: DOE cloud modernization past performance" />
          </label>
          <label>
            File or source reference
            <input id="evidence-filename" type="text" placeholder="Example: capability-statement.pdf" />
          </label>
          <label>
            Upload artifact
            <input id="evidence-file" type="file" />
          </label>
          <label class="evidence-wide">
            Evidence text
            <textarea
              id="evidence-content"
              rows="4"
              placeholder="Paste the key capability, certification, or past performance language that should support scoring and drafts."
            ></textarea>
          </label>
          <label class="evidence-wide">
            Notes
            <textarea
              id="evidence-notes"
              rows="3"
              placeholder="Add capture notes, agency fit, expiration reminders, or review caveats."
            ></textarea>
          </label>
        </div>
        <div class="workflow-row single-action">
          <button id="save-evidence-button" type="button" ${state.companies.length ? "" : "disabled"}>
            Add evidence
          </button>
        </div>
      </section>
      <p id="evidence-message" class="status muted">${escapeHtml(
        state.evidenceMessage || evidenceModeLabel(),
      )}</p>
      <section class="workflow-section">
        <div class="evidence-list-heading">
          <h3>Saved Evidence</h3>
          <span>${escapeHtml(documents.length)} artifact${documents.length === 1 ? "" : "s"}</span>
        </div>
        ${
          documents.length
            ? `<div class="evidence-list">
                ${documents.map((document) => renderEvidenceCard(document)).join("")}
              </div>`
            : '<p class="empty">No evidence artifacts have been saved for this company yet.</p>'
        }
      </section>
    </div>
  `;
}

function renderEvidenceCard(document) {
  return `
    <article class="evidence-card">
      <div>
        <span class="pill unscored">${escapeHtml(documentTypeLabel(document.document_type))}</span>
        <h4>${escapeHtml(document.title)}</h4>
      </div>
      ${document.filename ? `<p><strong>Reference:</strong> ${escapeHtml(document.filename)}</p>` : ""}
      ${document.content_text ? `<p>${escapeHtml(document.content_text)}</p>` : ""}
      ${document.notes ? `<p class="status muted">${escapeHtml(document.notes)}</p>` : ""}
    </article>
  `;
}

function evidenceModeLabel() {
  if (state.dataMode === "live") {
    return "Evidence artifacts are saved through the live company document API.";
  }
  return "Demo data is active; evidence artifacts update the local dashboard preview.";
}

function renderProposalTab(opportunity) {
  const companyOptions = state.companies.length
    ? state.companies
        .map(
          (company) =>
            `<option value="${escapeHtml(company.id)}" ${Number(company.id) === Number(defaultCompanyId()) ? "selected" : ""}>${escapeHtml(company.name)}</option>`,
        )
        .join("")
    : '<option value="">No company profiles available</option>';
  const draft = state.proposalDraft?.opportunity_id === opportunity.id ? state.proposalDraft : null;
  const reviewStatusOptions = proposalReviewStatuses
    .map((status) => {
      const selected = status === (draft?.review_status || "draft_generated") ? "selected" : "";
      return `<option value="${status}" ${selected}>${escapeHtml(formatStatus(status))}</option>`;
    })
    .join("");

  return `
    <div class="workflow-stack">
      <section class="workflow-section">
        <h3>Draft Response</h3>
        <div class="workflow-row proposal-action-row">
          <select id="proposal-company" aria-label="Select company for proposal draft">
            ${companyOptions}
          </select>
          <button id="generate-proposal-button" type="button" ${state.companies.length ? "" : "disabled"}>
            Generate draft
          </button>
          <button id="load-proposal-button" type="button">
            Load latest
          </button>
          <button
            id="export-proposal-button"
            type="button"
            ${draft ? "" : "disabled"}
            title="${draft ? "Download proposal export" : "Generate or load a draft first"}"
          >
            Download export
          </button>
        </div>
        <textarea
          id="proposal-instructions"
          class="proposal-instructions"
          rows="3"
          placeholder="Optional instructions, for example: emphasize transition plan or past performance."
          aria-label="Proposal draft instructions"
        ></textarea>
      </section>
      <p class="status muted">${escapeHtml(state.proposalMessage || proposalModeLabel())}</p>
      ${
        draft
          ? `<section class="workflow-section">
              <h3>Review Workflow</h3>
              <div class="proposal-review-grid">
                <label>
                  Review status
                  <select id="proposal-review-status">
                    ${reviewStatusOptions}
                  </select>
                </label>
                <label>
                  Readiness score
                  <input id="proposal-readiness-score" type="number" min="0" max="100" value="${escapeHtml(
                    draft.readiness_score ?? 30,
                  )}" />
                </label>
              </div>
              <label>
                Review notes
                <textarea id="proposal-review-notes" class="proposal-instructions" rows="3">${escapeHtml(
                  draft.review_notes || "",
                )}</textarea>
              </label>
              <label>
                Review gaps
                <textarea id="proposal-review-gaps" class="proposal-instructions" rows="3">${escapeHtml(
                  (draft.review_gaps || []).join("\n"),
                )}</textarea>
              </label>
              <div class="workflow-row single-action">
                <button id="save-proposal-review-button" type="button">Save review</button>
              </div>
            </section>
            <section class="proposal-draft">
              <div class="proposal-draft-header">
                <h3>${escapeHtml(draft.title)}</h3>
              </div>
              <pre>${escapeHtml(draft.draft_text)}</pre>
            </section>`
          : '<p class="empty">Generate a draft to turn this capture record into a first response outline.</p>'
      }
    </div>
  `;
}

function proposalModeLabel() {
  if (state.dataMode === "live") {
    return "Drafts use live opportunity, company profile, qualification, and document data.";
  }
  return "Demo data is active; draft generation previews a local response outline.";
}

function renderSourceTab(opportunity) {
  return `
    <div class="field-grid source-grid">
      ${fieldItem("SAM notice", opportunity.sam_notice_id || "Not imported from SAM")}
      ${fieldItem("Solicitation", opportunity.solicitation_number || "No solicitation")}
      ${fieldItem("Notice type", formatNoticeType(opportunity))}
      ${fieldItem("Opportunity ID", opportunity.id)}
      ${fieldItem("Status", formatStatus(opportunity.status))}
    </div>
    <pre class="json-preview">${escapeHtml(JSON.stringify(opportunity, null, 2))}</pre>
  `;
}

function fieldItem(label, value) {
  return `
    <div class="field-item">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
    </div>
  `;
}

function parseRationale(value) {
  return (value || "No qualification rationale has been saved yet.")
    .split(/\n\n+/)
    .filter(Boolean);
}

function updateTabs() {
  for (const tab of elements.tabs) {
    tab.classList.toggle("active", tab.dataset.tab === state.activeTab);
  }
}

function updateSidebarNav() {
  for (const link of elements.navLinks) {
    link.classList.toggle("active", link.hash === `#${state.activeNav}`);
  }
}

function renderNoticeTypeOptions() {
  const currentValue = elements.noticeTypeFilter.value;
  const noticeTypes = [
    ...new Set([
      ...defaultNoticeTypes,
      ...state.opportunities.map((opportunity) => formatNoticeType(opportunity)),
    ]),
  ].sort((left, right) => left.localeCompare(right));

  elements.noticeTypeFilter.innerHTML = [
    '<option value="all">All notice types</option>',
    ...noticeTypes.map((noticeType) => {
      const selected = noticeType === currentValue ? "selected" : "";
      return `<option value="${escapeHtml(noticeType)}" ${selected}>${escapeHtml(noticeType)}</option>`;
    }),
  ].join("");

  if (currentValue !== "all" && !noticeTypes.includes(currentValue)) {
    elements.noticeTypeFilter.value = "all";
  }
}

function bindWorkflowControls(opportunity) {
  const saveStatusButton = document.querySelector("#save-status-button");
  const autoScoreButton = document.querySelector("#auto-score-button");

  saveStatusButton?.addEventListener("click", () => updateOpportunityStatus(opportunity));
  autoScoreButton?.addEventListener("click", () => autoScoreOpportunity(opportunity));
}

function bindProposalControls(opportunity) {
  const generateButton = document.querySelector("#generate-proposal-button");
  const loadButton = document.querySelector("#load-proposal-button");
  const saveReviewButton = document.querySelector("#save-proposal-review-button");
  const exportButton = document.querySelector("#export-proposal-button");
  generateButton?.addEventListener("click", () => generateProposalDraft(opportunity));
  loadButton?.addEventListener("click", () => loadLatestProposalDraft(opportunity));
  saveReviewButton?.addEventListener("click", () => saveProposalReview(opportunity));
  exportButton?.addEventListener("click", () => exportProposalDraft(opportunity));
}

function bindEvidenceControls() {
  const companySelect = document.querySelector("#evidence-company");
  const saveButton = document.querySelector("#save-evidence-button");

  companySelect?.addEventListener("change", () => {
    state.evidenceMessage = evidenceModeLabel();
    render();
  });
  saveButton?.addEventListener("click", saveEvidenceArtifact);
}

function companyPayload() {
  const value = (element) => element?.value.trim() || null;
  return {
    name: elements.companyName.value.trim(),
    website: value(elements.companyWebsite),
    description: value(elements.companyDescription),
    core_capabilities: value(elements.companyCapabilities),
    certifications: value(elements.companyCertifications),
    target_naics_codes: value(elements.companyNaics),
    target_agencies: value(elements.companyAgencies),
  };
}

async function createCompanyProfile(event) {
  event.preventDefault();
  const payload = companyPayload();

  if (!payload.name) {
    elements.companyMessage.textContent = "Enter a company name before saving.";
    return;
  }

  elements.companySubmitButton.disabled = true;
  elements.companyMessage.textContent = "Saving company profile...";

  try {
    const company =
      state.dataMode === "live"
        ? await apiRequest("/api/v1/companies/", {
            method: "POST",
            body: JSON.stringify(payload),
          })
        : { id: Date.now(), created_at: new Date().toISOString(), ...payload };

    state.companies = [...state.companies, company];
    state.documentsByCompany = { ...state.documentsByCompany, [company.id]: [] };
    state.preferredCompanyId = company.id;
    state.companyMessage = `${company.name} is available in Qualification and Proposal.`;
    elements.companyForm.reset();
    elements.companyMessage.textContent = state.companyMessage;
    render();
  } catch (error) {
    elements.companyMessage.textContent = `Company save failed: ${error.message}`;
  } finally {
    elements.companySubmitButton.disabled = false;
  }
}

async function searchSamOpportunities() {
  const payload = samSearchPayload();
  state.activeNav = "search";
  elements.samSearchButton.disabled = true;
  state.samSearchMessage = "Searching SAM.gov...";
  renderSamSearch();

  try {
    const response = await apiRequest("/api/v1/sam/search", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    state.samSearchResults = (response.results || []).slice(0, 3);
    state.samSearchSource = response.source || "api";
    if ((response.source || "").includes("mock")) {
      state.samSearchMessage = state.samSearchResults.length
        ? `${state.samSearchResults.length} mock demo result${state.samSearchResults.length === 1 ? "" : "s"} ready to review. This is not live SAM.gov.`
        : "No mock demo results matched that search.";
    } else {
      state.samSearchMessage = state.samSearchResults.length
        ? `${state.samSearchResults.length} live SAM.gov result${state.samSearchResults.length === 1 ? "" : "s"} ready to review`
        : "No live SAM.gov results matched that search.";
    }
  } catch (_error) {
    state.samSearchResults = sampleSamSearchResults(payload);
    state.samSearchSource = "sample";
    state.samSearchMessage = state.samSearchResults.length
      ? `${state.samSearchResults.length} sample result${state.samSearchResults.length === 1 ? "" : "s"} shown because the API is offline`
      : "No sample results matched that search.";
  }

  elements.samSearchButton.disabled = false;
  renderSamSearch();
}

function clearSamSearch() {
  elements.samKeyword.value = "";
  elements.samNaics.value = "";
  elements.samAgency.value = "";
  elements.samNoticeType.value = "";
  elements.searchInput.value = "";
  elements.statusFilter.value = "all";
  elements.recommendationFilter.value = "all";
  elements.noticeTypeFilter.value = "all";
  elements.sortSelect.value = "score-desc";
  state.samSearchResults = [];
  state.samSearchSource = "dashboard";
  state.samSearchMessage =
    "Search filters cleared. Saved Review Queue records were kept for capture workflow continuity.";
  state.activeNav = "search";
  state.activeTab = "overview";
  renderSamSearch();
  render();
}

async function saveSamSearchResults() {
  if (!state.samSearchResults.length) {
    state.samSearchMessage = "Run a search before saving opportunities.";
    renderSamSearch();
    return;
  }

  const payload = samSearchPayload();
  elements.samSaveButton.disabled = true;
  state.samSearchMessage = "Saving search results to review queue...";
  renderSamSearch();

  if (state.samSearchSource === "sample") {
    const existingIds = new Set(state.opportunities.map((opportunity) => opportunity.sam_notice_id));
    const newOpportunities = state.samSearchResults
      .map(resultToOpportunity)
      .filter((opportunity) => !isAwardNotice(opportunity))
      .filter((opportunity) => !existingIds.has(opportunity.sam_notice_id));

    state.opportunities = [...newOpportunities, ...state.opportunities];
    state.selectedId = newOpportunities[0]?.id || state.selectedId;
    state.activeTab = "overview";
    state.activeNav = "search";
    const awardCount = state.samSearchResults.filter(isAwardNotice).length;
    state.samSearchMessage = newOpportunities.length
      ? `${newOpportunities.length} result${newOpportunities.length === 1 ? "" : "s"} added to the dashboard preview${awardCount ? `; ${awardCount} Award Notice${awardCount === 1 ? "" : "s"} kept informational` : ""}`
      : "Those results were already in the dashboard preview.";
    render();
    return;
  }

  try {
    const response = await apiRequest("/api/v1/sam/search/save", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    const awardCount = response.skipped_award_notice_count || 0;
    state.samSearchMessage = `${response.saved_count || 0} saved, ${response.skipped_existing_count || 0} skipped as existing${awardCount ? `, ${awardCount} Award Notice${awardCount === 1 ? "" : "s"} kept informational` : ""}. Refreshing review queue...`;
    await loadOpportunities({ preserveSearch: true });
  } catch (error) {
    state.samSearchMessage = `Search save failed: ${error.message}`;
    renderSamSearch();
  }
}

async function resetDemoQueue() {
  const confirmed = window.confirm(
    "Reset the demo review queue? This deletes saved opportunities and proposal drafts, but keeps companies and evidence.",
  );
  if (!confirmed) {
    return;
  }

  elements.resetDemoQueueButton.disabled = true;
  elements.resetDemoQueueButton.textContent = "Resetting...";

  if (state.dataMode !== "live") {
    state.opportunities = [];
    state.selectedId = null;
    state.samSearchResults = [];
    state.samSearchMessage = "Demo review queue reset in dashboard preview.";
    elements.resetDemoQueueButton.disabled = false;
    elements.resetDemoQueueButton.textContent = "Reset demo queue";
    render();
    return;
  }

  try {
    const response = await apiRequest("/api/v1/opportunities/demo/reset", { method: "POST" });
    state.samSearchResults = [];
    state.samSearchMessage = `${response.deleted_opportunities || 0} opportunity records and ${response.deleted_proposals || 0} proposal drafts deleted. Demo queue is ready.`;
    await loadOpportunities({ preserveSearch: true });
  } catch (error) {
    state.samSearchMessage = `Demo queue reset failed: ${error.message}`;
    renderSamSearch();
  } finally {
    elements.resetDemoQueueButton.disabled = false;
    elements.resetDemoQueueButton.textContent = "Reset demo queue";
  }
}

async function updateOpportunityStatus(opportunity) {
  const statusSelect = document.querySelector("#workflow-status");
  const nextStatus = statusSelect?.value || opportunity.status;

  if (state.dataMode !== "live") {
    replaceOpportunity({ ...opportunity, status: nextStatus });
    state.workflowMessage = `Status changed to ${formatStatus(nextStatus)} in dashboard preview.`;
    state.activeTab = "workflow";
    render();
    return;
  }

  try {
    const updated = await apiRequest(
      `/api/v1/opportunities/${opportunity.id}/status`,
      {
        method: "PATCH",
        body: JSON.stringify({ status: nextStatus }),
      },
    );
    replaceOpportunity(updated);
    state.workflowMessage = `Status saved as ${formatStatus(updated.status)}.`;
  } catch (error) {
    state.workflowMessage = `Status update failed: ${error.message}`;
  }

  state.activeTab = "workflow";
  render();
}

async function evidencePayload() {
  const typeSelect = document.querySelector("#evidence-type");
  const titleInput = document.querySelector("#evidence-title");
  const filenameInput = document.querySelector("#evidence-filename");
  const fileInput = document.querySelector("#evidence-file");
  const contentInput = document.querySelector("#evidence-content");
  const notesInput = document.querySelector("#evidence-notes");
  const file = fileInput?.files?.[0] || null;
  let contentText = contentInput?.value.trim() || null;

  if (file && !contentText && (file.type.startsWith("text/") || /\.(csv|json|md|txt)$/i.test(file.name))) {
    contentText = await file.text();
  }

  return {
    document_type: typeSelect?.value || "other",
    title: titleInput?.value.trim() || "",
    filename: filenameInput?.value.trim() || file?.name || null,
    content_text: contentText,
    notes: notesInput?.value.trim() || null,
  };
}

async function saveEvidenceArtifact() {
  const companySelect = document.querySelector("#evidence-company");
  const companyId = Number(companySelect?.value);
  const payload = await evidencePayload();

  if (!companyId) {
    state.evidenceMessage = "Select a company profile before adding evidence.";
    render();
    return;
  }

  if (!payload.title) {
    state.evidenceMessage = "Add a title before saving the evidence artifact.";
    render();
    return;
  }

  if (state.dataMode !== "live") {
    const document = {
      id: Date.now(),
      company_id: companyId,
      created_at: new Date().toISOString(),
      ...payload,
    };
    state.documentsByCompany = {
      ...state.documentsByCompany,
      [companyId]: [...(state.documentsByCompany[companyId] || []), document],
    };
    state.evidenceMessage = `${documentTypeLabel(payload.document_type)} added to dashboard preview.`;
    state.activeTab = "evidence";
    render();
    return;
  }

  try {
    const document = await apiRequest(`/api/v1/companies/${companyId}/documents`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    state.documentsByCompany = {
      ...state.documentsByCompany,
      [companyId]: [...(state.documentsByCompany[companyId] || []), document],
    };
    state.evidenceMessage = `${documentTypeLabel(document.document_type)} saved for company evidence.`;
  } catch (error) {
    state.evidenceMessage = `Evidence save failed: ${error.message}`;
  }

  state.activeTab = "evidence";
  render();
}

async function autoScoreOpportunity(opportunity) {
  const companySelect = document.querySelector("#workflow-company");
  const companyId = Number(companySelect?.value);

  if (!companyId) {
    state.workflowMessage = "Select a company profile before running auto score.";
    render();
    return;
  }

  if (state.dataMode !== "live") {
    const updated = {
      ...opportunity,
      qualification_score: opportunity.qualification_score ?? 7,
      qualification_recommendation:
        opportunity.qualification_recommendation || "consider",
      qualification_rationale:
        opportunity.qualification_rationale ||
        "Recommendation: Consider. Demo qualification was run from the dashboard workflow.\n\nStrengths: company profile selected for review.\n\nGaps to Review: connect live API data to persist the result.",
    };
    replaceOpportunity(updated);
    state.workflowMessage = "Auto score refreshed in dashboard preview.";
    state.activeTab = "workflow";
    render();
    return;
  }

  try {
    const updated = await apiRequest(
      `/api/v1/opportunities/${opportunity.id}/score/auto`,
      {
        method: "POST",
        body: JSON.stringify({ company_id: companyId }),
      },
    );
    replaceOpportunity(updated);
    state.workflowMessage = `Auto score saved: ${updated.qualification_score ?? "-"}/10, ${recommendationLabel(
      updated.qualification_recommendation,
    )}.`;
  } catch (error) {
    state.workflowMessage = `Auto score failed: ${error.message}`;
  }

  state.activeTab = "workflow";
  render();
}

function buildSampleDraft(opportunity, companyId, instructions) {
  const company = state.companies.find((candidate) => candidate.id === companyId) || state.companies[0];
  const title = `Draft Response: ${opportunity.title}`;
  const companyName = company?.name || "Selected company";
  const executiveSummary = `${companyName} can support ${opportunity.agency || "the agency"} with ${opportunity.title.toLowerCase()} by aligning its capabilities, qualification rationale, and capture evidence to the solicitation.`;
  const draftText = [
    title,
    "",
    "Executive Summary",
    executiveSummary,
    "",
    "Understanding of the Requirement",
    opportunity.description || "Use the full solicitation text to sharpen this section.",
    "",
    "Technical Approach",
    "Lead with the strongest capability alignment, delivery controls, transition readiness, and measurable outcomes.",
    "",
    "Management Approach",
    "Assign capture ownership, confirm compliance requirements, and manage review milestones against the due date.",
    "",
    "Past Performance and Evidence",
    "Add relevant project examples, certifications, key personnel, and document evidence before external use.",
    "",
    "Compliance Notes",
    `- Confirm response requirements for ${formatNoticeType(opportunity)}.`,
    "- Validate due date, page limits, submission portal, and required attachments.",
    instructions ? `- User instructions: ${instructions}` : "",
    "",
    "Review Gaps",
    "- Replace demo language with solicitation-specific requirements before submission.",
  ]
    .filter((line) => line !== "")
    .join("\n");

  return {
    id: Date.now(),
    opportunity_id: opportunity.id,
    company_id: companyId,
    title,
    review_status: "draft_generated",
    readiness_score: 30,
    review_notes: null,
    review_gaps: ["Replace demo language with solicitation-specific requirements before submission."],
    executive_summary: executiveSummary,
    draft_text: draftText,
  };
}

async function generateProposalDraft(opportunity) {
  const companySelect = document.querySelector("#proposal-company");
  const instructionsInput = document.querySelector("#proposal-instructions");
  const companyId = Number(companySelect?.value);
  const instructions = instructionsInput?.value.trim() || null;

  if (!companyId) {
    state.proposalMessage = "Select a company profile before generating a draft.";
    render();
    return;
  }

  if (state.dataMode !== "live") {
    const draft = buildSampleDraft(opportunity, companyId, instructions);
    state.proposalDraft = draft;
    state.proposalMessage = "Draft generated in dashboard preview.";
    replaceOpportunity({ ...opportunity, status: "drafting" });
    state.activeTab = "proposal";
    render();
    return;
  }

  try {
    const draft = await apiRequest(
      `/api/v1/opportunities/${opportunity.id}/proposal/draft`,
      {
        method: "POST",
        body: JSON.stringify({ company_id: companyId, instructions }),
      },
    );
    state.proposalDraft = draft;
    state.proposalMessage = "Draft generated and opportunity moved to drafting.";
    replaceOpportunity({ ...opportunity, status: "drafting" });
  } catch (error) {
    state.proposalMessage = `Draft generation failed: ${error.message}`;
  }

  state.activeTab = "proposal";
  render();
}

async function loadLatestProposalDraft(opportunity) {
  if (state.dataMode !== "live") {
    if (!state.proposalDraft || state.proposalDraft.opportunity_id !== opportunity.id) {
      state.proposalDraft = buildSampleDraft(opportunity, state.companies[0]?.id || 0, null);
    }
    state.proposalMessage = "Latest demo draft loaded.";
    state.activeTab = "proposal";
    render();
    return;
  }

  try {
    const draft = await apiRequest(`/api/v1/opportunities/${opportunity.id}/proposal/latest`);
    state.proposalDraft = draft;
    state.proposalMessage = "Latest proposal draft loaded.";
  } catch (error) {
    state.proposalMessage = `No proposal draft found yet: ${error.message}`;
  }

  state.activeTab = "proposal";
  render();
}

function proposalReviewPayload() {
  const statusSelect = document.querySelector("#proposal-review-status");
  const readinessInput = document.querySelector("#proposal-readiness-score");
  const notesInput = document.querySelector("#proposal-review-notes");
  const gapsInput = document.querySelector("#proposal-review-gaps");
  const readinessScore = Number(readinessInput?.value ?? 30);

  return {
    review_status: statusSelect?.value || "draft_generated",
    readiness_score: Math.max(0, Math.min(100, readinessScore)),
    review_notes: notesInput?.value.trim() || null,
    review_gaps: (gapsInput?.value || "")
      .split("\n")
      .map((gap) => gap.trim())
      .filter(Boolean),
  };
}

async function saveProposalReview(opportunity) {
  if (!state.proposalDraft?.id) {
    state.proposalMessage = "Generate or load a proposal draft before saving review status.";
    render();
    return;
  }

  const payload = proposalReviewPayload();

  if (state.dataMode !== "live") {
    state.proposalDraft = {
      ...state.proposalDraft,
      ...payload,
    };
    state.proposalMessage = "Proposal review saved in dashboard preview.";
    const nextStatus = payload.review_status === "submitted" ? "submitted" : "drafting";
    replaceOpportunity({ ...opportunity, status: nextStatus });
    state.activeTab = "proposal";
    render();
    return;
  }

  try {
    const draft = await apiRequest(
      `/api/v1/opportunities/${opportunity.id}/proposal/${state.proposalDraft.id}/review`,
      {
        method: "PATCH",
        body: JSON.stringify(payload),
      },
    );
    state.proposalDraft = draft;
    state.proposalMessage = "Proposal review saved.";
    const nextStatus = draft.review_status === "submitted" ? "submitted" : "drafting";
    replaceOpportunity({ ...opportunity, status: nextStatus });
  } catch (error) {
    state.proposalMessage = `Proposal review save failed: ${error.message}`;
  }

  state.activeTab = "proposal";
  render();
}

function safeFilename(value, fallback = "proposal-export") {
  const cleaned = String(value || fallback)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
  return cleaned || fallback;
}

function buildDashboardExportText(opportunity, draft) {
  return [
    "GovCaptureAI Proposal Export",
    "",
    `Proposal: ${draft.title || "Draft Response"}`,
    `Opportunity: ${opportunity.title || "Not provided"}`,
    `Agency: ${opportunity.agency || "Not provided"}`,
    `Notice Type: ${formatNoticeType(opportunity)}`,
    `Solicitation: ${opportunity.solicitation_number || "Not provided"}`,
    `NAICS: ${opportunity.naics_code || "Not provided"}`,
    `Set-Aside: ${opportunity.set_aside || "Not provided"}`,
    `Due Date: ${opportunity.due_date || "Not provided"}`,
    `Review Status: ${formatStatus(draft.review_status || "draft_generated")}`,
    `Readiness Score: ${draft.readiness_score ?? 30}/100`,
    "",
    "Review Notes",
    draft.review_notes || "No review notes recorded.",
    "",
    "Review Gaps",
    ...((draft.review_gaps || []).length
      ? draft.review_gaps.map((gap) => `- ${gap}`)
      : ["- No review gaps recorded."]),
    "",
    "Draft Response",
    draft.draft_text || "",
    "",
    "Export Note",
    "This draft is AI-assisted capture support and should be reviewed by the proposal team before external use.",
  ].join("\n");
}

function downloadTextFile(filename, content) {
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

async function exportProposalDraft(opportunity) {
  if (!state.proposalDraft?.id) {
    state.proposalMessage = "Generate or load a proposal draft before exporting.";
    render();
    return;
  }

  const filename = `${safeFilename(opportunity.title)}-proposal-export.txt`;

  if (state.dataMode !== "live") {
    downloadTextFile(filename, buildDashboardExportText(opportunity, state.proposalDraft));
    state.proposalMessage = "Proposal export downloaded from dashboard preview.";
    state.activeTab = "proposal";
    render();
    return;
  }

  try {
    const baseUrl = elements.apiBase.value.replace(/\/$/, "");
    const response = await fetch(
      `${baseUrl}/api/v1/opportunities/${opportunity.id}/proposal/${state.proposalDraft.id}/export`,
    );

    if (!response.ok) {
      const message = await response.text();
      throw new Error(message || `HTTP ${response.status}`);
    }

    const contentDisposition = response.headers.get("content-disposition") || "";
    const match = contentDisposition.match(/filename="([^"]+)"/);
    const exportFilename = match?.[1] || filename;
    downloadTextFile(exportFilename, await response.text());
    state.proposalMessage = "Proposal export downloaded.";
  } catch (error) {
    state.proposalMessage = `Proposal export failed: ${error.message}`;
  }

  state.activeTab = "proposal";
  render();
}

function replaceOpportunity(updatedOpportunity) {
  state.opportunities = state.opportunities.map((opportunity) =>
    opportunity.id === updatedOpportunity.id ? updatedOpportunity : opportunity,
  );
}

async function apiRequest(path, options = {}) {
  const baseUrl = elements.apiBase.value.replace(/\/$/, "");
  const response = await fetch(`${baseUrl}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let detail = "";
    try {
      const errorBody = await response.json();
      detail = errorBody.detail || errorBody.message || "";
    } catch (_error) {
      detail = await response.text();
    }
    throw new Error(detail || `API returned ${response.status}`);
  }

  return response.json();
}

async function loadSamApiMode() {
  try {
    const status = await apiRequest("/api/v1/sam/test");
    state.samApiMode = status.mode || "unknown";
  } catch (_error) {
    state.samApiMode = "unknown";
  }
}

async function loadCompanyDocuments(companies) {
  const entries = await Promise.all(
    companies.map(async (company) => {
      try {
        const documents = await apiRequest(`/api/v1/companies/${company.id}/documents`);
        return [company.id, documents];
      } catch (_error) {
        return [company.id, []];
      }
    }),
  );

  return Object.fromEntries(entries);
}

function render() {
  updateDemoEnvironment();
  updateSidebarNav();
  renderMetrics();
  renderNoticeTypeOptions();
  renderSamSearch();
  renderTable();
  renderDecisionPanel(
    state.opportunities.find((opportunity) => opportunity.id === state.selectedId),
  );
}

async function loadOpportunities(options = {}) {
  elements.apiStatus.textContent = "Loading opportunities";
  updateDemoEnvironment();

  try {
    await loadSamApiMode();
    const [opportunities, companies] = await Promise.all([
      apiRequest("/api/v1/opportunities/"),
      apiRequest("/api/v1/companies/"),
    ]);
    state.opportunities = opportunities.length || companies.length ? opportunities : sampleOpportunities;
    state.companies = companies.length ? companies : sampleCompanies;
    state.dataMode = opportunities.length || companies.length ? "live" : "sample";
    state.documentsByCompany = companies.length ? await loadCompanyDocuments(companies) : sampleDocuments;
    state.preferredCompanyId =
      state.companies.find((company) => company.name === "Illustris Enterprise LLC")?.id ||
      state.companies[0]?.id ||
      null;
    state.selectedId = state.opportunities[0]?.id ?? null;
    state.activeTab = "overview";
    state.activeNav = options.preserveSearch ? "search" : "opportunities";
    state.workflowMessage = "";
    state.evidenceMessage = "";
    state.proposalDraft = null;
    state.proposalMessage = "";
    elements.apiStatus.textContent = opportunities.length
      ? `Live API data · ${opportunities.length} records`
      : "API reachable · showing sample dashboard data";
  } catch (error) {
    state.samApiMode = "unknown";
    state.opportunities = sampleOpportunities;
    state.companies = sampleCompanies;
    state.documentsByCompany = sampleDocuments;
    state.dataMode = "sample";
    state.selectedId = sampleOpportunities[0].id;
    state.activeTab = "overview";
    state.activeNav = options.preserveSearch ? "search" : "opportunities";
    state.workflowMessage = "";
    state.evidenceMessage = "";
    state.proposalDraft = null;
    state.proposalMessage = "";
    elements.apiStatus.textContent = "API offline · showing sample dashboard data";
  }

  render();
}

elements.refreshButton.addEventListener("click", loadOpportunities);
elements.apiBase.addEventListener("input", updateDemoEnvironment);
elements.searchInput.addEventListener("input", render);
elements.statusFilter.addEventListener("change", render);
elements.recommendationFilter.addEventListener("change", render);
elements.noticeTypeFilter.addEventListener("change", render);
elements.sortSelect.addEventListener("change", render);
elements.samSearchButton.addEventListener("click", searchSamOpportunities);
elements.samClearButton.addEventListener("click", clearSamSearch);
elements.samSaveButton.addEventListener("click", saveSamSearchResults);
elements.resetDemoQueueButton.addEventListener("click", resetDemoQueue);
elements.companyForm.addEventListener("submit", createCompanyProfile);

for (const tab of elements.tabs) {
  tab.addEventListener("click", () => {
    state.activeTab = tab.dataset.tab;
    state.activeNav = ["qualification", "workflow", "evidence"].includes(state.activeTab)
      ? state.activeTab
      : "opportunities";
    render();
  });
}

for (const link of elements.navLinks) {
  link.addEventListener("click", (event) => {
    event.preventDefault();

    const target = link.hash.replace("#", "");
    state.activeTab = ["qualification", "workflow", "evidence"].includes(target)
      ? target
      : "overview";
    state.activeNav = target;

    window.history.replaceState(null, "", link.hash);
    render();

    const scrollTarget = target === "search"
      ? elements.opportunitySearchPanel
      : target === "companies"
        ? elements.companyPanel
      : target === "qualification" || target === "workflow" || target === "evidence"
        ? elements.decisionPanel
        : elements.workspace;
    scrollTarget?.scrollIntoView({ behavior: "smooth", block: "start" });
  });
}

loadOpportunities();
