import datetime
import os
import pathlib
import re


def slugify(title, fallback):
    s = title.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s or fallback


def main():
    title = os.environ["ISSUE_TITLE"].strip()
    body = os.environ.get("ISSUE_BODY") or ""
    number = os.environ["ISSUE_NUMBER"]

    kst = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(datetime.timezone.utc).astimezone(kst)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    slug = slugify(title, f"post-{number}")
    posts_dir = pathlib.Path("_posts")
    posts_dir.mkdir(exist_ok=True)

    filename = posts_dir / f"{date_str}-{slug}.md"
    i = 2
    while filename.exists():
        filename = posts_dir / f"{date_str}-{slug}-{i}.md"
        i += 1

    escaped_title = title.replace('"', '\\"')
    front_matter = (
        "---\n"
        "layout: post\n"
        f'title: "{escaped_title}"\n'
        f"date: {date_str} {time_str} +0900\n"
        "categories: [개발]\n"
        "---\n\n"
        f"{body}\n"
    )
    filename.write_text(front_matter, encoding="utf-8")

    github_output = os.environ["GITHUB_OUTPUT"]
    with open(github_output, "a", encoding="utf-8") as f:
        f.write(f"filename={filename.as_posix()}\n")


if __name__ == "__main__":
    main()
