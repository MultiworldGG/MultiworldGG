from .logic.requirements import AND, OR, COUNT, FOUND, isConsumable
from .checkMetadata import checkMetadataTable


class Explorer:
    def __init__(self):
        self.__inventory = {}
        self.__visited = set()
        self.__todo = []

    def getAccessableLocations(self):
        return self.__visited

    def getRequiredItemsForNextLocations(self):
        items = set()
        for loc, req in self.__todo:
            if isinstance(req, str):
                items.add(req)
            else:
                req.getItems(self.__inventory, items)
        return items

    def getInventory(self):
        return self.__visited

    def visit(self, location):
        self._visit(location)
        while self._process():
            pass

    def _visit(self, location):
        assert location not in self.__visited
        self.__visited.add(location)
        for ii in location.items:
            self.addItem(ii.item)

        for target, requirements in location.connections:
            if target not in self.__visited:
                if self.testRequirements(requirements):
                    self._visit(target)
                else:
                    self.__todo.append((target, requirements))

    def _process(self):
        self.__todo = list(filter(lambda n: n[0] not in self.__visited, self.__todo))
        for target, req in self.__todo:
            if target not in self.__visited and self.testRequirements(req):
                self._visit(target)
                return True
        return False

    def addItem(self, item, count=1):
        if item is None:
            return
        if item.startswith("RUPEES_"):
            if "_W" in item:
                rupee_item = item[:item.find("_W")]
                world_postfix = item[item.find("_W"):]
                self.__inventory["RUPEES"+world_postfix] = self.__inventory.get("RUPEES"+world_postfix, 0) + int(rupee_item[7:]) * count
            else:
                self.__inventory["RUPEES"] = self.__inventory.get("RUPEES", 0) + int(item[7:]) * count
        else:
            self.__inventory[item] = self.__inventory.get(item, 0) + count

    def consumeItem(self, item, amount=1):
        if item not in self.__inventory:
            return False
        if isConsumable(item):
            self.__inventory[item] -= amount
            if self.__inventory[item] <= 0:
                del self.__inventory[item]
        return True

    def testRequirements(self, req):
        if isinstance(req, str):
            return req in self.__inventory
        if req is None:
            return True
        if req.test(self.__inventory):
            return True
        return False

    def consumeRequirements(self, req):
        if isinstance(req, str):
            self.__inventory[req] -= 1
            if self.__inventory[req] == 0:
                del self.__inventory[req]
            self.__inventory["%s_USED" % req] = self.__inventory.get("%s_USED" % req, 0) + 1
        elif req is not None:
            req.consume(self.__inventory)

    def dump(self, logic):
        failed = 0
        for loc in logic.location_list:
            if loc not in self.__visited:
                failed += 1
        for loc in self.__visited:
            for target, req in loc.connections:
                if target not in self.__visited:
                    print("Missing:", req)
        for item, amount in sorted(self.__inventory.items()):
            print("%s: %d" % (item, amount))
        print("Cannot reach: %d locations" % (failed))
