"""census URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.views.i18n import JavaScriptCatalog
from .views import index

from . import views

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('export/events/', views.export_events),
    path('submit/', views.add_event),
    path('pending/', views.PendingList.as_view(), name = 'pending_list'),
    path('<int:pk>/update/', views.UpdateEvent.as_view(), name= 'event_update'),
]
js_info_dict = {
    'packages': ('recurrence', ),
}
urlpatterns += [
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(packages=['recurrence']),
         name='javascript-catalog')
]
