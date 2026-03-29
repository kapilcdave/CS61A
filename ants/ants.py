"""Ants Vs. SomeBees."""

from __future__ import annotations  # Enable forward references in type hints
import random  # Import random for choosing random bees/exits
from ucb import main, interact, trace  # Import utilities
from collections import OrderedDict  # Import OrderedDict for maintaining insertion order

################
# Core Classes #
################


class Place:
    """A Place holds insects and has an exit to another Place."""
    is_hive = False

    def __init__(self, name: str, exit: Place | None = None):
        """Create a Place with the given NAME and EXIT.

        name -- A string; the name of this Place.
        exit -- The Place reached by exiting this Place (may be None).
        """
        self.name = name  # Store the place name
        self.exit = exit  # Link going toward the hive
        self.bees: list[Bee] = []  # Initialize empty bee list
        self.ant: Ant | None = None  # No ant initially
        self.entrance: Place | None = None  # Will be set later
        # Phase 1: Add an entrance to the exit
        # BEGIN Problem 2
        if self.exit is not None:  # If this place has an exit
            self.exit.entrance = self  # Set that place's entrance to this place
        # END Problem 2

    def add_insect(self, insect: Insect):
        """Asks the insect to add itself to this place. This method exists so
        that it can be overridden in subclasses.
        """
        insect.add_to(self)  # Delegate to insect's add_to method

    def remove_insect(self, insect: Insect):
        """Asks the insect to remove itself from this place. This method exists so
        that it can be overridden in subclasses.
        """
        insect.remove_from(self)  # Delegate to insect's remove_from method

    def __str__(self) -> str:  # String representation
        return self.name  # Return the place's name


class Insect:
    """An Insect, the base class of Ant and Bee, has health and a Place."""

    next_id = 0  # Class variable for assigning unique IDs
    damage = 0  # Default damage value
    is_waterproof = False  # Default: not waterproof
    # ADD CLASS ATTRIBUTES HERE

    def __init__(self, health: int, place: Place | None = None):
        """Create an Insect with a health and a starting PLACE."""
        self.health = health  # Store current health
        self.full_health = health  # Store original health
        self.place = place  # Store current place

        # assign a unique ID to every insect
        self.id = Insect.next_id  # Assign unique ID
        Insect.next_id += 1  # Increment counter

    def reduce_health(self, damage_taken: float):
        """Reduce health by DAMAGE_TAKEN, and remove the insect from its place if it
        has no health remaining. Decorated in gui.py for GUI support.

        >>> test_insect = Insect(5)
        >>> test_insect.reduce_health(2)
        >>> test_insect.health
        3
        """
        self.health -= damage_taken  # Subtract damage from health
        if self.health <= 0:  # Check if dead
            self.zero_health_callback()  # Call death callback

            if self.place is not None:  # If in a place
                self.place.remove_insect(self)  # Remove from play

    def action(self, gamestate: GameState):
        """The action performed each turn."""

    def zero_health_callback(self):
        """
        Called when health reaches 0 or below.
        Decorated in gui.py to support GUI
        """

    def add_to(self, place: Place):  # Add insect to place
        self.place = place  # Update reference

    def remove_from(self, place: Place):  # Remove insect from place
        self.place = None  # Clear reference

    def __repr__(self):  # String representation
        cname = type(self).__name__  # Get class name
        return '{0}({1}, {2})'.format(cname, self.health, self.place)  # Format string


