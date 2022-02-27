from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse

from mapone_api.models import User, Entry, Archive
from mapone_api.constants import *

from mapone_api.user import UserClass
from mapone_api.entry import EntryClass
from mapone_api.archive import ArchiveClass


class UserView(APIView):

    def get(self, request):
        # create user class
        user_class = UserClass()

        # get params
        action = request.query_params.get('action')
        email_address = request.query_params.get('email_address')
        password = request.query_params.get('password')

        # if no params given
        if not action or not email_address or not password:
            # error
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        # convert action to int
        action = int(action)

        # create new user
        if action == CREATE_USER:
            response = user_class.create_new_user(email_address, password)

        # login
        elif action == LOGIN:
            response = user_class.verify_user(email_address, password)

        # change passord or delete user
        elif action == CHANGE_PASSWORD or action == DELETE_USER:
            # check if user is logged in
            valid_user = user_class.verify_user(email_address, password)

            # if user exists and is logged in
            if valid_user == SUCCESS:
                # get user id
                user_id = user_class.check_existing_user(email_address)

                if action == CHANGE_PASSWORD:
                    # get new password
                    new_password = request.query_params.get('new_password')

                    # if new password given
                    if new_password:
                        # change password
                        response = user_class.change_password(user_id, new_password)
                    
                    # param error
                    else:
                        return Response(None, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # delete user
                    response = user_class.delete_user(user_id)

            # user login error
            else:
                response = valid_user

        # invalid action
        else:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        # return valid action response
        return Response(response, status=status.HTTP_200_OK)

class EntryView(APIView):

    def get(self, request):
        # create entry class
        entry_class = EntryClass()

        # get params
        action = request.query_params.get('action')

        # if no params given
        if not action:
            # error
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        # convert action to int
        action = int(action)

        if action == MAIN_PAGE:
            # display all entries
            response = entry_class.get_all_entries()

        elif action == SEARCH_KEYWORD:
            # get keyword param
            keyword = request.query_params.get('keyword')

            # search database for keyword
            response = entry_class.search_keyword(keyword)

        # invalid action
        else:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        # return valid action response
        return Response(response, status=status.HTTP_200_OK)

class ArchiveView(APIView):

    def get(self, request):
        # create archive class
        archive_class = ArchiveClass()
        user_class = UserClass()

        # get params
        action = request.query_params.get('action')
        email_address = request.query_params.get('email_address')
        password = request.query_params.get('password')
        keyword = request.query_params.get('keyword')
        frequency = request.query_params.get('frequency')

        # if no params given
        if not action or not email_address or not password:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        # convert action to int
        action = int(action)

        # check if user is logged in
        valid_user = user_class.verify_user(email_address, password)

        # if user exists and is logged in
        if valid_user == SUCCESS:
            # get user id
            user_id = user_class.check_existing_user(email_address)

            if action == CREATE_ARCHIVE:
                # check necessary params
                if not keyword or not frequency:
                    # incorrect params error
                    return Response(None, status=status.HTTP_400_BAD_REQUEST)
                
                # create archive
                archive_class.create_new_archive(user_id, keyword, frequency)

                # operation success
                response = SUCCESS

            elif action == DISPLAY_USER_ARCHIVES:
                # display user saved archives
                response = archive_class.get_user_saved_searches(user_id)

            elif action == DELETE_ARCHIVE or action == UPDATE_FREQUENCY:
                # check params
                if not keyword:
                    # incorrect params error
                    return Response(None, status=status.HTTP_400_BAD_REQUEST)

                # get all user saved searches
                searches = archive_class.get_user_saved_searches(user_id)

                # loop through user searches
                for search in searches:
                    # keyword match
                    if search['keyword'] == keyword:
                        # get archive id
                        archive_id = search['archive_id']

                if action == DELETE_ARCHIVE:
                    # delete archive
                    archive_class.delete_archive(archive_id)

                else:
                    # get new frequency
                    new_frequency = request.query_params.get('new_frequency')

                    # update frequency
                    if new_frequency:
                        archive_class.update_frequency(archive_id, new_frequency)

                    # param error
                    else:
                        return Response(None, status=status.HTTP_400_BAD_REQUEST)
                
                # operation success
                response = SUCCESS

            # invalid action
            else:
                return Response(None, status=status.HTTP_400_BAD_REQUEST)

        # login user error
        else:
            response = valid_user

        # return valid action response
        return Response(response, status=status.HTTP_200_OK)
