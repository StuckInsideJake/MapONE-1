from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse

from mapone_api.models import Publication
class PublicationView(APIView):

    def get(self, request):

        # No params from frontend
        # Display all publications (front page)
        all_entries = Publication.objects.all()

        # print(all_entries)
        message = "MapONE backend server connected."
        response = {message, all_entries}
        return Response(response)
