from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState, MultiWorld
from worlds.AutoWorld import LogicMixin
from .Names.DLC import ExpansionNames, GamePackNames, StuffNames
from ..generic.Rules import set_rule

from .Names import EventNames, SkillNames, CareerNames, AspirationNames
from .Options import AspirationGoal, Sims4Options

if TYPE_CHECKING:
    from . import Sims4World


class Sims4Logic(LogicMixin):
    def _sims4_rule(self, player: int):
        return True

def set_rules(world: MultiWorld, player: int, options: Sims4Options):
    # TODO: Part Time Jobs?
    set_career_rules(world, player, options)
    set_aspiration_rules(world, player, options)
    set_skill_rules(world, player, options)
    set_completion_condition(world, player, options)

# TODO: use events for the completion condition in order to facilitate easier goal stuff, and presence in spoiler (also permits future goals to be more dynamic)
def set_completion_condition(world: MultiWorld, player: int, options: Sims4Options):
    goal = options.goal
    goal_value = goal.value

    if goal_value == goal.option_bodybuilder:
        world.completion_condition[player] = lambda state: state.has(EventNames.bodybuilder_item, player)
    elif goal_value == goal.option_painter_extraordinaire:
        world.completion_condition[player] = lambda state: state.has(EventNames.painter_extraordinaire_item, player)
    elif goal_value == goal.option_bestselling_author:
        world.completion_condition[player] = lambda state: state.has(EventNames.bestselling_author_item, player)
    elif goal_value == goal.option_musical_genius:
        world.completion_condition[player] = lambda state: state.has(EventNames.musical_genius_item, player)
    elif goal_value == goal.option_public_enemy:
        world.completion_condition[player] = lambda state: state.has(EventNames.public_enemy_item, player)
    elif goal_value == goal.option_chief_of_mischief:
        world.completion_condition[player] = lambda state: state.has(EventNames.chief_of_mischief_item, player)
    elif goal_value == goal.option_master_chef:
        world.completion_condition[player] = lambda state: state.has(EventNames.master_chef_item, player)
    elif goal_value == goal.option_master_mixologist:
        world.completion_condition[player] = lambda state: state.has(EventNames.master_mixologist_item, player)
    elif goal_value == goal.option_renaissance_sim:
        world.completion_condition[player] = lambda state: state.has(EventNames.renaissance_sim_item, player)
    elif goal_value == goal.option_nerd_brain:
        world.completion_condition[player] = lambda state: state.has(EventNames.nerd_brain_item, player)
    elif goal_value == goal.option_computer_whiz:
        world.completion_condition[player] = lambda state: state.has(EventNames.computer_whiz_item, player)
    elif goal_value == goal.option_serial_romantic:
        world.completion_condition[player] = lambda state: state.has(EventNames.serial_romantic_item, player)
    elif goal_value == goal.option_freelance_botanist:
        world.completion_condition[player] = lambda state: state.has(EventNames.freelance_botanist_item, player)
    elif goal_value == goal.option_the_curator:
        world.completion_condition[player] = lambda state: state.has(EventNames.the_curator_item, player)
    elif goal_value == goal.option_angling_ace:
        world.completion_condition[player] = lambda state: state.has(EventNames.angling_ace_item, player)
    elif goal_value == goal.option_joke_star:
        world.completion_condition[player] = lambda state: state.has(EventNames.joke_star_item, player)
    elif goal_value == goal.option_friend_of_the_world:
        world.completion_condition[player] = lambda state: state.has(EventNames.friend_of_the_world_item, player)
    elif goal_value == goal.option_neighborly_advisor:
        world.completion_condition[player] = lambda state: state.has(EventNames.neighborly_advisor_item, player)

