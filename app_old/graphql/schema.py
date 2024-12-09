from graphene import ObjectType, Schema, List, Field
from fastapi import APIRouter
from starlette.graphql import GraphQLApp

from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import app.db.models as models
from graphene import relay

router = APIRouter()


class User(SQLAlchemyObjectType):
    """
    A User type will be constructed with different pagination and sorting
    options, and with all fields automatically mapped.
    I have to add the field for the relationship `items` explicitely but
    the mapping gets resolved correctly.
    """
    class Meta:
        model = models.User
        interfaces = (relay.Node,)

    items = List(lambda: Item)


class Item(SQLAlchemyObjectType):
    """
    I am using lambda function to define the `Field` types because normally
    python wouldnt let me define a cricular dependency. And also I use
    `Item` before I define it.
    """
    class Meta:
        model = models.Item
        interfaces = (relay.Node,)

    owner = Field(lambda: User)


class Query(ObjectType):
    """
    In the root Query object I "mount" those special SQLAlchemy object types
    like below. This kind of generates all the resolvers automatically.
    I basically don't need `db.crud.py`!

    Note: Don't forget to add the session in the initialization. In my case
    it's in `db.__init__.py` together with the session objects.

        Base.query = scoped_session(SessionLocal).query_property()
    """
    all_users = SQLAlchemyConnectionField(User.connection)
    all_items = SQLAlchemyConnectionField(Item.connection)


router.add_route(
    "/", GraphQLApp(schema=Schema(query=Query)))
