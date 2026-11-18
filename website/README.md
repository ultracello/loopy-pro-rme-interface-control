# Website

One static page, built from the documents of this repository. No dependencies, no client-side script.

- `build.mjs` reads `../docs` and writes `dist/index.html`: the status table, the rules for a host and the open points come from the protocol reference, the list of reports from `../docs/milestones`, the counts from the test vectors and the measured curves.
- `site/text.mjs` holds the few paragraphs that are not in the documents. `site/styles.css` is the stylesheet.
- `public/share-preview-babyface-pro-fs-loopy-pro.png` is the picture a social network shows next to a link to the page. It carries the title and the controller screenshot; `tools/share-image.swift` draws it (on a Mac: `swift tools/share-image.swift public/controller-interface-page.png public/share-preview-babyface-pro-fs-loopy-pro.png`).
- `tests/site.test.mjs` checks the page against the documents.

Run with Node.js 22 or later, from this directory:

```
npm test
npm run build
```

To change what the page says about the state of the work, change the documents, then run `npm run stamp` and commit `site/stamp.json` with them. The stamp is a fingerprint of everything the page takes from the documents; the tests fail when it is not current. The workflow in `.github/workflows/pages.yml` publishes `dist/` whenever something under `website/` changes, and the stamp is what makes a change of the documents such a change.