def set_skill_rules(world: MultiWorld, player: int, options: Sims4Options):
    skills = {
        SkillNames.base_skill_comedy: (3, 11),
        SkillNames.base_skill_charisma: (3, 11),
        SkillNames.base_skill_logic: (3, 11),
        SkillNames.base_skill_fitness: (3, 11),
        SkillNames.base_skill_writing: (3, 11),
        SkillNames.base_skill_fishing: (3, 11),
        SkillNames.base_skill_gardening: (3, 11),
        SkillNames.base_skill_video_gaming: (3, 11),
        SkillNames.base_skill_programming: (3, 11),
        SkillNames.base_skill_handiness: (3, 11),
        SkillNames.base_skill_cooking: (3, 11),
        SkillNames.base_skill_mixology: (3, 11),
        SkillNames.base_skill_gourmet: (3, 11),
        SkillNames.base_skill_mischief: (3, 11),
        SkillNames.base_skill_piano: (3, 11),
        SkillNames.base_skill_violin: (3, 11),
        SkillNames.base_skill_guitar: (3, 11),
        SkillNames.base_skill_painting: (3, 11),
        SkillNames.base_skill_photography: (3, 6),
        SkillNames.base_skill_rocket_science: (3, 11),
    }

    eps = options.expansion_packs.value
    gps = options.game_packs.value
    sps = options.stuff_packs.value

    if ExpansionNames.get_to_work in eps:
        skills[SkillNames.gtw_baking_skill] = (3, 11)
    if ExpansionNames.get_together in eps:
        skills[SkillNames.gt_dancing_skill] = (3, 6)
        skills[SkillNames.gt_djmixing_skill] = (3, 11)
    if ExpansionNames.city_living in eps:
        skills[SkillNames.cl_singing_skill] = (3, 11)
    if ExpansionNames.cats_and_dogs in eps:
        skills[SkillNames.cnd_pettraining_skill] = (3, 6)
        skills[SkillNames.cnd_veterinarian_skill] = (3, 11)
    if ExpansionNames.seasons in eps:
        skills[SkillNames.se_flowerarranging_skill] = (3, 11)
    if ExpansionNames.get_famous in eps:
        skills[SkillNames.gf_acting_skill] = (3, 11)
        skills[SkillNames.gf_mediaproduction_skill] = (3, 6)
    if ExpansionNames.discover_university in eps:
        skills[SkillNames.du_robotics_skill] = (3, 11)
        skills[SkillNames.du_researchanddebate_skill] = (3, 11)
    if ExpansionNames.eco_lifestyle in eps:
        skills[SkillNames.el_fabrication_skill] = (3, 11)
        skills[SkillNames.el_juicefizzing_skill] = (3, 6)
    if ExpansionNames.snowy_escape in eps:
        skills[SkillNames.sy_rock_climbing_skill] = (3, 11)
        skills[SkillNames.sy_skiing_skill] = (3, 11)
        skills[SkillNames.sy_snowboarding_skill] = (3, 11)
    if ExpansionNames.cottage_living in eps:
        skills[SkillNames.cgl_cross_stitch_skill] = (3, 6)
    if ExpansionNames.high_school_years in eps:
        skills[SkillNames.hsy_entrepreneur_skill] = (3, 6)
    if ExpansionNames.horse_ranch in eps:
        skills[SkillNames.hr_horse_riding_skill] = (3, 11)
        skills[SkillNames.hr_nectar_making_skill] = (3, 6)
    if ExpansionNames.lovestruck in eps:
        skills[SkillNames.lv_romance_skill] = (3, 11)
    if ExpansionNames.life_and_death in eps:
        skills[SkillNames.lnd_thanatology_skill] = (3, 6)
    if ExpansionNames.business_and_hobbies in eps:
        skills[SkillNames.bnh_pottery_skill] = (3, 11)
        skills[SkillNames.bnh_tattooing_skill] = (3, 11)
    if ExpansionNames.enchanted_by_nature in eps:
        skills[SkillNames.ebn_apothecary_skill] = (3, 11)
        skills[SkillNames.ebn_natural_living_skill] = (3, 11)
    if GamePackNames.outdoor_retreat in gps:
        skills[SkillNames.or_herbalism_skill] = (3, 11)
    if GamePackNames.spa_day in gps:
        skills[SkillNames.sd_wellness_skill] = (3, 11)
    if GamePackNames.vampires in gps:
        skills[SkillNames.vamp_pipeorgan_skill] = (3, 11)
        skills[SkillNames.vamp_vampirelore_skill] = (3, 16)
    if GamePackNames.parenthood in gps:
        skills[SkillNames.ph_parenting_skill] = (3, 11)
    if GamePackNames.jungle_adventure in gps:
        skills[SkillNames.ja_archaeology_skill] = (3, 11)
        skills[SkillNames.ja_sevadoradianculture_skill] = (3, 6)
    if StuffNames.bowling_night in sps:
        skills[SkillNames.bns_bowling_skill] = (3, 6)
    if StuffNames.nifty_knitting in sps:
        skills[SkillNames.nk_knitting_skill] = (3, 11)
    if StuffNames.paranormal in sps:
        skills[SkillNames.pa_medium_skill] = (3, 6)
    if StuffNames.crystal_creations in sps:
        skills[SkillNames.cc_gemology_skill] = (3, 11)

    for skill, (low, high) in skills.items():
        for level in range(low, high):
            # print(skill, level)
            set_rule(world.get_location(f"{skill} {level}", player),
                     lambda state, s=skill, l=level: has_skill(state, s, player, l))

def _bodybuilder(world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_exercise_demon, player),
             lambda state: has_skill(state, SkillNames.base_skill_fitness, player, 4))
    set_rule(world.get_location(AspirationNames.base_aspiration_fit_to_a_t, player),
             lambda state: has_skill(state, SkillNames.base_skill_fitness, player, 6))
    set_rule(world.get_location(AspirationNames.base_aspiration_bodybuilder, player),
             lambda state: has_skill(state, SkillNames.base_skill_fitness, player, 10))
    set_rule(world.get_location(EventNames.bodybuilder, player),
             lambda state: state.can_reach(world.get_location(AspirationNames.base_aspiration_bodybuilder, player), player=player))

def _painter_extraordinaire(world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_fine_artist, player),
             lambda state: has_skill(state, SkillNames.base_skill_painting, player, 4))
    set_rule(world.get_location(AspirationNames.base_aspiration_brushing_with_greatness, player),
             lambda state: has_skill(state, SkillNames.base_skill_painting, player, 6))
    set_rule(world.get_location(AspirationNames.base_aspiration_painter_extraordinaire, player),
             lambda state: has_skill(state, SkillNames.base_skill_painting, player, 10))
    set_rule(world.get_location(EventNames.painter_extraordinaire, player),
             lambda state: state.can_reach(world.get_location(AspirationNames.base_aspiration_painter_extraordinaire, player),
                                           player=player))

def _bestselling_author(world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_competent_wordsmith, player),
             lambda state: has_skill(state, SkillNames.base_skill_writing, player, 4))
    set_rule(world.get_location(AspirationNames.base_aspiration_novelest_novelist, player),
             lambda state: has_skill(state, SkillNames.base_skill_writing, player, 6))
    set_rule(world.get_location(AspirationNames.base_aspiration_bestselling_author, player),
             lambda state: has_skill(state, SkillNames.base_skill_writing, player, 10))
    set_rule(world.get_location(EventNames.bestselling_author, player),
             lambda state: state.can_reach(
                 world.get_location(AspirationNames.base_aspiration_bestselling_author, player), player=player))

