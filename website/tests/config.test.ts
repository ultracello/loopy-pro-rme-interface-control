import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {EVIDENCE, REPORTS, PUBLIC_REPOSITORY, LAB_STATUS, LATEST_MILESTONE, STEP_SIMULATION} from '../src/lib/evidence.ts';
import {DEFAULT_CONFIG, PROJECT_NAME, INDEPENDENCE_NOTICE, PLAN_FILENAME, PLANNING_STEP_SIZES, VERSION, FEATURES, normalizeConfig, adjustLevel, buildPlan, buildGuide} from '../src/lib/config.ts';
test('defaults select the headphone controls only',()=>assert.deepEqual(DEFAULT_CONFIG.selected,['phones-fader','phones-steps','phones-mute']));
test('all 64 selections generate only selected controls and never executable code',()=>{for(let mask=0;mask<64;mask++){const selected=FEATURES.filter((_,i)=>mask&(1<<i)).map(f=>f.id);const p=buildPlan({...DEFAULT_CONFIG,selected});assert.equal(p.selectedControls.length,selected.length);assert.equal(p.executable,false);assert.equal(p.hardwareTested,false);assert.deepEqual(p.selectedControls.map(c=>c.id),selected);}});
test('invalid saved configuration is normalized',()=>{const c=normalizeConfig({selected:['phones-mute','phones-mute','fake'] as never,route:'fake' as never,step:999});assert.deepEqual(c.selected,['phones-mute']);assert.equal(c.route,'undecided');assert.equal(c.step,2)});
test('requested steps stay in the bounded preview range',()=>{assert.equal(adjustLevel(-1,3),0);assert.equal(adjustLevel(-59,-3),-60);assert.equal(adjustLevel(-24,2),-22);assert.equal(adjustLevel(-24,.5),-23.5)});
test('unsupported iPad app path is explicit in all artifacts',()=>{const c={...DEFAULT_CONFIG,route:'ipad-app' as const};assert.equal(buildPlan(c).status,'App remote control not supported');assert.match(buildGuide(c),/App remote control not supported/)});
test('guide preserves supplied model and versions but warns about no executable code',()=>{const guide=buildGuide({...DEFAULT_CONFIG,model:'Example model',loopyVersion:'Example version'});assert.match(guide,/Example model/);assert.match(guide,/Example version/);assert.match(guide,/No executable control code/)});
test('step data is only present on step controls',()=>{const p=buildPlan({...DEFAULT_CONFIG,selected:FEATURES.map(f=>f.id),step:3});assert.equal(p.selectedControls.filter(f=>'requestedStepDb' in f).length,2)});

test('exports carry pinned public evidence and remain nonexecutable',()=>{const p=buildPlan(DEFAULT_CONFIG);assert.equal(p.publicationStatus,'public-planning-release');assert.match(p.projectRepository.url,/github.com\/ultracello\/loopy-pro-rme-interface-control$/);assert.match(p.projectRepository.reviewedCommit,/^[0-9a-f]{40}$/);assert.equal(p.evidence.length,9);assert.equal(p.executable,false);assert.ok(buildGuide(DEFAULT_CONFIG).includes(`Planning release ${VERSION}`))});
test('validation requires reading current state and separate outputs',()=>{const text=buildPlan(DEFAULT_CONFIG).requiredValidation.join(' ');assert.match(text,/current hardware state/);assert.match(text,/headphones and main output independently/);assert.match(text,/restart, reconnect/)});

test('historical evidence stays separate from current scoped checkpoints',()=>{const p=buildPlan(DEFAULT_CONFIG);assert.equal(p.labEvidence.releaseReady,false);const v06=LAB_STATUS.entries.find(e=>e.id==='earlier-v06')!;const v08=LAB_STATUS.entries.find(e=>e.id==='earlier-v08')!;assert.match(v06.result,/output 1 only/);assert.match(v06.boundary,/native TotalMix mute/);assert.match(v08.level,/Historical offline/);assert.match(buildGuide(DEFAULT_CONFIG),/34,304/);assert.equal(p.hardwareTested,false)});


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

