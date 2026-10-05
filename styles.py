MOOD_FAMILIES = {

    "soft": [
        "affectionate",
        "calm",
        "content",
        "peaceful",
        "relaxed",
        "serene",
        "soothing",
        "tender",
        "tranquil"
    ],

    "joyful": [
        "amused",
        "blissful",
        "carefree",
        "cheerful",
        "delighted",
        "ecstatic",
        "excited",
        "happy",
        "joyful",
        "uplifted"
    ],

    "dreamy": [
        "dreamy",
        "hopeful",
        "inspired",
        "mysterious",
        "nostalgic",
        "wistful"
    ],

    "dark": [
        "angry",
        "bitter",
        "dejected",
        "desperate",
        "disappointed",
        "disgusted",
        "gloomy",
        "melancholic",
        "miserable",
        "ominous",
        "sad"
    ],

    "uneasy": [
        "anxious",
        "apprehensive",
        "eerie",
        "frustrated",
        "insecure",
        "jealous",
        "restless",
        "uneasy",
        "worried"
    ],

    "playful": [
        "curious",
        "playful"
    ],

    "reflective": [
        "thoughtful"
    ]
}

def get_style_family(mood):
    for family, moods in MOOD_FAMILIES.items():
        if mood in moods:
            return family

    return "soft"