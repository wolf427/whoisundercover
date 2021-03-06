from django.conf.urls import include, url
from django.contrib import admin


import game_process
# from game_process.AutomicallyCleanUpScheduler import startAutoSche

# startAutoSche()

urlpatterns = [
    # Examples:
    # url(r'^$', 'whoisundercover.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^wechat/', 'game_process.views.process'),
    url(r'^init/', 'game_process.AutomicallyCleanUpScheduler.startAutoSche'),
]
