import graphene
from graphene_django import DjangoObjectType
from .models import UserProfile
from django.contrib.auth.models import User
from graphql import GraphQLError
from django.contrib.auth import get_user_model


class Profile(DjangoObjectType):
    class Meta:
        model = UserProfile()


class Users(DjangoObjectType):
    class Meta:
        model = User()


class Query(graphene.ObjectType):
    me = graphene.Field(Users)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not Logged in!")

        return user


class Mutation(graphene.ObjectType):
    pass
