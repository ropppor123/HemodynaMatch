ANTIBODY_TO_ANTIGEN = {
    "anti-K": "K",
    "anti-k": "k",
    "anti-Kpa": "Kpa",
    "anti-Kpb": "Kpb",
    "anti-Fya": "Fya",
    "anti-Fyb": "Fyb",
    "anti-Jka": "Jka",
    "anti-Jkb": "Jkb"
}

# Recipient ABO groups: allowed donor ABO groups
# Red blood cell components only.
RED_CELL_ABO = {
    "A": ["A", "O"],
    "B": ["B", "O"],
    "AB": ["AB", "A", "B", "O"],
    "O": ["O"]
}

# Fresh frozen plasma, cryodepleted plasma and cryoprecipitate.
PLASMA_ABO = {
    "A": ["A", "AB"],
    "B": ["B", "AB"],
    "AB": ["AB"],
    "O": ["O", "A", "B", "AB"]
}

# Platelets components only.
PLATELET_ABO = {
    "A": ["A"],
    "B": ["B"],
    "AB": ["AB"],
    "O": ["O"]
}

# SHELF LIFE
SHELF_LIFE = {
    "Packed Red Cell": {"days": 42},
    "Red Cell Leucocyte Depleted": {"days": 42},
    "Washed Red Cell Leucocyte Depleted": {"days": 28},
    "Apheresis Platelets": {"days": 7},
    "Pooled Platelets": {"days": 7},
    "Fresh Frozen Plasma": {"months": 12},
    "Cryodepleted Plasma": {"months": 12},
    "Cryoprecipitate": {"months": 12}
}

# Red-cell workflow requirements only
EMERGENCY_O_NEGATIVE_MAX_AGE = {
    "Female": 50,
    "Male": 18
}