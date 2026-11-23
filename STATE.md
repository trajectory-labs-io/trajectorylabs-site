# STATE: trajectorylabs.io

Stage: live (company site; not an app, no pipeline stage)   Updated: 2026-11-20 by Claude Code (TL Ops)

## Where things stand
- Live: Cloudflare Worker old-darkness-5aae serves this repo from a pinned commit (see README). Pinned to main 2b7971b since Nov 15, 2026; every file served is identical to later main (d680903 and on change only STATE.md and README.md), checked Nov 18, 2026.
- Apps live on the App Store: Revest Analyzer, MythicRep, HamPrep (1.1.1, live Nov 17, 2026; All Licenses Bundle $9.99, its "All licenses" description approved by Apple Nov 18). DishDecoded: coming soon (launch goal Dec 1, 2026).
- Done Nov 18, 2026: hamprep-site GitHub Pages disabled and the repo archived; hamprep.trajectorylabs.io is answered by the worker only. Open: trajectorylabs.io/dishdecoded/ screenshot still shows a July date.

## Site design standards (all Trajectory Labs sites)
- Cards: an icon sits on the same row as the card title, to its left, at every screen width, with body text below; never an icon on a row by itself (Wes, Nov 15, 2026). Numbered step markers (accent line, "01", then the title) stay above the title on purpose; Wes kept that look.
- Follow each visitor's light or dark theme; no forced dark mode.
- Honest copy: no invented numbers, no overclaims, no price or trial we haven't confirmed, no fake store links.
- No em dashes in site copy.
- Publishing anything live needs Wes's yes; previews first.

## Log
- Nov 20, 2026 (TL Ops): local clone moved from ~/projects/trajectorylabs-site to ~/src/trajectorylabs-site (one folder per repo under ~/src). A symlink at the old path stays until about Nov 27. Nothing served changed.
- 2026-11-23: Revest page rebuilt on Revest's own design system to match the 1.3 redesign (revest.css copied from revest-analyzer-web/marketing/style.css; screens from its screenshots). Icons renamed with -v13 so browser caches pick them up. Preview first; production pin waits on Wes.
