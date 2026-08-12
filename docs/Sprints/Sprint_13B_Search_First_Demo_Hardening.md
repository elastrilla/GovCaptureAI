# Sprint 13B - Search-first Demo Hardening

## Buyer Feedback

A government contractor understood the core GovCaptureAI pain point, but recommended that the demo start with an actual SAM.gov search before moving into the workflow. The feedback was that even if the strongest product value happens after search, the buyer needs to see that search is integrated into the capture process.

The same buyer also asked whether the opportunity score was random, government-provided, or GovCaptureAI-generated. This needs to be clearer in the product and demo script.

## Sprint Goal

Make the demo feel credible from the first interaction by starting with SAM.gov search, showing short opportunity summaries, and labeling the score as GovCaptureAI's internal fit score.

## Scope

- Start the demo from the dashboard SAM.gov search panel.
- Show concise summaries for search results and saved opportunities.
- Add score transparency language to the dashboard.
- Make clear that scoring is not random and not a government percentage.
- Explain the current fit score inputs: NAICS, agency, set-aside, capability overlap, past performance, and evidence.

## Acceptance Criteria

- Search results display a short summary or description preview.
- Saved opportunities preserve the short summary for review.
- Qualification UI labels the score as `GovCaptureAI Fit Score`.
- UI or help text explains that the score is internally generated for bid/no-bid prioritization.
- Demo script includes a plain-language answer to scoring questions.

## Demo Talking Point

"The score is not random and it is not a government score. It is GovCaptureAI's internal fit score. It looks at company capabilities, NAICS, agency alignment, set-aside eligibility, evidence, and past performance. The purpose is to help the contractor decide whether this opportunity deserves capture effort. In a future version, we can also ingest solicitation evaluation factors and adjust scoring around Section L and Section M."

## Out Of Scope For This Sprint

- Full Section L/M extraction.
- Government evaluation-factor weighting.
- Cost proposal scoring.
- Final bid/no-bid automation without human review.

