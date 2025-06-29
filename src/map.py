from cave import Cave, Shop
from item import Item
from character import Ninja
from character import Enemy
from character import Friendly
from character import Boss
import random


class MapGraph:
    """Represents the in-game map of caves with a graph data structure

    You probably want to call the static method "generate" on this to
    instantiate a pre-generated MapGraph with all the caves already filled in.

    Each cave is a node whilst the available paths between caves is treated as
    an edge. The graph's data is stored within a 2D list (matrix). Currently,
    the graph is NOT expandable (size passed at instantiation is fixed)!

    This graph is undirected; if A -> B, then likewise B -> A implicitly.
    """

    def __init__(self, game, size):
        self.game = game
        self.size = size
        # create the 2d-list for storing the connections
        # starts out like
        # [
        #  # A  B  C
        #   [0, 0, 0] # A
        #   [0, 0, 0] # B
        #   [0, 0, 0] # C
        # ]
        # it is square, where A, B & C are caves and a 1 in the square between
        # caves means that they are linked. e.g. if the top right square between
        # C and A were flipped to a 1, then the caves C and A would be linked.
        # see the add_edge method for impl details
        self.matrix = [[0] * size for _ in range(size)]

        # list for storing the caves themselves, mapping them to their node IDs
        # in this graph
        self.cave_data = [None] * size

    def __add_edge(self, a, b):
        """Add a link between node `a` and `b`"""

        # a and b must be greater than or eq to 0 (min ID) and less than the
        # total size of the matrix. also self-linking is prohibited, a != b
        if 0 <= a < self.size and 0 <= b < self.size and a != b:
            self.matrix[a][b] = 1
            # also create a back-link B -> A
            self.matrix[b][a] = 1

    def __add_cave(self, cave, links):
        """Add a new Cave to the map, with a list of caves it is linked to

        Providing a cave with a duplicate number will OVERWRITE the existing
        cave but will NOT alter the existing links on the map, if any exist.

        Note: back-links are automatically handled for so there is no need to
        specify them.
        """

        # add cave to data list
        self.cave_data[cave.num] = cave

        # loop over linked caves and add an edge between them, linking them
        # together
        for link in links:
            self.__add_edge(cave.num, link)

    @staticmethod
    def generate(game):
        # Character list
        bats = Enemy("Bat", "A small filthy creature with sharp teeth", None)
        meatsack = Enemy("Jagrit", "A chunk of meat. Quite fat in fact, like a juggernaut", None)
        magri = Friendly("The Manual Sagri", "Short haired, bisexual boy who loves to fondle cosmo, his cat.", None)

        # Boss
        shogun = Boss("Shogun of Bizarre", "A strong and vigilant samurai with a long and sharp katana in hand.", None)
        shogun.set_weakness("Crossbow")

        """Generate a new MapGraph with caves"""

        new_map = MapGraph(game, 13)
        new_map.__add_cave(Cave(
            1, "Cave", "A small cave underground. No light seeps through although there are cracks in the ceiling", new_map), [])

        shop = Shop(
            2, "A nice and cozy room with a counter and some products", new_map)
        shop.add_shop_item(Item("Axe", "🪓", "A sharpened hatchet", 15))
        new_map.__add_cave(shop, [1])
        new_map.__add_cave(Cave(
            3, "Pit", "Deep, dark, bottomless, hole. Take care with your footing", new_map), [1])

        cave4 = Cave(
            4, "Dungeon", "Echoes of unseen horrors lurk beyond the flickering torchlight", new_map)
        ninja = Ninja(cave4)
        cave4.add_character(ninja)
        new_map.__add_cave(cave4, [1])

        cave5 = Cave(5, "Dungeon", "A large room with some equipment and metallic racks", new_map)
        new_map.__add_cave(cave5, [1])
        cave5.add_character(bats)

        new_map.__add_cave(Cave(
            6, "Lava Tube", "A long, cold tunnel", new_map), [3, 2])
        
        cave7 = Cave(
            7, "Grotto", "A cathedral of stone where time pools in the hush of dripping stalactites", new_map)
        new_map.__add_cave(cave7, [5, 3])
        cave7.add_character(meatsack)

        new_map.__add_cave(Cave(
            8, "Shop", "A nice and cozy room with a counter and some products", new_map), [4, 5])
        new_map.__add_cave(Cave(
            9, "Pit", "Deep, dark, bottomless, hole. Take care with your footing", new_map), [2, 4])
        
        cave10 = Cave(10, "Cave", "A small cave underground. A glimpse of light and some gentle gusts of air seep through the gaps between the rocks", new_map)
        new_map.__add_cave(cave10, [8, 9])
        cave10.add_character(bats)
        
        cave11 = Cave(
            11, "Cavern", "An enormous space with a throne-like chair in the middle.", new_map)
        new_map.__add_cave(cave11, [8, 7])
        cave11.add_character(shogun)

        cave12 = Cave(
            12, "Grotto", "A shadowed sanctuary where time drips like water from the jagged limestone.", new_map)
        new_map.__add_cave(cave12, [6, 7])
        cave12.add_character(magri)

        return new_map

    def random_cave(self):
        """Return a random cave"""
        return random.choice(self.cave_data)

    def get_cave(self, num):
        """Get a cave by number"""
        if num >= self.size:
            return None

        return self.cave_data[num]

    def check_link(self, a, b):
        """Check whether cave number A is linked to cave number B

        Accepts numbers only.
        """

        if a >= self.size or b >= self.size:
            return False

        return self.matrix[a][b] == 1

    def linked_caves(self, cave):
        """Return all the caves linked to the provided cave

        Pass a Cave instance, and returns a list of Cave instances
        """

        # Find linked caves
        links = self.matrix[cave.num]

        linked_caves = []
        for (i, link) in enumerate(links):
            # for every link that is valid (== 1)
            if link == 1:
                # find that cave and append it to the linked_caves list
                linked_caves.append(self.cave_data[i])

        return linked_caves
