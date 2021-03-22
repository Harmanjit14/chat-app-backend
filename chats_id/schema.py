from users.models import UserProfile
import graphene
from graphene_django import DjangoObjectType
from .models import ChatData
from graphql import GraphQLError
from django.db.models import Q


class Chat(DjangoObjectType):
    class Meta:
        model = ChatData


class Query(graphene.ObjectType):
    getChatIds = graphene.List(Chat)

    def resolve_getChatIds(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not Logged In!")

        profile = UserProfile.objects.get(user=user)
        return ChatData.objects.filter(Q(userA=profile) | Q(userB=profile))


class CreateChat(graphene.Mutation):
    ans = graphene.Field(Chat)

    class Arguments:
        id = graphene.String(required=True)
        collection = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not Logged In!")
        A = UserProfile.objects.get(user=user)
        B = UserProfile.objects.get(id=kwargs.get("id"))
        temp = ChatData.objects.create(
            userA=A, userB=B, collection=kwargs.get("collection"))

        return CreateChat(ans=temp)


class Mutation(graphene.ObjectType):
    create_chat = CreateChat.Field()
