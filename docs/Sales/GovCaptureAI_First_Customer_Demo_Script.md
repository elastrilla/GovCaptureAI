# GovCaptureAI First Customer Demo Script

## Demo Context

Target date: Thursday, July 16, 2026

Recommended length: 30 minutes

Primary goal: validate that the buyer has a real capture workflow pain and understands GovCaptureAI as a decision-support workspace, not just a SAM.gov search tool.

Secondary goal: identify whether this buyer is a pilot candidate, a referral source, or an early feedback partner.

## Demo Positioning

GovCaptureAI helps government contractors move from opportunity discovery to bid/no-bid decisions and proposal readiness with more structure, speed, and confidence.

The demo should stay focused on this simple buyer promise:

"GovCaptureAI helps a small contractor decide what is worth pursuing and start the response faster."

## What Not To Overpromise

Avoid saying:

- "This replaces your capture manager."
- "This writes a final proposal."
- "This guarantees better win rates."
- "This fully automates SAM.gov capture."
- "This is production-ready for your whole team today."

Safer wording:

- "This supports the capture decision."
- "This creates a stronger first draft, not a final submission."
- "This is designed for a focused pilot."
- "The goal is to reduce manual review time and make bid/no-bid decisions easier to explain."

## Pre-Demo Checklist

Complete this before the call:

- Start the backend API.
- Open the dashboard.
- Confirm the API base is correct.
- Confirm the dashboard shows live API data or the intended demo data mode.
- Confirm the visible app version looks current.
- Confirm the Opportunity Search panel can run a real SAM.gov search or has a known fallback.
- Confirm there are at least three demo opportunities.
- Confirm notice types include RFQ, RFP, and Sources Sought.
- Confirm at least one opportunity has a high score and "Pursue" recommendation.
- Confirm at least one opportunity has a generated proposal draft.
- Confirm the proposal export download works.
- Keep Swagger open in a separate tab as a backup.
- Keep the one-pager open as a backup.

## Suggested Call Flow

| Time | Segment | Purpose |
| --- | --- | --- |
| 0:00-0:03 | Warm opening | Set context and make the buyer comfortable |
| 0:03-0:08 | Discovery | Learn their current process before showing features |
| 0:08-0:10 | Product framing | Explain what GovCaptureAI is and is not |
| 0:10-0:22 | Live demo | Show the capture workflow from search to review to evidence to draft |
| 0:22-0:27 | Buyer reaction | Ask what fits, what is missing, and what matters |
| 0:27-0:30 | Close | Agree on next step |

## Opening Script

"Thanks for making time today. I am going to keep this practical. GovCaptureAI is an early AI-assisted capture workspace for small businesses and government contractors. The goal is not just to find more opportunities. The goal is to help a contractor decide what is worth pursuing, explain why, manage the review workflow, and start a proposal response faster."

"This is still an early product, so I am especially interested in your reaction to the workflow. I would love to learn where this matches how you actually review opportunities and where it needs to be sharper."

## Discovery Questions Before The Demo

Ask two or three before showing the product:

- "How do you currently find and track federal opportunities?"
- "When you see an RFI, RFQ, RFP, or Sources Sought notice, how do you decide whether it deserves time?"
- "Who is involved in your bid/no-bid decision?"
- "Where does the process usually slow down?"
- "What information do you reuse across proposals today?"
- "If this could save you time in one part of the capture process, where would that matter most?"

Listen for:

- Too many opportunities to review.
- Decisions living in spreadsheets or email.
- Weak documentation for bid/no-bid decisions.
- Company past performance scattered across files.
- Proposal drafts starting too late.
- Founder or BD lead doing too much manual screening.

## Transition To Demo

"That is helpful. Let me show you the workflow through the lens of a small contractor trying to decide what deserves attention. I will start with a focused opportunity search, save results into the review queue, then move into qualification, workflow tracking, supporting evidence, and a proposal draft."

"I am starting with search because that is where teams already begin. The value of GovCaptureAI is what happens next: turning search results into decisions, evidence, workflow, and response content."

## Demo Step 1: Opportunity Search

Show:

- Opportunity Search sidebar shortcut.
- Keyword field.
- NAICS field.
- Agency field.
- Notice type field.
- Search SAM.gov button.
- Preview results.
- Short summary or description preview.
- Save results to review queue button.

Suggested search:

- Keyword: IT support.
- Agency: Department of the Navy.
- NAICS: 541512 if the buyer wants a narrower IT services search.
- Leave notice type blank unless the buyer asks for RFI, RFQ, RFP, or Sources Sought.

Alternate search:

- Keyword: cybersecurity.
- NAICS: 541512.
- Leave agency and notice type blank unless the buyer asks for narrower filtering.

Talk track:

