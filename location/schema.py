import graphene
from graphql import GraphQLError
from .models import LastLocation
from graphene_django import DjangoObjectType


class Location(DjangoObjectType):
    class Meta:
        model = LastLocation


class Query(graphene.ObjectType):
    last_location = graphene.Field(Location)

    def resolve_last_location(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not Logged In!")

        loc = LastLocation.objects.get(user=user)

        return loc


class UpdateLocation(graphene.Mutation):
    loc = graphene.Field(Location)

    class Arguments:
        city: graphene.String()
        state: graphene.String()
        country: graphene.String()

    def mutate(self, info, city, state, country):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not Logged In!")

        loc = LastLocation.objects.get_or_create(user=user)
        loc.city = city
        loc.state = state
        loc.country = country

        loc.save()

        return UpdateLocation(loc=loc)


class Mutation(graphene.ObjectType):
    update_location = UpdateLocation.Field()
