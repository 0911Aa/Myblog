from django.conf.urls import url
from backend.views import user,trouble
from django.conf.urls import include

urlpatterns = [
    url(r'^index.html$', user.index),
    # url(r'^base-info.html$', user.base_info),
    # url(r'^tag.html$', user.tag),
    # url(r'^category.html$', user.category),
    url(r'^article-(?P<article_type_id>\d+)-(?P<category_id>\d+).html$', user.article,name='article'),
    url(r'^add-article.html$', user.add_article),
    url(r'^edit-article-(?P<nid>\d+).html$', user.edit_article),
    url(r'^delete-article-(?P<nid>\d+).html$',user.delete_article),
    url(r'^trouble.html$',trouble.trouble),
    url(r'^trouble-create.html$',trouble.trouble_create),
    url(r'^trouble-edit-(?P<nid>\d+).html$',trouble.trouble_edit),
    # url(r'^upload-avatar.html$', user.upload_avatar),
]