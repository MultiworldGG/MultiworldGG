# data for entrances in relevant settings
# entrance name: (area id, map id, exit id), which correspond to the entrance
#                you walk into a room from
bowser_shortened_entrances_rmv = [
    # remove these
    (22, 26, 0),  # Hall to Guard Door 1 -> Guard Door 1
    (22, 39, 1),  # Guard Door 2 -> Room with Hidden Door 2

    (22, 26, 2),  # Lower Grand Hall Lower -> Guard Door 1
    (22, 22, 0),  # Guard Door 2 -> Castle Battlement Lower Door

    (22, 48, 0),  # Hall to Water Puzzle -> Left Water Puzzle 1F
    (22, 49, 1),  # Bill Blaster Hall Lower -> Right Water Puzzle 1F

    (22, 27, 1),  # Castle Battlement Lower Door -> Guard Door 2
    (22, 39, 0),  # Hidden Passage 1 -> Room with Hidden Door 2

    (22, 19, 0),  # Upper Grand Hall Upper -> Split Level Hall
    (22, 16, 2),  # Blue Fire Bridge -> Maze Room Upper
]

bowser_shortened_entrances_add = [
    # add these in their place
    (22, 27, 0),  # Hall to Guard Door 1 -> Guard Door 2
    (22, 17, 1),  # Guard Door 2 -> Hall to Guard Door 1

    (22, 27, 1),  # Lower Grand Hall Lower -> Guard Door 2
    (22, 13, 0),  # Guard Door 2 -> Lower Grand Hall Lower

    (22, 47, 0),  # Hall to Water Puzzle -> Bill Blaster Hall Lower
    (22, 18, 1),  # Bill Blaster Hall Lower -> Hall to Water Puzzle

    (22, 47, 1),  # Castle Battlement Lower Door -> Bill Blaster Hall Upper
    (22, 22, 0),  # Hidden Passage 1 -> Castle Battlement Lower Door

    (22, 36, 0),  # Upper Grand Hall Upper -> Blue Fire Bridge
    (22, 14, 2),  # Blue Fire Bridge -> Upper Grand Hall Upper
]

bowser_boss_rush_entrances_rmv = [
    # remove entrances
    (22, 21, 4),  # Riding Star Ship Scene -> Ship Enter/Exit Scenes
    (22, 36, 1)  # Fake Peach Hallway -> Blue Fire Bridge
]

bowser_boss_rush_entrances_add = [
    # add these in their place
    (22, 20, 0),  # Riding Star Ship Scene -> Fake Peach Hallway
    (5, 8, 2)  # Fake Peach Hallway -> Riding Star Ship Scene
]
