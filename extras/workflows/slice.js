export const meta = {
  name: 'slice',
  description: 'Code-Slice: Entwickler (Tests + Code + Commit) -> QA (Review + Abnahme) -> hoechstens eine Korrektur. Maximal 4 Agenten, 5 bei sensiblen Pfaden.',
  whenToUse: 'Vom Skill /auftrag fuer Code-Slices. args: {slice_id, card, profile, findings?}',
  phases: [
    { title: 'Entwickeln', detail: 'implementer: rote Tests, Code, gruen, lokaler Commit' },
    { title: 'QA', detail: 'qa: Review + Abnahme gegen die Karte; security-auditor nur bei sensiblen Pfaden' },
  ],
}

// Kleines Team, harte Leitplanken: 2 Iterationen, dann eskalieren.
const MAX_ITERATIONS = 2
const SENSITIVE = /(auth|permission|api_?key|token|secret|tenant|billing|payment|iban|encrypt|\.env|finaliz|archive)/i

const { slice_id, card, profile } = args || {}
if (!slice_id || !card || !profile) throw new Error('args {slice_id, card, profile} fehlen')
const CTX = `Slice ${slice_id}. Eingefrorene Karte: ${card}. Projektprofil: ${profile}.`

const DEV = { type: 'object', required: ['green', 'sha', 'files', 'test_files', 'test_output'], properties: {
  green: { type: 'boolean', description: 'alle eigenen Tests + lint + imports gruen' },
  sha: { type: 'string', description: 'Commit-SHA, leer wenn nicht committet' },
  files: { type: 'array', items: { type: 'string' } },
  test_files: { type: 'array', items: { type: 'string' } },
  red_before: { type: 'string', description: 'Beleg, dass die neuen Tests vor dem Fix rot waren' },
  test_output: { type: 'string', description: 'Zusammenfassung der Testlaeufe, hoechstens 20 Zeilen' },
  notes: { type: 'string' } } }
const QA = { type: 'object', required: ['accepted', 'points', 'findings'], properties: {
  accepted: { type: 'boolean' },
  points: { type: 'array', items: { type: 'object', required: ['point', 'status', 'evidence'], properties: {
    point: { type: 'string' }, status: { type: 'string', enum: ['ERFUELLT', 'PARTIAL', 'OFFEN'] }, evidence: { type: 'string' } } } },
  findings: { type: 'array', items: { type: 'object', required: ['where', 'issue', 'fix'], properties: {
    where: { type: 'string' }, issue: { type: 'string' }, fix: { type: 'string', description: 'konkrete Korrekturanweisung: Fehler X in Datei:Zeile, so beheben' } } } } } }
const SEC = { type: 'object', required: ['findings'], properties: { findings: { type: 'array', items: {
  type: 'object', required: ['where', 'issue', 'fix'], properties: { where: { type: 'string' }, issue: { type: 'string' }, fix: { type: 'string' } } } } } }

let agents = 0
async function run(prompt, opts) {
  agents++
  return agent(prompt, opts)
}
function stop(status, reason, extra) {
  log(`${slice_id}: ${status} - ${reason} (${agents} Agenten)`)
  return { slice_id, status, reason, agents, ...extra }
}

try {
  const commits = []
  let feedback = args.findings ? JSON.stringify(args.findings) : ''
  let last = null
  for (let i = 1; i <= MAX_ITERATIONS; i++) {
    phase('Entwickeln')
    const dev = await run(`${CTX}\nIteration ${i}/${MAX_ITERATIONS}. ${feedback ? `QA hat zurueckgewiesen. Behebe genau das:\n${feedback}` : 'Setze die Karte um: erst rote Tests, dann Code bis gruen, dann lokal committen.'}`,
      { agentType: 'implementer', phase: 'Entwickeln', label: `implementer #${i}`, schema: DEV })
    if (!dev) return stop('BLOCKED', 'implementer lieferte kein Ergebnis', { commits })
    if (dev.sha) commits.push(dev.sha)
    if (!dev.green || !dev.sha) return stop('BLOCKED', `nicht gruen oder nicht committet: ${dev.notes || dev.test_output}`, { commits, dev })

    phase('QA')
    const sensitive = dev.files.some(f => SENSITIVE.test(f))
    const [qa, sec] = await parallel([
      () => run(`Karte: ${card}\nCommit: ${dev.sha}\nTestausgabe des Entwicklers:\n${dev.test_output}\nRot vorher: ${dev.red_before || '-'}`,
        { agentType: 'qa', phase: 'QA', label: `qa #${i}`, schema: QA }),
      () => sensitive ? run(`${CTX}\nCommit: ${dev.sha}. Security-Audit.`, { agentType: 'security-auditor', phase: 'QA', label: `security #${i}`, schema: SEC }) : Promise.resolve({ findings: [] }),
    ])
    if (!qa) return stop('BLOCKED', 'qa lieferte kein Ergebnis', { commits })
    const findings = qa.findings.concat(sec ? sec.findings : [])
    last = { qa, sec, dev }
    if (qa.accepted && findings.length === 0) return { slice_id, status: 'VERIFIED', commits, qa, test_output: dev.test_output, agents }
    feedback = JSON.stringify({ findings, offene_punkte: qa.points.filter(p => p.status !== 'ERFUELLT') })
  }
  return stop('PARTIAL', `nach ${MAX_ITERATIONS} Iterationen nicht abgenommen - eskalieren`, { commits, review: last, feedback })
} catch (e) {
  return stop('BLOCKED', `Abbruch: ${e && e.message ? e.message : e}`, {})
}
