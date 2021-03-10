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


class CreateUser(graphene.Mutation):

    new_user = graphene.Field(Users)

    class Argumsnts:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        # name = graphene.String()
        # gender = graphene.String()
        # image = graphene.String()
        # city = graphene.String()
        # state = graphene.String()
        # country = graphene.String()

    def mutate(self, info, **kwargs):
        if User.objects.filter(email=kwargs.get("email")).exists():
            raise GraphQLError("Email already registered")

        user = get_user_model()(
            username=kwargs.get("username"),
            email=kwargs.get("email"),
        )
        user.set_password(kwargs.get("password"))
        user.save()

        # name = kwargs.get("name")
        # gender = kwargs.get("gender")
        # image = kwargs.get("image")
        # city = kwargs.get("city")
        # state = kwargs.get("state")
        # country = kwargs.get("country")

        # UserProfile.objects.create(
        #     user=user, name=name, city=city, state=state, country=country, image=image, gender=gender)

        return CreateUser(new_user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
