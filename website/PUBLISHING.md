# Publishing the Handbook Website

This folder turns the markdown handbook into a website at
**https://giribabu22.github.io/modern-engineering-handbook/**.

The markdown files in the numbered folders are the single source of truth. Edit them as usual;
the website rebuilds automatically on every push to `main`.

## How it works

| File | Purpose |
|------|---------|
| `mkdocs.yml` (repo root) | Site name, URL, theme, and navigation menu |
| `website/seo.yml` | Google title and description for every page |
| `website/build_site.py` | Copies the handbook into `website/.docs/`, adds SEO data, writes `llms.txt` |
| `website/overrides/main.html` | Link-preview tags, structured data, search-engine verification tags |
| `website/static/robots.txt` | Crawler rules (search engines and AI crawlers are all welcome) |
| `.github/workflows/deploy-site.yml` | Builds and publishes the site with GitHub Pages |

## Preview locally

```bash
pip install -r website/requirements.txt
python website/build_site.py
mkdocs serve          # open http://127.0.0.1:8000/modern-engineering-handbook/
```

## When you add a new chapter

1. Write the chapter in its section folder, as usual.
2. Add a `title` and `description` for it in `website/seo.yml`.
   - Title: what a student would type into Google (under ~60 characters).
   - Description: one sentence promising what the page actually covers (120–160 characters).
3. Add it to the `nav:` list in `mkdocs.yml`.
4. Push. The site updates in a couple of minutes.

The build script prints any page that is missing SEO metadata.

## One-time setup (done by the repository owner)

### 1. Turn on GitHub Pages
1. Make sure the repository is **public**.
2. GitHub → repository → **Settings → Pages**.
3. Under *Build and deployment*, set **Source: GitHub Actions**.
4. Push to `main` (or run the *Publish website* workflow from the **Actions** tab).

### 2. Improve the GitHub repository page
In the repository's **About** section (gear icon on the main page):
- **Description:** "A free handbook explaining software engineering from first principles — computers, networks, databases, distributed systems, scalability, and AI engineering."
- **Website:** `https://giribabu22.github.io/modern-engineering-handbook/`
- **Topics:** `software-engineering`, `system-design`, `distributed-systems`, `computer-science`, `learning`, `handbook`, `interview-preparation`, `ai-engineering`, `llm`, `backend`

### 3. Google Search Console (most important)
1. Go to https://search.google.com/search-console and click **Add property**.
2. Choose **URL prefix** and enter `https://giribabu22.github.io/modern-engineering-handbook/`.
3. Choose the **HTML tag** verification method. Copy only the `content="..."` value.
4. Paste it into `google_site_verification:` in `mkdocs.yml`, push, wait for the site to rebuild, then click **Verify**.
5. Open **Sitemaps** and submit `sitemap.xml`.
6. Optional: use **URL Inspection → Request indexing** for the home page and your best chapters.

### 4. Bing Webmaster Tools
Bing's index feeds several AI assistants, including Copilot and ChatGPT search.
1. Go to https://www.bing.com/webmasters and sign in.
2. Choose **Import from Google Search Console** (easiest), or add the site and use the meta-tag
   method with `bing_site_verification:` in `mkdocs.yml`.
3. Submit the sitemap: `https://giribabu22.github.io/modern-engineering-handbook/sitemap.xml`.

### 5. Get links from other sites
Search engines and AI tools rank pages higher when other trusted sites link to them.
- Share individual chapters where they answer a real question (r/learnprogramming,
  r/cscareerquestions, r/systemdesign, dev.to, Hashnode, LinkedIn, Hacker News "Show HN").
- Submit to relevant "awesome" lists on GitHub (e.g., system design, software engineering, backend).
- Write short posts that summarize one chapter and link to the full version.
- Keep publishing: new chapters give people new reasons to link.

## Good to know

- **Timeline:** indexing usually takes days to a few weeks; ranking for competitive searches takes months.
- **`robots.txt` on a github.io project site:** crawlers only read `robots.txt` at the domain root
  (`giribabu22.github.io/robots.txt`), so the file in this project is informational until you use a
  custom domain. That's fine — without one, everything is allowed by default. Submit the sitemap
  in Search Console and Bing directly.
- **Custom domain (optional):** a domain like `engineeringhandbook.dev` looks more credible and makes
  `robots.txt` and `llms.txt` sit at the domain root. Set it in Settings → Pages → Custom domain,
  then update `site_url` in `mkdocs.yml`.
- **GitHub and the website both appear in Google.** Each website page declares itself the canonical
  version, and the repository README links to the site, so the two support each other.
