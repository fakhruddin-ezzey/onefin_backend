from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import UserCollections, UserCollectionMovies
from collection_app.serializer import UserSerializer, UserMoviesCollectionSerializer, UserMoviesBulkCRUDSerializer
from rest_framework.response import Response
from rest_framework import status
import requests
from requests.auth import HTTPBasicAuth
import os
from rest_framework.utils.serializer_helpers import ReturnDict
from collections import OrderedDict
import statistics


# creating user and storing the tokens for the same
class UserRegistrationAPIView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class UserMoviesList(APIView):
    http_method_names = ['get']
    target_url = 'https://demo.credy.in/api/v1/maya/movies/'

    def __get_all_movies(self, auth_user, auth_password, current_page):
        """
        Fetching the data from the Credy Demo API for movies.
        Authentication: Basic Auth
        Library: requests
        """
        if current_page is not None:
            url = self.target_url+'?page='+str(current_page)
        else:
            url = self.target_url

        basic_auth = HTTPBasicAuth(auth_user, auth_password)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', 
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate"
        }

        response = requests.request("GET", url, headers=headers, verify=False, auth=basic_auth)
        return response.json()

    def get(self, request, format=None):
        """
        Here we get the data from the Credy demo API and morph next and previous paginator links.
        Authentication: Token Authentication
        Library: DRF
        """
        
        current_page = None
        try:
            current_page = int(request.GET.get('page'))
        except Exception as e:
            pass

        AUTH_USERNAME = os.environ['AUTH_USERNAME']
        AUTH_PASSWORD = os.environ['AUTH_PASSWORD']

        demo_credy_api_data = self.__get_all_movies(auth_user=AUTH_USERNAME, auth_password=AUTH_PASSWORD, current_page=current_page)

        if 'is_success' in demo_credy_api_data.keys():
            if demo_credy_api_data['is_success'] == False:
                return Response(demo_credy_api_data)
        else:
            if current_page is None:
                demo_credy_api_data['next'] = f'http://localhost:8000/api/v1/movies?page=2'
            elif current_page == 2:
                demo_credy_api_data['next'] = f'http://localhost:8000/api/v1/movies?page=3'
                demo_credy_api_data['previous'] = f'http://localhost:8000/api/v1/movies'
            elif current_page > 2:
                demo_credy_api_data['next'] = f'http://localhost:8000/api/v1/movies?page={current_page+1}'
                demo_credy_api_data['previous'] = f'http://localhost:8000/api/v1/movies?page={current_page-1}'

        return Response(demo_credy_api_data)



