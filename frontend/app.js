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

const APP_VERSION = "14a-search-queue";
const SEARCH_HISTORY_KEY = "govcaptureai.sam-search-history";

function readSearchHistory() {
  try {
    const value = JSON.parse(window.localStorage.getItem(SEARCH_HISTORY_KEY) || "[]");
    return Array.isArray(value) ? value : [];
  } catch (_error) {
    return [];
  }
}

const state = {
  companies: [],
  documentsByCompany: {},
  opportunities: [],
  samSearchResults: [],
  searchHistory: readSearchHistory(),
  samSearchSource: "dashboard",
  selectedId: null,
  activeTab: "overview",
  activeNav: "opportunities",
  dataMode: "sample",
  samApiMode: "unknown",
  samSearchMessage: "Preview up to 15 results",
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
  samSearchHistory: document.querySelector("#sam-search-history"),
  samClearHistoryButton: document.querySelector("#sam-clear-history-button"),
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
  return (value || "new").replace(/_/