def _musical_genius(world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_fine_tuned, player),
             lambda state: has_skill(state, SkillNames.base_skill_guitar, player, 4)
                           or has_skill(state, SkillNames.base_skill_violin, player, 4)
                           or has_skill(state, SkillNames.base_skill_piano, player, 4))
    set_rule(world.get_location(AspirationNames.base_aspiration_harmonious, player),
             lambda state: has_skill(state, SkillNames.base_skill_guitar, player, 8)
                           or has_skill(state, SkillNames.base_skill_violin, player, 8)
                           or has_skill(state, SkillNames.base_skill_piano, player, 8))
    set_rule(world.get_location(AspirationNames.base_aspiration_musical_genius, player),
             lambda state: has_skill(state, SkillNames.base_skill_guitar, player, 10)
                           or has_skill(state, SkillNames.base_skill_violin, player, 10)
                           or has_skill(state, SkillNames.base_skill_piano, player, 10))
    set_rule(world.get_location(EventNames.musical_genius, player),
             lambda state: state.can_reach(
                 world.get_location(AspirationNames.base_aspiration_musical_genius, player), player=player))

def _public_enemy(world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_criminal_mind, player),
             lambda state: has_skill(state, SkillNames.base_skill_mischief, player, 3))
    set_rule(world.get_location(AspirationNames.base_aspiration_public_enemy, player),
             lambda state: has_skill(state, SkillNames.base_skill_mischief, player, 8)
                           and has_skill(state, SkillNames.base_skill_programming, player, 4))
    set_rule(world.get_location(EventNames.public_enemy, player),
             lambda state: state.can_reach(
                 world.get_location(AspirationNames.base_aspiration_public_enemy, player), player=player))

def _chief_of_mischief(world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_artful_trickster, player),
             lambda state: has_skill(state, SkillNames.base_skill_mischief, player, 3))
    set_rule(world.get_location(AspirationNames.base_aspiration_professional_prankster, player),
             lambda state: has_skill(state, SkillNames.base_skill_mischief, player, 6))
    set_rule(world.get_location(AspirationNames.base_aspiration_chief_of_mischief, player),
             lambda state: has_skill(state, SkillNames.base_skill_mischief, player, 10))
    set_rule(world.get_location(EventNames.chief_of_mischief, player),
             lambda state: state.can_reach(
                 world.get_location(AspirationNames.base_aspiration_chief_of_mischief, player), player=player))

def _master_chef(world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_captain_cook, player),
             lambda state: has_skill(state, SkillNames.base_skill_cooking, player, 5))
    set_rule(world.get_location(AspirationNames.base_aspiration_culinary_artist, player),
             lambda state: has_skill(state, SkillNames.base_skill_cooking, player, 5))
    set_rule(world.get_location(AspirationNames.base_aspiration_master_chef, player),
             lambda state: (has_skill(state, SkillNames.base_skill_gourmet, player, 6)
                            and has_skill(state, SkillNames.base_skill_cooking, player, 8))
                           or (has_skill(state, SkillNames.base_skill_gourmet, player, 5)
                               and has_skill(state, SkillNames.base_skill_mixology, player, 7)
                               and has_skill(state, SkillNames.base_skill_charisma, player, 4)))
    set_rule(world.get_location(EventNames.master_chef, player),
             lambda state: state.can_reach(
                 world.get_location(AspirationNames.base_aspiration_master_chef, player), player=player))

def _master_mixologist(world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_electric_mixer, player),
             lambda state: has_skill(state, SkillNames.base_skill_mixology, player, 4))
    set_rule(world.get_location(AspirationNames.base_aspiration_beverage_boss, player),
             lambda state: has_skill(state, SkillNames.base_skill_mixology, player, 7)
                           and has_skill(state, SkillNames.base_skill_cooking, player, 4))
    set_rule(world.get_location(AspirationNames.base_aspiration_master_mixologist, player),
             lambda state: has_skill(state, SkillNames.base_skill_mixology, player, 10)
                           and has_skill(state, SkillNames.base_skill_cooking, player, 4))
    set_rule(world.get_location(EventNames.master_mixologist, player),
             lambda state: state.can_reach(
                 world.get_location(AspirationNames.base_aspiration_master_mixologist, player), player=player))
def _renaissance_sim(world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_prudent_student, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=1))
    set_rule(world.get_location(AspirationNames.base_aspiration_jack_of_some_trades, player),
             lambda state: count_skills_over(2, state, player) >= 4)
    set_rule(world.get_location(AspirationNames.base_aspiration_pantologist, player),
             lambda state: count_skills_over(3, state, player) >= 5)
    set_rule(world.get_location(AspirationNames.base_aspiration_renaissance_sim, player),
             lambda state: count_skills_over(6, state, player) >= 6)
    set_rule(world.get_location(EventNames.renaissance_sim, player),
             lambda state: state.can_reach(
                 world.get_location(AspirationNames.base_aspiration_renaissance_sim, player), player=player))

def _nerd_brain(world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_prudent_student, player),
             lambda state: has_skill(state, SkillNames.base_skill_logic, player, 3))
    set_rule(world.get_location(AspirationNames.base_aspiration_erudite, player),
             lambda state: has_skill(state, SkillNames.base_skill_logic, player, 6))
    set_rule(world.get_location(AspirationNames.base_aspiration_rocket_scientist, player),
             lambda state: has_skill(state, SkillNames.base_skill_handiness, player, 5))
    set_rule(world.get_location(AspirationNames.base_aspiration_nerd_brain, player),
             lambda state: has_skill(state, SkillNames.base_skill_logic, player, 10)
                           and has_skill(state, SkillNames.base_skill_handiness, player, 5))
    set_rule(world.get_location(EventNames.nerd_brain, player),
             lambda state: state.can_reach(
                 world.get_location(AspirationNames.base_aspiration_nerd_brain, player), player=player))