test('new native write evidence is bounded and does not promote a release',()=>{
 assert.equal(LATEST_MILESTONE.id,'phones-fader-write');
 assert.match(LATEST_MILESTONE.result,/-10.5 → -11.0 → -10.5 dB/);
 assert.match(LATEST_MILESTONE.result,/Fresh full register readback/);
 assert.match(LATEST_MILESTONE.result,/Main stayed unchanged/);
 assert.match(LATEST_MILESTONE.boundary,/not a full-range fader pass/);
 assert.match(LATEST_MILESTONE.boundary,/No acoustic measurement or new complete outbound trace/);
 assert.equal(LAB_STATUS.releaseReady,false);
});
test('display query origin and fixed-button test remain distinct',()=>{
 const display=LAB_STATUS.entries.find(e=>e.id==='native-display')!;
 const step=LAB_STATUS.entries.find(e=>e.id==='phones-step')!;
 assert.match(display.boundary,/helper triggered the query, not the Loopy READ widget/);
 assert.match(display.boundary,/No gain writes/);
 assert.match(step.result,/Three separate Loopy READs/);
 assert.match(step.boundary,/separate experiments/);
 assert.notEqual(display.sourceUrl,step.sourceUrl);
});
test('all current milestone links are pinned and exported in both formats',()=>{
 assert.equal(PUBLIC_REPOSITORY.reviewedCommit,'6f4e1a50fb9ce24027b29c2068b2cf38c503a3e1');
 const json=JSON.stringify(buildPlan(DEFAULT_CONFIG));const guide=buildGuide(DEFAULT_CONFIG);
 for(const url of [REPORTS.faderWrite,REPORTS.display,REPORTS.step,REPORTS.mapping,REPORTS.stepSimulation]){
  assert.ok(url.includes(`/blob/${PUBLIC_REPOSITORY.reviewedCommit}/docs/`));
  assert.ok(json.includes(url));assert.ok(guide.includes(url));
 }
 for(const entry of LAB_STATUS.entries)assert.ok(guide.includes(entry.sourceUrl));
 assert.equal(new Set(EVIDENCE.map(e=>e.id)).size,EVIDENCE.length);
});
test('planning step choices never become validated native controls',()=>{
 for(const step of PLANNING_STEP_SIZES){
  const p=buildPlan({...DEFAULT_CONFIG,selected:FEATURES.map(f=>f.id),step});
  assert.equal(p.executable,false);assert.equal(p.hardwareTested,false);
  assert.ok(p.selectedControls.every(c=>c.verification==='not-hardware-verified'));
 }
 const remaining=LAB_STATUS.remaining.join(' ');
 for(const boundary of ['Full-range','Native selectable-step UI','mute','Stereo Main','reconnect','TotalMix-independent','iPhone'])assert.ok(remaining.includes(boundary));
 const app=readFileSync(new URL('../src/App.tsx',import.meta.url),'utf8');
 assert.ok(app.includes('Latest development checkpoint'));
 assert.ok(app.includes('Tested code export: not available yet'));
 assert.doesNotMatch(app,/Raw test artifacts are not bundled here and are not part of the pinned/);
});

test('step simulation keeps offline, compilation and native widget evidence separate',()=>{
 assert.deepEqual(STEP_SIMULATION.stepSizesDb,[0.5,1,2,3,6]);
 assert.equal(STEP_SIMULATION.offline.groups,6);
 assert.equal(STEP_SIMULATION.offline.cases,34102);
 assert.equal(STEP_SIMULATION.offline.additionalRegressions,1792);
 assert.equal(STEP_SIMULATION.offline.repeatedSameCaseSet,true);
 assert.equal(STEP_SIMULATION.offline.publiclyRerunnable,false);
 assert.equal(STEP_SIMULATION.backend.nativeCompilation,true);
 assert.equal(STEP_SIMULATION.backend.nativeRuntimeCommandsTested,false);
 assert.equal(STEP_SIMULATION.backend.senderConnected,false);
 assert.equal(STEP_SIMULATION.widgets.nativeCases,10);
 assert.equal(STEP_SIMULATION.widgets.widgetOnly,true);
});
test('native simulated startup and reload do not imply physical changes or device defaults',()=>{
 assert.equal(STEP_SIMULATION.widgets.inertStartup,true);
 assert.equal(STEP_SIMULATION.widgets.unknownDefaultNoop,true);
 assert.equal(STEP_SIMULATION.widgets.reloadPreservedStepDb,6);
 assert.equal(STEP_SIMULATION.newHardwareTest,false);
 assert.equal(STEP_SIMULATION.largerPhysicalStepsTested,false);
 assert.match(STEP_SIMULATION.boundary,/simulation reference, not a device factory default/);
 assert.equal(LATEST_MILESTONE.id,'phones-fader-write');
 assert.match(LATEST_MILESTONE.result,/-10.5 → -11.0 → -10.5 dB/);
});
test('five browser planning choices remain bounded and six-dB requests round-trip',()=>{
 assert.deepEqual(PLANNING_STEP_SIZES,[0.5,1,2,3,6]);
 for(const step of PLANNING_STEP_SIZES){
  const c=normalizeConfig({...DEFAULT_CONFIG,step});assert.equal(c.step,step);
  const p=buildPlan(c);assert.equal(p.executable,false);assert.equal(p.hardwareTested,false);
  assert.ok(buildGuide(c).includes(`(${step} dB requested)`));
  assert.equal(adjustLevel(-10.5,step),-10.5+step);
  assert.equal(adjustLevel(-10.5,-step),-10.5-step);
  assert.equal(adjustLevel(-59,-step),Math.max(-60,-59-step));
  assert.equal(adjustLevel(-1,step),Math.min(0,-1+step));
 }
 assert.equal(normalizeConfig({step:7}).step,2);
});
test('both exports include send-free boundaries and no simulated hardware promotion',()=>{
 const p=buildPlan({...DEFAULT_CONFIG,step:6});const guide=buildGuide({...DEFAULT_CONFIG,step:6});
 const sim=p.labEvidence.entries.find(e=>e.id==='step-simulation')!;
 assert.equal(sim.newHardwareTest,false);assert.equal(sim.backend.nativeRuntimeCommandsTested,false);
 for(const text of ['34,102','1,792','Ten Loopy-only','not executed at native runtime','not a device factory default'])assert.ok(guide.includes(text),text);
 assert.ok(guide.includes(REPORTS.stepSimulation));
 const app=readFileSync(new URL('../src/App.tsx',import.meta.url),'utf8');
 assert.ok(app.includes('NEW CHECKPOINT · SIMULATION ONLY'));
 assert.ok(app.includes('No MIDI sender or larger physical step was tested'));
 assert.ok(app.includes('Planning values only. Native selector simulation does not validate hardware steps.'));
 assert.ok(app.includes('PLANNING_STEP_SIZES.map'));
});
