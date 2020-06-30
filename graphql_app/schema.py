"""
More graphene+sqlalchemy examples:

    https://docs.graphene-python.org/projects/sqlalchemy/en/latest/examples/
"""
from graphene import ObjectType, Schema, List, Field
from fastapi import APIRouter
from starlette.graphql import GraphQLApp
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import graphql_app.models as models
from graphene import relay


class User(SQLAlchemyObjectType):
    """
    See only_fields. GraphQL states one should use business layer for authorization.
    That would be this class. E.g. I could add middlewares for certain classes
    or certain fields (would need to override resolvers). See:
        https://github.com/graphql-python/graphene-sqlalchemy/issues/186#issuecomment-477225034
    or
        https://github.com/encode/starlette/issues/740#issuecomment-595505414
    """
    class Meta:
        model = models.User
        interfaces = (relay.Node,)
        only_fields = ('email', 'is_active')

    items = List(lambda: Item)


class Item(SQLAlchemyObjectType):
    """
    Authentication via fastAPI?
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


router = APIRouter()
router.add_route(
    "/", GraphQLApp(schema=Schema(query=Query)))
