from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from main.views import (
    HomeView,
    NewsletterCreateView,
    ArticleDetailsView,
    CommentCreateView,
    ContactView,
    CategoryView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),

    # Maqola tafsilotlari uchun URL (HTMLdagi 'article-details'ga moslandi)
    path('articles/<slug:slug>/', ArticleDetailsView.as_view(), name='article-details'),

    path('newsletter/create/', NewsletterCreateView.as_view(), name='newsletter-create'),

    path('<slug:slug>/add-comment/', CommentCreateView.as_view(), name='comment_create'),

    path('contact-us/', ContactView.as_view(), name='contact-us'),

    path('<slug:slug>/articles/', CategoryView.as_view(), name='category'),
]

# Media fayllar (rasmlar) uchun sozlama
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)