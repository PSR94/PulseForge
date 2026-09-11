from pulseforge.services.entity_resolution import resolve_entity


def test_resolves_corporate_aliases():
    aliases = {"Microsoft": ["Microsoft Corp.", "Microsoft Corporation", "MSFT"]}
    result = resolve_entity("Microsoft Corporation", aliases)
    assert result is not None
    assert result.canonical_name == "Microsoft"
    assert result.confidence == 1.0


def test_does_not_force_weak_match():
    aliases = {"NVIDIA": ["NVDA"]}
    assert resolve_entity("National Video Archive", aliases) is None
