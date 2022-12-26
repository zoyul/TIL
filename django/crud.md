## :rocket: Django CRUD!!!



### :ocean: 

####  :black_small_square: ​application 생성, 등록

```bash
$ python manage.py startapp articles		# application 생성
```

##### :grey_exclamation: application 이름은 복수형을 권장



```python
# setting.py				# 앱 등록

INSTALLED_APPS = [
    'articles,'
    'django.contrib.admin',
	...
]
```

##### :grey_exclamation: 무조건 앱 생성 후 등록



####  :black_small_square: ​Model 생성

```python
# articles/models.py

from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) #생성시간
    updated_at = models.DateTimeField(auto_now=True)	#수정시간
    
    def __str__(self):				# admin site에서 보여지는 모습
    	return self.title
```



####  :black_small_square: ​Migration

```bash
$ python manage.py makemigrations		# 새로운 마이그레이션을 만듦
$ python manage.py migrate				# migration을 DB에 반영
```

##### :grey_exclamation: Model 에 변화가 생길 때마다 해줌



####  :black_small_square: ​Admin

```bash
$ python manage.py createsuperuser		# admin 계정 생성
```

##### admin 계정에서 관리하기 위해 Model 등록

```python
# articles/admin.py

from django.contrib import admin
from .models import Article

# Register your models here.
admin.site.register(Article)		#admin site에 등록
```



### :ocean: CRUD 작성준비!!



#### :black_small_square: url 정리

```python
# crud/urls.py

from django.contrib import admin
from django.urls import path, include		# 'include' import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls'))		# 추가
]
```

##### :grey_exclamation: app을 여러개 생성할 때 url주소가 겹칠 수 있어서 app끼리 따로 작성

##### 	주소가 articles/~ 로 시작하게 됨



#####  app아래에 urls.py 파일을 만들고 코드 작성

```python
# articles/urls.py

from django.urls import path

app_name = 'articles'
urlpatterns = [
    
]		# 여기까지 작성해둬야 오류가 안남
```



#### :black_small_square: 상속

##### 가장 바깥에 templates 폴더 생성 후(프로젝트와 같은 레벨), base.html 파일 생성

```python
# settings.py

TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR/ 'templates'],
        ...
    }
]
```

##### :grey_exclamation: django는 app 안의 templates 라는 폴더까지만 읽을 수 있음.  바깥에 위치한 base.html 을 읽게 하기 위해서 경로를 정해줌



```html
# base.html

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  {% block content %}
  
  {% endblock content %}
</body>
</html>
```

##### :grey_exclamation: block tag 바깥을 감싸는 내용을 상속해줄 수 있음



```html
# .html

{% extends 'base.html' %}

{% block content %}
	~내용~
{% endblock content %}
```

##### :grey_exclamation: block tag 안에 내용 작성

##### :grey_exclamation: extends 태그는 무조건 최상단



---



### :ocean: CRUD 작성!!

##### 	:bulb: :bulb: ​​ urls  -> views -> html 순서로 작성



#### :black_small_square:  READ

```python
# articles/urls.py

from django.urls import path
from . import views					# views.index를 작성해야하니까

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index')
]
```

##### :grey_exclamation: url의 주소가 바뀌었을 때 프로젝트에 작성된 모든 url을 수정하기 어렵기 때문에 이름을 부여

​	`<a href="{% url 'articles:index' %}">Main</a>`  로 표현 가능

##### :grey_exclamation: app이 여러개일 때, url이름이 겹치면 settings.py에 등록된 app 순서대로 url을 찾기 때문에, 충돌을 막기 위해 app_name을 정해줌.



```python
# views.py

from django.shortcuts import render
from .models import Article		# 명시적 상대경로

# Create your views here.
def index(request):
    articles = Article.objects.all()	# Article Model을 읽어옴
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)
```

##### :grey_exclamation: django는 명시적 상대경로를 권장함. 현재파일과 같은 레벨에 있다는 의미의 . 을 찍어줌

##### :grey_exclamation: ​Queryset API

##### 	전체 데이터를 받을 때 `.objects.all()`				현재 QuerySet의 복사본을 반환

##### 	특정 조건의 데이터 만들 때 `.objects.filter()`

##### 	하나의 데이터만 받을 때 `.object.get(pk=1)`		get은 객체가 없으면 DoesNotExist 예외 발생

##### 	정렬 `.order_by('-pk')`



```html
# articles/template/articles/index.html

{% extends 'base.html' %}

{% block content %}
{% for article in articles %}
    <p>Title: {{ article.title }}</p>
    <p>content: {{ article.content }}</p>
{% endfor %}
{% endblock content %}
```