def _computer_whiz(world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_technically_adept, player),
             lambda state: has_skill(state, SkillNames.base_skill_programming, player, 3))
    set_rule(world.get_location(AspirationNames.base_aspiration_computer_geek, player),
             lambda state: has_skill(state, SkillNames.base_skill_programming, player, 7))
    set_rule(world.get_location(AspirationNames.base_aspiration_computer_whiz, player),
             lambda state: has_skill(state, SkillNames.base_skill_programming, player, 7)
                           and has_skill(state, SkillNames.base_skill_video_gaming, player, 4))
    set_rule(world.get_location(EventNames.computer_whiz, player),
             lambda state: state.can_reach(
                 world.get_location(AspirationNames.base_aspiration_computer_whiz, player), player=player))

def _serial_romantic(world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_up_to_date, player),
             lambda state: has_skill(state, SkillNames.base_skill_charisma, player, 4))
    set_rule(world.get_location(AspirationNames.base_aspiration_romance_juggler, player),
             lambda state: has_skill(state, SkillNames.base_skill_charisma, player, 6))
    set_rule(world.get_location(AspirationNames.base_aspiration_serial_romantic, player),
             lambda state: has_skill(state, SkillNames.base_skill_charisma, player, 6))
    set_rule(world.get_location(EventNames.serial_romantic, player),
             lambda state: state.can_reach(
                 world.get_location(AspirationNames.base_aspiration_serial_romantic, player), player=player))

def _freelance_botanist (world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_garden_variety, player),
             lambda state: has_skill(state, SkillNames.base_skill_gardening, player, 4))
    set_rule(world.get_location(AspirationNames.base_aspiration_nature_nurturer, player),
             lambda state: has_skill(state, SkillNames.base_skill_gardening, player, 6))
    set_rule(world.get_location(AspirationNames.base_aspiration_freelance_botanist, player),
             lambda state: has_skill(state, SkillNames.base_skill_gardening, player, 10))
    set_rule(world.get_location(EventNames.freelance_botanist, player),
             lambda state: state.can_reach(
                 world.get_location(AspirationNames.base_aspiration_freelance_botanist, player), player=player))

def _angling_ace(world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_hooked, player),
             lambda state: has_skill(state, SkillNames.base_skill_fishing, player, 4))
    set_rule(world.get_location(AspirationNames.base_aspiration_reel_smart, player),
             lambda state: has_skill(state, SkillNames.base_skill_fishing, player, 6))
    set_rule(world.get_location(AspirationNames.base_aspiration_angling_ace, player),
             lambda state: has_skill(state, SkillNames.base_skill_fishing, player, 10))
    set_rule(world.get_location(EventNames.angling_ace, player),
             lambda state: state.can_reach(
                 world.get_location(AspirationNames.base_aspiration_angling_ace, player), player=player))

def _joke_star(world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_practical_joker, player),
             lambda state: has_skill(state, SkillNames.base_skill_comedy, player, 3))
    set_rule(world.get_location(AspirationNames.base_aspiration_standup_startup, player),
             lambda state: has_skill(state, SkillNames.base_skill_comedy, player, 3))
    set_rule(world.get_location(AspirationNames.base_aspiration_funny, player),
             lambda state: has_skill(state, SkillNames.base_skill_comedy, player, 6)
                           and (has_skill(state, SkillNames.base_skill_guitar, player, 3)
                                or has_skill(state, SkillNames.base_skill_violin, player, 3)))
    set_rule(world.get_location(AspirationNames.base_aspiration_joke_star, player),
             lambda state: has_skill(state, SkillNames.base_skill_comedy, player, 10)
                           and (has_skill(state, SkillNames.base_skill_guitar, player, 3)
                                or has_skill(state, SkillNames.base_skill_violin, player, 3)))
    set_rule(world.get_location(EventNames.joke_star, player),
             lambda state: state.can_reach(
                 world.get_location(AspirationNames.base_aspiration_joke_star, player), player=player))

def _friend_of_the_world(world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_well_liked, player),
             lambda state: has_skill(state, SkillNames.base_skill_charisma, player, 4))
    set_rule(world.get_location(AspirationNames.base_aspiration_super_friend, player),
             lambda state: has_skill(state, SkillNames.base_skill_charisma, player, 6))
    set_rule(world.get_location(AspirationNames.base_aspiration_friend_of_the_world, player),
             lambda state: has_skill(state, SkillNames.base_skill_charisma, player, 10))
    set_rule(world.get_location(EventNames.friend_of_the_world, player),
             lambda state: state.can_reach(
                 world.get_location(AspirationNames.base_aspiration_friend_of_the_world, player), player=player))

def _neighborly_advisor(world: MultiWorld, player: int):
    set_rule(world.get_location(AspirationNames.base_aspiration_neighborly_advisor, player),
             lambda state: has_skill(state, SkillNames.base_skill_charisma, player, 7))
    set_rule(world.get_location(EventNames.neighborly_advisor, player),
             lambda state: state.can_reach(
                 world.get_location(AspirationNames.base_aspiration_neighborly_advisor, player), player=player))

ASPIRATION_RULES = {
        AspirationGoal.option_bodybuilder: _bodybuilder,
        AspirationGoal.option_painter_extraordinaire: _painter_extraordinaire,
        AspirationGoal.option_bestselling_author: _bestselling_author,
        AspirationGoal.option_musical_genius: _musical_genius,
        AspirationGoal.option_public_enemy: _public_enemy,
        AspirationGoal.option_chief_of_mischief: _chief_of_mischief,
        AspirationGoal.option_master_chef: _master_chef,
        AspirationGoal.option_master_mixologist: _master_mixologist,
        AspirationGoal.option_renaissance_sim: _renaissance_sim,
        AspirationGoal.option_nerd_brain: _nerd_brain,
        AspirationGoal.option_computer_whiz: _computer_whiz,
        AspirationGoal.option_serial_romantic: _serial_romantic,
        AspirationGoal.option_freelance_botanist: _freelance_botanist,
        AspirationGoal.option_angling_ace: _angling_ace,
        AspirationGoal.option_joke_star: _joke_star,
        AspirationGoal.option_friend_of_the_world: _friend_of_the_world,
        AspirationGoal.option_neighborly_advisor: _neighborly_advisor,
    }

