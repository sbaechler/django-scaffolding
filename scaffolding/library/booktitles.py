# -*- coding: utf-8 -*-
""" taken from http://mdbenoit.com/rtg.htm """
from __future__ import unicode_literals
import random

NOUNS = (
    "Dream", "Dreamer", "Dreams", "Waves",
    "Sword", "Kiss", "Sex", "Lover",
    "Slave", "Slaves", "Pleasure", "Servant",
    "Servants", "Snake", "Soul", "Touch",
    "Men", "Women", "Gift", "Scent",
    "Ice", "Snow", "Night", "Silk", "Secret", "Secrets",
    "Game", "Fire", "Flame", "Flames",
    "Husband", "Wife", "Man", "Woman", "Boy", "Girl",
    "Truth", "Edge", "Boyfriend", "Girlfriend",
    "Body", "Captive", "Male", "Wave", "Predator",
    "Female", "Healer", "Trainer", "Teacher",
    "Hunter", "Obsession", "Hustler", "Consort",
    "Dream", "Dreamer", "Dreams", "Rainbow",
    "Dreaming", "Flight", "Flying", "Soaring",
    "Wings", "Mist", "Sky", "Wind",
    "Winter", "Misty", "River", "Door",
    "Gate", "Cloud", "Fairy", "Dragon",
    "End", "Blade", "Beginning", "Tale",
    "Tales", "Emperor", "Prince", "Princess",
    "Willow", "Birch", "Petals", "Destiny",
    "Theft", "Thief", "Legend", "Prophecy",
    "Spark", "Sparks", "Stream", "Streams", "Waves",
    "Sword", "Darkness", "Swords", "Silence", "Kiss",
    "Butterfly", "Shadow", "Ring", "Rings", "Emerald",
    "Storm", "Storms", "Mists", "World", "Worlds",
    "Alien", "Lord", "Lords", "Ship", "Ships", "Star",
    "Stars", "Force", "Visions", "Vision", "Magic",
    "Wizards", "Wizard", "Heart", "Heat", "Twins",
    "Twilight", "Moon", "Moons", "Planet", "Shores",
    "Pirates", "Courage", "Time", "Academy",
    "School", "Rose", "Roses", "Stone", "Stones",
    "Sorcerer", "Shard", "Shards", "Slave", "Slaves",
    "Servant", "Servants", "Serpent", "Serpents",
    "Snake", "Soul", "Souls", "Savior", "Spirit",
    "Spirits", "Voyage", "Voyages", "Voyager", "Voyagers",
    "Return", "Legacy", "Birth", "Healer", "Healing",
    "Year", "Years", "Death", "Dying", "Luck", "Elves",
    "Tears", "Touch", "Son", "Sons", "Child", "Children",
    "Illusion", "Sliver", "Destruction", "Crying", "Weeping",
    "Gift", "Word", "Words", "Thought", "Thoughts", "Scent",
    "Ice", "Snow", "Night", "Silk", "Guardian", "Angel",
    "Angels", "Secret", "Secrets", "Search", "Eye", "Eyes",
    "Danger", "Game", "Fire", "Flame", "Flames", "Bride",
    "Husband", "Wife", "Time", "Flower", "Flowers",
    "Light", "Lights", "Door", "Doors", "Window", "Windows",
    "Bridge", "Bridges", "Ashes", "Memory", "Thorn",
    "Thorns", "Name", "Names", "Future", "Past",
    "History", "Something", "Nothing", "Someone",
    "Nobody", "Person", "Man", "Woman", "Boy", "Girl",
    "Way", "Mage", "Witch", "Witches", "Lover",
    "Tower", "Valley", "Abyss", "Hunter",
    "Truth", "Edge"
)
ADJECTIVES = (
    "Lost", "Only", "Last", "First",
    "Third", "Sacred", "Bold", "Lovely",
    "Final", "Missing", "Shadowy", "Seventh",
    "Dwindling", "Missing", "Absent",
    "Vacant", "Cold", "Hot", "Burning", "Forgotten",
    "Weeping", "Dying", "Lonely", "Silent",
    "Laughing", "Whispering", "Forgotten", "Smooth",
    "Silken", "Rough", "Frozen", "Wild",
    "Trembling", "Fallen", "Ragged", "Broken",
    "Cracked", "Splintered", "Slithering", "Silky",
    "Wet", "Magnificent", "Luscious", "Swollen",
    "Erect", "Bare", "Naked", "Stripped",
    "Captured", "Stolen", "Sucking", "Licking",
    "Growing", "Kissing", "Green", "Red", "Blue",
    "Azure", "Rising", "Falling", "Elemental",
    "Bound", "Prized", "Obsessed", "Unwilling",
    "Hard", "Eager", "Ravaged", "Sleeping",
    "Wanton", "Professional", "Willing", "Devoted",
    "Misty", "Lost", "Only", "Last", "First",
    "Final", "Missing", "Shadowy", "Seventh",
    "Dark", "Darkest", "Silver", "Silvery", "Living",
    "Black", "White", "Hidden", "Entwined", "Invisible",
    "Next", "Seventh", "Red", "Green", "Blue",
    "Purple", "Grey", "Bloody", "Emerald", "Diamond",
    "Frozen", "Sharp", "Delicious", "Dangerous",
    "Deep", "Twinkling", "Dwindling", "Missing", "Absent",
    "Vacant", "Cold", "Hot", "Burning", "Forgotten",
    "Some", "No", "All", "Every", "Each", "Which", "What",
    "Playful", "Silent", "Weeping", "Dying", "Lonely", "Silent",
    "Laughing", "Whispering", "Forgotten", "Smooth", "Silken",
    "Rough", "Frozen", "Wild", "Trembling", "Fallen",
    "Ragged", "Broken", "Cracked", "Splintered"
)


class Title(object):
    def __iter__(self):
        return self

    def make_title(self):
        adj = random.choice(ADJECTIVES)
        noun = random.choice(NOUNS)
        noun2 = random.choice(NOUNS)
        return random.choice([
            lambda: "%s %s" % (adj, noun),
            lambda: "The %s %s" % (adj, noun),
            lambda: "%s of %s" % (noun, noun2),
            lambda: "%s's %s" % (noun, noun2),
            lambda: "The %s of the %s" % (noun, noun2),
            lambda: "%s in the %s" % (noun, noun2)
        ])()

    def next(self):
        return self.make_title()