##### :grey_exclamation: html 파일 작성 경로

##### 	django는 templates 까지 읽을 수 있음. app이 여러개일 경우 여러 앱의 teamplate들을 한 곳에 모아두고 찾기 시작함. html파일의 이름이 겹칠 경우 충돌이 생길 수 있기 때문에 app 폴더 안에 templates/articles 라고 폴더를 하나 더 만든 후 그 안에 html 파일을 작성하고 django에게 templates안의 ariticles의 html파일로 가도록 경로를 설정해줌



#### :black_medium_small_square: CREATE

#####  	입력을 받을 Modelform 생성

```python
# articles/forms.py				# 파일 직접 생성

from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = '__all__'		# Model의 모든 필드 상속
```

##### :grey_exclamation: fields 작성법

##### fields = ('title', 'content')  -> 원하는 필드

##### exclude = ('title', ) 	-> 제외하고싶은 필드



##### 추가 기능

```python
class ArticleForm(forms.ModelForm):
    REGION_A = 'sl'
    REGION_B = 'gm'
    REGION_C = 'dj'
    REGION_CHOICES = [
        (REGION_A, '서울'),
        (REGION_B, '구미'),
        (REGION_C, '대전'),
    ]
    region = forms.ChoiceField(choices=REGION_CHOICES, widget=forms.Select)

    class Meta:
        model = Article
        fields = '__all__'
```

##### category 형식으로 나옴 ('서울, 구미, 대전' 은 화면으로 보임)

##### 화면엔 Region: 서울, 구미 대전	/	value 값으로 sl, gm, dj 넘어감



```python
# articles/urls.py

from django.contrib import admin
from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),		#추가
]

```



```python
# articles/views.py

from django.shortcuts import redirect, render		# redirect import
from .forms import ArticleForm		# form을 import함

def create(request):
    # create
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')

    # new								# new를 먼저 작성
    else:
        form = ArticleForm()
    context = {
        'form'  : form,
    }
    return render(request, 'articles/create.html', context)
```

##### :grey_exclamation: POST를 먼저 검사하는 이유

##### 		else 의 뜻은 POST를 제외한 모든 method라는 뜻인데, GET을 먼저 검사할 경우 GET을 제외한 모든 method(POST, PUT 등)가 else문으로 가기 때문에 POST를 먼저 검사해야한다. 우리는 POST로 온 값만 새로 생성할 것이기 때문

##### :grey_exclamation: context가 한단계 앞에 나와있는 이유

##### 		if 문 안의 if문에서 form.is_valid() 로 form의 유효성 검사를 하게 되는데, 만약 POST method로 들어온 값이 유효성 검사를 통과하지 못했을 경우에 갈 곳이 필요하기 때문이다.

##### :grey_exclamation: redirect

##### 	POST는 DB에 조작을 가함. html을 요청하는 것이 아님. html 파일을 받을 수 있는 곳으로 redirect 해야함.

##### :grey_exclamation: 유효성 검사 error message

##### 	.is_valid() 로 유효성 검사를 실행하면 form에 error message가 포함된다.

##### :grey_exclamation: form.save()

##### 	form.save() 를 하면 객체를 반환



```html
# create.html

{% extends 'base.html' %}

{% block content %}
<h2>CREATE</h2>
<form action="{% url 'articles:create' %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>
<a href="{% url 'articles:index' %}">Main</a>
{% endblock content %}
```

##### :grey_exclamation: POST / csrf_token

##### 	데이터는 key=value 형태로 넘어오게 되는데 이 때, key 값이 노출되면 데이터베이스의 구조를 유추할 수 있기 때문에 위험하다. create나 update처럼 DB를 조작하는 역할을 할 땐 최소한의 신원 확인이 필요하기 때문에 CSRF_token을 함께 넘겨준다.

##### :grey_exclamation: form.as_p (.as_ul, .as_table)

##### 각 필드가 `<p>` 태그로 감싸져서 렌더링 됨



##### :heavy_check_mark: index.html에 추가

```html
<a href="{% url 'articles:create' %}">CREATE</a>
```



#### :black_medium_small_square: DETAIL

```python
# articles/urls.py

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),		# 추가
]

```

##### :grey_exclamation: variable routing

#####  변수를 URL 주소로 사용하는 것

##### str이 기본값, int는 따로 표시



```python
# articles/views.py

def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article' : article,
    }
    return render(request, 'articles/detail.html', context)
```

