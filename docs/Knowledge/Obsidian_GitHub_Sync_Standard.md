# Obsidian and GitHub Sync Standard

GovCaptureAI can use Obsidian-style markdown knowledge, but only through curated, demo-safe content.

## Repository Boundaries

| Area | Location | GitHub Sync Rule |
| --- | --- | --- |
| GovCaptureAI app | `/Users/enriquelastrilla/GovCaptureAI` | Sync to `elastrilla/GovCaptureAI` |
| GovCaptureAI curated knowledge | `/Users/enriquelastrilla/GovCaptureAI/knowledge/obsidian_import` | May sync if reviewed and demo-safe |
| CMMC ReadinessAI | `/Users/enriquelastrilla/CMMCReadinessAI` | Use a separate private repository |
| Nested CMMC workspace copy | `/Users/enriquelastrilla/GovCaptureAI/CMMCReadinessAI` | Do not sync in GovCaptureAI |
| Client evidence | client-controlled folders only | Do not sync to public/product repositories |

## GovCaptureAI Knowledge Rule

Only copy sanitized markdown notes into:

```text
knowledge/obsidian_import/
```

Notes in this folder should be safe for demos, product testing, and future pilot workflows.

## Do Not Commit

- Credentials, keys, tokens, passwords, or `.env` files
- Client evidence files
- CUI or FCI-sensitive details
- Proprietary pricing inputs, indirect rates, or margin targets
- Customer-specific CMMC assessment notes unless a private repository and access boundary are approved
- Raw Obsidian vaults that include mixed personal, client, or confidential notes

## Recommended Workflow

1. Keep the working Obsidian vault as the source of personal notes.
2. Copy only reviewed notes into `knowledge/obsidian_import/`.
3. Mark copied notes with front matter such as `demo_safe: true`.
4. Review `git status` before any commit.
5. Keep CMMC ReadinessAI in a separate private repository.

## Future Product Direction

GovCaptureAI should treat Obsidian knowledge as a read-only source at first. A future importer can read selected markdown files, store reviewed metadata, and retrieve relevant knowledge for qualification and proposal drafting.

