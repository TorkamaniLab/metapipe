import cmd, textwrap

from metapipe import monty

""" The following is a borrowed and cut down version of this:
https://raw.githubusercontent.com/asweigart/textadventuredemo/master/textadventuredemo.py
"""

DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
GROUND = 'ground'
GROUNDDESC = 'grounddesc'
SHORTDESC = 'shortdesc'
LONGDESC = 'longdesc'
DESCWORDS = 'descwords'

SCREEN_WIDTH = 80

location = monty('Ebpxl Yrqtr')
inventory = [monty('Ubyl Unaq Teranqr bs Nagvbpu')]
health = 3
showFullExits = True


worldRooms = {
    monty('Ebpxl Yrqtr'): {
        DESC: monty('Lbh svaq lbhefrys ba n ebpxl bhgpebccvat fgerja jvgu ynetr obhyqref. Lbh ner whfg bhg bs fvtug bs gur pnir bs Pnreonaabt.'),
        EAST: monty('Pnir bs Pnreonaabt'),
        WEST: monty('Fprar 24'),
        GROUNDDESC: '',
        GROUND: []},
    monty('Pnir bs Pnreonaabt'): {
        DESC: '',
        WEST: monty('Ebpxl Yrqtr'),
        GROUNDDESC: '',
        GROUND: []},
    monty('Fprar 24'): {
        DESC: monty('Gurer vf fbzr irel ybiryl npgvat tbvat ba urer.'),
        EAST: monty('Ebpxl Yrqtr'),
        GROUND: []},
    }


worldItems = {
    monty('Ubyl Unaq Teranqr bs Nagvbpu'): {
        SHORTDESC: monty('Bar bs gur fnperq eryvpf gung Oebgure Znlaneq pneevrf jvgu uvz.'),
        LONGDESC: monty('Svefg funyg gubh gnxr bhg gur Ubyl Cva, gura funyg gubh pbhag gb guerr, ab zber, ab yrff. Guerr funyy or gur ahzore gubh funyg pbhag, naq gur ahzore bs gur pbhagvat funyy or guerr. Sbhe funyg gubh abg pbhag, arvgure pbhag gubh gjb, rkprcgvat gung gubh gura cebprrq gb guerr. Svir vf evtug bhg. Bapr gur ahzore guerr, orvat gur guveq ahzore, or ernpurq, gura yboorfg gubh gul Ubyl Unaq Teranqr bs Nagvbpu gbjneqf gul sbr, jub orvat anhtugl va Zl fvtug, funyy fahss vg.'),
        DESCWORDS: ['holy', 'hand', 'grenade', 'antioch']},
    }


def displayLocation(loc):
    print(loc)
    print('=' * len(loc))

    print('\n'.join(textwrap.wrap(worldRooms[loc][DESC], SCREEN_WIDTH)))

    if len(worldRooms[loc][GROUND]) > 0:
        print()
        for item in worldRooms[loc][GROUND]:
            print(worldItems[item][GROUNDDESC])

    exits = []
    for direction in (NORTH, SOUTH, EAST, WEST):
        if direction in worldRooms[loc].keys():
            exits.append(direction.title())
    print()
    if showFullExits:
        for direction in (NORTH, SOUTH, EAST, WEST):
            if direction in worldRooms[location]:
                print('%s: %s' % (direction.title(), worldRooms[location][direction]))
    else:
        print('Exits: %s' % ' '.join(exits))


def moveDirection(direction):
    global location

    if direction in worldRooms[location]:
        print('You move to the %s.' % direction)
        location = worldRooms[location][direction]
        displayLocation(location)
    else:
        print('You cannot move in that direction')


def getAllDescWords(itemList):
    itemList = list(set(itemList))
    descWords = []
    for item in itemList:
        descWords.extend(worldItems[item][DESCWORDS])
    return list(set(descWords))

def getAllFirstDescWords(itemList):
    itemList = list(set(itemList))
    descWords = []
    for item in itemList:
        descWords.append(worldItems[item][DESCWORDS][0])
    return list(set(descWords))

def getFirstItemMatchingDesc(desc, itemList):
    itemList = list(set(itemList))
    for item in itemList:
        if desc in worldItems[item][DESCWORDS]:
            return item
    return None