class Ant(Insect):
    """An Ant occupies a place and does work for the colony."""

    implemented = False  # Only deployable if True
    food_cost = 0  # Cost in food
    is_container = False  # Can contain other ants
    # ADD CLASS ATTRIBUTES HERE
    # BEGIN Problem 8a
    "*** YOUR CODE HERE ***"
    # END Problem 8a

    def __init__(self, health: int = 1):
        super().__init__(health)

    def can_contain(self, other: Ant) -> bool:  # Check if can contain
        return False  # Regular ants can't contain

    def store_ant(self, ant: Ant):  # Store ant inside
        assert False, "{0} cannot contain an ant".format(self)  # Error

    def remove_ant(self, ant: Ant):  # Remove stored ant
        assert False, "{0} cannot contain an ant".format(self)  # Error

    def add_to(self, place: Place):  # Add ant to place
        if place.ant is None:  # Place empty
            place.ant = self  # Place directly
        else:  # Place occupied
            # BEGIN Problem 8b
            if place.ant.can_contain(self):  # Existing can contain this
                place.ant.store_ant(self)  # Store inside
            elif self.can_contain(place.ant):  # This can contain existing
                original_ant = place.ant  # Save existing
                place.ant = self  # Replace with this
                self.store_ant(original_ant)  # Store existing inside
            else:  # Neither can contain
                assert place.ant is None, 'Too many ants in {0}'.format(place)  # Error
            # END Problem 8b
        Insect.add_to(self, place)  # Call parent

    def remove_from(self, place: Place):  # Remove ant from place
        if place.ant is self:  # Directly in place
            place.ant = None  # Clear slot
        elif place.ant is None:  # Place empty
            assert False, '{0} is not in {1}'.format(self, place)  # Error
        else:  # Inside container
            place.ant.remove_ant(self)  # Tell container
        Insect.remove_from(self, place)  # Call parent

    def double(self):  # Double this ant's damage
        """Double this ants's damage, if it has not already been doubled."""
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"  # Placeholder
        # END Problem 12


class HarvesterAnt(Ant):
    """HarvesterAnt produces 1 additional food per turn for the colony."""

    name = 'Harvester'  # Name
    implemented = True  # Deployable
    food_cost = 2  # Cost
    initial_health = 1  # Health

    def action(self, gamestate: GameState):  # Each turn
        """Produce 1 additional food for the colony.

        gamestate -- The GameState, used to access game state information.
        """
        # BEGIN Problem 1
        gamestate.food += 1  # Add 1 food
        # END Problem 1


class ThrowerAnt(Ant):  # Thrower ant - attacks bees
    """ThrowerAnt throws a leaf each turn at the nearest Bee in its range."""

    name = 'Thrower'  # Name
    implemented = True  # Deployable
    damage = 1  # Damage
    food_cost = 3  # Cost
    initial_health = 1  # Health
    lower_bound = 0  # Min distance
    upper_bound = float('inf')  # Max distance

    def nearest_bee(self) -> Bee | None:  # Find nearest bee
        """Return a random Bee from the nearest Place (excluding the Hive) that contains Bees and is reachable from
        the ThrowerAnt's Place by following entrances.

        This method returns None if there is no such Bee (or none in range).
        """
        if not self.place:  # Not placed
            return None  # No bee
        # BEGIN Problem 3 and 4
        current_place = self.place  # Start here
        distance = 0  # Init distance
        while current_place is not None and not current_place.is_hive:  # Traverse
            if current_place.bees and self.lower_bound <= distance <= self.upper_bound:  # In range
                return random_bee(current_place.bees)  # Return random bee
            current_place = current_place.entrance  # Move backward
            distance += 1  # Increment distance
            if distance > self.upper_bound:  # Too far
                break  # Stop
        return None  # None found
        # END Problem 3 and 4

    def throw_at(self, target: Bee | None):  # Throw at target
        """Throw a leaf at the target Bee, reducing its health."""
        if target is not None:  # If target exists
            target.reduce_health(self.damage)  # Damage it

    def action(self, gamestate: GameState):  # Each turn
        """Throw a leaf at the nearest Bee in range."""
        self.throw_at(self.nearest_bee())  # Find and throw


def random_bee(bees: list[Bee]) -> Bee | None:  # Pick random bee
    """Return a random bee from a list of bees, or return None if bees is empty."""
    assert isinstance(bees, list), \  # Check type
        "random_bee's argument should be a list but was a %s" % type(bees).__name__  # Error msg
    if bees:  # If list not empty
        return random.choice(bees)  # Return random