class UserCollectionsAPIView(APIView):
    queryset = UserCollections.objects.all()
    serializer_class = UserMoviesCollectionSerializer
    __movies = None


    def __sanitize_collections_request(self, uncleaned_data):
        self.__movies = uncleaned_data['movies']
        uncleaned_data.pop('movies')
        return uncleaned_data


    def __get_favourite_genres_list(self, collection_list):
        genres_list = []
        for elem in collection_list:
            genres_list.append(elem['current_category_favorite'])
        
        return genres_list[:4]
    
    def __return_id_set_with_ops(self, collection_uuid):
        user_collection_movies_list = UserCollectionMovies.objects.filter(collection_map=collection_uuid).values()
        user_collection_movies_list = list(user_collection_movies_list)

        movies_id_ops = {
            'create':[],
            'update':[],
            'delete':[]
        }

        current_movies_uuid = []
        for elem in user_collection_movies_list:
            current_movies_uuid.append(str(elem['uuid']))
            
        for elem in self.__movies:
            try:
                if str(elem['uuid']) in current_movies_uuid:
                    movies_id_ops['update'].append(elem)
                
                current_movies_uuid.remove(str(elem['uuid']))
            except Exception as e:
                movies_id_ops['create'].append(elem)
        
        movies_id_ops['delete'] = current_movies_uuid
        print(movies_id_ops)
        
        return movies_id_ops
        
        

    def get_object(self, pk):
        try:
            return UserCollections.objects.get(uuid=pk)
        except Exception as e:
            raise LookupError(f'Instance for {pk} not found')


    def post(self, request, format=None):
        """
        Splitting validated data for collection and user's selected movies
        """
        user_movie_collection_data = request.data.copy()
        user_movie_collection_data = self.__sanitize_collections_request(user_movie_collection_data)

        serializer = UserMoviesCollectionSerializer(data=user_movie_collection_data, context={'show_response_for':'POST'})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        """
        Sanitization - 
        Here we split movies and map it using the movies serializer.
        """
        if self.__movies is not None:
            user_movies_selected = [dict(elem, **{'collection_map':serializer.data['collection_uuid']}) for elem in self.__movies]
            movies_serializer = UserMoviesBulkCRUDSerializer(data=user_movies_selected)
            movies_serializer.is_valid(raise_exception=True)
            movies_serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):

        if kwargs.get('uuid', None) is not None:
            try:
                instance = UserCollections.objects.get(uuid=kwargs['uuid'])
                serializer = UserMoviesCollectionSerializer(instance=instance)
                return Response(serializer.data)
            except Exception as e:
                return Response({'error_message': str(e)})
        
        instance = list(UserCollections.objects.all())
        serializer = UserMoviesCollectionSerializer(instance=instance, context={'show_response_for':'GET'}, many=True)

        return Response(serializer.data)
    

    def delete(self, request, *args, **kwargs):

        status_code = status.HTTP_202_ACCEPTED
        response_msg = {'message':''}

        if kwargs.get('uuid', None) is not None:
            if UserCollections.objects.filter(uuid=kwargs['uuid']).exists():
                UserCollections.objects.filter(uuid=kwargs['uuid']).delete()
                response_msg['message'] = f'Successfully removed the collection.'
            else:
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                response_msg['message'] = f'UUID is either deleted already or not present. Please check the request.'
            return Response(response_msg,status=status_code)
        else:
            return Response({'message':'UID is either corrupted or not present. Please check the request.'},status=status.HTTP_400_BAD_REQUEST)
        
    

    def put(self, request, *args, **kwargs):
        print('entered')
        status_code = status.HTTP_202_ACCEPTED
        response_msg = {'message':''}

        data = request.data

        if kwargs.get('uuid', None) is not None:
            try:
                self.__movies = data['movies']
                data.pop('movies')
                instance = UserCollections.objects.get(uuid=kwargs['uuid'])
                collections_serializer = UserMoviesCollectionSerializer(instance=instance, data=data, partial=True)
               
                if collections_serializer.is_valid():
                    collections_serializer.save()

                    """
                    Creating new movies, deleting unfound in requests and updating with given UUID
                    """
                    store_id_ops_map = self.__return_id_set_with_ops(kwargs['uuid'])

                    # creating new movies inside the existing collection
                    store_id_ops_map['create'] = [UserCollectionMovies(**elem) for elem in store_id_ops_map['create']]

                    print(store_id_ops_map['create'])
                    UserCollectionMovies.objects.bulk_create(store_id_ops_map['create'])

                    # updating the existing movies with new values (if any)
                    print('check 11')
                    movies_bulk_update_queryset = [UserCollectionMovies.objects.get(uuid=elem['uuid']) for elem in store_id_ops_map['update']]

                    for elem, updated_vals in zip(movies_bulk_update_queryset, store_id_ops_map['update']):
                        elem.title = updated_vals['title']
                        elem.description = updated_vals['description']
                        elem.genres = updated_vals['genres']

                    UserCollectionMovies.objects.bulk_update(movies_bulk_update_queryset,['title', 'description', 'genres'])

                    # deleting the movies unmentioned in provided request
                    UserCollectionMovies.objects.filter(uuid__in=store_id_ops_map['delete']).delete()

                else:
                    response_msg['message'] = collections_serializer.errors

                response_msg['message'] = f'Successfully removed the collection.'
            except Exception as e:
                print(e)
                response_msg['message'] = f'UUID is either deleted already or not present. Please check the request'
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(response_msg,status=status_code)
            
        else:
            return Response({'message':'UID is either corrupted or not present. Please check the request.'})



    def finalize_response(self, request, response, *args, **kwargs):
        new_response = response
        if isinstance(response.data, list):

            collections_list = list(response.data)
            
            new_response = {
                'is_success':True,
                'data':{
                    'collections': collections_list,
                    'favourite_genres': self.__get_favourite_genres_list(collections_list)
                }
            }
            new_response = Response(new_response)

        return super().finalize_response(request, new_response, *args, **kwargs)



