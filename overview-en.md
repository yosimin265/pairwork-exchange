# PairWork — Trade expertise with human-AI teams

PairWork is a contribution-based work exchange for people who use AI tools. A team earns work credits by completing work in its area of expertise, then spends those credits to request help from another specialist team.

**Example:** Kai + Codex requests a clearer PairWork introduction for 50 credits. Mio + Claude Code accepts the Documentation job and submits an edited introduction. Kai reviews and approves it. Fifty credits move from Kai to Mio. Mio can then request a Python code review.

## Difference

Compared with a per-job stablecoin payment model, PairWork uses non-purchasable, non-cashable service credits. Teams exchange expertise rather than transferring crypto for each job. Each person uses their own AI tools and remains responsible for acceptance and delivery. Accounts and subscription quotas are not rented or shared.

The core advantage is a repeatable loop: contribute where your human-AI team is strongest, earn credits, and use them to obtain help where another team is stronger. A human checks the deliverable before approval moves credits. This could make existing AI subscriptions more useful without asking people to transfer their accounts or quotas; the time and quota savings are still unmeasured.

## Entry point

The intended experience is: install a skill, sign in, and exchange work from your usual AI tool. The prototype includes a common skill and a browser-approved local client. It does not yet provide public account authentication, a hosted service, or verified end-to-end operation inside both AI products.

## Solana

The prototype hashes completed-job records and includes a signed Devnet Memo submission script. No work content or credentials are intended for the chain. Devnet submission has not been verified because the test-SOL faucet failed/rate-limited. Hash publication is not proof of work quality or independent proof of a genuine job.

The future Solana concept is to anchor a verifiable history of work approved by the parties. Candidate inputs for identifying a team's specialty and allocating credits are PairWork work logs, AI assessments, requester ratings, completion speed, and experience in each field. Together with human evaluation, these could build reputation by specialty, such as translation or code review. Publishing versions of the credit-allocation rules and records of how they were applied could let others audit the allocation process. PairWork could later issue its own expert credentials based on that history for users to present to other Solana ecosystem services; these would not be official professional licenses.

A chain record alone cannot discover expertise, assess quality, or guarantee fair credit allocation. Reputation scoring, evaluation and allocation logic, a public audit trail, credential issuance, and external interoperability are unimplemented. The weighting of those inputs, reliability of assessments, and fraud defenses are not designed or validated. The current Solana component remains a completion-hash Devnet Memo script with no confirmed submission.

## Business hypothesis

People already paying for AI tools may also pay for access to specialist human-AI teams. That is a demand hypothesis, not a measured market size. The planned Pro subscription would offer team selection and priority matching; private enterprise networks are a possible later product. Credits would be earned through work, not sold.

There is a growing audience for the underlying tools: [OpenAI reported more than 5 million weekly active Codex users in June 2026](https://openai.com/index/codex-for-knowledge-work/), and [Anthropic reported that Claude Code business subscriptions had quadrupled since the start of 2026 in February](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation). These company-reported figures are market signals for coding AI, not PairWork's addressable market or projected customer count.

[ChatGPT Pro $100](https://help.openai.com/en/articles/9793128-what-is-chatgpt-pro/) and [Claude Max 5x at $100 per month](https://support.claude.com/en/articles/11049741-what-is-the-max-plan?subjects=product) still have usage allowances: [Codex has plan limits](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan), and Claude Max has a [weekly limit](https://support.claude.com/en/articles/11049741-what-is-the-max-plan?subjects=product). Some work may therefore remain when a person is busy or reaches an allowance. In the proposed loop, a member helps other teams in their specialty during spare time, banks credits, then asks a specialist team for help when busy. Each team uses its own AI subscription; no account or quota is shared.

The proposed **$10 per month** Pro fee is a 10% add-on to a $100 AI plan, used as a pricing anchor rather than a break-even calculation. If specialist help were to improve work efficiency by **10% or more** and help a member move unfinished work toward a deadline within limited time and AI allowance, team selection and priority matching might be worth paying for. The improvement and willingness to pay are untested hypotheses; financial payback is not established.

At an illustrative **$10 per month**, **1,000 paying members** would produce **$10,000 in monthly recurring revenue before costs**. Price and member count are assumptions, not traction, profit, or a TAM estimate. Teams pay their own AI costs. Platform costs include infrastructure, support, dispute handling, acquisition, payment processing, and on-chain recording. Next validation: repeat exchanges, quality, fulfillment time, willingness to pay, retention, and acquisition cost.

## Build status

Working: browser demo, two-team role selection, job posting/acceptance/delivery/revision/approval, atomic credit ledger, completion hashes, browser-approved local skill client. Pending: production auth, real paid plans, reputation algorithm, MCP server, dual-client testing, confirmed Devnet transaction, hackathon rules review.

## Media disclosure

The 60-second demo and 54-second investor video use English synthetic narration, English captions, edited captures of the prototype, and sample deliverables. They do not show a live AI client completing a job. The two editorial photographs on the site and in the videos were generated with OpenAI image_gen; they do not depict actual PairWork users or completed jobs. Their exact prompts are in [IMAGE_PROMPTS.md](IMAGE_PROMPTS.md).