##############
# Extensions #
##############


class ShortThrower(ThrowerAnt):  # Short range thrower
    """A ThrowerAnt that only throws leaves at Bees at most 3 places away."""

    name = 'Short'  # Name
    food_cost = 2  # Cost
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 4
    lower_bound = 0  # Min 0
    upper_bound = 3  # Max 3
    implemented = True  # Deployable
    # END Problem 4


class LongThrower(ThrowerAnt):  # Long range thrower
    """A ThrowerAnt that only throws leaves at Bees at least 5 places away."""

    name = 'Long'  # Name
    food_cost = 2  # Cost
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 4
    lower_bound = 5  # Min 5
    upper_bound = float('inf')  # Max infinity
    implemented = True  # Deployable
    # END Problem 4


class FireAnt(Ant):  # Fire ant - explodes on death
    """FireAnt cooks any Bee in its Place when it expires."""

    name = 'Fire'  # Name
    damage = 3  # Explosion damage
    food_cost = 5  # Cost
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 5
    initial_health = 3  # Health
    implemented = True  # Deployable
    # END Problem 5

    def __init__(self, health: int = 3):  # Init
        """Create an Ant with a HEALTH quantity."""
        super().__init__(health)  # Call parent

    def reduce_health(self, damage_taken: float):  # Take damage
        """Reduce health by DAMAGE_TAKEN, and remove the FireAnt from its place if it
        has no health remaining.

        Make sure to reduce the health of each bee in the current place, and apply
        the additional damage if the fire ant dies.
        """
        # BEGIN Problem 5
        current_place = self.place  # Get place
        bees_to_hit = list(current_place.bees)  # List bees
        for bee in bees_to_hit:  # For each bee
            bee.reduce_health(damage_taken)  # Damage it
        Ant.reduce_health(self, damage_taken)  # Damage self
        if self.health <= 0:  # If dying
            for bee in bees_to_hit:  # For each bee
                if bee.health > 0:  # If alive
                    bee.reduce_health(self.damage)  # Explosion damage
        # END Problem 5

# BEGIN Problem 6
# The WallAnt class
class WallAnt(Ant):  # Wall ant - tank
    name = 'Wall'  # Name
    food_cost = 4  # Cost
    implemented = True  # Deployable
    def __init__(self, health=4):  # Init with 4 health
        super().__init__(health)  # Call parent
# END Problem 6

# BEGIN Problem 7
# The HungryAnt Class
class HungryAnt(Ant):  # Hungry ant - eats bees
    name = 'Hungry'  # Name
    food_cost = 4  # Cost
    chew_cooldown = 3  # Cooldown after eating
    implemented = True  # Deployable
    def __init__(self, health=1):  # Init
        super().__init__(health)  # Call parent
        self.cooldown = 0  # Start not chewing
    def action(self, gamestate):  # Each turn
        if self.cooldown > 0:  # Chewing
            self.cooldown -= 1  # Decrement
        else:  # Not chewing
            bee = random_bee(self.place.bees)  # Pick bee
            if bee:  # If one exists
                bee.reduce_health(bee.health)  # Eat it (kill)
                self.cooldown = self.chew_cooldown  # Start cooldown
# END Problem 7


