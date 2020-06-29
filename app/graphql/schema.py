import graphene
from fastapi import APIRouter
from starlette.graphql import GraphQLApp

router = APIRouter()


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        print(info)
        return "Hello " + name


router.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))
