from django.shortcuts import render
from django.conf import settings
import requests
from rest_framework.views import APIView
from .serializer import UserSearchSerializer
import json
from .models import UserDetails, Hits
from rest_framework import status
from rest_framework.response import Response
import uuid
import shutil
from datetime import datetime
# Create your views here.


def gitapi(**kwargs):
    url = "https://api.github.com/search/users?q={0}".format(kwargs['name'])
    if kwargs.get('gt_repos') and kwargs.get('lt_repos'):
        url = url + "repos:{0}..{1}+".format(kwargs.get('gt_repos'), kwargs.get('lt_repos'))
    else:
        if kwargs.get('gt_repos'):
            url = url + "repos:%3E{0}+".format(kwargs['gt_repos'])
        if kwargs.get('lt_repos'):
            url = url + "repos:%3C{0}+".format(kwargs['lt_repos'])
    if kwargs.get('gt_followers') and kwargs.get('lt_followers'):
        url = url + "followers:%{0}..{1}".format(kwargs.get('gt_followers'), kwargs.get('lt_followers'))
    else:
        if kwargs.get('gt_followers'):
            url = url + "followers:%3E{0}+".format(kwargs['gt_followers'])
        if kwargs.get('lt_followers'):
            url = url + "followers:%3C{0}+".format(kwargs['lt_followers'])
    if kwargs.get('location'):
        url = url + "location:{0}+".format(kwargs['location'])
    url = url + "&client_id={0}&client_secret={1}".format(settings.CLIENT_ID, settings.CLIENT_SECRET)
    # print(url)
    key = "hit_url_per_day"
    today_date = datetime.now().date()
    total_hit = Hits.objects.get_or_create(key=key, created_at=today_date)[0]
    total_hit.value += 1
    total_hit.save()
    return url


class SearchUser(APIView):
    def get(self, request):
        user_data = UserSearchSerializer(data=request.GET)
        if user_data.is_valid():
            url = gitapi(**user_data.data)
            data = requests.get(url)
            if data.status_code == 200:
                request_data = json.loads(data.text)
                for user_data in request_data['items']:
                    user, is_created = UserDetails.objects.get_or_create(username=user_data['login'])
                    user.avatar_url = user_data['avatar_url']
                    user.gravatar_id = user_data["gravatar_id"]
                    user.url = user_data['url']
                    user.html_url = user_data['html_url']
                    user.followers_url = user_data['followers_url']
                    user.following_url = user_data['following_url']
                    user.gists_url = user_data['gists_url']
                    user.starred_url = user_data['starred_url']
                    user.subscriptions_url = user_data['subscriptions_url']
                    user.organizations_url = user_data['organizations_url']
                    user.repos_url = user_data['repos_url']
                    user.save()
                    try:
                        uuid_code = str(uuid.uuid4()) + '.jpg'
                        image_url = "{0}/{1}".format(settings.MEDIA_ROOT, uuid_code)
                        response = requests.get(user_data['avatar_url'], stream=True)
                        with open(image_url, 'wb') as out_file:
                            shutil.copyfileobj(response.raw, out_file)
                        del response
                        user.image = uuid_code
                        user.save()
                    except Exception as e:
                        print(e)
                return Response({"success": True})
            else:
                return Response({"success": False, "message": "Validation Failed.", "errors": data.read()},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response({"message": "Validation Failed.", "errors": user_data.errors},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
