from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from main.feeds import SeriesFeed
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
                       ('^$','main.views.index'),
                       ('^dashboard/','main.views.dashboard'),
                       ('^recent_operations/','main.views.recent_operations'),
                       ('^most_recent_operation/','main.views.most_recent_operation'),
                       ('^accounts/',include('djangowind.urls')),
                       (r'^admin/(.*)', admin.site.root),
                       (r'^capture/file_upload','main.views.test_upload'),
                       (r'^add_series/$','main.views.add_series'),
                       (r'^series/(?P<id>\d+)/$','main.views.series'),
                       (r'^series/(?P<id>\d+)/edit/$','main.views.edit_series'),
                       (r'^series/(?P<id>\d+)/delete/$','main.views.delete_series'),
                       (r'^series/(?P<id>\d+)/remove_tag/(?P<tagname>\w+)/$','main.views.remove_tag_from_series'),
                       (r'^series/(?P<id>\d+)/rss/$', SeriesFeed()),
                       (r'^video/(?P<id>\d+)/edit/$','main.views.edit_video'),
                       (r'^video/(?P<id>\d+)/delete/$','main.views.delete_video'),
                       (r'^video/(?P<id>\d+)/remove_tag/(?P<tagname>\w+)/$','main.views.remove_tag_from_video'),
                       (r'^file/$','main.views.file_index'),
                       (r'^file/(?P<id>\d+)/$','main.views.file'),
                       (r'^user/(?P<username>\w+)/','main.views.user'),
                       (r'^file/(?P<id>\d+)/delete/$','main.views.delete_file'),
                       (r'^file/(?P<id>\d+)/surelink/$','main.views.file_surelink'),
                       (r'^operation/(?P<id>\d+)/delete/$','main.views.delete_operation'),
                       (r'^tag/$','main.views.tags'),
                       (r'^tag/(?P<tagname>\w+)/$','main.views.tag'),
                       (r'^upload/$', 'main.views.upload'),
                       (r'^scan_directory/$', 'main.views.scan_directory'),
                       (r'^vital/',include('vital.urls')),
                       (r'^vitaldrop/$', 'vital.views.drop'),
                       (r'^mediathread/$', 'main.views.mediathread'),
                       (r'^youtube/$','main.views.youtube'),
                       (r'^youtube/done/$','main.views.youtube_done'),
                       (r'^done/$','main.views.done'),
                       (r'^surelink/$','main.views.surelink'),
                       (r'^video/$','main.views.video_index'),
                       (r'^video/(?P<id>\d+)/$','main.views.video'),
                       (r'^video/(?P<id>\d+)/pcp_submit/$','main.views.video_pcp_submit'),
                       (r'^video/(?P<id>\d+)/mediathread_submit/$','main.views.video_mediathread_submit'),
                       (r'^video/(?P<id>\d+)/zencoder_submit/$','main.views.video_zencoder_submit'),
                       (r'^video/(?P<id>\d+)/add_file/$','main.views.video_add_file'),
                       (r'^video/(?P<id>\d+)/select_poster/(?P<image_id>\d+)/$','main.views.video_select_poster'),
                       (r'^list_workflows/$','main.views.list_workflows'),
                       (r'^search/$','main.views.search'),
                       (r'^api/tagautocomplete/$','main.views.tag_autocomplete'),
                       (r'^api/subjectautocomplete/$','main.views.subject_autocomplete'),
                       (r'^celery/', include('djcelery.urls')),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
) 

