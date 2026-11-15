# trajectorylabs.io

The Trajectory Labs, LLC website: the homepage and one page per app.

- `index.html`: homepage with the app cards
- `hamprep/`: the HamPrep page, with its support and privacy pages (the App Store listing links here)
- `revest/`, `dishdecoded/`, `mythic-rep/`: app pages built from the same template
- `shared/`: the shared app-page stylesheet and the official App Store badge
- `favicon.svg`, `apple-touch-icon.png`: the Trajectory Labs mark

## How it is served

trajectorylabs.io runs on a Cloudflare Worker that serves these files from a pinned commit of this repo. To publish a change, push it here, then move the worker's pinned commit to the new one. Rolling back means pointing the worker at an earlier commit.

HamPrep lives at trajectorylabs.io/hamprep/. The old address hamprep.trajectorylabs.io forwards there with a 301, handled by the same worker.
