from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_article_email(article, user):
    subject = f'Новая статья в категории {article.category.name}'
    html_message = render_to_string('mail/new_article.html', {'article': article})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, 'your_email@example.com', [user.email], html_message=html_message)


def send_weekly_articles_email(category, articles, user):
    subject = f'Новые статьи в категории {category.name}'
    html_message = render_to_string('mail/weekly_articles.html', {'category': category, 'articles': articles})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, 'your_email@example.com', [user.email], html_message=html_message)
