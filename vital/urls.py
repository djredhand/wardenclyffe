from django.conf.urls.defaults import patterns

urlpatterns = patterns('vital.views',
                       (r'^done/$','done',{},'vital-done'),
                       (r'^received/$','received',{},'vital-received'),
                       (r'^posterdone/$','posterdone',{},'vital-posterdone'),
                       (r'^drop/$','drop',{},'vital-drop'),
                       (r'^submit/(?P<id>\d+)/$','submit',{},'vital-submit'),
)