def set_aspiration_rules(world: MultiWorld, player: int, options: Sims4Options):
    handler = ASPIRATION_RULES.get(options.goal)
    if handler:
        handler(world, player)

def _career_athlete(world: MultiWorld, player: int):
    set_rule(world.get_location(CareerNames.base_career_athlete_4, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=1)
                           and state.has(SkillNames.base_skill_fitness, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_athlete_5A, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=2)
                           and state.has(SkillNames.base_skill_fitness, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_athlete_5B, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=2)
                           and state.has(SkillNames.base_skill_fitness, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_athlete_6A, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=2)
                           and state.has(SkillNames.base_skill_fitness, player, count=3))
    set_rule(world.get_location(CareerNames.base_career_athlete_7A, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=2)
                           and state.has(SkillNames.base_skill_fitness, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_athlete_8A, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=3)
                           and state.has(SkillNames.base_skill_fitness, player, count=6))
    set_rule(world.get_location(CareerNames.base_career_athlete_9A, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=4)
                           and state.has(SkillNames.base_skill_fitness, player, count=7))
    set_rule(world.get_location(CareerNames.base_career_athlete_10A, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=6)
                           and state.has(SkillNames.base_skill_fitness, player, count=8))
    set_rule(world.get_location(CareerNames.base_career_athlete_6B, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=3)
                           and state.has(SkillNames.base_skill_fitness, player, count=6))
    set_rule(world.get_location(CareerNames.base_career_athlete_7B, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=3)
                           and state.has(SkillNames.base_skill_fitness, player, count=7))
    set_rule(world.get_location(CareerNames.base_career_athlete_8B, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=4)
                           and state.has(SkillNames.base_skill_fitness, player, count=8))
    set_rule(world.get_location(CareerNames.base_career_athlete_9B, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=5)
                           and state.has(SkillNames.base_skill_fitness, player, count=8))
    set_rule(world.get_location(CareerNames.base_career_athlete_10B, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=6)
                           and state.has(SkillNames.base_skill_fitness, player, count=8))

def _career_astronaut(world: MultiWorld, player: int):
    set_rule(world.get_location(CareerNames.base_career_astronaut_4, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_astronaut_5, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=2)
                           and state.has(SkillNames.base_skill_fitness, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_astronaut_6, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=3)
                           and state.has(SkillNames.base_skill_fitness, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_astronaut_7, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=3)
                           and state.has(SkillNames.base_skill_fitness, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_astronaut_8A, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=4)
                           and state.has(SkillNames.base_skill_fitness, player, count=5))
    set_rule(world.get_location(CareerNames.base_career_astronaut_8B, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=4)
                           and state.has(SkillNames.base_skill_fitness, player, count=5))
    set_rule(world.get_location(CareerNames.base_career_astronaut_9A, player),
             lambda state: state.has(SkillNames.base_skill_fitness, player, count=6))
    set_rule(world.get_location(CareerNames.base_career_astronaut_10A, player),
             lambda state: state.has(SkillNames.base_skill_rocket_science, player, count=2)
                           and state.has(SkillNames.base_skill_fitness, player, count=8))
    set_rule(world.get_location(CareerNames.base_career_astronaut_9B, player),
             lambda state: state.has(SkillNames.base_skill_fitness, player, count=6))
    set_rule(world.get_location(CareerNames.base_career_astronaut_10B, player),
             lambda state: state.has(SkillNames.base_skill_rocket_science, player, count=2)
                           and state.has(SkillNames.base_skill_fitness, player, count=8))

def _career_business(world: MultiWorld, player: int):
    set_rule(world.get_location(CareerNames.base_career_business_5, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_business_6, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_business_7A, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=2)
                           and state.has(SkillNames.base_skill_logic, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_business_7B, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=2)
                           and state.has(SkillNames.base_skill_logic, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_business_8A, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=4)
                           and state.has(SkillNames.base_skill_logic, player, count=3))
    set_rule(world.get_location(CareerNames.base_career_business_9A, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=6)
                           and state.has(SkillNames.base_skill_logic, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_business_10A, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=8)
                           and state.has(SkillNames.base_skill_logic, player, count=6))
    set_rule(world.get_location(CareerNames.base_career_business_8B, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=3)
                           and state.has(SkillNames.base_skill_logic, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_business_9B, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=4)
                           and state.has(SkillNames.base_skill_logic, player, count=6))
    set_rule(world.get_location(CareerNames.base_career_business_10B, player),
             lambda state: state.has(SkillNames.base_skill_charisma, player, count=6)
                           and state.has(SkillNames.base_skill_logic, player, count=8))

def _career_criminal(world: MultiWorld, player: int):
    set_rule(world.get_location(CareerNames.base_career_criminal_4, player),
             lambda state: state.has(SkillNames.base_skill_mischief, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_criminal_5, player),
             lambda state: state.has(SkillNames.base_skill_mischief, player, count=3))
    set_rule(world.get_location(CareerNames.base_career_criminal_6A, player),
             lambda state: state.has(SkillNames.base_skill_mischief, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_criminal_6B, player),
             lambda state: state.has(SkillNames.base_skill_mischief, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_criminal_7A, player),
             lambda state: state.has(SkillNames.base_skill_mischief, player, count=5))
    set_rule(world.get_location(CareerNames.base_career_criminal_8A, player),
             lambda state: state.has(SkillNames.base_skill_mischief, player, count=6))
    set_rule(world.get_location(CareerNames.base_career_criminal_9A, player),
             lambda state: state.has(SkillNames.base_skill_mischief, player, count=7)
                           and state.has(SkillNames.base_skill_handiness, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_criminal_10A, player),
             lambda state: state.has(SkillNames.base_skill_mischief, player, count=8)
                           and state.has(SkillNames.base_skill_handiness, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_criminal_7B, player),
             lambda state: state.has(SkillNames.base_skill_mischief, player, count=5)
                           and state.has(SkillNames.base_skill_programming, player, count=0))
    set_rule(world.get_location(CareerNames.base_career_criminal_8B, player),
             lambda state: state.has(SkillNames.base_skill_mischief, player, count=6)
                           and state.has(SkillNames.base_skill_programming, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_criminal_9B, player),
             lambda state: state.has(SkillNames.base_skill_mischief, player, count=7)
                           and state.has(SkillNames.base_skill_programming, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_criminal_10B, player),
             lambda state: state.has(SkillNames.base_skill_mischief, player, count=8)
                           and state.has(SkillNames.base_skill_programming, player, count=6))
