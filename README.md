# trajectorylabs.io

The Trajectory Labs, LLC website: the homepage and one page per app.

- `index.html`: homepage with the app cards
- `hamprep/`: the HamPrep page, with its support and privacy pages (the App Store listing links here)
- `revest/`, `dishdecoded/`, `mythic-rep/`, `grol/`, `prism/`: app pages built from the same template
- `shared/`: the shared app-page stylesheet and the official App Store badge
- `favicon.svg`, `apple-touch-icon.png`: the Trajectory Labs mark

## How it is served

trajectorylabs.io runs on a Cloudflare Worker that serves these files from a pinned commit of this repo. To publish a change, push it here, then move the worker's pinned commit to the new one. Rolling back means pointing the worker at an earlier commit.

HamPrep lives at trajectorylabs.io/hamprep/. The old address hamprep.trajectorylabs.io forwards there with a 301, handled by the same worker.
The old hamprep-site repo is archived and its GitHub Pages is off (Nov 18, 2026); nothing is served from it.

## After an app's App Store release

The page must match what Apple approved. Check it against App Store Connect, never from memory:
- prices (HamPrep: each license $4.99, All Licenses Bundle $9.99 since Nov 12, 2026);
- what the app covers (HamPrep 1.1.1: Technician, General and Extra, 1,431 questions, iPhone and iPad);
- the smart banner (`apple-itunes-app` meta on the app's main page only);
- support and privacy pages, which the App Store listing links to.

A page change publishes only when the worker's pinned commit moves to it (Ada does this, then checks it live). A commit
that changes only README.md or STATE.md needs no redeploy.
