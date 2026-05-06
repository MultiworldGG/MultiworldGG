class Dungeon(object):

    def __init__(self, world, name, hint, font_color):

        self.world = world
        self.name = name
        self.hint_text = hint
        self.font_color = font_color
        self.regions = []
        self.boss_key = []
        self.small_keys = []
        self.maps = []
        self.compasses = []

        for region in world.multiworld.regions:
            if region.player == world.player and region.dungeon == self.name:
                region.dungeon = self
                self.regions.append(region)


    def copy(self, new_world):
        new_dungeon = Dungeon(new_world, self.name, self.hint_text, self.font_color)
        new_dungeon.boss_key = [item.copy(new_world) for item in self.boss_key]
        new_dungeon.small_keys = [item.copy(new_world) for item in self.small_keys]
        new_dungeon.maps = [item.copy(new_world) for item in self.maps]
        new_dungeon.compasses = [item.copy(new_world) for item in self.compasses]

        return new_dungeon


    @property
    def keys(self):
        return self.small_keys + self.boss_key


    @property
    def shuffle_map(self):
        return self.world.shuffle_map

    @property
    def shuffle_compass(self):
        return self.world.shuffle_compass


    @property
    def dungeon_items(self):
        return self.maps + self.compasses


    @property
    def all_items(self):
        return self.maps + self.compasses + self.keys


    def is_dungeon_item(self, item):
        return item.name in [dungeon_item.name for dungeon_item in self.all_items]


    def item_name(self, name):
        return f"{name} ({self.name})"


    def __str__(self):
        return str(self.__unicode__())


    def __unicode__(self):
        return '%s' % self.name