def _career_culinary(world: MultiWorld, player: int):
    set_rule(world.get_location(CareerNames.base_career_culinary_5, player),
             lambda state: state.has(SkillNames.base_skill_cooking, player, count=1)
                           and state.has(SkillNames.base_skill_mixology, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_culinary_6A, player),
             lambda state: state.has(SkillNames.base_skill_cooking, player, count=2)
                           and state.has(SkillNames.base_skill_mixology, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_culinary_6B, player),
             lambda state: state.has(SkillNames.base_skill_cooking, player, count=2)
                           and state.has(SkillNames.base_skill_mixology, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_culinary_7A, player),
             lambda state: state.has(SkillNames.base_skill_cooking, player, count=4)
                           and state.has(SkillNames.base_skill_gourmet, player, count=0)
                           and state.has(SkillNames.base_skill_mixology, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_culinary_8A, player),
             lambda state: state.has(SkillNames.base_skill_cooking, player, count=6)
                           and state.has(SkillNames.base_skill_gourmet, player, count=4)
                           and state.has(SkillNames.base_skill_mixology, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_culinary_9A, player),
             lambda state: state.has(SkillNames.base_skill_cooking, player, count=6)
                           and state.has(SkillNames.base_skill_gourmet, player, count=4)
                           and state.has(SkillNames.base_skill_mixology, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_culinary_10A, player),
             lambda state: state.has(SkillNames.base_skill_cooking, player, count=8)
                           and state.has(SkillNames.base_skill_gourmet, player, count=6)
                           and state.has(SkillNames.base_skill_mixology, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_culinary_7B, player),
             lambda state: state.has(SkillNames.base_skill_mixology, player, count=3)
                           and state.has(SkillNames.base_skill_charisma, player, count=0)
                           and state.has(SkillNames.base_skill_cooking, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_culinary_8B, player),
             lambda state: state.has(SkillNames.base_skill_mixology, player, count=5)
                           and state.has(SkillNames.base_skill_charisma, player, count=2)
                           and state.has(SkillNames.base_skill_cooking, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_culinary_9B, player),
             lambda state: state.has(SkillNames.base_skill_mixology, player, count=6)
                           and state.has(SkillNames.base_skill_charisma, player, count=4)
                           and state.has(SkillNames.base_skill_cooking, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_culinary_10B, player),
             lambda state: state.has(SkillNames.base_skill_mixology, player, count=8)
                           and state.has(SkillNames.base_skill_charisma, player, count=6)
                           and state.has(SkillNames.base_skill_cooking, player, count=2))

def _career_entertainer(world: MultiWorld, player: int):
    set_rule(world.get_location(CareerNames.base_career_entertainer_5A, player),
             lambda state: (state.has(SkillNames.base_skill_guitar, player, count=1)
                            or state.has(SkillNames.base_skill_violin, player, count=1))
                           and state.has(SkillNames.base_skill_comedy, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_entertainer_5B, player),
             lambda state: (state.has(SkillNames.base_skill_guitar, player, count=1)
                            or state.has(SkillNames.base_skill_violin, player, count=1))
                           and state.has(SkillNames.base_skill_comedy, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_entertainer_6A, player),
             lambda state: state.has(SkillNames.base_skill_violin, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_entertainer_7A, player),
             lambda state: (state.has(SkillNames.base_skill_guitar, player, count=3)
                            or state.has(SkillNames.base_skill_violin, player, count=3))
                           and state.has(SkillNames.base_skill_piano, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_entertainer_8A, player),
             lambda state: (state.has(SkillNames.base_skill_guitar, player, count=4)
                            or state.has(SkillNames.base_skill_violin, player, count=4))
                           and state.has(SkillNames.base_skill_piano, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_entertainer_9A, player),
             lambda state: (state.has(SkillNames.base_skill_guitar, player, count=5)
                            or state.has(SkillNames.base_skill_violin, player, count=5))
                           and state.has(SkillNames.base_skill_piano, player, count=6))
    set_rule(world.get_location(CareerNames.base_career_entertainer_10A, player),
             lambda state: (state.has(SkillNames.base_skill_guitar, player, count=6)
                            or state.has(SkillNames.base_skill_violin, player, count=6))
                           and state.has(SkillNames.base_skill_piano, player, count=8))
    set_rule(world.get_location(CareerNames.base_career_entertainer_6B, player),
             lambda state: state.has(SkillNames.base_skill_comedy, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_entertainer_7B, player),
             lambda state: state.has(SkillNames.base_skill_comedy, player, count=5))
    set_rule(world.get_location(CareerNames.base_career_entertainer_8B, player),
             lambda state: state.has(SkillNames.base_skill_comedy, player, count=6)
                           and state.has(SkillNames.base_skill_charisma, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_entertainer_9B, player),
             lambda state: state.has(SkillNames.base_skill_comedy, player, count=7)
                           and state.has(SkillNames.base_skill_charisma, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_entertainer_10B, player),
             lambda state: state.has(SkillNames.base_skill_comedy, player, count=8)
                           and state.has(SkillNames.base_skill_charisma, player, count=6))

