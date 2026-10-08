# Michael Reichle — academic homepage

This folder is a complete static website for GitHub Pages. It has no npm install, build service, or external frontend dependency. The generated pages are already present, so GitHub Pages can serve the folder as-is.

## Edit the content

Edit `content.json`, then run `python3 build.py` in this folder. The script regenerates seven HTML pages. It uses only Python's standard library.

- `tabs` contains one `true`/`false` toggle for each navigation tab. Set a value to `false` to hide that tab from the navigation; the corresponding HTML page is still generated so it can be previewed directly and restored without losing content.
- `homeIntro`, `news`, `highlights`, and `recruitment` control the home page. Set `recruitment.visible` to `true` to show the PhD/postdoc notice or `false` to hide it. Add a news item with a month and year in `date` and a short `text`; put newer items first. `groupProgram` and `groupGoals` control the group page; `resourcesIntro` and `resources` control Resources; `programCommittees`, `subreviews`, and `serviceActivities` control Service.
- Each `groupGoals` entry has an `image` path and `imageAlt` description. The three vector illustrations and the website icon (`images/favicon.svg`) are in `images/`; replace an SVG there to update its appearance.
- The home-page portrait is `images/michael-reichle.jpg`. Its visible crop and size are controlled by `.hero-portrait` in `style.css`.
- `scholarUrl`, `dblpUrl`, and `email` control the profile links beneath the name.
- `lastUpdated` controls the date shown in the footer; update it whenever the public content changes.
- Add papers to `publications` or `manuscripts`. Each paper has a `tags` list; new tag names automatically become filter buttons.
- Add talks to `presentations`, courses to `teaching`, and supervised theses or projects to `supervision`. Talk entries can use `slides` and `paper`; omit any that do not apply. For local slide PDFs, place the file in `slides/` and use a relative path such as `slides/example.pdf`.
- Edit `style.css` for the design. The highlight red (`#ff5151`) follows INSAIT's palette; other surfaces use neutral colors.

The research highlights, group goals, and recruiting paragraph are drafts for review. Check the group/recruitment language before making the website public.

## Preview locally

Open `index.html` in a browser. The links between pages work directly from the folder. For a local server, run `python3 -m http.server 8000` and visit `http://localhost:8000/`.

## Publish later with GitHub Pages

1. Create a GitHub repository and upload the **contents of this folder** to its root.
2. In the repository's **Settings → Pages**, choose **Deploy from a branch**, select the branch, and select **/(root)**.
3. Keep the generated HTML, `style.css`, `filters.js`, and `.nojekyll` in the repository root. After editing `content.json`, run `python3 build.py` and commit the regenerated pages.

All page and asset links are relative, so the site works both as a GitHub user site and under a project path.
