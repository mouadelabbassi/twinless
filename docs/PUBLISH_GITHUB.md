# Publish TWINLESS to a new public GitHub repository

This is a participant action. We cannot provision new GitHub repositories via
the current connected GitHub action set. Do not publish any private tokens.

## Step 1 — Create the repository

Go to `https://github.com/new` and create a repo with:

- Owner: your connected GitHub account (`mouadelabbassi`)
- Repository name: `twinless` (or `twinless-meta-hackathon-2026` if occupied)
- Visibility: **Public**
- **Do not** select "Add a README", ".gitignore" or "License" because the
  local initial scaffold already contains documentation and ignores.

## Step 2 — Publish from the extracted project folder

```bash
# Linux / WSL terminal in the extracted twinless_day1 directory
# Set git user.name and user.email in Git first if not yet configured.

git init -b main
git status
git add .
git diff --cached --stat
# IMPORTANT: review staged files; never add .env / API tokens.
git commit -m "feat: bootstrap TWINLESS scientific kernel during Meta hackathon"
git remote add origin https://github.com/mouadelabbassi/twinless.git
git push -u origin main
```

If the GitHub repository had to be named differently, replace `twinless.git`
with that exact name. GitHub may require browser credential login / credential
manager. Do not share credentials with anyone or paste into chat.

## Step 3 — Independently verify

Open `https://github.com/mouadelabbassi/twinless` in a **logged-out** or
incognito browser. Make sure `README.md`, `src/`, `tests/`, `docs/` and the
`.github/workflows/tests.yml` GitHub Actions workflow are visible. Inspect
Actions > Tests to verify that CI passes after pushing.

Save the URL for the submission. Keep committing small, honest increments.

## Helpful pre-push checks

```bash
git status --short
git ls-files | grep -Ei '\\.(env|key|pem)$' || true
```

GitHub's native secret scanning and push protection are useful but NOT a
substitute for checking your own repository before every public push.
