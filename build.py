#!/usr/bin/env python3
"""Build the static pages from content.json. Requires only Python 3."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))


def e(value):
    return html.escape(str(value), quote=True)


def a(label, url, class_name=""):
    return f'<a class="{e(class_name)}" href="{e(url)}">{e(label)}</a>'


def linked_people(text):
    result = e(text)
    for person in DATA["people"]:
        result = result.replace(e(person["name"]), a(person["name"], person["url"]))
    return result


NAV_ITEMS = [
    ("home", "Home", "index.html"),
    ("publications", "Publications", "publications.html"),
    ("presentations", "Presentations", "presentations.html"),
    ("teaching", "Teaching", "teaching.html"),
    ("group", "Group", "group.html"),
    ("resources", "Resources", "resources.html"),
    ("service", "Service", "service.html"),
]
NAV = [
    (label, url)
    for key, label, url in NAV_ITEMS
    if DATA.get("tabs", {}).get(key, True)
]


def layout(title, active, body, script=""):
    nav_parts = []
    for label, url in NAV:
        current = ' aria-current="page"' if label == active else ""
        nav_parts.append(f'<a href="{url}"{current}>{label}</a>')
    nav = "".join(nav_parts)
    description = "Michael Reichle is tenure-track faculty at INSAIT, working in cryptography."
    script_tag = f'<script src="{script}" defer></script>' if script else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#292929">
  <meta name="description" content="{e(description)}">
  <title>{e(title)} · Michael Reichle</title>
  <link rel="icon" type="image/svg+xml" href="images/favicon.svg">
  <link rel="stylesheet" href="style.css">
  {script_tag}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="header-inner">
      <nav class="main-nav" aria-label="Main navigation">{nav}</nav>
    </div>
  </header>
  <main id="main">{body}</main>
  <footer class="site-footer">
    <div class="footer-inner">
      <span>Michael Reichle · Cryptography at <a href="{e(DATA["institutionUrl"])}">INSAIT</a> <span class="last-updated">· Last updated {e(DATA["lastUpdated"])}</span></span>
      <div>{a("Google Scholar", DATA["scholarUrl"])}{a("dblp", DATA["dblpUrl"])}{a("Email", "mailto:" + DATA["email"])}</div>
    </div>
    <p class="acknowledgement">Website generated with ChatGPT. Built with Python 3, HTML, CSS, and JavaScript.</p>
  </footer>
</body>
</html>
"""


def page_intro(kicker, title, description="", lead_html=""):
    lead = f'<p class="page-lead">{lead_html or e(description)}</p>' if lead_html or description else ""
    return (
        '<div class="page-intro container">'
        f'<p class="kicker">{e(kicker)}</p><h1>{e(title)}</h1>'
        f'{lead}</div>'
    )


def render_home():
    intro = "".join(f"<p>{linked_people(p)}</p>" for p in DATA["homeIntro"])
    recruitment = DATA["recruitment"]
    news = []
    for item in DATA["news"]:
        news.append(
            '<li class="news-item">'
            f'<span class="news-date">{e(item["date"])}</span>'
            f'<span class="news-text">{e(item["text"])}</span>'
            '</li>'
        )
    highlights = []
    papers = {p["title"]: p for p in DATA["publications"] + DATA.get("manuscripts", [])}
    for item in DATA["highlights"]:
        refs = " ".join(
            a(papers[name]["title"] + "", papers[name]["url"], "paper-ref")
            for name in item["papers"]
        )
        highlights.append(
            '<article class="highlight">'
            f'<p class="highlight-label">{e(item["label"])}</p>'
            f'<h3>{e(item["title"])}</h3><p>{e(item["text"])}</p>'
            f'<div class="highlight-refs">{refs}</div></article>'
        )
    recruitment_block = ""
    if recruitment.get("visible", True):
        recruitment_block = f"""
    <section class="recruit-section container" aria-labelledby="recruit-title">
      <div class="recruit-copy">
        <p class="kicker kicker-light">Work with us</p>
        <h2 id="recruit-title">{e(recruitment["title"])}</h2>
        <p>{e(recruitment["text"])}</p>
      </div>
      <div class="recruit-actions">
        {a("PhD at INSAIT", recruitment["phdUrl"], "button button-white")}
        {a("Postdoc at INSAIT", recruitment["postdocUrl"], "button button-white")}
        {a("Get in touch", "mailto:" + DATA["email"], "button button-white")}
      </div>
    </section>
    """
    body = f"""
    <div class="home-hero">
      <div class="container hero-grid">
        <figure class="hero-portrait">
          <img src="images/michael-reichle.jpg" alt="Michael Reichle" width="2000" height="1335">
        </figure>
        <div class="hero-identity">
          <p class="kicker">INSAIT / Cryptography</p>
          <h1>Michael<br>Reichle</h1>
          <p class="role">Tenure-track faculty at <a href="{e(DATA["institutionUrl"])}">INSAIT</a></p>
          <div class="profile-links" aria-label="Academic profiles and contact">
            {a("Google Scholar", DATA["scholarUrl"])}
            {a("dblp", DATA["dblpUrl"])}
            {a("Email", "mailto:" + DATA["email"])}
          </div>
        </div>
        <div class="hero-summary">{intro}
          <div class="hero-links">{a("Explore the group", "group.html", "inline-action")}{a("Publications", "publications.html", "inline-action")}</div>
        </div>
      </div>
    </div>
    {recruitment_block}
    <section class="home-section news-section container" aria-labelledby="news-title">
      <div class="section-heading"><div><p class="kicker">Updates</p><h2 id="news-title">News</h2></div></div>
      <ul class="news-list">{"".join(news)}</ul>
    </section>
    <section class="home-section highlights-section container" aria-labelledby="highlights-title">
      <div class="section-heading"><div><p class="kicker">Selected work</p><h2 id="highlights-title">Research highlights</h2></div>
      {a("All publications", "publications.html", "section-action")}</div>
      <div class="highlight-grid">{"".join(highlights)}</div>
    </section>
    """
    return layout("Home", "Home", body)