class ContainerAnt(Ant):  # Container ant - holds other ants
    """
    ContainerAnt can share a space with other ants by containing them.
    """
    is_container = True  # Mark as container

    def __init__(self, health: int):  # Init
        super().__init__(health)  # Call parent
        self.ant_contained = None  # No ant inside yet

    def can_contain(self, other: Ant) -> bool:  # Check if can contain
        # BEGIN Problem 8a
        return self.ant_contained is None and not other.is_container  # Empty and other not container
        # END Problem 8a

    def store_ant(self, ant: Ant):  # Store ant inside
        # BEGIN Problem 8a
        self.ant_contained = ant  # Store it
        # END Problem 8a

    def remove_ant(self, ant: Ant):  # Remove contained ant
        if self.ant_contained is not ant:  # Check it's there
            assert False, "{} does not contain {}".format(self, ant)  # Error if not
        self.ant_contained = None  # Remove it

    def remove_from(self, place: Place):  # Remove container
        # Special handling for container ants
        if place.ant is self:  # Container is slot ant
            # Container was removed. Contained ant should remain in the game
            place.ant = self.ant_contained  # Contained ant takes slot
            Insect.remove_from(self, place)  # Remove container
        else:  # Contained ant being removed
            # default to normal behavior
            Ant.remove_from(self, place)  # Normal removal

    def action(self, gamestate: GameState):  # Each turn
        # BEGIN Problem 8a
        if self.ant_contained is not None:  # If containing ant
            self.ant_contained.action(gamestate)  # Let it act
        # END Problem 8a


class ProtectorAnt(ContainerAnt):  # Protector ant - container
    """ProtectorAnt provides protection to other Ants."""

    name = 'Protector'  # Name
    food_cost = 4  # Cost
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 8c
    implemented = True  # Deployable
    def __init__(self, health=2):  # Init with 2 health
        super().__init__(health)  # Call parent
    # END Problem 8c

# BEGIN Problem 9
# The TankAnt class
class TankAnt(ContainerAnt):  # Tank ant - container that deals damage
    name = 'Tank'  # Name
    damage = 1  # Damage each turn
    food_cost = 6  # Cost
    implemented = True  # Deployable
    def __init__(self, health=2):  # Init with 2 health
        super().__init__(health)  # Call parent
    def action(self, gamestate):  # Each turn
        super().action(gamestate)  # Let contained ant act
        bees_in_place = list(self.place.bees)  # Get bees
        for bee in bees_in_place:  # For each bee
            bee.reduce_health(self.damage)  # Damage it
# END Problem 9


class Water(Place):  # Water place - kills non-waterproof ants
    """Water is a place that can only hold waterproof insects."""

    def add_insect(self, insect: Insect):  # Add insect to water
        """Add an Insect to this place. If the insect is not waterproof, reduce
        its health to 0."""
        # BEGIN Problem 10
        Place.add_insect(self, insect)  # Add normally
        if not insect.is_waterproof:  # Not waterproof
            insect.reduce_health(insect.health)  # Kill it
        # END Problem 10

# BEGIN Problem 11
# The ScubaThrower class
class ScubaThrower(ThrowerAnt):  # Scuba thrower - waterproof
    name = 'Scuba'  # Name
    food_cost = 6  # Cost
    is_waterproof = True  # Can traverse water
    implemented = True  # Deployable

# END Problem 11


class QueenAnt(ThrowerAnt):  # Queen ant - boosts others and loses on death
    """QueenAnt boosts the damage of all ants behind her."""

    name = 'Queen'  # Name
    food_cost = 7  # Cost
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem 12
    implemented = True  # Deployable
    # END Problem 12

    def action(self, gamestate: GameState):  # Each turn
        """A queen ant throws a leaf, but also doubles the damage of ants
        in her tunnel.
        """
        # BEGIN Problem 12
        super().action(gamestate)  # Throw like thrower
        current_place = self.place.exit  # Next place
        while current_place is not None:  # Travel
            ant = current_place.ant  # Get ant
            if ant is not None:  # If ant here
                self.double_ant(ant)  # Double it
                if ant.is_container and ant.ant_contained is not None:  # Container
                    self.double_ant(ant.ant_contained)  # Double contained too
            current_place = current_place.exit  # Move forward
    
    def double_ant(self, ant):  # Double an ant's damage
        if not hasattr(ant, 'doubled'):  # Not doubled yet
            ant.damage *= 2  # Double damage
            ant.doubled = True  # Mark as doubled
        # END Problem 12

    def reduce_health(self, damage_taken: float):  # Take damage
        """Reduce health by DAMAGE_TAKEN, and if the QueenAnt has no health
        remaining, signal the end of the game.
        """
        # BEGIN Problem 12
        super().reduce_health(damage_taken)  # Take damage
        if self.health <= 0:  # If dies
            ants_lose()  # Ants lose
        # END Problem 12


