# GovCaptureAI Knowledge Library

This folder is the curated knowledge staging area for GovCaptureAI.

GovCaptureAI may eventually use selected markdown notes from an Obsidian vault to improve qualification rationale, proposal drafting, buyer objection handling, and capture workflow guidance. This folder is intentionally separate from the source Obsidian vault so only reviewed, demo-safe notes are used.

## Safety Rules

- Copy only notes that are safe to use in demos, pilots, or product testing.
- Do not copy credentials, private keys, customer-sensitive details, CUI, proprietary pricing, or confidential client notes.
- Prefer general capture guidance, reusable proposal language, public terminology, and sanitized examples.
- Keep customer-specific material in a separate client-controlled boundary until GovCaptureAI has formal access controls.

## Current Approach

The first implementation path is read-only:

1. Curate safe Obsidian notes into `obsidian_import/`.
2. Review the notes before using them in demos.
3. Later, add a backend importer that reads these markdown files into a GovCaptureAI knowledge table.
4. Use selected knowledge entries as supporting context for qualification and proposal drafting.

