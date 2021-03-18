import graphene
from graphql import GraphQLError
from .models import LastLocation
from graphene_django import DjangoObjectType


class Location(DjangoObjectType):
    class Meta:
        model = LastLocation


class Query(graphene.ObjectType):
    lastLocation = graphene.Field(Location)

    def resolve_lastLocation(self, info):
        u = info.context.user
        if u.is_anonymous:
            raise GraphQLError("Not Logged In!")

        loc = LastLocation.objects.get(user=u)

        return loc


class UpdateLocation(graphene.Mutation):
    l = graphene.Field(Location)

    class Arguments:
        city: graphene.String()
        state: graphene.String()
        country: graphene.String()

    def mutate(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not Logged In!")

        loc = LastLocation.objects.get(user=user).exists()
        loc.city = kwargs.get("city")
        loc.state = kwargs.get("state")
        loc.country = kwargs.get("country")

        loc.save()

        return UpdateLocation(l=loc)


class Mutation(graphene.ObjectType):
    update_location = UpdateLocation.Field()
