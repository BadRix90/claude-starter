export const meta = {
  name: 'council',
  description: 'Entscheidung ohne Rueckfrage: zwei unabhaengige Berater, ein Vorsitz (3 Agenten), eine begruendete Festlegung',
  whenToUse: 'Von /auftrag und slice, wenn eine fachliche Festlegung fehlt oder ein Slice festhaengt. args: {question, context}',
  phases: [
    { title: 'Berater', detail: 'Contrarian und Executor parallel und blind zueinander' },
    { title: 'Vorsitz', detail: 'eine Festlegung mit Begruendung' },
  ],
}

const { question, context } = args || {}
if (!question) throw new Error('args {question, context} fehlen')

const ADVICE = { type: 'object', required: ['answer', 'reason', 'risk'], properties: {
  answer: { type: 'string' }, reason: { type: 'string' }, risk: { type: 'string' } } }
const DECISION = { type: 'object', required: ['decision', 'reason', 'security', 'dissent'], properties: {
  decision: { type: 'string', description: 'konkrete Festlegung, umsetzbar ohne weitere Rueckfrage' },
  reason: { type: 'string' },
  security: { type: 'boolean', description: 'true nur, wenn die Festlegung eine security-sensitive Mutation verlangt (Passwoerter, Keys, Rollen, Mandanten, .env, finalisierte Datensaetze)' },
  dissent: { type: 'string' } } }

const LENSES = [
  ['Contrarian', 'Suche, was an der naheliegenden Loesung scheitert. Welche Invariante, welcher zweite Pfad, welcher Bestandsdatensatz bricht?'],
  ['Executor', 'Welche Loesung ist im Scope am kleinsten, an der Wurzel und sofort testbar?'],
]
const base = `Frage: ${question}\nKontext: ${context || '-'}\nCode und Laufzeit sind die Wahrheit; nachsehen statt raten (graphify query aus dem Repo-Root zuerst). Hoechstens 8 Werkzeugaufrufe. Du aenderst nichts.`

phase('Berater')
const advice = (await parallel(LENSES.map(([name, lens]) => () =>
  agent(`${base}\nDeine Sicht: ${name}. ${lens}`, { agentType: 'general-purpose', phase: 'Berater', label: name, schema: ADVICE, effort: 'medium' })
))).filter(Boolean)
if (!advice.length) return { decision: '', reason: 'Kein Berater lieferte ein Ergebnis', security: false, dissent: '', failed: true }

phase('Vorsitz')
const opinions = advice.map((a, i) => `Berater ${i + 1}: ${a.answer}\nGrund: ${a.reason}\nRisiko: ${a.risk}`).join('\n\n')
const d = await agent(`${base}\nZwei unabhaengige Berater (anonym):\n${opinions}\n\nTriff EINE Festlegung. Keine Rueckfrage, keine Optionenliste. Bei Gleichstand gilt die kleinere Loesung an der Wurzel.`,
  { agentType: 'general-purpose', phase: 'Vorsitz', label: 'Vorsitz', schema: DECISION, effort: 'medium' })
return d || { decision: advice[0].answer, reason: `Vorsitz ausgefallen, Berater 1 uebernommen: ${advice[0].reason}`, security: false, dissent: '' }
