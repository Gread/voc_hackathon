

def test_theme_ids_do_not_depend_on_other_buckets():
    """A global counter made one bucket's ids shift when another bucket gained a theme, which
    invalidated cached batches and could re-point assignments already written against the old ids."""
    from voc.theme.registry import Registry

    first = Registry()
    a1 = first.add("unexpected_charge|negative", "A", "p", "c")["theme_id"]
    first.add("money_held_or_not_returned|negative", "B", "p", "c")
    a2 = first.add("unexpected_charge|negative", "C", "p", "c")["theme_id"]

    second = Registry()
    second.add("money_held_or_not_returned|negative", "B", "p", "c")
    second.add("money_held_or_not_returned|negative", "X", "p", "c")
    b1 = second.add("unexpected_charge|negative", "A", "p", "c")["theme_id"]
    b2 = second.add("unexpected_charge|negative", "C", "p", "c")["theme_id"]

    assert (a1, a2) == (b1, b2)
    assert a1 != a2


def test_a_buckets_registry_snapshot_is_stable_across_runs():
    """The batch cache key embeds the registry the model was shown, so that view must not move
    when an unrelated bucket changes."""
    from voc.theme.registry import Registry, prompt_view, registry_hash

    def snapshot(extra_buckets: int) -> str:
        reg = Registry()
        for i in range(extra_buckets):
            reg.add("no_response_or_follow_up|negative", f"other {i}", "p", "c")
        reg.add("unexpected_charge|negative", "A", "problem", "cause")
        reg.add("unexpected_charge|negative", "B", "problem", "cause")
        return registry_hash(prompt_view(reg.active("unexpected_charge|negative")))

    assert snapshot(0) == snapshot(7)
