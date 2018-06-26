"""FacultyPlanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from django.contrib import admin

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'student', views.StudentView)
router.register(r'specialization', views.SpecializationView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^schedule/', views.get_schedule_by_group, name="get_schedule_by_group"),
    url(r'^parse/fsega/', views.scrape_faculty, name="parse_fsega"),
    url(r'^year_structures/', views.get_year_structures, name="year_structures"),
    url(r'^professor_data/', views.parse_professor_information, name="professor_data"),
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
]