################
# Extra Challenge #
################

class SlowThrower(ThrowerAnt):  # Slow thrower - EC
    """ThrowerAnt that causes Slow on Bees."""

    name = 'Slow'  # Name
    food_cost = 6  # Cost
    # BEGIN Problem EC 1
    implemented = False  # Not enabled
    # END Problem EC 1

    def throw_at(self, target: Bee | None):  # Throw at target
        # BEGIN Problem EC 1
        "*** YOUR CODE HERE ***"  # Placeholder
        # END Problem EC 1


class ScaryThrower(ThrowerAnt):  # Scary thrower - EC
    """ThrowerAnt that intimidates Bees, making them back away instead of advancing."""

    name = 'Scary'  # Name
    food_cost = 6  # Cost
    # BEGIN Problem EC 2
    implemented = False  # Not enabled
    # END Problem EC 2

    def throw_at(self, target: Bee | None):  # Throw at target
        # BEGIN Problem EC 2
        "*** YOUR CODE HERE ***"  # Placeholder
        # END Problem EC 2


class NinjaAnt(Ant):  # Ninja ant - EC
    """NinjaAnt does not block the path and damages all bees in its place."""

    name = 'Ninja'  # Name
    damage = 1  # Damage
    food_cost = 5  # Cost
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem EC 3
    implemented = False  # Not enabled
    # END Problem EC 3

    def action(self, gamestate: GameState):  # Each turn
        # BEGIN Problem EC 3
        "*** YOUR CODE HERE ***"  # Placeholder
        # END Problem EC 3


class LaserAnt(ThrowerAnt):  # Laser ant - EC
    """ThrowerAnt that damages all Insects standing in its path."""

    name = 'Laser'  # Name
    food_cost = 10  # Cost
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN Problem EC 4
    implemented = False  # Not enabled
    # END Problem EC 4

    def __init__(self, health: int = 1):  # Init
        super().__init__(health)  # Call parent
        self.insects_shot = 0  # Track kills

    def insects_in_front(self) -> dict[Bee, int]:  # Get insects in path
        # BEGIN Problem EC 4
        return {}  # Placeholder
        # END Problem EC 4

    def calculate_damage(self, distance: int) -> float:  # Damage by distance
        # BEGIN Problem EC 4
        return 0  # Placeholder
        # END Problem EC 4

    def action(self, gamestate: GameState):  # Each turn
        insects_and_distances = self.insects_in_front()  # Get insects
        LaserAnt.play_sound_effect()  # Play sound
        for insect, distance in insects_and_distances.items():  # For each
            damage = self.calculate_damage(distance)  # Get damage
            insect.reduce_health(damage)  # Damage it
            if damage:  # If damaged
                self.insects_shot += 1  # Track

    @classmethod
    def play_sound_effect(cls):  # Play sound
        """Play laser sound effect. Decorated in gui.py"""
        pass  # Decorated


########
# Bees #
########

