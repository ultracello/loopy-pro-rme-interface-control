// Builds the project page from the documents of this repository. No dependencies.
// The page has little text of its own (site/text.mjs); status table, rules for a host, open points, the list of reports
// and all counts are read from ../docs at build time, so the page cannot fall behind the documents.
import { readFileSync, readdirSync, writeFileSync, mkdirSync, copyFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { TEXT } from './site/text.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..');
export const REPO = 'https://github.com/ultracello/loopy-pro-rme-interface-control';
export const SITE = 'https://ultracello.github.io/loopy-pro-rme-interface-control/';
const blob = (path) => `${REPO}/blob/main/${path}`;
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
export const MARKS = ['measured', 'reported', 'notes', 'unknown'];

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
// The little markdown the documents use inside a line: `code`, **bold**, [text](url). The four marks become labels.
export function inline(md) {
  return md.split(/(`[^`]*`)/).map((part) => {
    if (part.startsWith('`') && part.endsWith('`') && part.length > 1) return `<code>${esc(part.slice(1, -1))}</code>`;
    let s = esc(part);
    s = s.replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g, '<a href="$2">$1</a>');
    s = s.replace(/\*\*([^*]+)\*\*/g, (all, word) => (MARKS.includes(word) ? `<span class="mark ${word}">${word}</span>` : `<strong>${word}</strong>`));
    return s;
  }).join('');
}
function section(text, number) {
  const lines = text.split('\n');
  const start = lines.findIndex((l) => l.startsWith(`## ${number}. `));
  if (start < 0) throw new Error(`The reference has no section ${number}`);
  let end = lines.findIndex((l, i) => i > start && l.startsWith('## '));
  if (end < 0) end = lines.length;
  return { title: lines[start].replace(/^## \d+\. /, ''), lines: lines.slice(start + 1, end) };
}

export function collect(root = ROOT) {
  const referencePath = 'docs/protocol/BABYFACE-PRO-FS-CC-REFERENCE.md';
  const reference = readFileSync(join(root, referencePath), 'utf8');
  // coverage: the table of section 5
  const coverage = section(reference, 5).lines.filter((l) => l.startsWith('|')).slice(2).map((l) => {
    const cells = l.split('|').slice(1, -1).map((c) => c.trim());
    const mark = (cells[1].match(/\*\*(measured|reported|notes|unknown)\*\*/) || [])[1] || 'other';
    return { name: cells[0], status: cells[1], mark, page: cells[2] || '' };
  });
  // rules for a host: the numbered list of section 4, lead sentence and rest
  const rules = section(reference, 4).lines.filter((l) => /^\d+\. /.test(l)).map((l) => {
    const m = l.match(/^\d+\. \*\*(.+?)\*\*\s*(.*)$/);
    if (!m) throw new Error('A rule of section 4 has no lead in bold: ' + l.slice(0, 60));
    return { lead: m[1], rest: m[2] };
  });
  const open = section(reference, 6).lines.filter((l) => l.startsWith('- ')).map((l) => l.slice(2));
  const tested = (reference.match(/worked out on one unit \(([^)]+)\) between ([^.]+)\./) || []).slice(1);
  // reports: every file of docs/milestones, newest first
  const dir = join(root, 'docs/milestones');
  const reports = readdirSync(dir).filter((f) => f.endsWith('.md')).map((file) => {
    const text = readFileSync(join(dir, file), 'utf8');
    const title = (text.match(/^# (.+)$/m) || [])[1];
    if (!title) throw new Error('A report has no title: ' + file);
    const [y, mo, d] = file.slice(0, 10).split('-').map(Number);
    const time = (text.match(/^Completed [^\n]*?(\d{1,2}:\d{2})/m) || [])[1] || '00:00';
    return { file, title, date: file.slice(0, 10), day: `${d} ${MONTHS[mo - 1]} ${y}`, time: time.padStart(5, '0'), url: blob('docs/milestones/' + file) };
  }).sort((a, b) => (b.date + b.time + b.file).localeCompare(a.date + a.time + a.file));
  const vectors = JSON.parse(readFileSync(join(root, 'docs/protocol/reference/test-vectors.json'), 'utf8')).vectors;
  const curves = JSON.parse(readFileSync(join(root, 'docs/protocol/reference/eq-curves-measured.json'), 'utf8')).settings;
  const law = JSON.parse(readFileSync(join(root, 'docs/protocol/reference/output-level-law-measured.json'), 'utf8')).rows;
  // progress: of the functions that belong to the unit, how many are measured, and how many the controller page offers
  const unit = coverage.filter((r) => r.mark !== 'other');
  const share = (n) => Math.round((100 * n) / unit.length);
  const progress = { functions: unit.length, measured: unit.filter((r) => r.mark === 'measured').length, onPage: unit.filter((r) => r.page === 'yes').length };
  progress.measuredPercent = share(progress.measured); progress.onPagePercent = share(progress.onPage);
  for (const r of unit) if (!['yes', 'no'].includes(r.page)) throw new Error('The coverage table does not say yes or no for the controller page: ' + r.name);
  const counts = Object.fromEntries([...MARKS, 'other'].map((m) => [m, coverage.filter((r) => r.mark === m).length]));
  return { coverage, counts, progress, rules, open, tested, reports, vectors: vectors.length, vectorsMeasured: vectors.filter((v) => v.status === 'measured').length,
    levelValues: law.length, lawUrl: blob('docs/protocol/reference/output-level-law-measured.json'), curves: curves.length, curvePoints: curves.reduce((n, c) => n + c.points.length, 0), referenceUrl: blob(referencePath),
    codecUrl: blob('docs/protocol/reference/babyface_cc.py'), vectorsUrl: blob('docs/protocol/reference/test-vectors.json'), curvesUrl: blob('docs/protocol/reference/eq-curves-measured.json') };
}

export function render(c, t = TEXT) {
  const latest = c.reports[0];
  const days = [];
  for (const r of c.reports) { if (!days.length || days[days.length - 1].day !== r.day) days.push({ day: r.day, date: r.date, items: [] }); days[days.length - 1].items.push(r); }
  const p = (list) => list.map((x) => `<p>${inline(x)}</p>`).join('\n');
  const ul = (list) => `<ul>\n${list.map((x) => `<li>${inline(x)}</li>`).join('\n')}\n</ul>`;
  const summary = MARKS.filter((m) => c.counts[m]).map((m) => `${c.counts[m]} ${m}`).join(', ');
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(t.title)}</title>
<meta name="description" content="${esc(t.description)}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="canonical" href="${SITE}">
<meta property="og:type" content="website">
<meta property="og:url" content="${SITE}">
<meta property="og:title" content="${esc(t.title)}">
<meta property="og:description" content="${esc(t.description)}">
<meta property="og:image" content="${SITE}${t.share.file}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="${t.share.width}">
<meta property="og:image:height" content="${t.share.height}">
<meta property="og:image:alt" content="${esc(t.share.alt)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="./favicon.svg">
<link rel="stylesheet" href="./styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
<header class="top">
<div class="wrap">
<p class="project">${esc(t.project)}</p>
<nav aria-label="Sections"><a href="#progress">Progress</a><a href="#status">Status</a><a href="#page">Controller</a><a href="#questions">Questions</a><a href="#developers">For developers</a><a href="#open">Open points</a><a href="#reports">Reports</a><a href="${REPO}">GitHub</a></nav>
</div>
</header>
<main id="main" class="wrap">
<section class="intro">
<h1>${esc(t.heading)}</h1>
${p(t.intro)}
<p class="updated">Last report: <a href="${latest.url}">${esc(latest.title)}</a>, <time datetime="${latest.date}">${latest.day}</time>. This page is built from the documents in the repository.</p>
</section>

<section id="progress" aria-labelledby="h-progress">
<h2 id="h-progress">How far it is</h2>
${p(t.progress)}
<div class="meters">
<div class="meter"><p><strong>${c.progress.measuredPercent} %</strong> measured on the unit: ${c.progress.measured} of ${c.progress.functions} functions</p><div class="bar" role="img" aria-label="${c.progress.measuredPercent} percent"><span style="width:${c.progress.measuredPercent}%"></span></div></div>
<div class="meter"><p><strong>${c.progress.onPagePercent} %</strong> usable today from the controller page: ${c.progress.onPage} of ${c.progress.functions} functions</p><div class="bar" role="img" aria-label="${c.progress.onPagePercent} percent"><span style="width:${c.progress.onPagePercent}%"></span></div></div>
<div class="meter"><p><strong>${esc(t.nativePercent)}</strong> ${inline(t.native)}</p><div class="bar" role="img" aria-label="${esc(t.nativePercent)}"><span style="width:0%"></span></div></div>
</div>
${p(t.progressAfter)}
</section>

<section id="status" aria-labelledby="h-status">
<h2 id="h-status">What can be controlled</h2>
${p(t.status)}
<dl class="legend">
${t.marks.map(([m, text]) => `<div><dt><span class="mark ${m}">${m}</span></dt><dd>${inline(text)}</dd></div>`).join('\n')}
</dl>
<p class="count">${c.coverage.length} functions of TotalMix FX are listed: ${summary}${c.counts.other ? `, ${c.counts.other} that do not belong to the unit or cannot be read` : ''}.</p>
<table>
<thead><tr><th scope="col">Function</th><th scope="col">Status</th><th scope="col">On the controller page</th></tr></thead>
<tbody>
${c.coverage.map((r) => `<tr><th scope="row">${inline(r.name)}</th><td>${inline(r.status)}</td><td class="page">${esc(r.page)}</td></tr>`).join('\n')}
</tbody>
</table>
<p class="source">Source: <a href="${c.referenceUrl}">protocol reference</a>, section 5.</p>
</section>

<section id="page" aria-labelledby="h-page">
<h2 id="h-page">${esc(t.pageHeading)}</h2>
${p(t.page)}
${ul(t.pageList)}
<figure>
<img src="./${t.figure.file}" width="${t.figure.width}" height="${t.figure.height}" alt="${esc(t.figure.alt)}" loading="lazy">
<figcaption>${inline(t.figure.caption)}</figcaption>
</figure>
${p(t.pageAfter)}
</section>

<section id="questions" aria-labelledby="h-q">
<h2 id="h-q">Questions</h2>
<dl class="qa">
${t.questions.map(([q, a]) => `<div><dt>${inline(q)}</dt><dd>${inline(a)}</dd></div>`).join('\n')}
</dl>
</section>

<section id="developers" aria-labelledby="h-dev">
<h2 id="h-dev">For developers</h2>
${p(t.developers)}
<ul class="files">
<li><a href="${c.referenceUrl}">Protocol reference</a>: every message byte for byte, with the formulas for the dB values${c.tested.length ? `. Worked out on one unit (${esc(c.tested[0])}) between ${esc(c.tested[1])}` : ''}.</li>
<li><a href="${c.codecUrl}">Reference codec</a> in Python. It builds and parses bytes and sends nothing.</li>
<li><a href="${c.vectorsUrl}">${c.vectors} test vectors</a>, ${c.vectorsMeasured} of them with an effect that was measured at the unit.</li>
<li><a href="${c.curvesUrl}">${c.curves} measured equaliser curves</a> with ${c.curvePoints} points, next to the values the codec calculates.</li>
<li><a href="${c.lawUrl}">The measured level of an output</a> for each of its ${c.levelValues} raw values.</li>
</ul>
<h3>What a host has to build around</h3>
<ol class="rules">
${c.rules.map((r) => `<li><strong>${inline(r.lead)}</strong> ${inline(r.rest)}</li>`).join('\n')}
</ol>
<p class="source">Source: <a href="${c.referenceUrl}">protocol reference</a>, section 4.</p>
</section>

<section id="open" aria-labelledby="h-open">
<h2 id="h-open">Open points</h2>
${p(t.open)}
${ul(c.open)}
<p class="source">Source: <a href="${c.referenceUrl}">protocol reference</a>, section 6.</p>
</section>

<section id="reports" aria-labelledby="h-reports">
<h2 id="h-reports">Reports</h2>
${p(t.reports)}
${days.map((d) => `<h3><time datetime="${d.date}">${d.day}</time></h3>\n<ul class="reports">\n${d.items.map((r) => `<li><a href="${r.url}">${esc(r.title)}</a></li>`).join('\n')}\n</ul>`).join('\n')}
</section>
</main>
<footer>
<div class="wrap">
${p(t.footer)}
</div>
</footer>
</body>
</html>
`;
}

// A fingerprint of everything the page takes from the documents. It is kept in site/stamp.json; a test fails when it is not
// current. The stamp lies under website/, so a change of the documents always comes with a change that publishes the page.
export function stamp(c = collect()) {
  return { content: createHash('sha256').update(JSON.stringify(c)).digest('hex'), reports: c.reports.length, latest: c.reports[0].file };
}

// The same figures for the README of the repository, between two marker lines.
export function readmeBlock(c = collect()) {
  const bar = (percent) => '█'.repeat(Math.round(percent / 5)) + '░'.repeat(20 - Math.round(percent / 5));
  const latest = c.reports[0];
  return [
    '| | | |',
    '|---|---|---|',
    `| Measured on the unit | \`${bar(c.progress.measuredPercent)}\` | **${c.progress.measuredPercent} %**, ${c.progress.measured} of ${c.progress.functions} functions |`,
    `| Usable today from the controller page | \`${bar(c.progress.onPagePercent)}\` | **${c.progress.onPagePercent} %**, ${c.progress.onPage} of ${c.progress.functions} functions |`,
    `| Native support in Loopy Pro | \`${bar(0)}\` | not started |`,
    '',
    `Counted from the [coverage table](docs/protocol/BABYFACE-PRO-FS-CC-REFERENCE.md#5-coverage-against-what-totalmix-fx-offers) of the protocol reference. Last report: [${latest.title}](docs/milestones/${latest.file}), ${latest.day}.`,
  ].join('\n');
}
const START = '<!-- progress:start (written by website/build.mjs --stamp; do not edit by hand) -->', END = '<!-- progress:end -->';
export function readmeWith(text, block) {
  const a = text.indexOf(START), b = text.indexOf(END);
  if (a < 0 || b < a) throw new Error('The README has no progress markers');
  return text.slice(0, a + START.length) + '\n' + block + '\n' + text.slice(b);
}

export function build(out = join(HERE, 'dist')) {
  const html = render(collect());
  mkdirSync(out, { recursive: true });
  writeFileSync(join(out, 'index.html'), html);
  copyFileSync(join(HERE, 'site/styles.css'), join(out, 'styles.css'));
  for (const file of readdirSync(join(HERE, 'public'))) copyFileSync(join(HERE, 'public', file), join(out, file));
  return html;
}
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const html = build();
  console.log(`dist/index.html written, ${html.length} characters`);
  if (process.argv.includes('--stamp')) {
    writeFileSync(join(HERE, 'site/stamp.json'), JSON.stringify(stamp(), null, 1) + '\n'); console.log('site/stamp.json written');
    const readme = join(ROOT, 'README.md'); writeFileSync(readme, readmeWith(readFileSync(readme, 'utf8'), readmeBlock())); console.log('README.md: progress written');
  }
}
