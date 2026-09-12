# ADR 0003 — Evidence-first AI boundary

**Status:** Accepted

LLMs may extract or explain structured information. They do not decide whether an alert threshold fired,
whether two stored values conflict, or whether an event has the required source corroboration. Those
decisions are deterministic functions over stored state.
