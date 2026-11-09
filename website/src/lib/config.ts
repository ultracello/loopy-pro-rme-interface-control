import { EVIDENCE, PUBLIC_REPOSITORY, RELEASE_GATES, LAB_STATUS } from './evidence.ts';
export const PROJECT_NAME = 'Loopy Pro Interface Control';
export const INDEPENDENCE_NOTICE = 'Independent software. Not affiliated with RME.';
export const PLAN_FILENAME = 'loopy-pro-interface-control-plan';
export const VERSION = '0.2.6';
export const RELEASE_DATE = '2026-11-09';
export const PLANNING_STEP_SIZES = [0.5,1,2,3,6] as const;
export const FEATURES = [
  { id: 'phones-fader', group: 'Headphones', name: 'Smooth level fader', description: 'A dedicated continuous volume control.', kind: 'fader' },
  { id: 'phones-steps', group: 'Headphones', name: 'Volume step buttons', description: 'A pair of level up / down buttons.', kind: 'steps' },
  { id: 'phones-mute', group: 'Headphones', name: 'Mute / unmute', description: 'One toggle, separate from the main output.', kind: 'mute' },
  { id: 'main-fader', group: 'Main output', name: 'Smooth level fader', description: 'A separate fader for your main speakers.', kind: 'fader' },
  { id: 'main-steps', group: 'Main output', name: 'Volume step buttons', description: 'Independent level changes for the main output.', kind: 'steps' },
  { id: 'main-mute', group: 'Main output', name: 'Mute / unmute', description: 'Mute the main output independently.', kind: 'mute' },
] as const;
export type FeatureId = typeof FEATURES[number]['id'];
export type Route = 'undecided' | 'standalone' | 'desktop' | 'ipad-app';
export type Config = { selected: FeatureId[]; route: Route; step: number; model: string; loopyVersion: string; totalmixVersion: string; };
export const DEFAULT_CONFIG: Config = { selected: ['phones-fader', 'phones-steps', 'phones-mute'], route: 'undecided', step: 2, model: '', loopyVersion: '', totalmixVersion: '' };
export const ROUTES: Record<Route, {title:string; status:string; detail:string}> = {
  undecided: { title: 'Choose a setup', status: 'Setup needed', detail: 'The control path depends on the hardware, host and software versions. Choose the setup you intend to use.' },
  standalone: { title: 'iPad → direct RME interface', status: 'Scoped lab evidence · no released profile', detail: 'Babyface research includes bounded Main/Phones fader writes with exact restoration, three correct startups and specific transport-stop/missing-return gates, alongside step-button and gain-mute tests. Auxiliary feedback, gain-mute lifecycle and physical USB reconnect/duration remain open. Full-range control and TotalMix-independent operation are not established. No installable profile is released.' },
  desktop: { title: 'iPad + Mac / PC host', status: 'Protocol documented · setup untested', detail: 'Desktop TotalMix FX documents MIDI remote control and OSC. The Loopy-to-host transport, exact channel map and feedback still need validation for your setup.' },
  'ipad-app': { title: 'TotalMix FX for iPad', status: 'App remote control not supported', detail: 'RME excludes MIDI / OSC and TCP/IP remote control from TotalMix FX for iPad. This app limitation does not rule out a separate, device-specific hardware path. Do not apply desktop remote instructions to this app.' },
};
export function normalizeConfig(input: Partial<Config>): Config {
  const routes = Object.keys(ROUTES);
  return { selected: [...new Set((input.selected ?? DEFAULT_CONFIG.selected).filter(id => FEATURES.some(f=>f.id===id)))], route: routes.includes(input.route ?? '') ? input.route! : 'undecided', step: (PLANNING_STEP_SIZES as readonly number[]).includes(Number(input.step)) ? Number(input.step) : 2, model: String(input.model ?? '').slice(0,100), loopyVersion: String(input.loopyVersion ?? '').slice(0,60), totalmixVersion: String(input.totalmixVersion ?? '').slice(0,60) };
}
export function adjustLevel(level:number, delta:number) { return Math.min(0,Math.max(-60, Math.round((level+delta)*10)/10)); }
export function buildPlan(config: Config) {
  const c = normalizeConfig(config);
  return { schemaVersion: '2', release: VERSION, publicationStatus: 'public-planning-release', evidenceReviewed: RELEASE_DATE, artifactType: 'control-plan', executable: false, hardwareTested: false, setup: { route: c.route, routeLabel: ROUTES[c.route].title, hardwareModel: c.model || 'Not specified', loopyVersion: c.loopyVersion || 'Not specified', totalmixVersion: c.totalmixVersion || 'Not specified' }, selectedControls: FEATURES.filter(f=>c.selected.includes(f.id)).map(f=>({id:f.id, output:f.group, control:f.name, ...(f.kind==='steps'?{requestedStepDb:c.step}:{}), verification:'not-hardware-verified'})), status: ROUTES[c.route].status, restrictions: ['Planning document only. Not a Loopy project, StreamByter script or MIDI/OSC command file.', 'No hardware control, routing changes or device connection.', 'Exact dB steps require a verified level curve and synchronized state.', 'Mute requires verified semantics and state feedback; local UI state is not hardware state.'], requiredValidation: [...RELEASE_GATES], evidence: EVIDENCE.map(e=>({title:e.title,type:e.type,url:e.url,finding:e.finding})), labEvidence: LAB_STATUS, projectRepository: {url:PUBLIC_REPOSITORY.url, reviewedCommit:PUBLIC_REPOSITORY.reviewedCommit, reviewedDate:PUBLIC_REPOSITORY.reviewedDate} };
}
export function buildGuide(config: Config) {
  const p = buildPlan(config);
  return `# ${PROJECT_NAME} control plan\n\nPlanning release ${VERSION} · ${RELEASE_DATE}\n\nPLANNING ONLY. No executable control code is included. This configurator does not test or control hardware. Scoped project-reported device observations are listed separately below.\n\n## Setup\n- Path: ${p.setup.routeLabel}\n- Interface: ${p.setup.hardwareModel}\n- Loopy Pro version: ${p.setup.loopyVersion}\n- TotalMix version: ${p.setup.totalmixVersion}\n- Compatibility: ${p.status}\n\n## Requested controls\n${p.selectedControls.map(f=>`- ${f.output}: ${f.control}${'requestedStepDb' in f ? ` (${f.requestedStepDb} dB requested)` : ''}`).join('\n') || '- None selected'}\n\n## Before a hardware test\n${p.requiredValidation.map((s,i)=>`${i+1}. ${s}`).join('\n')}\n\n## Restrictions\n${p.restrictions.map(s=>`- ${s}`).join('\n')}\n\n## Evidence and project status\n${p.evidence.map(e=>`- ${e.title} (${e.type}): ${e.url}\n  ${e.finding}`).join('\n')}\n\n## Scoped lab status\n${p.labEvidence.evidenceType}\n${p.labEvidence.entries.map(e=>`- ${e.revision} (${e.level}): ${e.result} ${e.boundary}\n  Report: ${e.sourceUrl}`).join('\n')}\n\nOpen: ${p.labEvidence.remaining.join('; ')}.\n\nRepository revision reviewed: ${p.projectRepository.reviewedCommit}. This is a dated snapshot, not a live test result.\n\nKeep the original Loopy project and TotalMix routing unchanged. Save a separate working copy before any later approved setup changes. This file does not instruct you to connect MIDI, alter a port, route audio or send a command.\n`;
}
