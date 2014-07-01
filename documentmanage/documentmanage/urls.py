from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('doc.views',
    # Examples:
    # url(r'^$', 'documentmanage.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$','d_login'),
    url(r'^adddepart/$','add_depart'),
    url(r'^modifydepart/(\d+)/$','modify_depart'),
    url(r'^resetpass/$','reset_pass'),
    url(r'^upload/$','upload'),
    url(r'^delete/(\d+)/$','delete'),
    url(r'^modify/(\d+)/$','modify'),
    url(r'^download/(\d+)/$','download'),
    url(r'^logout/$','d_logout'),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
    url(r'^site_media/(?P<path>.*)','django.views.static.serve',{'document_root': '/home/xuk/PycharmProjects/documentmanage/static/'}),




)