from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse

from mapone_api.models import User, Entry, Archive

# may not be able to be same name
from mapone_api.user import UserClass
from mapone_api.entry import EntryClass
from mapone_api.archive import ArchiveClass


# may need main page view?
# maybe use action as a param --> other big functions? separate files

class UserView(APIView):

    def get(self, request):
        message = {'TEST'}
        return Response(message, status=status.HTTP_200_OK)

class EntryView(APIView):

    def get(self, request):
        message = {'TEST'}
        return Response(message, status=status.HTTP_200_OK)

class ArchiveView(APIView):

    def get(self, request):
        message = {'TEST'}
        return Response(message, status=status.HTTP_200_OK)
