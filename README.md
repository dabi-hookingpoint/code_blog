# code_blog

공부한 내용을 정리하는 블로그. [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) 테마 fork + GitHub Pages(GitHub Actions 빌드)로 만들었습니다.

- 배포 주소: https://dabi-hookingpoint.github.io/code_blog/

## 글 쓰는 법

블로그 상단 **"글쓰기"** 탭의 링크를 누르면 이 저장소의 새 이슈(Issue) 작성 화면이 열립니다. 제목과 내용을 쓰고 **Submit new issue**를 누르면, GitHub Actions가 자동으로 `_posts/`에 글 파일을 만들어 커밋하고 이슈를 닫아줍니다. 1~2분 뒤 블로그에 반영됩니다. (`.github/workflows/publish-post-from-issue.yml`)

별도 토큰이나 로그인 절차 없이, 이미 로그인되어 있는 GitHub 계정으로 바로 쓸 수 있습니다.

직접 파일을 추가하고 싶다면 `_posts/` 폴더에 `YYYY-MM-DD-제목.md` 형식으로 파일을 추가하고, 아래 형식으로 작성 후 `master` 브랜치에 푸시하면 됩니다.

```markdown
---
layout: post
title: "제목"
date: 2026-07-24 09:00:00 +0900
categories: [카테고리]
---

내용...
```

## 로컬에서 미리보기 (선택)

```bash
bundle install
npm install && npm run build
bundle exec jekyll serve
```