def _career_painter(world: MultiWorld, player: int):
    set_rule(world.get_location(CareerNames.base_career_painter_4, player),
             lambda state: state.has(SkillNames.base_skill_painting, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_painter_5, player),
             lambda state: state.has(SkillNames.base_skill_painting, player, count=3))
    set_rule(world.get_location(CareerNames.base_career_painter_6, player),
             lambda state: state.has(SkillNames.base_skill_painting, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_painter_7A, player),
             lambda state: state.has(SkillNames.base_skill_painting, player, count=5))
    set_rule(world.get_location(CareerNames.base_career_painter_7B, player),
             lambda state: state.has(SkillNames.base_skill_painting, player, count=5))
    set_rule(world.get_location(CareerNames.base_career_painter_8A, player),
             lambda state: state.has(SkillNames.base_skill_painting, player, count=6))
    set_rule(world.get_location(CareerNames.base_career_painter_9A, player),
             lambda state: state.has(SkillNames.base_skill_painting, player, count=7)
                           and state.has(SkillNames.base_skill_logic, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_painter_10A, player),
             lambda state: state.has(SkillNames.base_skill_painting, player, count=8)
                           and state.has(SkillNames.base_skill_logic, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_painter_8B, player),
             lambda state: state.has(SkillNames.base_skill_painting, player, count=6))
    set_rule(world.get_location(CareerNames.base_career_painter_9B, player),
             lambda state: state.has(SkillNames.base_skill_painting, player, count=7)
                           and state.has(SkillNames.base_skill_charisma, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_painter_10B, player),
             lambda state: state.has(SkillNames.base_skill_painting, player, count=8)
                           and state.has(SkillNames.base_skill_charisma, player, count=4))
def _career_secret_agent(world: MultiWorld, player: int):
    set_rule(world.get_location(CareerNames.base_career_secret_agent_4, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=1)
                           and state.has(SkillNames.base_skill_charisma, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_secret_agent_5, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=1)
                           and state.has(SkillNames.base_skill_charisma, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_secret_agent_6, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=3)
                           and state.has(SkillNames.base_skill_charisma, player, count=3))
    set_rule(world.get_location(CareerNames.base_career_secret_agent_7, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=3)
                           and state.has(SkillNames.base_skill_charisma, player, count=3))
    set_rule(world.get_location(CareerNames.base_career_secret_agent_8A, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=4)
                           and state.has(SkillNames.base_skill_charisma, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_secret_agent_8B, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=4)
                           and state.has(SkillNames.base_skill_charisma, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_secret_agent_9A, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=6)
                           and state.has(SkillNames.base_skill_charisma, player, count=5))
    set_rule(world.get_location(CareerNames.base_career_secret_agent_10A, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=8)
                           and state.has(SkillNames.base_skill_charisma, player, count=6))
    set_rule(world.get_location(CareerNames.base_career_secret_agent_9B, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=6))
    set_rule(world.get_location(CareerNames.base_career_secret_agent_10B, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=8)
                           and state.has(SkillNames.base_skill_mischief, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_secret_agent_11B, player),
             lambda state: state.has(SkillNames.base_skill_logic, player, count=8)
                           and state.has(SkillNames.base_skill_mischief, player, count=4))
def _career_style_influencer(world: MultiWorld, player: int):
    set_rule(world.get_location(CareerNames.base_career_style_influencer_4, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_style_influencer_5, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_style_influencer_6A, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=3)
                           and state.has(SkillNames.base_skill_charisma, player, count=1)
                           and state.has(SkillNames.base_skill_painting, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_style_influencer_7A, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=4)
                           and state.has(SkillNames.base_skill_charisma, player, count=3)
                           and state.has(SkillNames.base_skill_painting, player, count=2)
                           and state.has(SkillNames.base_skill_photography, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_style_influencer_8A, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=5)
                           and state.has(SkillNames.base_skill_charisma, player, count=4)
                           and state.has(SkillNames.base_skill_painting, player, count=3))
    set_rule(world.get_location(CareerNames.base_career_style_influencer_9A, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=6)
                           and state.has(SkillNames.base_skill_charisma, player, count=5)
                           and state.has(SkillNames.base_skill_painting, player, count=6))
    set_rule(world.get_location(CareerNames.base_career_style_influencer_10A, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=7)
                           and state.has(SkillNames.base_skill_charisma, player, count=6)
                           and state.has(SkillNames.base_skill_painting, player, count=5))
    set_rule(world.get_location(CareerNames.base_career_style_influencer_6B, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=3)
                           and state.has(SkillNames.base_skill_charisma, player, count=1)
                           and state.has(SkillNames.base_skill_painting, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_style_influencer_7B, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=4)
                           and state.has(SkillNames.base_skill_charisma, player, count=3)
                           and state.has(SkillNames.base_skill_painting, player, count=2)
                           and state.has(SkillNames.base_skill_photography, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_style_influencer_8B, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=5)
                           and state.has(SkillNames.base_skill_charisma, player, count=4)
                           and state.has(SkillNames.base_skill_painting, player, count=3))
    set_rule(world.get_location(CareerNames.base_career_style_influencer_9B, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=6)
                           and state.has(SkillNames.base_skill_charisma, player, count=5)
                           and state.has(SkillNames.base_skill_painting, player, count=6))
    set_rule(world.get_location(CareerNames.base_career_style_influencer_10B, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=7)
                           and state.has(SkillNames.base_skill_charisma, player, count=6)
                           and state.has(SkillNames.base_skill_painting, player, count=5))
