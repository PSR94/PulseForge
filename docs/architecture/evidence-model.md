# Evidence model

Every extracted claim points to one or more `EvidenceRef` records. Evidence stores the source id, document id, excerpt, publication time, retrieval time, and canonical URL. Claims carry extraction confidence but are not truth values.

Contradictions are first-class objects linking incompatible claims about a normalized `(subject, property)` pair. Resolution is explicit and may remain unresolved.

Analyst responses return `citations` that refer to claim, event, signal, or evidence identifiers. The UI can traverse those identifiers back to original source metadata.
