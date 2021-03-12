import graphene
import users.schema
import location.schema
import graphql_jwt


# class Query(users.schema.Query, graphene.ObjectType):
#     pass


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(mutation=Mutation)
