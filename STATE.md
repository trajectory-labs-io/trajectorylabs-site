# STATE: trajectorylabs.io

Stage: live (company site; not an app, no pipeline stage)   Updated: 2026-11-25 by Claude (Play badges)

## Where things stand
- Nov 25, 2026: worker pin moved e7307e8 -> **63cb603** (Wes approved): Google Play badges for Revest Analyzer and MythicRep on the homepage cards and both app pages (shared/google-play-badge.png, Google's official badge), Android in their copy, Google trademark line in their footers. Prod worker version 39ed69a4. Rollback: set PIN back to e7307e8849827e0961691b17dc830a8a287d4dd1 (version d61f8188). Checked live: homepage cards, /revest/, /mythic-rep/, hamprep subdomain redirect.
- Nov 24, 2026: worker pin moved 004f29f -> **e7307e8** (Wes approved): new DishDecoded icon and current app screens (Ada's branch claude/project-thread-cpf5np, fast-forwarded into main). Rollback: set PIN back to 004f29fd28e9f3adfebca807f286132aae1c12e4. Only the PIN constant in worker.js changed; assets binding kept. Checked live: pages 200, all referenced images 200, hamprep 301 intact. The July-date screenshot item below is resolved by this.
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
- 2026-11-23: Revest page keeps the TL layout. Images that change content get a new file name (for example app-icon-v13.webp), because images cache in browsers for 24 hours. Jonathon-style rebuild parked on branch claude/revest-redesign, not used.
- 2026-11-24: DishDecoded page and homepage card carry the new icon (fork that forms a D, mint-to-coral ring) on branch claude/project-thread-cpf5np. Icon files renamed with -v2 so cached copies refresh. Not live: goes live with the DishDecoded 1.1 App Store release when the worker pin moves, on Wes's yes.
