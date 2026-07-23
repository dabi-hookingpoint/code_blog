import os
import re


def parse_issue_form(body):
    """GitHub issue forms render each field as '### Label\n\nAnswer\n\n'."""
    fields = {}
    blocks = re.split(r"\n### ", body.strip())
    for block in blocks:
        block = block.lstrip("# ").strip()
        if not block:
            continue
        lines = block.split("\n", 1)
        label = lines[0].strip()
        value = lines[1].strip() if len(lines) > 1 else ""
        if value == "_No response_":
            value = ""
        fields[label] = value
    return fields


def replace_line(path, pattern, replacement):
    text = open(path, encoding="utf-8").read()
    new_text, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
    return count


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def lighten_for_dark_mode(hex_color, amount=0.45):
    r, g, b = hex_to_rgb(hex_color)
    r = round(r + (255 - r) * amount)
    g = round(g + (255 - g) * amount)
    b = round(b + (255 - b) * amount)
    return f"rgb({r} {g} {b})"


def main():
    fields = parse_issue_form(os.environ["ISSUE_BODY"])
    changed = []

    title = fields.get("사이트 제목", "")
    if title:
        n = replace_line("_config.yml", r"^title:.*$", f"title: {title}")
        if n:
            changed.append(f"제목 → {title}")

    tagline = fields.get("부제목 (태그라인)", "")
    if tagline:
        n = replace_line("_config.yml", r"^tagline:.*$", f"tagline: {tagline}")
        if n:
            changed.append(f"부제목 → {tagline}")

    avatar_url = fields.get("아바타 이미지 URL", "")
    if avatar_url:
        n = replace_line("_config.yml", r"^avatar:.*$", f"avatar: {avatar_url}")
        if n:
            changed.append(f"아바타 → {avatar_url}")

    accent_color = fields.get("강조 색상 (hex 코드)", "")
    if accent_color:
        if re.fullmatch(r"#[0-9a-fA-F]{6}", accent_color):
            n1 = replace_line(
                "_sass/themes/_light.scss",
                r"^(\s*--link-color:)\s*.*;",
                rf"\1 {accent_color};",
            )
            dark_value = lighten_for_dark_mode(accent_color)
            n2 = replace_line(
                "_sass/themes/_dark.scss",
                r"^(\s*--link-color:)\s*.*;",
                rf"\1 {dark_value};",
            )
            if n1 or n2:
                changed.append(f"강조 색상 → {accent_color} (다크 모드는 {dark_value})")
        else:
            changed.append(f"강조 색상 값 '{accent_color}'은 #rrggbb 형식이 아니라 건너뜀")

    github_output = os.environ["GITHUB_OUTPUT"]
    with open(github_output, "a", encoding="utf-8") as f:
        if changed:
            summary = "; ".join(changed)
        else:
            summary = "변경할 내용이 없습니다 (모든 항목이 비어 있음)"
        f.write(f"changed={summary}\n")
        f.write(f"has_changes={'true' if changed else 'false'}\n")


if __name__ == "__main__":
    main()
