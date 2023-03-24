# Default lang is used for: ChatGPT summary, app display
# It should be set to the language used by the user to store its moments
DEFAULT_LANG = "fr"

DAYS = {
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "fr": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
}

SIZE = len(DAYS[DEFAULT_LANG])

TODAY = {
    "en": "Today",
    "fr": "Aujourd'hui"
}

SUMMARY_TYPES = {
    "en": ["50 words", "5 adjectives", "1 sentence"],
    "fr": ["50 mots", "5 adjectifs", "1 phrase"]
}


AUTHORIZED_LATE_DAYS = 2

NUM_MOMENTS = 3

MIN_MOMENTS_SUMMARY = 3


PROMPT = {
    "en":"Can you summarize in {} top my week based on the happy moments that I recorded every day of the week.",
    "fr":"Peux-tu résumer en {} maximum ma semaine à partir des petits bonheurs que j'ai noté chaque jour de la semaine."
}