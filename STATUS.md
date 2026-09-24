# Build status and verification record

## Implemented

- Playable browser preview (`index.html`), local Python server, and SQLite persistence.
- Two demo teams; job posting, acceptance, delivery, revision requests, and approval.
- Credit reservation when a job is posted; atomic credit transfer on approval; duplicate-approval rejection.
- Local completion records and SHA-256 hashes of deliverables.
- Shared skill package and installer for Codex and Claude Code.
- Browser-approved local connection. Sessions expire after eight hours or a server restart.
- Code for operator-signed Solana Devnet Memo submission, limited to Devnet.
- Editorial web and materials pages with two AI-generated photographs and explanatory diagrams.
- A 60-second product walkthrough and a 54-second investor video with synthetic English narration, baked-in English captions, WebVTT and SRT files, plus an English overview.

## Verified

- Six unit tests passed: exchange loop, concurrent approval, authorization, credit reservation, revision, and hashing.
- In the browser, the starter documentation-polishing job was accepted, a sample result submitted and approved, and 50 credits transferred.
- The specialist's balance became 350 credits and could fund a new 50-credit code-review request.
- The common client started a connection, received browser approval, and retrieved the requester's 250-credit balance.
- The bundled skill passed the official `SKILL.md` validator.
- Both videos decoded completely as H.264/AAC with audible-range narration tracks; all captions and selected frames were visually inspected. Playback in Safari or Chrome has not been verified as part of this record.

## Unverified or unimplemented

- End-to-end use of the installed skill inside either Codex or Claude Code. The validated common client is separate from in-product testing.
- Public account authentication, external hosting of the Python API, one-click installation, an MCP server, billing, advanced ratings, and fraud defenses.
- The proposed $10/month Pro plan, 1,000 paying members, and $10,000 monthly revenue before costs. Price, conversion, retention, and acquisition cost are untested assumptions.
- A confirmed Solana Devnet transaction. The faucet returned an internal error and HTTP 429; no confirmed signature is available.
- Signatures from both job parties, independent proof of work quality, or measured time and AI-usage savings.
- This year's hackathon rules, deadline, and required video lengths. No submission has been made.

The videos use an illustrated demo flow, explanatory slides, and AI-generated editorial photographs. They include synthetic English narration and captions. The current demo uses a sample documentation edit; neither video shows an AI product completing a job live. See [IMAGE_PROMPTS.md](IMAGE_PROMPTS.md) for the generated-image prompts.

## One-day scope decision

To make the demo reproducible without another service account, this build uses Python's standard library, SQLite, and a direct-API skill instead of a full Next.js/Supabase/MCP stack. Public user authentication, automatic execution, and production operations are later-stage work.
