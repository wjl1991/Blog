#coding:utf-8

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

try:
    import pytz
except:
    pass

from models import Article, ArticleManage, Category, Tag, BlogComment, UserProfile

def create_article():
    # time_2011_8 = datetime.datetime(2011, 8, 22, 11, 23, 45, 564, tzinfo=pytz.utc)
    # article2 = Article.objects.create(title='title2', body='article',created_time=time_2011_8,\
    pass

class IndexViewTests(TestCase):
    def setUp(self):
        article1 = Article.objects.create(title='title1', body='article',status='p')
        article2 = Article.objects.create(title='title2', body='article',status='p')
        time_now = timezone.now() + timezone.timedelta(seconds=20)
        article3 = Article.objects.create(title='title3', body='article',created_time=time_now,last_modified_time=time_now, status='p', topped=True)
        time_now = timezone.now() + timezone.timedelta(seconds=30)
        article4 = Article.objects.create(title='title4', body='article',created_time=time_now,last_modified_time=time_now, status='p', topped=True)
        
    def test_get_queryset_with_topped(self):
        '''
        if articles contains topped and untopped, the topped one should be first.
        '''
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(response.context[2]['article_list'],['<Article: title3>', '<Article: title4>','<Article: title1>', '<Article: title2>'])

    def test_get_context_data(self):
        response = self.client.get(reverse('blog:index'))
        time_now = timezone.now()
        self.assertQuerysetEqual(response.context[1]['date_archive'],['(%s, [%s])' % (time_now.year, time_now.month)])
        
class ArticleDetaiilViewTests(TestCase):
    def setUp(self):
        category1 = Category.objects.create(name='category1')
        tag1 = Tag.objects.create(name='tag1')
        body_with_markdown = '''
            ```python
            def justcode(args):
                if args:
                    print 'Func has args'
                else:
                    print 'Func does\'t have args
            ```
        '''
        body_without_markdown = '''
            def justcode(args):
                if args:
                    print 'Func has args'
                else:
                    print 'Func does\'t have args
        '''
        self.article1 = Article.objects.create(title='title1', body=body_with_markdown, status='p', category=category1)
        article2 = Article.objects.create(title='title2', body='article',status='p')
        # 多对多的数据要用add添加
        article2.tags.add(tag1)
        article3 = Article.objects.create(title='title3', body=body_without_markdown, status='p', category=category1)
        article3.tags.add(tag1)
        article4 = Article.objects.create(title='title4', body='article', status='p')
    def test_get_object(self):
        response = self.client.get(reverse('blog:detail',args=(self.article1.id,)))
        print response
        self.assertQuerysetEqual(response.context[2]['article_list'],['<Article: title3>', '<Article: title4>','<Article: title1>', '<Article: title2>'])