def _career_tech_guru(world: MultiWorld, player: int):
    # TODO check project manager career logic https://discord.com/channels/731205301247803413/1079002955262480424/1403764728177758252
    set_rule(world.get_location(CareerNames.base_career_tech_guru_4, player),
             lambda state: has_skill(state, SkillNames.base_skill_programming, player, 3))
    set_rule(world.get_location(CareerNames.base_career_tech_guru_5, player),
             lambda state: has_skill(state, SkillNames.base_skill_programming, player, 4)
                           and has_skill(state, SkillNames.base_skill_video_gaming, player, 3))
    set_rule(world.get_location(CareerNames.base_career_tech_guru_6, player),
             lambda state: state.has(SkillNames.base_skill_programming, player, count=3)
                           and state.has(SkillNames.base_skill_video_gaming, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_tech_guru_7A, player),
             lambda state: state.has(SkillNames.base_skill_programming, player, count=4)
                           and state.has(SkillNames.base_skill_video_gaming, player, count=3))
    set_rule(world.get_location(CareerNames.base_career_tech_guru_7B, player),
             lambda state: state.has(SkillNames.base_skill_programming, player, count=4)
                           and state.has(SkillNames.base_skill_video_gaming, player, count=3))
    set_rule(world.get_location(CareerNames.base_career_tech_guru_8A, player),
             lambda state: state.has(SkillNames.base_skill_programming, player, count=4)
                           and state.has(SkillNames.base_skill_video_gaming, player, count=4))
    set_rule(world.get_location(CareerNames.base_career_tech_guru_9A, player),
             lambda state: state.has(SkillNames.base_skill_programming, player, count=5)
                           and state.has(SkillNames.base_skill_video_gaming, player, count=6))
    set_rule(world.get_location(CareerNames.base_career_tech_guru_10A, player),
             lambda state: state.has(SkillNames.base_skill_programming, player, count=6)
                           and state.has(SkillNames.base_skill_video_gaming, player, count=8))
    set_rule(world.get_location(CareerNames.base_career_tech_guru_8B, player),
             lambda state: state.has(SkillNames.base_skill_programming, player, count=6)
                           and state.has(SkillNames.base_skill_charisma, player, count=0))
    set_rule(world.get_location(CareerNames.base_career_tech_guru_9B, player),
             lambda state: state.has(SkillNames.base_skill_programming, player, count=7)
                           and state.has(SkillNames.base_skill_charisma, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_tech_guru_10B, player),
             lambda state: state.has(SkillNames.base_skill_programming, player, count=8)
                           and state.has(SkillNames.base_skill_charisma, player, count=4))
def _career_writer(world: MultiWorld, player: int):
    set_rule(world.get_location(CareerNames.base_career_writer_4, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_writer_5, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_writer_6A, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=3))
    set_rule(world.get_location(CareerNames.base_career_writer_6B, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=3))
    set_rule(world.get_location(CareerNames.base_career_writer_7A, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=5))
    set_rule(world.get_location(CareerNames.base_career_writer_8A, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=6)
                           and state.has(SkillNames.base_skill_logic, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_writer_9A, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=7)
                           and state.has(SkillNames.base_skill_logic, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_writer_10A, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=8)
                           and state.has(SkillNames.base_skill_logic, player, count=3))
    set_rule(world.get_location(CareerNames.base_career_writer_7B, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=5))
    set_rule(world.get_location(CareerNames.base_career_writer_8B, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=6)
                           and state.has(SkillNames.base_skill_charisma, player, count=1))
    set_rule(world.get_location(CareerNames.base_career_writer_9B, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=7)
                           and state.has(SkillNames.base_skill_charisma, player, count=2))
    set_rule(world.get_location(CareerNames.base_career_writer_10B, player),
             lambda state: state.has(SkillNames.base_skill_writing, player, count=8)
                           and state.has(SkillNames.base_skill_charisma, player, count=3))

CAREER_RULES = {
    CareerNames.base_career_athlete: _career_athlete,
    CareerNames.base_career_astronaut: _career_astronaut,
    CareerNames.base_career_business: _career_business,
    CareerNames.base_career_criminal: _career_criminal,
    CareerNames.base_career_culinary: _career_culinary,
    CareerNames.base_career_entertainer: _career_entertainer,
    CareerNames.base_career_painter: _career_painter,
    CareerNames.base_career_secret_agent: _career_secret_agent,
    CareerNames.base_career_style_influencer: _career_style_influencer,
    CareerNames.base_career_tech_guru: _career_tech_guru,
    CareerNames.base_career_writer: _career_writer,
}

def set_career_rules(world: MultiWorld, player: int, options: Sims4Options):
    # TODO relearn how the career locations send, and then refactor this to use has_skill
    career = options.career

    for career_name, handler in CAREER_RULES.items():
        if career_name in career:
            handler(world, player)

def count_skills_over(threshold: int, state, player) -> int:
    total_count = 0

    if state.has(SkillNames.base_skill_charisma, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_fitness, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_mischief, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_logic, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_cooking, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_mixology, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_comedy, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_writing, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_fishing, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_gardening, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_video_gaming, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_programming, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_photography, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_handiness, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_piano, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_violin, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_guitar, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_painting, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_rocket_science, player, count=threshold):
        total_count += 1
    if state.has(SkillNames.base_skill_gourmet, player, count=threshold):
        total_count += 1

    return total_count

def has_skill(state: CollectionState, skill: str, player: int, skill_level: int) -> bool:
    # determines how many skill items are required based on the skill level passed into the function
    skills_required: int = skill_level - 2
    return state.has(skill, player, skills_required)

def has_multiple_skills(state: CollectionState, skills_and_levels: dict[str, int], player: int):
    skills = list(skills_and_levels.keys())
    return has_skill(state, skills[0], player, skills_and_levels[skills[0]]) and has_skill(state, skills[1], player, skills_and_levels[skills[1]])