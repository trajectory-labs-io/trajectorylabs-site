# trajectorylabs.io

The Trajectory Labs, LLC website: the homepage and one page per app.

- `index.html`: homepage with the app cards
- `revest/`, `dishdecoded/`, `mythic-rep/`: app pages built from the hamprep-site template (see `TEMPLATE.md` in trajectory-labs-io/hamprep-site)
- `shared/`: the shared app-page stylesheet and the official App Store badge
- `favicon.svg`, `apple-touch-icon.png`: the Trajectory Labs mark

## How it is served

trajectorylabs.io runs on a Cloudflare Worker that serves these files from a pinned commit of this repo. To publish a change, push it here, then move the worker's pinned commit to the new one. Rolling back means pointing the worker at an earlier commit.

HamPrep has its own site at hamprep.trajectorylabs.io (trajectory-labs-io/hamprep-site).
