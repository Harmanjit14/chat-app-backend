import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .models import UserProfile
from graphql import GraphQLError


class Profile(DjangoObjectType):
    class Meta:
        model = UserProfile


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class Query(graphene.ObjectType):
    me = graphene.Field(Profile)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not Logged In!")
        return user


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        name = graphene.String()
        image = graphene.String()
        gender = graphene.String()
        city = graphene.String()
        state = graphene.String()
        country = graphene.String()

    def mutate(self, info, username, password, email, **kwargs):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        img = kwargs.get("image")
        gen = kwargs.get("gender")

        if img is None:
            profile = UserProfile.objects.create(user=user, name=kwargs.get(
                "name"), gender=gen, city=kwargs.get("city"), state=kwargs.get("state"), country=kwargs.get("country"))
            profile.save()
        else:
            profile = UserProfile.objects.create(user=user, name=kwargs.get(
                "name"), image=img, gender=gen, city=kwargs.get("city"), state=kwargs.get("state"), country=kwargs.get("country"))
            profile.save()

        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    update = graphene.Field(Profile)

    class Arguments:
        name = graphene.String(required=False)
        image = graphene.String(required=False)
        gender = graphene.String(required=False)
        city = graphene.String(required=False)
        state = graphene.String(required=False)
        country = graphene.String(required=False)

    def mutate(self, info, **kwargs):

        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("Not Logged In!")

        profile = UserProfile.objects.get(user=user)

        name = kwargs.get("name")
        image = kwargs.get("image")
        gender = kwargs.get("gender")
        city = kwargs.get("city")
        state = kwargs.get("state")
        country = kwargs.get("country")

        if image is not None:
            profile.image = image
        if gender is not None:
            profile.gender = gender
        if name is not None:
            profile.name = name
        if city is not None:
            profile.city = city
        if state is not None:
            profile.state = state
        if country is not None:
            profile.country = country

        profile.save()

        return UpdateUser(update=profile)
z

class DeleteUser(graphene.Mutation):
    user = graphene.String()

    def mutate(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("Not Logged In!")

        user.delete()
        str = "Done!"

        return DeleteUser(user=str)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
