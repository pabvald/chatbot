PATH_KNOWLEDGE_BASE = 'knowledge/base'
PATH_SCHEMA = 'docs/schemas/knowledge.schema.json'

from knowledge.train import main as train_knowledge
from knowledge.validate import main as validate_knowledge
