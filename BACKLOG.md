# Backlog

Future tickets (become GitHub issues later).

## 🟢 Easy
| ID | Ticket |
|---|---|
| ~~J-1~~ | ~~Add `GET /health` returning `{"status": "ok"}` (for Docker/k8s health checks)~~ — done by hand (2026-11-21), first release through CD-0 |
| J-2 | Clean up tags: trim, lowercase, remove duplicates (`"App, app ,"` → `["app"]`) |
| J-3 | Add `updated_at`; show "edited …" on the idea page |
| J-4 | Show relative dates ("3 days ago") with the full date on hover |

## 🟡 Medium
| ID | Ticket |
|---|---|
| J-5 | Filter by tag: `/?tag=app`, tags on cards become links |
| J-6 | Status: `new` / `exploring` / `parked` / `done` (default `new`), shown as a badge |
| J-7 | Pagination on the home page (20 per page, next/previous links) |
| J-8 | Star ideas; starred ideas show first |
| J-9 | Duplicate an idea ("Make a copy") |

## 🟠 Harder
| ID | Ticket |
|---|---|
| J-10 | Votes: upvote an idea, sort by score |
| J-11 | Link related ideas ("see also") both ways |
| J-12 | Search title and details: search box on the home page (`/?q=…`) |
| J-13 | Export all ideas as a Markdown or JSON download |

## 🖥️ UI
| ID | Ticket |
|---|---|
| J-19 | Status filter tabs: All / New / Exploring / Parked / Done (needs J-6) |
| J-20 | Keyboard shortcut: `n` opens "New idea" |
| J-21 | Character counter and max length on the details field |
| J-22 | Playwright end-to-end test: add, edit and delete an idea in the browser |
| J-23 | Friendly 404 page instead of JSON |

## 🔴 Security / bug-fix (some will be planted on purpose)
| ID | Ticket |
|---|---|
| J-14 | Accounts: sign up / log in (sessions); users only see their own ideas |
| J-15 | Fix: a user can open another user's idea by changing the URL (planted after J-14) |
| J-16 | Fix: unsafe SQL in search (planted after J-12) |
| J-17 | Markdown in idea details, rendered without XSS |
| J-18 | Limit details size (e.g. 20 KB) and number of tags |
| J-24 | CSRF protection on all forms (needed once J-14 adds logins) |
