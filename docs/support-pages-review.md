# Support pages review

- Firebase serves files from public/. Root homepage duplicates are left unchanged.
- public/404.html replaces the Firebase default. Asset and navigation paths are absolute, so nested missing URLs work.
- Maintenance is a standalone page, not an automatic outage handler. No maintenance redirects are enabled.
- Thank-you is an unlinked template. It deliberately does not claim a message was delivered. Connect it only after a real form confirms success, then update its copy.
- Privacy is an explicitly marked, noindex draft. Confirm hosting processing/logging/retention, privacy contact and applicable rights before final publication. No homepage footer link is added yet.
- Pages reuse the current site's typography and layout with burgundy buttons and purple accents; no external assets or JavaScript dependencies.
- All utility pages are noindex.

## Review locally
Run Firebase Hosting emulator from the repository root (firebase emulators:start --only hosting).
Check /404.html, /maintenance.html, /thank-you.html and /privacy.html at desktop and mobile widths.
Request a nonexistent nested URL, e.g. /missing/nested/page, and confirm HTTP 404, styled content and working asset links.
Check keyboard focus, both system color schemes and home/selected-work navigation.
Do not redirect all unknown paths to index.html: that would bypass the 404.
Merge and deploy only after review. A repository change is not a live deployment.
