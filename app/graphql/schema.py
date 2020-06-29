from graphene import String, Field, Schema, ObjectType
from fastapi import APIRouter
from starlette.graphql import GraphQLApp

router = APIRouter()


class Person(ObjectType):
    """
    Person can be greeted
    """
    first_name = String(description="a first name")
    last_name = String(default_value="Griffin")
    full_name = String()
    greet = String(say=String(default_value="hi"),
                   description="greet a person")

    @staticmethod
    def resolve_full_name(parent, info):
        return f"{parent.first_name} {parent.last_name}"

    @staticmethod
    def resolve_greet(parent, info, say):
        return f"{say} {parent.first_name} {parent.last_name}"


class Query(ObjectType):
    """Root Query"""
    me = Field(Person, description="Who am I")

    @staticmethod
    def resolve_me(parent, info):
        return Person(first_name="Peter")


router.add_route(
    "/", GraphQLApp(schema=Schema(query=Query)))