def pub_row(item):
    tags = "".join(f'<span class="tag">{e(tag)}</span>' for tag in item["tags"])
    return (
        f'<article class="publication" data-tags="{e("|".join(item["tags"]))}">'
        f'<div class="pub-meta"><span>{e(item.get("venue", "Preprint"))}</span><span>{e(item["year"])}</span></div>'
        f'<div class="pub-content"><h3>{e(item["title"])}</h3>'
        f'<p class="authors">{e(item["authors"])}</p>'
        f'<div class="tags">{tags}</div>'
        + (f'<p class="pub-note">{e(item["note"])}</p>' if item.get("note") else "")
        + '</div><div class="pub-action">'
        + a("Paper", item["url"], "small-action")
        + '</div></article>'
    )


def render_publications():
    available_tags = {tag for p in DATA["publications"] + DATA["manuscripts"] for tag in p["tags"]}
    preferred_tags = [
        "Signatures", "Zero-knowledge", "Encryption", "Classical cryptography",
        "Post-quantum cryptography",
    ]
    tags = [tag for tag in preferred_tags if tag in available_tags]
    tags += sorted(available_tags - set(tags))
    filters = '<button type="button" class="filter active" data-filter="all" aria-pressed="true">All</button>'
    filters += "".join(
        f'<button type="button" class="filter" data-filter="{e(tag)}" aria-pressed="false">{e(tag)}</button>'
        for tag in tags
    )
    rows = []
    year = None
    for item in DATA["publications"]:
        if item["year"] != year:
            year = item["year"]
            rows.append(f'<h2 class="pub-year">{year}</h2>')
        rows.append(pub_row(item))
    rows.append('<h2 class="pub-year">Preprints &amp; other manuscripts</h2>')
    rows.extend(pub_row(item) for item in DATA["manuscripts"])
    body = (
        page_intro(
            "Research / Publications",
            "Publications",
            lead_html=(
                "An overview of published papers, preprints, and other manuscripts. "
                "Select a topic to narrow the list. For a complete and up-to-date record, see "
                + a("dblp", DATA["dblpUrl"]) + "."
            ),
        )
        + '<div class="container content-area">'
        + f'<div class="filter-bar" role="group" aria-label="Filter publications by topic">{filters}</div>'
        + f'<p class="results-count" aria-live="polite">Showing {len(DATA["publications"])+len(DATA["manuscripts"])} publications</p>'
        + '<div class="publication-list">' + "".join(rows) + '</div>'
        + '<p class="empty-message" hidden>No publications match this topic.</p></div>'
    )
    return layout("Publications", "Publications", body, "filters.js")


def render_presentations():
    rows = []
    for item in DATA["presentations"]:
        links = a("Slides", item["slides"], "small-action") if item.get("slides") else ""
        if item.get("paper"):
            links += a("Paper", item["paper"], "small-action")
        rows.append(
            '<article class="list-row">'
            f'<div class="row-date">{e(item["date"])}</div>'
            f'<div><p class="row-venue">{e(item["venue"])}</p><h2>{e(item["title"])}</h2></div>'
            f'<div class="row-actions">{links}</div></article>'
        )
    body = page_intro("Academic activity / Talks", "Presentations",
                      "Selected conference talks and seminars, with slides.")
    body += '<div class="container content-area"><div class="simple-list">' + "".join(rows) + '</div></div>'
    return layout("Presentations", "Presentations", body)


