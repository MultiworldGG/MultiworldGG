from rule_builder.rules import And, Rule


class ActThreeActive(Rule, game='Hollow Knight: Silksong'):
    class Resolved(Rule.Resolved):
        force_recalculate = True

        def _evaluate(self, state):
            return getattr(state.multiworld.worlds[self.player], '_silksong_act_three_active', False)

        def explain_json(self, state=None):
            color = 'green' if state is not None and self(state) else 'salmon'
            return [{'type': 'color', 'color': color, 'text': 'Currently in Act 3'}]


def install_act_gate(world):
    if (not getattr(world.multiworld, 'generation_is_fake', False)
            or getattr(world.multiworld, 'enforce_deferred_connections', 'default') == 'off'):
        return
    region = world.multiworld.get_region('Event: Act 3 Started', world.player)
    for entrance in region.entrances:
        if getattr(entrance, '_silksong_act_gate', False):
            continue
        entrance.access_rule = And.Resolved(
            (entrance.access_rule, ActThreeActive().resolve(world)),
            player=world.player, caching_enabled=False,
        )
        entrance._silksong_act_gate = True


def receive_act_state(world, value):
    if (not getattr(world.multiworld, 'generation_is_fake', False)
            or getattr(world.multiworld, 'enforce_deferred_connections', 'default') == 'off'):
        return
    world._silksong_act_three_active = value is True
    world.multiworld.state.stale[world.player] = True
