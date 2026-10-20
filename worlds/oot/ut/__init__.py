from .entrances import serialize_entrances


def apply_replay_options(world, slot_data: dict) -> None:
    slot_options = slot_data["options"]
    for option_name, option_type in world.options_dataclass.type_hints.items():
        if option_name in world.ut_omitted_slot_options:
            continue
        setattr(world.options, option_name, option_type.from_any(slot_options[option_name]))

    generation_results = slot_data["generation_results"]
    for option_name, randomized in generation_results["option_randomized"].items():
        getattr(world.options, option_name).randomized = bool(randomized)


def serialize_slot_options(world):
    return world.options.as_dict(*(
        option_name
        for option_name in world.options_dataclass.type_hints
        if option_name not in world.ut_omitted_slot_options
    ))


def serialize_generation_results(world):
    # New options are included automatically by serialize_slot_options(). Add an
    # entry here when generation produces state UT needs that cannot be rebuilt
    # deterministically from those options and received items (e.g. selected MQ
    # dungeons, rolled prices, or entrance connections). Also restore that state
    # from ut_replay_results before its usual generation step would reroll it.
    return {
        'entrances': serialize_entrances(world),
        'connect_name': world.connect_name,
        'file_hash': list(world.file_hash),
        'skipped_trials': dict(world.skipped_trials),
        'dungeon_mq': dict(world.dungeon_mq),
        'precompleted_dungeons': dict(world.precompleted_dungeons),
        'empty_dungeon_reward_assignments': dict(world.empty_dungeon_reward_assignments),
        'empty_dungeon_starting_rewards': list(getattr(world, 'empty_dungeon_starting_rewards', [])),
        'dungeon_shortcuts': sorted(world.dungeon_shortcuts),
        'key_rings': sorted(world.key_rings),
        'silver_rupee_pouches': sorted(world.silver_rupee_pouches),
        'selected_adult_trade_item': world.selected_adult_trade_item,
        'shop_prices': dict(world.shop_prices),
        'scrub_prices': dict(world.scrub_prices),
        'randomized_starting_items': dict(world.randomized_starting_items),
        'song_notes': {name: str(notes) for name, notes in world.song_notes.items()},
        'rauru_starting_item': getattr(world, 'rauru_starting_item', None),
        'rauru_free_post_fill': getattr(world, 'rauru_free_post_fill', False),
        'option_randomized': {
            'trials': world.trials_random,
            'mq_dungeons_count': world.mq_dungeons_random,
            'empty_dungeons_count': world.options.empty_dungeons_count.randomized,
            'special_deal_price_min': world.options.special_deal_price_min.randomized,
            'special_deal_price_max': world.options.special_deal_price_max.randomized,
        },
    }
