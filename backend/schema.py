import graphene
import users.schema
import location.schema


class Query(users.schema.Query, location.schema.Query, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, location.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
