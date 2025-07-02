from static.lists.levels_list import levels_list_top
from static.lists.challenges_list import challenges_list_top

players = [
    (
        "Gild56", "@gild56gmd",
        [
            "Shitty Amethyst",
            "Shitty Acheron",
            "Shitty Kyouki",
            "Zetsubo",
            "Psychedelique",
            "Obsolete",
            "La Longue Attente",
            "Shmyak",
            "The Ghost",
            "Deadly",
            "A R K A D",
            "Hell",
            "Game",
            "Machinas Error",
            "Rainbow",
            "MG"
        ],
        [
            "Slaughterhouse Spam",
            "12qwe2d1",
            "RubRub",
            "RI Wave x2",
            "Wave Challenge Final",
            "Spam VIII",
            "Pushing On",
            "LegendOfConsistensy",
            "DaughterHouse",
            "SpaM I",
            "Unnamed",
            "SpaM VII",
            "SpaM VI",
            "SpaM V",
            "SpaM IV",
            "SpaM III",
            "SpaM II"
        ]
    ),
    (
        "MysticNull", "@mystic_nullgmd",
        [
            "Shitty Andromeda"
        ],
        []
    ),
    (
        "kevino", "@qelzzu",
        [
            "Shitty Amethyst",
            "Psychedelique"
        ],
        []
    ),
    (
        "Uranium", "@UraniumGMD",
        [
            "Shitty Andromeda",
            "Shitty Amethyst",
            "Shitty Acheron",
            "Shitty Kyouki",
            "Zetsubo",
            "Psychedelique",
            "Obsolete",
            "La Longue Attente",
            "Shmyak",
            "The Ghost",
            "Deadly",
            "A R K A D",
            "Hell",
            "Game",
            "Machinas Error",
            "Rainbow",
            "MG"
        ],
        []
    ),
    (
        "Itwabosballss", "@Picklehi27GD",
        [
            "Shitty Andromeda"
        ],
        []
    ),
    (
        "Panzer", "@TheRealPanzer",
        [
            "Shitty Andromeda"
        ],
        []
    ),
    (
        "minhmnvnnet", "@minhmnvnnet",
        [
            "Shitty Andromeda"
        ],
        []
    ),
    (
        "Loliquiem", "@loliquiemgd",
        [
            "Shitty Andromeda"
        ],
        []
    ),
    (
        "Ylissen", "@Ylissen",
        [],
        []
    )
]


level_points = {
    level[0]: (len(levels_list_top) - i) * 10
    for i, level in enumerate(levels_list_top)
}

top_players = []
for name, tag, passed_levels_1, passed_levels_2 in players:
    total_points = sum(level_points.get(lvl, 0) for lvl in passed_levels_1)
    top_players.append((name, tag, passed_levels_1, passed_levels_2, total_points))

top_players.sort(key=lambda x: x[4], reverse=True)


challenge_points = {
    challenge[0]: (len(challenges_list_top) - i) * 10
    for i, challenge in enumerate(challenges_list_top)
}

top_challenge_players = []
for name, tag, passed_levels_1, passed_levels_2 in players:
    challenge_score = sum(challenge_points.get(lvl, 0) for lvl in passed_levels_2)
    top_challenge_players.append((name, tag, passed_levels_1, passed_levels_2, challenge_score))

top_challenge_players.sort(key=lambda x: x[4], reverse=True)