def getAllItemsMatchingDesc(desc, itemList):
    itemList = list(set(itemList))
    matchingItems = []
    for item in itemList:
        if desc in worldItems[item][DESCWORDS]:
            matchingItems.append(item)
    return matchingItems

class Tac(cmd.Cmd):
    prompt = '\n> '

    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    def do_quit(self, arg):
        """Quit the game."""
        return True

    def do_attack(self, arg):
        """Go to the area to the north, if possible."""
        attack(arg)

    def do_runaway(self, arg):
        """Go to the area to the south, if possible."""
        moveDirection('away')

    def do_north(self, arg):
        """Go to the area to the north, if possible."""
        moveDirection('north')

    def do_south(self, arg):
        """Go to the area to the south, if possible."""
        moveDirection('south')

    def do_east(self, arg):
        """Go to the area to the east, if possible."""
        moveDirection('east')

    def do_west(self, arg):
        """Go to the area to the west, if possible."""
        moveDirection('west')

    def do_exits(self, arg):
        """Toggle showing full exit descriptions or brief exit descriptions."""
        global showFullExits
        showFullExits = not showFullExits
        if showFullExits:
            print('Showing full exit descriptions.')
        else:
            print('Showing brief exit descriptions.')

    def do_use(self, args):
        pass

    def do_inventory(self, arg):
        """Display a list of the items in your possession."""

        if len(inventory) == 0:
            print('Inventory:\n  (nothing)')
            return

        itemCount = {}
        for item in inventory:
            if item in itemCount.keys():
                itemCount[item] += 1
            else:
                itemCount[item] = 1

        print('Inventory:')
        for item in set(inventory):
            if itemCount[item] > 1:
                print('  %s (%s)' % (item, itemCount[item]))
            else:
                print('  ' + item)

    def do_look(self, arg):
        lookingAt = arg.lower()
        if lookingAt == '':
            displayLocation(location)
            return

        if lookingAt == 'exits':
            for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
                if direction in worldRooms[location]:
                    print('%s: %s' % (direction.title(), worldRooms[location][direction]))
            return

        if lookingAt in ('north', 'west', 'east', 'south', 'n', 'w', 'e', 's'):
            if lookingAt.startswith('n') and NORTH in worldRooms[location]:
                print(worldRooms[location][NORTH])
            elif lookingAt.startswith('w') and WEST in worldRooms[location]:
                print(worldRooms[location][WEST])
            elif lookingAt.startswith('e') and EAST in worldRooms[location]:
                print(worldRooms[location][EAST])
            elif lookingAt.startswith('s') and SOUTH in worldRooms[location]:
                print(worldRooms[location][SOUTH])
            else:
                print('There is nothing in that direction.')
            return

        item = getFirstItemMatchingDesc(lookingAt, worldRooms[location][GROUND])
        if item != None:
            print('\n'.join(textwrap.wrap(worldItems[item][LONGDESC], SCREEN_WIDTH)))
            return

        item = getFirstItemMatchingDesc(lookingAt, inventory)
        if item != None:
            print('\n'.join(textwrap.wrap(worldItems[item][LONGDESC], SCREEN_WIDTH)))
            return

        print('You do not see that nearby.')


    def complete_look(self, text, line, begidx, endidx):
        possibleItems = []
        lookingAt = text.lower()

        invDescWords = getAllDescWords(inventory)
        groundDescWords = getAllDescWords(worldRooms[location][GROUND])
        shopDescWords = getAllDescWords(worldRooms[location].get(SHOP, []))

        for descWord in invDescWords + groundDescWords + shopDescWords + [NORTH, SOUTH, EAST, WEST, UP, DOWN]:
            if line.startswith('look %s' % (descWord)):
                return []

        if lookingAt == '':
            possibleItems.extend(getAllFirstDescWords(worldRooms[location][GROUND]))
            possibleItems.extend(getAllFirstDescWords(worldRooms[location].get(SHOP, [])))
            for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
                if direction in worldRooms[location]:
                    possibleItems.append(direction)
            return list(set(possibleItems))

        for descWord in groundDescWords:
            if descWord.startswith(lookingAt):
                possibleItems.append(descWord)

        for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
            if direction.startswith(lookingAt):
                possibleItems.append(direction)

        for descWord in invDescWords:
            if descWord.startswith(lookingAt):
                possibleItems.append(descWord)

        return list(set(possibleItems))
