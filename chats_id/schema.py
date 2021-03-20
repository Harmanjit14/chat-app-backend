import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .models import ChatData
from graphql import GraphQLError