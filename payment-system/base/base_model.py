from neomodel import StructuredNode
from neomodel import UniqueIdProperty
from neomodel.properties import BooleanProperty


# === BaseModel ===
class BaseModel(StructuredNode):
    """
    This is a base class for models stored in Neo4J.

    *  make unique identifies uid for all objects
    *  give active property for all objets (used instead of delete)
    """

    # Unique identifier (use it instead of neo4j id)
    uid = UniqueIdProperty()
    active_ = BooleanProperty(default=True)

    @property
    def active(self):
        return self.active_

    @active.setter
    def active(self, state):
        self.active_ = state
