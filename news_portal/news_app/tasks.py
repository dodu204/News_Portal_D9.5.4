from datetime import timedelta
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Category, Article
from .mail import send_article_email, send_weekly_articles_email
from django.conf import settings

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')


def send_new_article_emails():
    categories = Category.objects.all()
    for category in categories:
        articles = Article.objects.filter(category=category).order_by('-created_at')[:5]
        for article in articles:
            subscribers = category.subscribers.all()
            for user in subscribers:
                send_article_email(article, user)


def send_weekly_articles_emails():
    categories = Category.objects.all().prefetch_related('subscribers', 'article_set')
    for category in categories:
        subscribers = category.subscribers.all()
        for user in subscribers:
            articles = category.article_set.filter(created_at__gt=timedelta(weeks=1))
            if articles.exists():
                send_weekly_articles_email(category, articles, user)


def register_scheduler_jobs():
    scheduler.add_job(send_new_article_emails, 'interval', minutes=settings.SCHEDULER_RUN_EVERY_MINS)
    scheduler.add_job(send_weekly_articles_emails, 'interval', weeks=1)
    scheduler.start()
