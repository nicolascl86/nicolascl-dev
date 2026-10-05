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

After editing the root homepage files, copy them into `public/` before deploying:

```sh
cp index.html styles.css script.js public/
firebase deploy --only hosting
```

Deployment requires the Firebase CLI and access to the configured project. Track the hosting configuration and `public/` files in Git; generated `.firebase/` cache files and Firebase debug logs are ignored.

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
