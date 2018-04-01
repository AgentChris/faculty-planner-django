import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse

# from myngs.models import MyDashboardUserProfile


@login_required
def index(request):
    raise NotImplemented

#     if request.user.is_staff:
#         return redirect('/admin/')
#     context = {}
#     react_props = {
#         'api_url': reverse('mydashboard_service:api_base')
#     }
#
#     user_profile = None
#     try:
#         user_profile: MyDashboardUserProfile = \
#             request.user.mydashboard_user_profile
#     except ObjectDoesNotExist:
#         # user is not a salesforce user. ex: admin
#         pass
#
#     if user_profile:
#         context['sf_user_id'] = user_profile.get_sf_user_id()
#
#     current_user_username = request.user.username if request.user else None
#
#     context['props'] = json.dumps(react_props)
#     context['current_user'] = current_user_username
#
#     return render(request, 'dashboard/index.html', context)
