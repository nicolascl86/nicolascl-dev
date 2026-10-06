# nicolascl.dev

Personal homepage for Nicolas Kleovoulou, introducing his work across operations, digital transformation, AI, automation, and technology.

Built with plain HTML, CSS, and JavaScript. No dependencies or build step are required.

## Features

- Responsive layout with selected work and current interests.
- Light and dark themes, following the system preference until a theme is selected.
- Saved theme preference using local storage when available.
- Keyboard focus indicators and support for reduced motion preferences.
- Back-to-top button and links to LinkedIn and GitHub.
- Core content remains accessible without JavaScript.

## Run locally

Open `index.html` in a browser, or serve the project folder with Python 3:

```sh
python3 -m http.server 8000
```

Then visit <http://localhost:8000>. Stop the server with `Ctrl+C`.

## Project files

| File | Purpose |
| --- | --- |
| `index.html` | Page content, structure, and metadata |
| `styles.css` | Layout, responsive styles, and theme colors |
| `script.js` | Theme switching, keyboard focus, and back-to-top behavior |
| `.gitignore` | Excludes macOS metadata and the local homepage ZIP archive |

## Deployment

Firebase Hosting serves the `public/` folder, as configured in `firebase.json`. The default Firebase project is set in `.firebaserc`.

Automatic deployment is configured in `.github/workflows/` once the setup PR
is merged into `main`:

- `firebase-hosting-merge.yml` deploys the full `public/` folder to the live site
  on pushes to `main`, including PR merges.
- `firebase-hosting-pull-request.yml` creates preview deployments for pull
  requests from branches in this repository. Fork PRs are excluded.
- No build is required; the generated build step only prints a message.
- Both workflows reference the GitHub Actions repository secret
  `FIREBASE_SERVICE_ACCOUNT_NICOLASCL_DEV_WEBSITE`, created by the user's
  successful Firebase CLI setup. Its presence and validity have not been
  independently verified; credentials must never be committed.

Keep each root HTML/CSS/JavaScript file synchronized with its `public/` copy
before committing. GitHub Actions reads `firebase.json`, which selects `public/`
and the project `nicolascl-dev-website` from the workflows.

Initialization alone does not deploy. Merging the setup PR should deploy all
current main content, including the already-merged Lab page. Confirm success in
GitHub Actions before treating the live site as updated. Manual deployment remains
available using `firebase deploy --only hosting` with authorized Firebase access.

### Deployment setup verification — 5 October 2026

- Generated workflows inspected for main-push live deployment, same-repository
  PR previews, matching project ID and service-account secret references.
- Hosting configuration preserved; root/public website copies remain identical.
- Workflow YAML parsed and deployment trigger/configuration assertions passed.
- User reported visually verifying the Lab page and merging its PR into main.
  This is user-confirmed visual verification, not an automated browser test.
- No deployment run or credential validity was verified during setup preparation.
  The setup workflows must first be merged into main.

## Lab page

The homepage’s Explore the Lab link opens `thelab.html` at its dedicated Lab introduction. The Lab page uses
its own `thelab.css` and `thelab.js`; matching copies live in `public/` for
Firebase Hosting. JavaScript moves keyboard focus to the selected section or
project while retaining native anchor navigation. Content and navigation remain
available without JavaScript.

### Verification — 5 October 2026

- Passed JavaScript syntax validation with `node --check thelab.js`.
- Passed HTML parsing and checks that local assets and anchor destinations exist
  for both homepage and Lab copies.
- Passed byte-for-byte consistency checks for all six HTML/CSS/JavaScript files
  between the root directory and Firebase’s `public/` directory.
- Passed isolated JavaScript behavior checks for initial deep links, all four
  section/project links, hash/history changes, modified clicks, and missing or
  malformed fragments. Focus uses `preventScroll` to retain native scrolling.
- Passed Git whitespace checks.
- Browser rendering and real-browser keyboard interaction remain unverified:
  browser security policy rejected opening local file URLs. The isolated checks
  do not establish visual layout or browser-level accessibility.

No Firebase deployment was performed. The repository documents manual deployment
and contains no checked-in GitHub Actions deployment workflow.

### Lab opening revision — 5 October 2026

- Replaced the repeated homepage hero with “The Lab” and a short introduction
  specific to the existing projects and experiments. Added a Back to home link
  and linked the NK mark to the homepage.
- Updated both homepage links to open the Lab at the top, without skipping its
  introduction via a fragment.
- Passed JavaScript syntax, HTML asset/fragment checks, root/public consistency,
  distinct opening content, homepage return-link, and Git whitespace checks.
- Category/project content and page-specific JavaScript are unchanged; the
  isolated interaction checks recorded above still apply. Browser rendering
  remains unverified due to the previously recorded security restriction.

### Portfolio project pages — 6 October 2026

Explore the Lab now links to `thelab.html#selected-projects`. Four responsive
project cards link to individual static HTML pages with overviews, focus areas,
return links and next-project navigation. The first three pages use introductory
copy pending detailed project documentation; no outcomes or metrics are claimed.
Content and navigation work without JavaScript.

Root and public copies use identical content. In-memory checks verify local
page/asset destinations, section fragments and copy consistency.
Browser rendering and Firebase preview deployment have not been verified.
This revision supersedes the earlier description of opening the Lab without a fragment.
