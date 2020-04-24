"""
    Intents module.
"""

INTENTS = ["cancel", "appointment", "help",  "welcome", "contact", "farewell", "thank", "fallback"]
FALLBACK_INTENT = "fallback"
INTENTS_PRIORITIES = {
    "cancel": 1.4,
    "contact": 1.4,
    "appointment": 1.2,
    "help": 1,
    "welcome": 1,
    "farewell": 1,
    "thank": 1,
    "fallback": 1
}
PATH_DEFINITIONS = './intents/definitions'
PATH_SCHEMA = './docs/schemas/intent.schema.json'

from intents.validate import main as validate_intents
from intents.train import main as train_intents
