# GovCaptureAI Database Design

## Core Tables

### users

- id
- username
- email
- password_hash
- role
- created_at

### companies

- id
- company_name
- cage_code
- uei
- website
- description

### certifications

- id
- company_id
- certification_type
- expiration_date

### naics_codes

- id
- naics_code
- description

### company_naics

- company_id
- naics_id

### opportunities

- id
- solicitation_number
- title
- agency
- office
- posted_date
- response_due_date
- notice_type
- set_aside
- naics_code
- description
- sam_url

### opportunity_scores

- id
- opportunity_id
- score
- recommendation
- reasoning

### proposal_status

- id
- opportunity_id
- status
- assigned_to
- due_date
- submitted_date

### documents

- id
- company_id
- document_type
- filename
- upload_date

### ai_analysis

- id
- opportunity_id
- summary
- strengths
- weaknesses
- recommendation