class Bee(Insect):  # Bee - the enemy
    """A Bee moves from place to place, following exits and stinging ants."""

    name = 'Bee'  # Name
    damage = 1  # Damage
    is_waterproof = True  # Can cross water


    def sting(self, ant: Ant):  # Attack ant
        """Attack an ANT, reducing its health by 1."""
        ant.reduce_health(self.damage)  # Damage it

    def move_to(self, place: Place):  # Move to place
        """Move from the Bee's current Place to a new PLACE."""
        if self.place is not None:  # If current place exists
            self.place.remove_insect(self)  # Remove from it

        if place is not None:  # If new place exists
            place.add_insect(self)  # Add to it

    def blocked(self) -> bool:  # Check if blocked
        """Return True if this Bee cannot advance to the next Place."""
        # Special handling for NinjaAnt
        # BEGIN Problem EC 3
        return self.place is not None and self.place.ant is not None  # Blocked if ant here
        # END Problem EC 3

    def action(self, gamestate: GameState):  # Each turn
        """A Bee's action stings the Ant that blocks its exit if it is blocked,
        or moves to the exit of its current place otherwise.

        gamestate -- The GameState, used to access game state information.
        """
        destination = None  # Init destination
        if self.place:  # If placed
            destination = self.place.exit  # Next place


        if self.blocked() and self.place and self.place.ant:  # Blocked
            self.sting(self.place.ant)  # Attack
        elif self.health > 0 and destination is not None:  # Can move
            self.move_to(destination)  # Move forward

    def add_to(self, place: Place):  # Add bee to place
        place.bees.append(self)  # Add to place's list
        super().add_to(place)  # Call parent

    def remove_from(self, place: Place):  # Remove bee from place
        place.bees.remove(self)  # Remove from list
        super().remove_from(place)  # Call parent

    def scare(self, length: int):  # Scare bee
        """
        If this Bee has not been scared before, cause it to attempt to
        go backwards LENGTH times.
        """
        # BEGIN Problem EC 2
        "*** YOUR CODE HERE ***"  # Placeholder
        # END Problem EC 2


class Wasp(Bee):  # Wasp - strong bee
    """Class of Bee that has higher damage."""
    name = 'Wasp'  # Name
    damage = 2  # Higher damage


class Boss(Wasp):  # Boss bee - final boss
    """The leader of the bees. Damage to the boss by any attack is capped.
    """
    name = 'Boss'  # Name
    damage_cap = 8  # Max damage

    def reduce_health(self, damage_taken: float):  # Take damage
        super().reduce_health(min(damage_taken, self.damage_cap))  # Cap damage

    @classmethod
    def play_sound_effect(cls):  # Play sound
        "Play sound effect when boss arrives! Decorated in gui.py"  # Sound
        pass  # Decorated


class Hive(Place):  # Hive - bee spawn location
    """The Place from which the Bees launch their assault.

    assault_plan -- An AssaultPlan; when & where bees enter the colony.
    """
    is_hive = True  # Mark as hive

    def __init__(self, assault_plan: AssaultPlan):  # Init
        self.name = 'Hive'  # Name
        self.assault_plan = assault_plan  # Store plan
        self.bees: list[Bee] = []  # Init bee list
        for bee in assault_plan.all_bees():  # For each bee
            self.add_insect(bee)  # Add it
        # The following attributes are always None for a Hive
        self.entrance: None = None  # No entrance
        self.ant: None = None  # No ants
        self.exit: Place | None = None  # No exit

    def strategy(self, gamestate: GameState):  # Deploy bees
        exits = [p for p in gamestate.places.values() if p.entrance is self]  # Get entrances

        for bee in self.assault_plan.get(gamestate.time, []):  # Get scheduled bees
            if Boss in bee.__class__.__mro__:  # If boss bee
                Boss.play_sound_effect()  # Play sound
                GameState.display_notification('Boss Bee is Here!')  # Show message
            bee.move_to(random.choice(exits))  # Send to random entrance
            gamestate.active_bees.append(bee)  # Add to active

###################
# Game Components #
###################