def render_teaching():
    courses = "".join(
        '<article class="list-row teaching-row">'
        f'<div class="row-date">{e(item["years"])}</div>'
        f'<div><p class="row-venue">{e(item["institution"])}</p><h2>{e(item["course"])}</h2></div></article>'
        for item in DATA["teaching"]
    )
    theses = "".join(
        '<article class="list-row teaching-row">'
        f'<div class="row-date">{e(item["period"])}</div>'
        f'<div><p class="row-venue">{e(" · ".join(filter(None, [item.get("institution"), item.get("type"), item["student"]])))}</p>'
        f'<h2>{e(item["project"])}</h2></div></article>'
        for item in DATA["supervision"]
    )
    body = page_intro("Academic activity / Teaching", "Teaching and Supervision", DATA["teachingIntro"])
    body += '<div class="container content-area"><h2 class="subheading">Courses & seminars</h2><div class="simple-list">'
    body += courses + '</div><h2 class="subheading second-subheading">Thesis supervision</h2><div class="simple-list">'
    body += theses + '</div></div>'
    return layout("Teaching and Supervision", "Teaching", body)


def render_group():
    goals = "".join(
        '<article class="goal">'
        f'<h3>{e(item["title"])}</h3>'
        f'<img class="goal-image" src="{e(item["image"])}" alt="{e(item["imageAlt"])}" '
        'width="400" height="400" loading="lazy">'
        f'<p>{e(item["text"])}</p>'
        '</article>'
        for item in DATA["groupGoals"]
    )
    body = page_intro("At INSAIT / Cryptography", "Cryptography Group", "")
    body += f"""
    <div class="container content-area">
      <div class="group-grid">
        <div><p class="kicker">Research agenda</p><h2 class="group-heading">What we are working toward</h2>
          <p class="group-copy">{e(DATA["groupProgram"])}</p>
        </div>
        <div class="goal-list">{goals}</div>
      </div>
      <div class="group-note"><p class="kicker">People</p><h2>Group members</h2>
        <p>Details of the group and its members will be added here as the research program develops.</p></div>
    </div>
    """
    return layout("Cryptography Group", "Group", body)


def render_service():
    committee_years = {}
    for item in DATA["programCommittees"]:
        committee_years.setdefault(item["name"], []).append(item["year"])
    committees = "; ".join(
        f'{e(name)} ({e(", ".join(years))})'
        for name, years in committee_years.items()
    )
    subreviews = "; ".join(
        f'{e(item["name"])} ({e(item["years"])})'
        for item in DATA["subreviews"]
    )
    activities = "".join(
        f'<article class="service-activity"><h3>{e(item["title"])}</h3><p>{e(item["text"])}</p></article>'
        for item in DATA["serviceActivities"]
    )
    body = page_intro(
        "Academic activity / Service",
        "Service",
        "Program committees, reviewing, and organization.",
    )
    body += (
        '<div class="container content-area service-page">'
        f'<section><h2>Program committees</h2><p>{committees}</p></section>'
        f'<section><h2>Subreviews</h2><p>{subreviews}</p></section>'
        f'<section><h2>Organization</h2><div class="service-activities">{activities}</div></section>'
        '</div>'
    )
    return layout("Service", "Service", body)


def render_resources():
    entries = "".join(
        '<article class="resource-entry">'
        f'<p class="row-venue">{e(item["category"])}</p>'
        f'<h2>{a(item["title"], item["url"])}</h2>'
        f'<p>{e(item["description"])}</p>'
        '</article>'
        for item in DATA["resources"]
    )
    body = page_intro(
        "References / Resources",
        "Resources",
        DATA["resourcesIntro"],
    )
    body += f'<div class="container content-area resource-list">{entries}</div>'
    return layout("Resources", "Resources", body)


PAGES = {
    "index.html": render_home(),
    "publications.html": render_publications(),
    "presentations.html": render_presentations(),
    "teaching.html": render_teaching(),
    "group.html": render_group(),
    "resources.html": render_resources(),
    "service.html": render_service(),
}
for filename, markup in PAGES.items():
    (ROOT / filename).write_text(markup, encoding="utf-8")
print("Generated " + ", ".join(PAGES))
