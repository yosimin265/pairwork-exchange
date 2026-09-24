# PairWork

**Trade expertise with human-AI teams.**

PairWork is a 2026 hackathon prototype for exchanging specialist work. A human-AI team earns credits by completing work in its strongest field, then uses those credits to request help from a different specialist team.

> **Prototype, not a live service.** The local version has two demo teams and no public account system. The current hackathon rules and required video lengths have not been checked. Solana Devnet submission remains unverified because the test-SOL faucet failed or rate-limited the attempt.

![AI-generated editorial illustration of two specialists reviewing work together](editorial-collaboration.png)

## Watch and try

- [Complete source package, including the skill and tests](pairwork-source.zip)

- [Product walkthrough: 60 seconds, English narration and captions](demo.mp4) ([WebVTT](demo.vtt) / [SRT](demo.srt))
- [Investor pitch: 54 seconds, English narration and captions](investor.mp4) ([WebVTT](investor.vtt) / [SRT](investor.srt))
- [One-page English overview](overview-en.pdf) and [detailed English overview](overview-en.md)
- [Build status and verification record](STATUS.md)
- [Prompts for the AI-generated editorial images](IMAGE_PROMPTS.md)

The site uses an editorial design with photographs and explanatory diagrams. Its two portraits were generated with AI and do not show actual PairWork users or completed jobs. The videos combine an illustrated demo flow and explanatory slides with synthetic English narration. The product walkthrough illustrates sample work; it does not show Codex or Claude Code autonomously doing a job. The current playable demo starts with a documentation-polishing request.

### Fastest path: public browser preview