"We start with focused discovery using SAM.gov as the source. The goal is not to dump hundreds of opportunities on a small team. For the demo, GovCaptureAI previews up to three results, shows a short summary so the team can quickly understand the need, then lets us save the relevant opportunities into the review queue."

"This keeps discovery connected to the capture workflow. Once an opportunity is saved, it can be qualified, assigned a status, connected to evidence, and used to start a proposal draft."

Demo boundary:

"This dashboard search is intentionally simple for the pilot conversation: keyword, NAICS, agency, and notice type. A pilot can add saved searches, date filters, exclusions, and richer scoring before save."

## Demo Step 2: Opportunity Review Dashboard

Show:

- Total opportunities.
- Average score.
- Pursue candidates.
- Need review count.
- Search box.
- Status filter.
- Recommendation filter.
- Notice type filter.
- Sort by score.

Talk track:

"The first job is triage. A small team does not need more noise. They need a short list of opportunities that deserve review. This dashboard is organized around that review process."

"Notice that we can separate RFI, RFQ, RFP, and Sources Sought activity. That matters because each notice type represents a different kind of decision. An RFI or Sources Sought may be early positioning. An RFQ or RFP may require a faster bid/no-bid call."

What to ask:

"Would this kind of filtered review be useful for your team, or do you already have a clean way to separate these opportunity types?"

## Demo Step 3: Open A Strong Opportunity

Choose a high-scoring opportunity with a "Pursue" recommendation.

Show:

- Opportunity title.
- Agency.
- Notice type.
- Due date.
- NAICS.
- Set-aside.
- Short summary.
- Description.

Talk track:

"Once we select an opportunity, the idea is to keep the important capture context in one place. The team should not have to jump between SAM.gov, a spreadsheet, and a document folder just to understand whether this is worth a closer look. The summary is the quick first read; the full description is still available for deeper review."

## Demo Step 4: Qualification Review

Show:

- GovCaptureAI Fit Score.
- Recommendation.
- Rationale.
- Strengths.
- Gaps.

Talk track:

"The GovCaptureAI Fit Score is not the decision. It is a structured first read. It is not random and it is not a government-provided evaluation percentage. GovCaptureAI compares the opportunity against the company profile, including capabilities, target NAICS codes, target agencies, certifications, differentiators, past performance, and supporting evidence."

"The value is not just the number. The value is the rationale. It gives the team something to discuss: why this looks like a fit, what evidence supports that, and what gaps need human review."

What to ask:

"Does this match the kind of reasoning you use when deciding whether to spend capture or proposal time?"

If the buyer asks whether the score comes from the government:

"No. The government does not provide this fit score. This is GovCaptureAI's internal bid/no-bid support score based on company-to-opportunity alignment. If the solicitation includes formal evaluation factors in Section L or Section M, a future version can ingest those factors and make the scoring model more solicitation-specific."

## Demo Step 5: Workflow Status

Show:

- Workflow tab.
- Status update.
- Review notes or gaps if available.

Talk track:

"The next layer is workflow. A lot of small teams have the decision in someone's head, in an email thread, or in a spreadsheet cell. GovCaptureAI is intended to make the opportunity status visible: new, reviewing, qualified, no-bid, drafting, submitted, or awarded."

"This becomes especially useful when there are multiple opportunities competing for the same limited proposal time."

## Demo Step 6: Evidence Library

Show the Evidence tab before generating or loading the draft.

Show:

- Company evidence library.
- Capability statement artifact.
- Past performance artifact.
- Certification artifact.
- Upload artifact control.
- Evidence text and notes.

Talk track:

"The scoring and proposal draft are only useful if the system has reusable company knowledge. This Evidence tab is where we capture artifacts like capability statements, past performance, certifications, key personnel notes, and other support material."

"For the demo, this captures artifact metadata and evidence text, and it can read text-based files. For a pilot, the next enhancement would be full binary document storage and parsing for PDFs and Word files."

What to ask:

"Where does this information live today: shared drives, old proposals, resumes, certification folders, spreadsheets, or someone's inbox?"

## Demo Step 7: Proposal Draft

Show:

- Proposal tab.
- Company selector.
- Generate draft or load latest.
- Draft response.
- Review workflow.
- Readiness score.
- Review notes.
- Review gaps.

Talk track:

"If the team decides this opportunity is worth pursuing, GovCaptureAI can generate a starting response using the opportunity details, company profile, qualification rationale, and supporting company knowledge."

"This is not meant to be a final proposal. It is a better starting point than a blank page. The proposal team still reviews, edits, adds solicitation-specific requirements, and validates compliance."

What to ask:

"Which proposal sections would be most valuable for you to draft first: executive summary, technical approach, past performance, staffing, or compliance matrix?"

