from neomodel import StructuredNode, UniqueIdProperty, StringProperty
from neomodel.hooks import hooks
from neomodel.properties import BooleanProperty


class BaseModel(StructuredNode):
    """
    This is a base class for models stored in Neo4J.
    Main idea of this class is give an uid for object
    and grant access to database
    """

    # Unique identifier
    uid = UniqueIdProperty()
    active = BooleanProperty(default=True)

    ## TODO: use uid as neo4j internal id instead of uid