Open the [playable browser demo](https://yosimin265.github.io/pairwork-exchange/). Its state is stored in your browser's `localStorage`, so it is separate from the Python server and does not connect a Codex or Claude Code skill. To open `index.html` locally, keep `editorial-collaboration.png` and `editorial-review.png` beside it. GitHub's file preview does not run the app.

The starting state gives each team 300 credits and includes a 50-credit Documentation request to polish the PairWork introduction. Switch between Kai + Codex and Mio + Claude Code to walk through the exchange.

### Local version with the skill client

Python 3.10 or later is required. The core server uses only the Python standard library.

```sh
python3 server.py
```

Open `http://127.0.0.1:8765` in a browser. On macOS, `sh start.command` starts the server as well.

1. Select Mio + Claude Code and accept the starter documentation-polishing request.
2. Insert the sample result in the delivery dialog, review it, and submit it.
3. Switch to Kai + Codex, inspect the result, and approve it.
4. Confirm Kai now has 250 credits and Mio has 350.
5. As Mio, post a new 50-credit Python code-review request.
6. Inspect the completion record and its SHA-256 hash. A hash alone does not mean a transaction was recorded on-chain.

To add the optional skill to a project, run these commands from the unpacked source root. The installer does not overwrite an existing skill:

```sh
python3 install_skill.py --target codex --project /absolute/path/to/your/project
python3 install_skill.py --target claude --project /absolute/path/to/your/project
```

Open that project in Codex or Claude Code and ask it to connect to PairWork. The skill instructs the client to run `scripts/client.py connect`, which opens a local browser approval page. Choose a demo team and approve the connection there.

This is **local demo authorization, not a public sign-in**. Automatic skill recognition and end-to-end operation inside both AI products have not been verified. The common client has been checked for connection, balance retrieval, and the post/accept/deliver/approve API flow. This version calls the local API directly; it is not an MCP server. Its `.session.json` file contains a local session and must not be shared or committed. Sessions expire after eight hours or a server restart. The server is bound to localhost and is not a production service for people on separate computers.

## Why earned credits?

The intended loop is **install a skill → approve a local connection → contribute skilled work → human review → earn credits → request another specialty**. Each team uses its own Codex, Claude Code, or other AI subscription as a tool. It does not rent or share an account or usage allowance.

Compared with a per-job stablecoin payment model, PairWork does not require buying or transferring crypto for each task. Credits are earned by contribution and cannot be purchased, cashed out, or transferred freely. A person still reviews each deliverable and decides whether to approve it. This could reduce payment steps, but ease of use, time savings, usage savings, and legal or policy implications have not been measured. We make no claim that a particular competitor works a certain way or that this design removes all fees or legal risk.

## Solana's role and future direction

The current design creates a SHA-256 hash of a completed-job record and includes a script for the operator to sign and publish that hash in a Solana Devnet Memo. The work product, personal information, and credentials are not intended for the chain. Credits themselves remain in the local SQLite ledger.

```sh
python3 -m pip install pynacl
python3 solana_receipt.py --hash <64-character-SHA-256> --out docs/devnet-receipt.json
```

On first use, the script creates a dedicated test key under `.pairwork/` and requests free Devnet test SOL. It does **not** support Mainnet or handle real funds. The faucet returned an internal error and HTTP 429 during this build, so there is no confirmed Devnet signature. A receipt JSON file is written only after successful submission. A matching hash can show data consistency; it cannot independently prove work quality, a real job, or agreement by both parties. Only the operator signs today; dual-party wallet signatures are not implemented.

A future version could build a verifiable history of approved work and use it to describe specialty-specific reputation, such as translation or code review. Candidate inputs for identifying strengths and allocating credits include PairWork work logs, AI assessments, requester ratings, completion speed, and experience in each field. Published versions of the allocation rules and records of how they were applied could make that process auditable. Expert credentials based on PairWork history could later be presented to other Solana ecosystem services; they would not be official professional licenses.

A chain record does not by itself discover expertise, judge quality, or guarantee fair credit allocation. Reputation scoring, the evaluation and allocation logic, public audits, credential issuance, and external interoperability are unimplemented. Input weights, assessment reliability, and fraud defenses are not yet designed or validated. The current Solana component remains an unconfirmed Devnet Memo submission script.

## Business hypothesis

The proposed business asks whether people who already pay for AI tools would also pay to access specialist human-AI teams. This is a demand hypothesis, not a measured market size. Work exchanges would use earned credits; a **proposed $10/month Pro plan** could offer team selection and priority matching. Private enterprise networks are a later possibility. Credits would not be sold.

The underlying tools have sizable audiences. [OpenAI reported more than 5 million weekly active Codex users in June 2026](https://openai.com/index/codex-for-knowledge-work/), while [Anthropic reported in February 2026 that Claude Code business subscriptions had quadrupled since the start of that year](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation). These are company-reported signals for coding AI, **not** PairWork's addressable market, users, or paying members.

[ChatGPT Pro $100](https://help.openai.com/en/articles/9793128-what-is-chatgpt-pro/) and [Claude Max 5x at $100/month](https://support.claude.com/en/articles/11049741-what-is-the-max-plan?subjects=product) still have usage allowances: [Codex has plan limits](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan), and Claude Max has a [weekly limit](https://support.claude.com/en/articles/11049741-what-is-the-max-plan?subjects=product). Work could remain when someone is busy or reaches an allowance. In the proposed loop, a member contributes in a strong field during spare time, banks credits, and later asks another team for help. Each team pays for and uses its own AI account; there is no account or quota sharing.

The $10 Pro price is a **pricing hypothesis** equal to 10% of a $100 AI plan. If specialist help were to improve work efficiency by **10% or more** and help a member move unfinished work toward a deadline, team selection and priority matching *might* be worth $10/month. Neither that improvement nor willingness to pay has been tested, and financial payback is not established.

As a revenue illustration, **$10/month × 1,000 paying members = $10,000 in monthly revenue before costs**. Both price and member count are assumptions. This is not traction, profit, or a total-addressable-market estimate. Platform costs could include infrastructure, support, disputes, acquisition, payment processing, and on-chain recording; each team would pay its own AI costs. Retention, acquisition cost, and paid conversion are untested.

## Architecture and tests

- Browser preview: HTML, CSS, and JavaScript; no build step; `localStorage` state.
- Local API: Python standard library and SQLite; approval transfers reserved credits in one transaction.
- Skill package: shared `SKILL.md`, Python client, and browser-approved local connection.
- Solana: operator-signed Memo on Devnet only; submission not yet verified.

```text
Human + AI → skill package → localhost API → SQLite ledger
                                ↑
                         Browser approval
Completed-job record → SHA-256 → Devnet Memo (optional separate script)
```

The demo's team choice is role selection, not production login. Run the server only on localhost; do not expose it directly to the public internet. The skill instructions do not implement an operating-system sandbox.

```sh
python3 -m unittest discover -s tests -v
```

Six tests cover the work-exchange loop, point reservation, revisions, unauthorized approval, concurrent approval without double payment, and completion hashing. See [STATUS.md](STATUS.md) for the current verification record.

## Relationship to last year's submission

The [2025 CONPRO AI Chain / SOUL CHAIN repository](https://github.com/yosimin265/yosi1) informed the high-level *purpose → mechanism → future direction* explanation. PairWork is a separate concept and codebase, with a playable demo, reproducible steps, stated implementation boundaries, and two videos. Last year's documents and intellectual-property claims were not copied.

## References and independence

- [Codex skill documentation](https://developers.openai.com/codex/skills/)
- [Claude Code skill documentation](https://code.claude.com/docs/en/skills)
- [Solana transaction documentation](https://solana.com/docs/core/transactions)

Codex, Claude Code, and Solana belong to their respective providers. PairWork is an independent prototype.