##### :grey_exclamation: pk 인자



```html
# detail.html

{% extends 'base.html' %}

{% block content %}

<p>Title: {{ article.title }}</p>
<p>Content: {{ article.content }}</p>
<p>작성 시간: {{ article.created_at }}</p>
<p>수정 시간: {{ article.updated_at }}</p>
<a href="{% url 'articles:index' %}">Main</a>

{% endblock content %}
```



##### :heavy_check_mark: index.html에 추가

```html
<a href="{% url 'articles:detail' article.pk %}">DETAIL</a>
```

##### :heavy_check_mark: views.py / create함수 변경

```python
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()			# 인자로 받고
            return redirect('articles:detail', article.pk)		# 넘겨주기
    else:
        form = ArticleForm()
    context = {
        'form' : form,
    }
    return render(request, 'articles/create.html', context)
```

##### :grey_exclamation: article.pk  넘겨주기



#### :black_small_square: DELETE

```python
# articles/urls.py

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),	# 추가
]
```

```python
# articles/views.py

def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('articles:index')
    return redirect('articles:detail', article.pk)
```

#####  별도의 html 파일 필요 X



##### :heavy_check_mark: detail.html 에 추가

```html
<form action="{% url 'articles:delete' article.pk %}" method="POST">
  {% csrf_token %}
  <input type="submit" value="DELETE">
</form>
```



#### :black_medium_small_square: UPDATE

```python
# articles/urls.py

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete', views.delete, name='delete'),
    path('<int:pk>/update', views.update, name='update'),	#추가
]
```

```python
# articles/views.py

def update(request, pk):
    article = Article.objects.get(pk=pk)
    # update
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
    # edit
    else:
        form = ArticleForm(instance=article)
    context = {
        'article': article,
        'form' : form,
    }
    return render(request, 'articles/update.html', context)
```

##### :grey_exclamation: ArticleForm의 instance 인자

##### 	ModelForm의 하위 클래스는 기존 모델 인스턴스를 키워드 인자 instance 로 받아들일 수 있음

##### 	instance인자가 제공되면 save()는 해당 인스턴스를 업데이트,

##### 								 제공되지 않으면 save()는 새 인스턴스를 만듦



```html
# update.html

{% extends 'base.html' %}

{% block content %}

<h1>UPDATE</h1>
<form action="{% url 'articles:update' article.pk %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="EDIT">
</form>
<a href="{% url 'articles:detail' article.pk %}">BACK</a>

{% endblock content %}
```



##### :heavy_check_mark: detail.html 에 추가

```html
<a href="{% url 'articles:update' article.pk %}">EDIT</a>
```



---

### :ocean: django를 더 단단하게!!



#### :black_medium_square: django shortcuts functions

##### 			render(),		 redirect(),		 get_object_or_404(), 		get_list_or_404()

##### :carrot: get_object_or_404()

​	모델 manager objects에서 get()을 호출하지만, 객체가 없을 경우 DoesNotExist 대신에 Http 404

​	get() 메서드는 조건에 맞는 데이터가 없으면 Http 500을 보여줌



```python
# views.py

from django.shortcuts import get_object_or_404

def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)		# 수정
	pass

def delete(request, pk):
    article = get_object_or_404(Article, pk=pk)		# 수정
	pass

def update(request, pk):
    article = get_object_or_404(Article, pk=pk)			# 수정
	pass
```



#### :black_medium_square: decorator

​	함수에 기능을 추가하고 싶을 때, 해당 함수를 수정하지 않고 기능을 연장해주는 함수

* ##### require_http_methods()

  view 함수가 특정 method 요청에 대해서만 허용

* ##### require_POST()

  view 함수가 POST method 요청만 승인

* ##### require_GET()

  GET method만 승인. (근데 require_safe를 쓰라고함 장고가)

* ##### require_safe()



```python
# views.py

from django.views.decorators.http import require_http_methods, require_POST, require_safe

@require_safe
def index(request):
    pass

@require_http_methods(['GET', 'POST'])
def create(request):
    pass

@require_safe
def detail(request, pk):
    pass

@require_POST
def delete(request, pk):
    pass

@require_http_methods(['GET', 'POST'])
def update(request, pk):
```



---



### :ocean: CRUD 최종!!!!



```python
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .models import Article
from .forms import ArticleForm

# Create your views here.
@require_safe
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


@require_safe
def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)


@require_POST
def delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('articles:index')


@require_http_methods(['GET', 'POST'])
def update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/update.html', context)
```

