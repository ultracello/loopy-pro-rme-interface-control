// The page has to say what the documents say. Run: npm test
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { collect, render, inline, stamp, REPO, MARKS } from '../build.mjs';
import { TEXT } from '../site/text.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const c = collect();
const html = render(c);
const reference = readFileSync(join(ROOT, 'docs/protocol/BABYFACE-PRO-FS-CC-REFERENCE.md'), 'utf8');
const between = (from, to) => reference.slice(reference.indexOf(from), reference.indexOf(to));

test('every report of docs/milestones is listed once, newest first', () => {
  const files = readdirSync(join(ROOT, 'docs/milestones')).filter((f) => f.endsWith('.md'));
  assert.deepEqual(c.reports.map((r) => r.file).sort(), files.sort());
  for (const r of c.reports) assert.equal(html.split(r.url).length - 1, r === c.reports[0] ? 2 : 1, r.file);
  const keys = c.reports.map((r) => r.date + r.time);
  assert.deepEqual(keys, [...keys].sort().reverse());
  assert.equal(c.reports[0].date, files.map((f) => f.slice(0, 10)).sort().pop());
});

test('the status table is the table of section 5 of the reference, row for row', () => {
  const rows = between('## 5. ', '## 6. ').split('\n').filter((l) => l.startsWith('|')).slice(2);
  assert.equal(c.coverage.length, rows.length);
  assert.ok(rows.length >= 15);
  c.coverage.forEach((r, i) => { assert.ok(rows[i].includes(r.name)); assert.ok(html.includes(`<th scope="row">${inline(r.name)}</th>`)); });
  assert.equal(Object.values(c.counts).reduce((a, b) => a + b, 0), rows.length);
  for (const m of MARKS) assert.equal(c.counts[m], rows.filter((l) => (l.split('|')[2].match(/\*\*(measured|reported|notes|unknown)\*\*/) || [])[1] === m).length, m);
});

test('rules and open points come from sections 4 and 6', () => {
  assert.equal(c.rules.length, between('## 4. ', '## 5. ').split('\n').filter((l) => /^\d+\. /.test(l)).length);
  assert.ok(c.rules.length >= 5);
  const open = between('## 6. ', '## 7. ').split('\n').filter((l) => l.startsWith('- '));
  assert.equal(c.open.length, open.length);
  for (const o of c.open) assert.ok(html.includes(inline(o)));
});

test('counts are counted, not typed', () => {
  const vectors = JSON.parse(readFileSync(join(ROOT, 'docs/protocol/reference/test-vectors.json'), 'utf8')).vectors;
  const curves = JSON.parse(readFileSync(join(ROOT, 'docs/protocol/reference/eq-curves-measured.json'), 'utf8')).settings;
  assert.equal(c.vectors, vectors.length);
  assert.equal(c.curves, curves.length);
  assert.ok(html.includes(`${vectors.length} test vectors`) && html.includes(`${curves.length} measured equaliser curves`));
  // the text of the page itself carries no number of vectors, curves or reports
  assert.doesNotMatch(JSON.stringify(TEXT), /\d+ (test )?vectors|\d+ (measured )?curves|\d+ reports/);
});

test('links lead somewhere', () => {
  const ids = new Set([...html.matchAll(/ id="([^"]+)"/g)].map((m) => m[1]));
  for (const m of html.matchAll(/href="#([^"]+)"/g)) assert.ok(ids.has(m[1]), '#' + m[1]);
  for (const m of html.matchAll(/href="([^"#][^"]*)"/g)) {
    const url = m[1];
    if (url.startsWith('./')) continue;
    assert.ok(url.startsWith('https://'), url);
    if (url.startsWith(REPO + '/blob/main/')) assert.ok(existsSync(join(ROOT, url.slice((REPO + '/blob/main/').length))), url);
  }
});

test('the picture is there and described', () => {
  const m = html.match(/<img src="\.\/([^"]+)" width="(\d+)" height="(\d+)" alt="([^"]+)"/);
  assert.ok(m && m[4].length > 40);
  const file = readFileSync(join(ROOT, 'website/public', m[1]));
  assert.equal(file.readUInt32BE(16), Number(m[2]));   // PNG: width and height stand in the header
  assert.equal(file.readUInt32BE(20), Number(m[3]));
  assert.ok(file.length < 600000);
  assert.ok(html.includes('<figcaption>'));
});

test('the page is one plain document', () => {
  assert.equal(html.split('<h1').length - 1, 1);
  assert.ok(html.startsWith('<!doctype html>\n<html lang="en">'));
  assert.doesNotMatch(html, /<script|undefined|NaN|\[object|TODO|Lorem/);
  for (const tag of ['section', 'table', 'ul', 'ol', 'dl', 'nav', 'main', 'header', 'footer']) assert.equal(html.split('<' + tag).length, html.split('</' + tag + '>').length, tag);
  assert.ok(html.length < 40000);
});

test('inline markdown: code, bold, marks, links, and nothing else gets through', () => {
  assert.equal(inline('a `b<c` **d** **measured** [e](https://x.y/z) <f>'), 'a <code>b&lt;c</code> <strong>d</strong> <span class="mark measured">measured</span> <a href="https://x.y/z">e</a> &lt;f&gt;');
});

test('the stamp is current: the documents did not change without the page', () => {
  const kept = JSON.parse(readFileSync(join(ROOT, 'website/site/stamp.json'), 'utf8'));
  assert.deepEqual(kept, stamp(c), 'The documents changed. Run "npm run stamp" in website/ and commit site/stamp.json with them.');
});
