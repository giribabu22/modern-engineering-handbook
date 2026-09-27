"""Prepare the handbook for MkDocs.

The handbook's markdown lives in numbered folders at the repository root so it
reads well on GitHub. MkDocs needs a separate docs directory, so this script
copies the content into website/.docs/ and, on the way:

  * adds SEO front matter (title, description) from website/seo.yml
  * renames README.md -> index.md so each section gets a clean URL
  * turns links to not-yet-written chapters into plain text (no 404s)
  * writes llms.txt and llms-full.txt for AI crawlers and assistants

Usage:
    python website/build_site.py            # then: mkdocs build / mkdocs serve
"""
import pathlib
import re
import shutil

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
WEBSITE = ROOT / "website"
OUT = WEBSITE / ".docs"
CONFIG = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
SITE_URL = CONFIG["site_url"].rstrip("/") + "/"

SEO = yaml.safe_load((WEBSITE / "seo.yml").read_text(encoding="utf-8"))
SECTION = re.compile(r"^\d\d-")
LINK = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)\)")


def source_pages():
    yield ROOT / "README.md"
    for folder in sorted(p for p in ROOT.iterdir() if p.is_dir() and SECTION.match(p.name)):
        # Section overview (README) first, then chapters.
        yield from sorted(folder.glob("*.md"), key=lambda p: (p.name != "README.md", p.name))


def out_rel(rel: str) -> str:
    """Repository path -> path inside the MkDocs docs directory."""
    return re.sub(r"(^|/)README\.md$", r"\1index.md", rel)


def page_url(rel: str) -> str:
    path = out_rel(rel)
    path = re.sub(r"(^|/)index\.md$", r"\1", path)
    path = re.sub(r"\.md$", "/", path)
    return SITE_URL + path


def fix_links(text: str, src: pathlib.Path) -> str:
    def replace(match):
        bang, label, target = match.groups()
        if bang or re.match(r"^[a-z]+:|^#", target):
            return match.group(0)
        path, _, anchor = target.partition("#")
        resolved = (src.parent / path).resolve()
        if not resolved.exists():
            return label                      # planned chapter: keep text, drop link
        new = re.sub(r"(^|/)README\.md$", r"\1index.md", path)
        return f"[{label}]({new}{'#' + anchor if anchor else ''})"

    # Leave fenced code blocks untouched.
    parts = re.split(r"(^```.*?^```)", text, flags=re.M | re.S)
    return "".join(p if p.startswith("```") else LINK.sub(replace, p) for p in parts)


def front_matter(meta: dict) -> str:
    return "---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=1000) + "---\n\n"


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    pages, missing = [], []
    for src in source_pages():
        rel = src.relative_to(ROOT).as_posix()
        text = src.read_text(encoding="utf-8").replace("\r\n", "\n")
        meta = SEO.get(rel)
        if meta is None:
            missing.append(rel)
            meta = {}
        dest = OUT / out_rel(rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(front_matter(meta) + fix_links(text, src), encoding="utf-8")
        h1 = re.search(r"^# (.+)$", text, re.M)
        pages.append({"rel": rel, "url": page_url(rel), "text": text,
                      "title": h1.group(1).strip() if h1 else rel,
                      "description": meta.get("description", "")})

    for extra in (WEBSITE / "static").iterdir():
        text = extra.read_text(encoding="utf-8").replace("{{SITE_URL}}", SITE_URL)
        (OUT / extra.name).write_text(text, encoding="utf-8")

    write_llms_txt(pages)
    print(f"Prepared {len(pages)} pages in {OUT.relative_to(ROOT)}")
    if missing:
        print("Pages without SEO metadata in website/seo.yml:", *missing, sep="\n  ")


def write_llms_txt(pages):
    """llms.txt: a proposed convention (https://llmstxt.org) giving AI tools a
    clean index of the site. llms-full.txt contains the complete text."""
    home = pages[0]
    lines = [f"# {CONFIG['site_name']}", "", f"> {CONFIG['site_description']}", "",
             "Free, first-principles explanations of software engineering: how computers and the "
             "internet work, data and storage, distributed systems, scalability, and AI-era "
             "engineering (LLMs, RAG, agents, evals, AI security). Each chapter covers the problem, "
             "history, internals, tradeoffs, failure scenarios, interview questions, and further reading.",
             ""]
    current = None
    for page in pages[1:]:
        section = page["rel"].split("/")[0]
        if section != current:
            current = section
            lines += ["", f"## {section[3:].replace('-', ' ')}", ""]
        desc = f": {page['description']}" if page["description"] else ""
        lines.append(f"- [{page['title']}]({page['url']}){desc}")
    lines += ["", "## Optional", "", f"- [Full text of every page]({SITE_URL}llms-full.txt)",
              f"- [Source repository]({CONFIG['repo_url']})", ""]
    (OUT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")

    full = [f"# {CONFIG['site_name']}\n\nSource: {home['url']}\n"]
    for page in pages:
        full.append(f"\n\n---\n\nURL: {page['url']}\n\n{page['text'].strip()}\n")
    (OUT / "llms-full.txt").write_text("".join(full), encoding="utf-8")


if __name__ == "__main__":
    main()
