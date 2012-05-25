from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from wardenclyffe.main.feeds import CollectionFeed
from django.views.generic.simple import direct_to_template
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
                       ('^$','main.views.index'),
                       ('^dashboard/','main.views.dashboard'),
                       ('^recent_operations/','main.views.recent_operations'),
                       ('^most_recent_operation/','main.views.most_recent_operation'),
                       ('^accounts/',include('djangowind.urls')),
                       ('^cuit/',include('cuit.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^capture/file_upload','main.views.test_upload'),
                       (r'^add_collection/$','main.views.add_collection'),
                       (r'^collection/(?P<id>\d+)/$','main.views.collection'),
                       (r'^collection/(?P<id>\d+)/videos/$','main.views.all_collection_videos'),
                       (r'^collection/(?P<id>\d+)/operations/$','main.views.all_collection_operations'),
                       (r'^collection/(?P<id>\d+)/edit/$','main.views.edit_collection'),
                       (r'^collection/(?P<id>\d+)/delete/$','main.views.delete_collection'),
                       (r'^collection/(?P<id>\d+)/remove_tag/(?P<tagname>\w+)/$','main.views.remove_tag_from_collection'),
                       (r'^collection/(?P<id>\d+)/rss/$', CollectionFeed()),
                       (r'^video/(?P<id>\d+)/edit/$','main.views.edit_video'),
                       (r'^video/(?P<id>\d+)/delete/$','main.views.delete_video'),
                       (r'^video/(?P<id>\d+)/remove_tag/(?P<tagname>\w+)/$','main.views.remove_tag_from_video'),

                       (r'^breakme/$','main.views.breakme'),

                       (r'^server/$','main.views.servers'),
                       (r'^server/add/$','main.views.add_server'),
                       (r'^server/(?P<id>\d+)/$','main.views.server'),
                       (r'^server/(?P<id>\d+)/edit/$','main.views.edit_server'),
                       (r'^server/(?P<id>\d+)/delete/$','main.views.delete_server'),

                       (r'^file/$','main.views.file_index'),
                       (r'^file/(?P<id>\d+)/$','main.views.file'),

                       (r'^file/filter/$','main.views.file_filter'),
                       (r'^operation/(?P<uuid>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/info/$','main.views.operation_info'),
                       (r'^operation/(?P<uuid>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/$','main.views.operation'),

                       (r'^bulk_file_operation/$','main.views.bulk_file_operation'),
                       (r'^user/(?P<username>\w+)/','main.views.user'),
                       (r'^file/(?P<id>\d+)/delete/$','main.views.delete_file'),
                       (r'^file/(?P<id>\d+)/surelink/$','main.views.file_surelink'),
                       (r'^file/(?P<id>\d+)/submit_to_workflow/$','main.views.file_pcp_submit'),
                       (r'^operation/(?P<id>\d+)/delete/$','main.views.delete_operation'),
                       (r'^tag/$','main.views.tags'),
                       (r'^tag/(?P<tagname>\w+)/$','main.views.tag'),
                       (r'^upload/$', 'main.views.upload_form'),
                       (r'^upload/post/$', 'main.views.upload'),
                       (r'^scan_directory/$', 'main.views.scan_directory'),
                       (r'^vital/',include('vital.urls')),
                       (r'^vitaldrop/$', 'vital.views.drop'),
                       (r'^mediathread/$', 'mediathread.views.mediathread'),
                       (r'^mediathread/post/$', 'mediathread.views.mediathread_post'),
                       (r'^youtube/$','youtube.views.youtube'),
                       (r'^youtube/done/$','youtube.views.youtube_done'),
                       (r'^uploadify/$','main.views.uploadify'),
                       (r'^done/$','main.views.done'),
                       (r'^posterdone/$','main.views.posterdone'),
                       (r'^received/$','main.views.received'),
                       (r'^surelink/$','main.views.surelink'),
                       (r'^video/$','main.views.video_index'),
                       (r'^video/(?P<id>\d+)/$','main.views.video'),
                       (r'^video/(?P<id>\d+)/pcp_submit/$','main.views.video_pcp_submit'),
                       (r'^video/(?P<id>\d+)/mediathread_submit/$','mediathread.views.video_mediathread_submit'),
                       (r'^video/(?P<id>\d+)/zencoder_submit/$','main.views.video_zencoder_submit'),
                       (r'^video/(?P<id>\d+)/add_file/$','main.views.video_add_file'),
                       (r'^video/(?P<id>\d+)/select_poster/(?P<image_id>\d+)/$','main.views.video_select_poster'),
                       (r'^list_workflows/$','main.views.list_workflows'),
                       (r'^search/$','main.views.search'),
                       (r'^uuid_search/$','main.views.uuid_search'),
                       (r'^api/tagautocomplete/$','main.views.tag_autocomplete'),
                       (r'^api/subjectautocomplete/$','main.views.subject_autocomplete'),
                       (r'^celery/', include('djcelery.urls')),
                       (r'munin/total_videos/','main.views.total_videos'),
                       (r'munin/total_files/','main.views.total_files'),
                       (r'munin/total_operations/','main.views.total_operations'),
                       (r'munin/total_minutes/','main.views.total_minutes'),
                       ('^munin/',include('munin.urls')),

                       ('^stats/',direct_to_template, {'template': 'main/stats.html'}),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
) 

