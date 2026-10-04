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

Upload `index.html`, `styles.css`, and `script.js` together to a static web host. No server-side application is needed.