class GameState:  # Game state manager
    """An ant collective that manages global game state and simulates time.

    Attributes:
    time -- elapsed time
    food -- the colony's available food total
    places -- A list of all places in the colony (including a Hive)
    bee_entrances -- A list of places that bees can enter
    """

    def __init__(self, beehive: Hive, ant_types: list, create_places, dimensions, food: int = 2):  # Init
        """Create an GameState for simulating a game.

        Arguments:
        beehive -- a Hive full of bees
        ant_types -- a list of ant classes
        create_places -- a function that creates the set of places
        dimensions -- a pair containing the dimensions of the game layout
        """
        self.time: int = 0  # Start at turn 0
        self.food = food  # Set initial food
        self.beehive = beehive  # Store hive
        self.ant_types = OrderedDict((a.name, a) for a in ant_types)  # Map names to classes
        self.dimensions = dimensions  # Store dimensions
        self.active_bees: list = []  # Init active bees
        self.configure(beehive, create_places)  # Set up board

    def configure(self, beehive: Hive, create_places):  # Set up board
        """Configure the places in the colony."""
        self.base: AntHomeBase = AntHomeBase('Ant Home Base')  # Create base
        self.places: OrderedDict = OrderedDict()  # Init places
        self.bee_entrances: list = []  # Init entrances

        def register_place(place: Place, is_bee_entrance: bool):  # Register helper
            self.places[place.name] = place  # Add to dict
            if is_bee_entrance:  # If entrance
                place.entrance = beehive  # Connect to hive
                self.bee_entrances.append(place)  # Track entrance
        register_place(self.beehive, False)  # Register hive
        create_places(self.base, register_place,  # Create layout
                      self.dimensions[0], self.dimensions[1])  # With dimensions

    def ants_take_actions(self):  # Ants act
        for ant in self.ants:  # For each ant
            if ant.health > 0:  # If alive
                ant.action(self)  # Call action

    def bees_take_actions(self, num_bees: int) -> int:  # Bees act
        for bee in self.active_bees[:]:  # For each bee (copy)
            if bee.health > 0:  # If alive
                bee.action(self)  # Call action
            if bee.health <= 0:  # If died
                num_bees -= 1  # Decrement count
                self.active_bees.remove(bee)  # Remove
        if num_bees == 0:  # All defeated
            GameState.play_win_sound()  # Play sound
            raise AntsWinException()  # Win
        return num_bees  # Return count

    def simulate(self):  # Main game loop
        """Simulate an attack on the ant colony. This is called by the GUI to play the game."""
        num_bees = len(self.bees)  # Count bees
        try:  # Wrap
            while True:  # Loop
                self.beehive.strategy(self)  # Deploy bees
                yield None  # Pause for player
                self.ants_take_actions()  # Ants act
                self.time += 1  # Advance time
                yield None  # Pause for animation
                num_bees = self.bees_take_actions(num_bees)  # Bees act
        except AntsWinException:  # Ants win
            print('All bees are vanquished. You win!')  # Message
            yield True  # Signal
        except AntsLoseException:  # Ants lose
            print('The bees reached homebase or the queen ant queen has perished. Please try again :(')
            yield False  # Signal

    def deploy_ant(self, place_name: str, ant_type_name: str) -> Ant | None:  # Deploy ant
        """Place an ant if enough food is available.

        This method is called by the current strategy to deploy ants.
        """
        ant_type = self.ant_types[ant_type_name]  # Get class
        if ant_type.food_cost > self.food:  # Not enough food
            message = 'Not enough food!'  # Message
            print(message)  # Print
            GameState.display_notification(message)  # Show
        else:  # Enough food
            ant: Ant = ant_type()  # Create
            self.places[place_name].add_insect(ant)  # Place
            self.food -= ant.food_cost  # Deduct
            return ant  # Return

    def remove_ant(self, place_name: str):  # Remove ant
        """Remove an Ant from the game."""
        place = self.places[place_name]  # Get place
        if place.ant is not None:  # If ant here
            place.remove_insect(place.ant)  # Remove

    @staticmethod
    def display_notification(message):  # Display message
        """Display a notification! Decorated in gui.py for GUI support"""
        pass  # Decorated

    @classmethod
    def play_win_sound(cls):  # Play sound
        """Play the sound effect when ants win! Decorated in gui.py"""
        pass  # Decorated

    @property
    def ants(self):  # Get all ants
        return [p.ant for p in self.places.values() if p.ant is not None]  # List

    @property
    def bees(self):  # Get all bees
        return [b for p in self.places.values() for b in p.bees]  # List

    @property
    def insects(self):  # Get all insects
        return self.ants + self.bees  # Combined

    def __str__(self):  # String repr
        status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)  # Format
        return str([str(i) for i in self.ants + self.bees]) + status  # Return


