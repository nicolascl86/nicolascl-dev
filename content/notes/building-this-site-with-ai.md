---
title: The making of this website
date: 2026-11-03
summary: A Computer Science A Level, two degrees in Biology and a decade of impostor syndrome later, I built nicolascl.dev with Codex, Claude Code and Adobe Creative Cloud as my team.
tags: [ai, product-management, web]
---

Programming, coding and I have a classic love-hate relationship.

While still at school, I took Computer Science GCE A Level - ***yes I am this old*** - and I was infatuated by the subject. I spent hours and hours on *Microsoft Access* creating my DVD Club project. When my teacher called me with my grade, she said that I got a straight A and also that I came first in Cyprus that year. She told me I should consider pursuing a degree in computer science. So I did the right thing for an 18-year-old. I ignored her advice and studied something that would provide me with much more lucrative employment opportunities. ***Biology***. The programming itch came back soon after I finished my master's degree. You guessed it. Also in Biology. I was convinced this was my calling. Throughout the years I learned a lot in my free time. I learned alone, typing away on my keyboard, but I also suffered from impostor syndrome, and so I have nothing to show for it. This website is the first project allowed outside my personal web browser.

## How the site came together

“I built my website with AI” can sound like “I am good at prompting” or prompt engineering - whatever you want to call it. I prefer, however, to describe it like this:

As a project manager, I work with a couple of tools, camouflaged as professionals in their fields. The tools are Codex and Claude Code, acting as my engineers. I act as the product manager, and I also act as the lead UI/UX designer. I also have a senior designer on my team. Her name is Adobe Creative Cloud. The skills that made it work were the ones I use every day as a project lead.

The very first draft - which was never published - was done using OpenAI's GPTSites feature. I used a well-structured, simple prompt, and the result was a similarly simple, static homepage with basic information about what the website is, who I am and what I do.

Following the first team sprint, a simple web inspector revealed a **gigantic** HTML soup document with inline CSS and JavaScript. GPTSites was given the freedom to decide on styling, colour palettes and fonts. As you will see from the screenshot below, styling is not GPTSites' strongest skill. I have no idea what chain of thought led it to believe that military-style branding was the way to go.

![The first GPTSites draft of nicolascl.dev: an olive and khaki homepage with my name in large dark lettering](/assets/GPTSites.png)

Using what little coding skill I have, I went down a rabbit hole, creating three separate files out of the soup: an HTML, a CSS and a JS file. It was a hideous process, as you can imagine. But from then on I had full visibility of what was behind a website initially created with a single prompt, and I was able to get more involved in the programming parts of the project with Codex and Claude Code. They can confirm that I am **NOT** a micromanager.

## The Random Google Developer Course

You will see in upcoming posts that I am a volunteer for an amazing bunch of people at the [Google Developer Group Cyprus](https://gdg.community.dev/gdg-cyprus/). Check us out. We spent the month of October preparing for GDG Cyprus DevFest 2026, which took place on October 31st, 2026. The impostor syndrome kicked in again, and I found myself taking random courses because all the other volunteers are obviously developers. [Grounded Agents with Firebase SQL Connect](https://developers.google.com/solutions/learn/data-connect-grounded-agents) was the course of choice. Don't ask me why.

Nevertheless, finishing that course introduced me to a number of technologies, including Firebase, Firebase SQL Connect, Vertex AI and Next.js. One of them made this website possible: Firebase Hosting is what I use to host it. I am also using one of the thousands of domains I bought and immediately parked during my programming-itch years, for no reason at all. That would be [nicolascl.dev](https://nicolascl.dev).

## Git, GitHub and a Pipeline I Didn't Know I Had

What kind of biologist pretending to understand code wouldn't use Git and GitHub? I learned both years ago and never used them. It turns out I already knew the idea, just under a different name.

In pharma, every controlled document has a version history and an audit trail: who changed what, when and why. Git does the same. But for code. GitHub is where that history lives, and where every change is proposed and reviewed before it is accepted. And good luck finding pull request number 10 when you are on pull request number five thousand.

The second part took me longer to understand. Every time Codex or Claude Code implements a change after a heated back and forth (remember, I am the product manager), the site checks it automatically and Firebase publishes a private preview for me to review. Nothing goes live until I approve it. Developers call this CI/CD: continuous integration and continuous delivery. In my world, it is change control with a QC release, and I had been running one for weeks without knowing its name.

This post went through exactly that process. You are reading the version that passed. I hope you enjoyed it. Look out for the next ones.

Nicolas Cl