## Demo Step 8: Export

Show:

- Download export button.
- Open or reference the downloaded text export.

Talk track:

"The export is intentionally simple right now. The goal is to move the draft, metadata, review status, readiness score, notes, and gaps into a shareable package. That makes it easier to hand off from capture review into proposal work."

"Over time, this can become a more polished Word or proposal template export, but the first priority is proving the workflow."

## Product Vision Close

"The larger vision is an AI-assisted capture workspace. Discovery is only the beginning. The real value is connecting opportunities to company fit, evidence, workflow status, bid/no-bid decisions, and proposal readiness."

"For an early pilot, I would not try to boil the ocean. I would pick a focused set of target agencies or NAICS codes, load a useful company profile, review a batch of opportunities, and measure whether the team can make faster and clearer pursuit decisions."

## Buyer Feedback Questions

Ask these after the demo:

- "Where did this feel closest to your current pain?"
- "Where did it not match how you work?"
- "Would your team care more about opportunity screening, bid/no-bid documentation, or proposal drafting?"
- "What would need to be true for you to try this on 10 to 25 real opportunities?"
- "What would make this credible enough for your team to trust the recommendations?"
- "Who else would need to see this before a pilot?"

## Objection Handling

### "We already use SAM.gov."

"That makes sense. GovCaptureAI is not trying to replace SAM.gov as the source. The product is meant to help with what happens after discovery: review, qualification, bid/no-bid, workflow, and proposal readiness."

### "We already track opportunities in a spreadsheet."

"That is exactly the behavior this is designed around. The question is whether we can make the spreadsheet process smarter by connecting each opportunity to company fit, rationale, status, and draft response content."

### "Can we trust the AI score?"

"The score is not random and it is not a government percentage. It is GovCaptureAI's internal fit score based on company profile, NAICS, agency alignment, set-aside eligibility, capability overlap, past performance, and evidence. It should not be treated as the final answer. It should be treated as a structured recommendation with supporting rationale. The human team still owns the decision."

### "Can this write the whole proposal?"

"Not today, and I would be careful with that promise. The current value is a stronger first draft and a clearer handoff from capture to proposal. Final compliance, customer-specific language, pricing, and review still need human ownership."

### "Is this ready for production?"

"It is ready for a focused pilot conversation, not a full enterprise rollout. The safest pilot would use a limited company profile, a defined opportunity set, and feedback on whether the workflow saves time and improves decision quality."

## Demo Recovery Plan

If the live dashboard has an issue:

- Say: "This is an early demo environment, so I have a backup path ready."
- Use Swagger to show the API capabilities.
- Use the one-pager to keep the conversation on buyer outcomes.
- Use the demo deck to walk through the workflow visually.
- Offer to send a short follow-up video or screenshots after the call.

If data does not load:

- Confirm the API base.
- Refresh the dashboard.
- Switch to local demo data if available.
- Continue the conversation around the workflow instead of debugging live.

If the proposal draft fails:

- Load the latest saved draft.
- Use the export file as proof of the intended handoff.
- Say: "The important point here is the capture-to-draft workflow. The pilot would help us tune the generated content around your real company profile and opportunity types."

## Recommended Close

"Based on what you saw, I would love your honest reaction: is this solving a real problem, or is it adjacent to the problem?"

If they are interested:

"The best next step would be a focused pilot. We would pick a small target area, maybe one or two agencies or NAICS codes, load a practical company profile, review 10 to 25 opportunities, and track whether GovCaptureAI improves screening speed, bid/no-bid clarity, and first-draft readiness."

If they are not ready:

"That is still helpful. If you are open to it, I would like to capture what was missing or not compelling so I can improve the workflow before the next demo."

## Post-Demo Notes To Capture

Record these immediately after the call:

- Buyer name and organization.
- Buyer role.
- Current opportunity tracking process.
- Primary pain mentioned.
- Most interesting feature.
- Least convincing feature.
- Objections.
- Requested capabilities.
- Pilot interest level.
- Referral possibilities.
- Next action.

## Follow-Up Email Template

Subject: Thank you for reviewing GovCaptureAI

Hi [Name],

Thank you for taking time to review GovCaptureAI today.

The main takeaway I heard was that [insert buyer pain or priority]. GovCaptureAI is being built to help contractors move from opportunity discovery into clearer qualification, bid/no-bid workflow, and proposal readiness.

Based on our conversation, the most relevant areas seem to be:

- [Relevant area 1]
- [Relevant area 2]
- [Relevant area 3]

If useful, the next step could be a focused pilot using a small set of target agencies, NAICS codes, and representative opportunities to test whether the workflow reduces review time and improves pursuit decision quality.

Thank you again for the feedback. It is very helpful at this stage.

Best,
Enrique
