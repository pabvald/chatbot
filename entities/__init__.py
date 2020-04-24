"""
    Entities module 
"""

# --- Entities ---
CUSTOM_ENTITIES = ['TOPIC', 'TIME', 'DATE']
TELEGRAM_ENTITY_LABELS =  {
        "mention": "MENTION",
        "hashtag": "HASHTAG",
        "bot_command": "BOT_COMMAND",
        "phone_number": "PHONE_NUMBER",
        "url": "URL",
        "email": "EMAIL",
        "bold": "BOLD",
        "italic": "ITALIC",
        "code": "CODE",
        "pre": "PRE",
        "text_link": "TEXT_LINK",
        "text_mention": "TEXT_MENTION"
    }
TELEGRAM_ENTITIES = list(TELEGRAM_ENTITY_LABELS.values())
ENTITIES = CUSTOM_ENTITIES #+ TELEGRAM_ENTITIES

# --- Paths ---
PATH_DEFINITIONS = 'entities/definitions'
PATH_SCHEMA = 'docs/schemas/entity.schema.json'


# --- Imports ---
from entities.validate import main as validate_entities
from entities.train import main as train_entities

