import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {DEFAULT_CONFIG, PROJECT_NAME, INDEPENDENCE_NOTICE, PLAN_FILENAME, VERSION, FEATURES, normalizeConfig, adjustLevel, buildPlan, buildGuide} from '../src/lib/config.ts';
test('defaults select the headphone controls only',()=>assert.deepEqual(DEFAULT_CONFIG.selected,['phones-fader','phones-steps','phones-mute']));
test('all 64 selections generate only selected controls and never executable code',()=>{for(let mask=0;mask<64;mask++){const selected=FEATURES.filter((_,i)=>mask&(1<<i)).map(f=>f.id);const p=buildPlan({...DEFAULT_CONFIG,selected});assert.equal(p.selectedControls.length,selected.length);assert.equal(p.executable,false);assert.equal(p.hardwareTested,false);assert.deepEqual(p.selectedControls.map(c=>c.id),selected);}});
test('invalid saved configuration is normalized',()=>{const c=normalizeConfig({selected:['phones-mute','phones-mute','fake'] as never,route:'fake' as never,step:999});assert.deepEqual(c.selected,['phones-mute']);assert.equal(c.route,'undecided');assert.equal(c.step,2)});
test('requested steps stay in the bounded preview range',()=>{assert.equal(adjustLevel(-1,3),0);assert.equal(adjustLevel(-59,-3),-60);assert.equal(adjustLevel(-24,2),-22);assert.equal(adjustLevel(-24,.5),-23.5)});
test('unsupported iPad app path is explicit in all artifacts',()=>{const c={...DEFAULT_CONFIG,route:'ipad-app' as const};assert.equal(buildPlan(c).status,'App remote control not supported');assert.match(buildGuide(c),/App remote control not supported/)});
test('guide preserves supplied model and versions but warns about no executable code',()=>{const guide=buildGuide({...DEFAULT_CONFIG,model:'Example model',loopyVersion:'Example version'});assert.match(guide,/Example model/);assert.match(guide,/Example version/);assert.match(guide,/No executable control code/)});
test('step data is only present on step controls',()=>{const p=buildPlan({...DEFAULT_CONFIG,selected:FEATURES.map(f=>f.id),step:3});assert.equal(p.selectedControls.filter(f=>'requestedStepDb' in f).length,2)});

test('exports carry pinned public evidence and remain nonexecutable',()=>{const p=buildPlan(DEFAULT_CONFIG);assert.equal(p.publicationStatus,'public-planning-release');assert.match(p.projectRepository.url,/github.com\/ultracello\/loopy-pro-rme-interface-control$/);assert.match(p.projectRepository.reviewedCommit,/^[0-9a-f]{40}$/);assert.equal(p.evidence.length,4);assert.equal(p.executable,false);assert.ok(buildGuide(DEFAULT_CONFIG).includes(`Planning release ${VERSION}`))});
test('validation requires reading current state and separate outputs',()=>{const text=buildPlan(DEFAULT_CONFIG).requiredValidation.join(' ');assert.match(text,/current hardware state/);assert.match(text,/headphones and main output independently/);assert.match(text,/restart, reconnect/)});

test('lab evidence distinguishes scoped device checks from offline tests and release readiness',()=>{const p=buildPlan(DEFAULT_CONFIG);assert.equal(p.labEvidence.releaseReady,false);assert.equal(p.labEvidence.entries[1].level,'Offline tests only');assert.match(p.labEvidence.entries[0].result,/output 1 only/);assert.match(p.labEvidence.entries[0].boundary,/native TotalMix mute/);assert.match(buildGuide(DEFAULT_CONFIG),/34,304/);assert.equal(p.hardwareTested,false)});

test('project branding is consistent in the UI, title and planning downloads',()=>{
 assert.equal(PROJECT_NAME,'Loopy Pro Interface Control');
 assert.equal(PLAN_FILENAME,'loopy-pro-interface-control-plan');
 assert.ok(buildGuide(DEFAULT_CONFIG).startsWith(`# ${PROJECT_NAME} control plan`));
 assert.doesNotMatch(buildGuide(DEFAULT_CONFIG),/loopmix/i);
 const app=readFileSync(new URL('../src/App.tsx',import.meta.url),'utf8');
 const index=readFileSync(new URL('../index.html',import.meta.url),'utf8');
 const readme=readFileSync(new URL('../README.md',import.meta.url),'utf8');
 assert.ok(index.includes(`<title>${PROJECT_NAME} · Control Planner</title>`));
 assert.ok(readme.startsWith(`# ${PROJECT_NAME} planning website`));
 for(const marker of ['className="brand-name">{PROJECT_NAME}','className="tiny-brand">{PROJECT_NAME}','className="footer-brand">{PROJECT_NAME}']) assert.ok(app.includes(marker));
 // Preserve the original browser key so the naming correction does not erase saved plans.
 const withoutLegacyKey=app.replaceAll('loopmix-public-plan-v2','existing-plan-key');
 assert.doesNotMatch(withoutLegacyKey,/loopmix/i);
 assert.doesNotMatch(index+readme,/loopmix/i);
});

test('website and GitHub README clearly state software independence',()=>{
 assert.equal(INDEPENDENCE_NOTICE,'Independent software. Not affiliated with RME.');
 const app=readFileSync(new URL('../src/App.tsx',import.meta.url),'utf8');
 const readme=readFileSync(new URL('../../README.md',import.meta.url),'utf8');
 assert.ok(app.includes('className="independence-note">{INDEPENDENCE_NOTICE}'));
 assert.ok(app.includes('<p>{INDEPENDENCE_NOTICE}<br/>'));
 assert.ok(readme.includes(`**${INDEPENDENCE_NOTICE}**`));
 assert.ok(readme.startsWith(`# ${PROJECT_NAME}`));
});
