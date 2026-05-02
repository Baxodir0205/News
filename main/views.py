from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Newsletter, Category, Contact, Comment


class HomeView(View):
    def get(self, request):
        top_articles = Article.pub_objects.order_by('-important', '-views')[:10]
        latest_news = Article.pub_objects.order_by('-created_at')[:5]
        most_viewed = Article.pub_objects.order_by('-views')[:5]
        lifestyle = Article.pub_objects.filter(category__name__icontains='life').order_by('-created_at')[:2]

        categories = Category.objects.all()
        whats_new = []

        for category in categories:
            articles = Article.pub_objects.filter(
                category=category
            ).order_by('-created_at')[:6]

            if articles.exists():
                whats_new.append({
                    'category': category,
                    'articles': articles,
                })

        context = {
            "top_articles": top_articles,
            "latest_news": latest_news,
            "most_viewed": most_viewed,
            "lifestyle": lifestyle,
            "whats_new": whats_new,
        }
        return render(request, 'index.html', context)


class NewsletterCreateView(View):
    def post(self, request):
        Newsletter.objects.create(
            email=request.POST['email'],
        )
        return redirect('home')


class ArticleDetailsView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article.pub_objects, slug=slug)
        related_articles = Article.pub_objects.filter(
            category=article.category
        ).exclude(slug=slug).order_by('-created_at')[:2]

        context = {
            'article': article,
            'related_articles': related_articles,
        }
        return render(request, 'detail-page.html', context)


class CommentCreateView(View):
    def post(self, request, slug):
        Comment.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            content=request.POST['text'],
            article=get_object_or_404(Article, slug=slug),
        )
        return redirect('article-details', slug=slug)


class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')

    def post(self, request):
        Contact.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone_number=request.POST.get('phone'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        return redirect('contact-us')




class CategoryView(View):
    def get(self, request, slug):
        category = get_object_or_404(Category.objects, slug=slug)
        articles = Article.pub_objects.filter(category=category).order_by('-created_at')
        context = {
            'category': category,
            'articles': articles,

        }
        return render(request, 'category.html', context)