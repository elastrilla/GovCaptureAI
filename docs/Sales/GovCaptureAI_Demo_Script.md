# GovCaptureAI Demo Script

## Demo Goal

Show that GovCaptureAI is not just an opportunity search tool. The demo should prove a contractor can move from discovery to qualification, evidence management, workflow tracking, and proposal readiness inside one guided process.

Target demo length: 10 to 15 minutes.

## Audience

- Small business owner
- Capture manager
- Business development manager
- Proposal manager
- Proposal consultant

## Demo Setup

Before the demo:

- Start the backend API.
- Open the dashboard.
- Confirm the dashboard is pointed at the correct API base.
- Confirm the Opportunity Search panel shows a 3-result demo limit.
- Confirm SAM.gov search is ready for the demo, or confirm the intended fallback data mode.
- Have at least two saved opportunities available.
- Have one company profile populated with capabilities, certifications, target NAICS codes, target agencies, and past performance.
- Have at least one evidence artifact available, such as a capability statement, certification, or past performance record.
- Have at least one opportunity with a qualification score and recommendation.
- Have at least one opportunity with a generated proposal draft.

## Talk Track

### 1. Open With The Buyer Problem

"Most small contractors do not struggle because they cannot find opportunities. They struggle because they have too many things to review and not enough structure for deciding what is worth pursuing. GovCaptureAI is built to help with the capture decision, not just the search."

### 2. Search For Opportunities

What to show:

- Opportunity Search sidebar shortcut
- Keyword, NAICS, agency, and notice type fields
- Search SAM.gov button
- Preview results
- Short summary or description preview for each opportunity
- Save results to review queue button

Suggested search:

- Keyword: IT support
- Agency: Department of the Navy
- NAICS: 541512
- Limit: 3 results

Alternate search:

- Keyword: cybersecurity
- NAICS: 541512

Key message:

"GovCaptureAI starts where contractors already start: SAM.gov. The difference is that search does not end as a static list. We preview a focused set of opportunities, show a short summary so the team can quickly understand the need, then save the relevant results into the review queue."

Demo boundary:

"The current dashboard search is intentionally simple: keyword, NAICS, agency, and notice type. A pilot can add richer date filters, saved searches, exclusions, and stronger result triage."

### 3. Show The Opportunity Review Dashboard

What to show:

- Opportunity count
- Average score
- Pursue candidates
- Search and filters
- Notice type filter for RFI, RFQ, RFP, and Sources Sought
- Status and recommendation filters

Key message:

"The dashboard is designed around review and prioritization. A contractor can quickly narrow the list to the opportunities that deserve attention."

### 4. Open An Opportunity Detail View

What to show:

- Title
- Agency
- Notice type
- NAICS code
- Due date
- Set-aside
- Status
- Short summary
- Description

Key message:

"The opportunity record keeps the fields a capture team needs close to the decision, instead of forcing them to jump between SAM.gov, spreadsheets, and shared folders. The short summary gives the team a fast first read before they inspect the full solicitation detail."

### 5. Explain Qualification

What to show:

- GovCaptureAI Fit Score
- Recommendation
- Rationale
- Company profile context
- Score explanation inputs

Key message:

"The score is not random, and it is not a government evaluation percentage. It is GovCaptureAI's internal fit score. It compares the opportunity against the company profile, including NAICS, agency alignment, set-aside eligibility, capability overlap, past performance, and evidence. The scoring is not meant to replace a human capture decision; it gives the team a structured first read: why this may be a fit, where the risk is, and whether the opportunity deserves more time."

### 6. Update Workflow Status

What to show:

- Status update controls
- Review state moving through the workflow

Key message:

"GovCaptureAI keeps the opportunity moving from discovered to reviewed to decision-ready. This is the capture workflow layer."

### 7. Show Evidence Upload

What to show:

- Evidence Upload sidebar shortcut
- Evidence tab in Opportunity Detail
- Company evidence library
- Capability statement, past performance, certification, key personnel, or other evidence type
- Upload artifact control
- Evidence text and notes

Key message:

"GovCaptureAI needs reusable company knowledge to support qualification and drafting. The Evidence Upload workflow captures capability statements, past performance, certifications, key personnel notes, and other support material that can feed the score rationale and proposal draft."

Demo boundary:

"The current demo captures artifact metadata, evidence text, and text-based file content. Full PDF and Word document parsing is a pilot enhancement."

### 8. Generate Or Load A Proposal Draft

What to show:

- Proposal draft tab
- Draft section content
- Readiness score
- Review status
- Notes and gaps

Key message:

"Once the team decides an opportunity is worth pursuing, GovCaptureAI can use the opportunity, company profile, qualification rationale, and evidence artifacts to create a starting draft. The draft still needs review, but it gives the proposal team a better first page than a blank document."

### 9. Close With The Product Vision

"The end goal is a full AI-assisted capture workspace: discover relevant opportunities, qualify fit, manage bid/no-bid decisions, and generate stronger proposal responses from reusable company knowledge."

## Discovery Questions

Use these after the demo:

- How do you decide today whether to bid or pass?
- Which opportunities take the most time to screen?
- What information is hardest to reuse across proposals?
- Who needs to approve a bid/no-bid decision?
- Which proposal sections would save the most time if drafted first?
- Do you care more about RFIs, RFQs, RFPs, or Sources Sought notices at this stage?
- Would you trust an internal fit score more if the score showed the specific inputs behind it?

## Demo Success Criteria

The demo lands if the buyer understands:

- GovCaptureAI focuses on capture decisions, not only SAM.gov search.
- SAM.gov search is integrated into the workflow and does not require a separate handoff.
- Short summaries help the team triage search results quickly.
- The GovCaptureAI Fit Score is internal decision support, not a government score.
- The company profile improves opportunity qualification.
- Qualification rationale makes bid/no-bid decisions easier to discuss.
- Proposal drafting starts from structured capture context.
- The product can be piloted with a focused set of opportunities.

## Backup Talking Points

If the live environment has an issue:

- Use Swagger to show the backend API is modular and inspectable.
- Show the static dashboard and explain the intended workflow.
- Use the one-pager to keep the conversation centered on buyer outcomes.
- Offer a follow-up pilot using the buyer's target NAICS codes and agencies.
