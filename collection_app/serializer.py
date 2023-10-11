from rest_framework import serializers
from .models import UserCollectionMovies, UserCollections
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from collections import OrderedDict
from rest_framework.fields import SerializerMethodField
import statistics


# creating a new user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username','password']

    def to_representation(self, data):
        data = super(UserSerializer, self).to_representation(data)
        token_fetched = RefreshToken.for_user(self.instance)
        
        data = OrderedDict({
            'access_token': str(token_fetched.access_token),
            'refresh_token': str(token_fetched)
        })

        return data



# serializer for the movie collections
class UserMoviesCollectionSerializer(serializers.ModelSerializer):

    movies = SerializerMethodField()

    class Meta:
        model = UserCollections
        fields = ['uuid', 'title', 'description', 'user_map', 'movies']

    def __get_favorite_genres(self, movies_data):
        genres_list = []
        movies_data = dict(movies_data)['movies']

        for elem in movies_data:
            genres_list+=elem['genres'].split(',')
        
        return statistics.mode(genres_list)

    
    def get_movies(self, obj):
        return obj.usercollectionmovies_set.values()

    def to_representation(self, instance):
        response_controller = self.context
        data = super(UserMoviesCollectionSerializer, self).to_representation(instance)

        modified_data = OrderedDict({})
        if response_controller.get('show_response_for', None) is not None:
            if response_controller['show_response_for'] == 'POST':
                modified_data = OrderedDict({
                    'collection_uuid': data['uuid']
                })
            elif response_controller['show_response_for'] == 'GET':

                data['current_category_favorite'] = self.__get_favorite_genres(data)
                
                data.pop('movies')
                data.pop('user_map')
                
                modified_data = data
                modified_data = OrderedDict(modified_data)
        else:
            data.pop('user_map')
            modified_data = OrderedDict(data)
        return modified_data

# serializer for inserting movies into the collection
class UserMoviesForCollectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCollectionMovies
        fields = ['uuid','collection_map','title','description','genres']


class UserMoviesBulkCRUDSerializer(serializers.ListSerializer):
    child = UserMoviesForCollectionsSerializer()