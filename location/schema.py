import graphene
from graphql import GraphQLError
from .models import LastLocation
from graphene_django import DjangoObjectType


class Location(DjangoObjectType):
    class Meta:
        model = LastLocation
        