class AntHomeBase(Place):  # Home base - bee reaches = loss
    """AntHomeBase at the end of the tunnel, where the queen normally resides."""

    def add_insect(self, insect):  # Add insect
        """Add an Insect to this Place.

        Can't actually add Ants to a AntHomeBase. However, if a Bee attempts to
        enter the AntHomeBase, a AntsLoseException is raised, signaling the end
        of a game.
        """
        assert isinstance(insect, Bee), 'Cannot add {0} to AntHomeBase'  # Only bees
        raise AntsLoseException()  # Lose


def ants_win():  # Win signal
    """Signal that Ants win."""
    raise AntsWinException()  # Raise


def ants_lose():  # Loss signal
    """Signal that Ants lose."""
    raise AntsLoseException()  # Raise


def ant_types() -> list:  # Get ant list
    """Return a list of all implemented Ant classes."""
    all_ant_types: list = []  # Init
    new_types: list = [Ant]  # Start with Ant
    while new_types:  # While have types
        new_types = [t for c in new_types for t in c.__subclasses__()]  # Get children
        all_ant_types.extend(new_types)  # Add them
    return [t for t in all_ant_types if t.implemented]  # Return implemented


def bee_types() -> list:  # Get bee list
    """Return a list of all implemented Bee classes."""
    all_bee_types: list = []  # Init
    new_types: list = [Bee]  # Start with Bee
    while new_types:  # While have types
        new_types = [t for c in new_types for t in c.__subclasses__()]  # Get children
        all_bee_types.extend(new_types)  # Add them
    return all_bee_types  # Return all


class GameOverException(Exception):  # Base exception
    """Base game over Exception."""
    pass  # Base


class AntsWinException(GameOverException):  # Win exception
    """Exception to signal that the ants win."""
    pass  # Inherits


class AntsLoseException(GameOverException):  # Loss exception
    """Exception to signal that the ants lose."""
    pass  # Inherits


###########
# Layouts #
###########


def wet_layout(queen: AntHomeBase, register_place, tunnels: int = 3, length: int = 9, moat_frequency: int = 3):  # Create layout with water
    """Register a mix of wet and and dry places."""
    for tunnel in range(tunnels):  # For each tunnel
        exit = queen  # Start from base
        for step in range(length):  # For each step
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:  # Water?
                exit = Water('water_{0}_{1}'.format(tunnel, step), exit)  # Create water
            else:  # Land
                exit = Place('tunnel_{0}_{1}'.format(tunnel, step), exit)  # Create place
            register_place(exit, step == length - 1)  # Register


def dry_layout(queen: AntHomeBase, register_place, tunnels: int = 3, length: int = 9):  # Create dry layout
    """Register dry tunnels."""
    wet_layout(queen, register_place, tunnels, length, 0)  # No water


#################
# Assault Plans #
#################

class AssaultPlan(dict):  # Assault plan - bee schedule
    """The Bees' plan of attack for the colony.  Attacks come in timed waves.

    An AssaultPlan is a dictionary from times (int) to waves (list of Bees).

    >>> AssaultPlan().add_wave(4, 2)
    {4: [Bee(3, None), Bee(3, None)]}
    """
    def add_wave(self, bee_type, bee_health: int, time: int, count: int) -> AssaultPlan:  # Add wave
        """Add a wave at time with count Bees that have the specified health."""
        bees = [bee_type(bee_health) for _ in range(count)]  # Create bees
        self.setdefault(time, []).extend(bees)  # Add to time slot
        return self  # Return self

    def all_bees(self) -> list:  # Get all bees
        """Place all Bees in the beehive and return the list of Bees."""
        return [bee for wave in self.values() for bee in wave]