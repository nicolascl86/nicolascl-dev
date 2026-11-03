---
title: I built this site with AI coding assistants. Here's what my job actually was.
date: 2026-11-03
summary: How I used OpenAI Codex and Claude Code to build nicolascl.dev and this Field Notes section, and why the work that mattered most was defining, deciding and reviewing.
tags: [ai, product-management, web]
---

This website was built with AI coding assistants. OpenAI Codex did most of the early implementation, and Claude Code built the section you are reading now.

"I built it with AI" can sound like "I pressed a button and a website appeared". That is not what happened, and it is not the interesting part. The interesting part is that working with an AI engineer feels a lot like working with a fast, talented, slightly overconfident team member. The skills that made it work were the ones I use every day as a project lead.

## Who did what

| I was responsible for | The AI assistants were responsible for |
|---|---|
| What the site is for and who it is for | Writing the HTML, CSS, JavaScript and Python |
| Constraints: plain HTML, no framework, accessible, light and dark themes | Proposing ways to meet those constraints |
| Choosing between options and saying no | Implementing the option I chose |
| Branding: the purple palette, the origami elephant, Adobe typography | Wiring assets and fonts into every page |
| Reviewing each change before it went live | Tests, checks and documentation |

That split is deliberate. I am moving into technical project and product management, and this is the job: own the *what* and the *why*, understand the *how* well enough to challenge it, and make sure nothing ships that hasn't been checked.

## How the site came together

The first version went live in early October 2026: a simple homepage, Firebase Hosting, and automatic preview deployments for every change. The Lab came next, a home for my projects and experiments, followed by dedicated pages for each project.

At the end of October I did a larger refresh: a new palette, the origami elephant logo prepared with Adobe tools, Adobe Fonts for typography, and an interactive simulation of an n8n news workflow. The DevFest Cyprus case study and a page for my personal n8n automations followed in November.

Every change went through the same loop. I described the outcome, the AI proposed and built it on a separate branch, Firebase published a private preview, and I reviewed it before merging. Nothing reached the live site without that last step.

## The bug that taught me the most

After the logo release, a screenshot of the live site showed the elephant stacked awkwardly on the page. The code was correct, so the problem had to be elsewhere.

The cause was caching. Browsers and hosting providers keep copies of files like stylesheets to make sites load faster. The live site was serving new HTML alongside an *old* stylesheet, and the two didn't match. We confirmed it by deliberately recreating the broken combination locally, which is a far better approach than guessing.

The fix was to give every stylesheet, script and image a fingerprint in its URL, generated from its content. When a file changes, its fingerprint changes, and browsers fetch the new version. We also added an automated check that blocks deployment if any fingerprint is out of date.

The lesson wasn't really about caching. It was that "it works on my machine" is not a definition of done. Verification has to be part of the process, not an afterthought, and that applies just as much to an ERP migration as to a personal website.

## Building Field Notes

For this section I tried something I would do with any vendor or team: I asked for options before any work started. The AI looked at the site's structure and came back with four approaches, from hand-written pages to adopting a full static site framework to using a hosted platform like Substack.

I chose the option that fit what already existed: I write posts in Markdown, and a small Python script turns them into pages that match the rest of the site. It also produces the RSS feed, the reading time on each post, and the "latest note" card on the homepage.

A few decisions I'm glad I made early:

- **Privacy-friendly analytics.** I'm based in Cyprus, so GDPR applies. Instead of tools that need a cookie banner, the site uses GoatCounter, which counts visits without cookies.
- **Tags now, tag pages later.** Every post carries tags from day one, but clickable tag pages wait until there are enough posts to make them useful. One post per tag page would make the site look emptier, not richer.
- **Shareable by design.** Each post has proper link previews for LinkedIn and messaging apps, a sitemap for search engines, and plain share links without tracking scripts.

## What transfers to my day job

- **Constraints are the spec.** The more precisely I described what I wanted, and what I didn't, the better the result. Vague requests produce confident, plausible, wrong answers.
- **Ask for options first.** Asking "what are my choices?" before "build it" kept me in the decision-maker's seat.
- **Review everything.** AI assistants are fast and articulate, and that makes it easy to accept their output without checking it. Reviewing it is the job.
- **Understand enough to challenge.** I don't need to write every line, but I do need to know why a cache breaks a page or why a build step exists. That's what lets me ask the right questions.

This section is where I'll write about what I learn, at work and on projects like this one. If you want to follow along, the [RSS feed](/feed.xml) is the easiest way for now. An email newsletter will come later.
