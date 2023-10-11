from django.db import models
from django.contrib.auth import get_user_model
import uuid

# user-created movie collections
class UserCollections(models.Model):
    uuid = models.UUIDField(primary_key=True, null=False, blank=False, default=uuid.uuid4)
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(default='N/A', blank=False, null=False)
    user_map = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_movies_collection'


# user-curated movies list inside a certain collections
class UserCollectionMovies(models.Model):
    collection_map = models.ForeignKey(UserCollections, on_delete=models.CASCADE, null=False, blank=False)
    uuid = models.UUIDField(primary_key=True, null=False, blank=False, default=uuid.uuid4)
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(default='N/A', blank=False, null=False)
    genres = models.CharField(max_length=200, null=False, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_movies_collection_specific'