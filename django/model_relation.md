## :rocket: model relation



#### :ocean: Foreign Key

* 외래 키
* many-to-one relationship
* 키를 사용하여 부모 테이블의 유일한 값을 참조(참조 무결성)
* 외래키는 반드시 유일한 값이어야 함
* 참조하는 테이블에서 1개의 키에 해당하고, 이는 참조되는 측 테이블의 기본 키를 가리킴.
* 참조하는 테이블의 행 여러개가, 참조되는 테이블의 동일한 행을 참조할 수 있음.

##### :heavy_check_mark: 참조 무결성

​	데이터베이스 관계 모델에서 관련된 2개의 테이블 간의 일관성



#### :ocean: article - comment 사이 1:N 관계



```python
# articles/models.py

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
```

##### :heavy_check_mark: on_delete : 부모 객체(참조 된 객체)가 삭제 됐을 때 이를 참조하는 객체도 삭제

​	(글이 삭제되면 댓글도 삭제)

##### :heavy_check_mark: 데이터 무결성 : 데이터의 정확성과 일관성을 유지하고 보증하는 것



모델에 변화가 생겼으니 migration 진행

article_comment 테이블에 article_id 라는 컬럼이 생김



#### :ocean: 1:N 관계 related manager

##### 참조

comment > article

`comment.article` 로 접근

##### 역참조

article > comment

`article.comment_set` 로 접근

역참조 시 사용할 이름 `model_set` 은 related_name 으로 설정 가능

```python
# arciels/models.py

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
	...
```

related_name 변경 시

`article.comments` 로 접근

모델에 변화가 생겼으니 migration 진행



#### :ocean: Comment CRUD

##### :blue_book: CREATE

```python
# articles/forms.py

class CommntForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'
```

article detail 페이지에 댓글 폼 보이기

```python
# articles/views.py

from .forms import CommentForm
@require_safe
def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm()
    context = {
        'article': article,
        'comment_form': comment_form
    }
    return render(request, 'articles/detail.html', context)
```

```html
# articles/detail.html

<form action="" method="POST">
  {% csrf_token %}
  {{ comment_form.as_p }}
  <input type="submit">
</form>
<hr>
```

입력 폼에 article 을 선택하는 창을 없애기 위해 CommentForm 수정

```python
# articles/forms.py

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ('article',)
```

```python
# articles/urls.py

app_name = 'articles'
urlpatterns = [
	...
    path('<int:pk>/create_comment/', views.create_comment, name='create_comment'),	# 추가
]

```

```python
# articles/views.py

@require_POST
def create_comment(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.save()
        return redirect('articles:detail', article.pk)
    return redirect('accounts:login')
```

##### :heavy_check_mark: save() method

​	save(commit=False): 아직 데이터베이스에 저장되지 않은 인스턴스를 반환

​	article을 지정해줘야 하기 때문에

```python
# articles/detail.py

<form action="{% url 'articles:delete' article.pk %}" method="POST">
  {% csrf_token %}
  <input type="submit" value="삭제">
</form>
```



##### :blue_book: READ

```python
# articles/views.py

@require_safe
def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm()
    comments = article.comments.all()
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)
```

```html
# articles/detail.html

<ul>
  {% for comment in comments %}
    <li>{{ comment.content }}</li>
  {% endfor %}
</ul>
```



##### :blue_book: DELETE

```python
# articles/urls.py

app_name = 'articles'
urlpatterns = [

    path('<int:article_pk>/comment_delete/<int:comment_pk>/', views.comment_delete, name='comment_delete'),
]

```

```python
# articles/views.py

@require_POST
def comment_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
    return redirect('articles:detail', article_pk)
```

```html
# articles/detail.py

<ul>
  {% for comment in comments %}
    <li>{{ comment.content }}</li>
    <form action="{% url 'articles:comment_delete' article.pk comment.pk %}" method="POST">
      {% csrf_token %}
      <input type="submit" value="delete">
    </form>
  {% endfor %}
</ul>
```



#### :ocean: User - Article 사이 1:N 관계

##### :blue_book: User 모델 참조하기

`setting.AUTH_USER_MODEL` 

User 모델에 대한 외래 키 또는 다대다 관계를 정의할 때

models.py 에서 사용

`get_user_model()`

현재 활성화된 User 모델을 반환

models.py 가 아닌 모든 곳에서 사용



```python
# articles/models.py

from django.conf import settings

class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ...
```

모델에 변화가 생겼으니 migration 진행

```python
# articles/forms.py

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        # fields = '__all__'
        fields = ('title', 'content',)
        exclude = ('user',)
```

```python
# articles/views.py
# article create 함수

			if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()

# article delete 함수

@require_POST
def delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user.is_authenticated:
        if request.user == article.user:			# 작성자만 삭제 가능
            article.delete()
            return redirect('articles:index')
    return redirect('accounts:detail', article.pk)

# article update 함수
@require_http_methods(['GET', 'POST'])
@login_required
def update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user == article.user:				# 작성자만 수정 가능
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'articles/update.html', context)
```

```html
# articles/detail.html

{% if user == article.user %}
  <form action="{% url 'articles:delete' article.pk %}" method="POST">
    {% csrf_token %}
    <input type="submit" value="삭제">
  </form>
  <a href="{% url 'articles:update' article.pk %}">update</a>
{% endif %}
```

작성자만 삭제, 수정 버튼 볼 수 있게



#### :ocean: User - Comment 사이 1:N 관계

```python
# articles/models.py

class Comment(models.Model):
	...
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	...
```

모델에 변화가 생겼으니 migrations 진행

```python
# articles/forms.py

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ('article', 'user',)			# user필드 추가제거
```



##### CREATE

```python
# articles/views.py
# comment create 함수

			comment.user = request.user
```



##### READ

비로그인 유저에게는 댓글 form 출력 하지않기

```html
# articles/detail.html

{% if request.user.is_authenticated %}
  <form action="{% url 'articles:create_comment' article.pk%}" method="POST">
    {% csrf_token %}
    {{ comment_form.as_p }}
    <input type="submit">
  </form>
{% else %}
  <a href="{% url 'accounts:login' %}">[댓글을 작성하려면 로그인하세요]</a>
{% endif %}
```



##### DELETE

자기가 작성한 댓글만 삭제 가능

```python
# articles/views.py

@require_POST
def comment_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('articles:detail', article_pk)
```

```html
# articles/detail.py

<ul>
  <p>{{ comments | length }} 개의 댓글</p>
  {% for comment in comments %}
    <li>{{ comment.content }}</li>
    {% if user == comment.user %}			# 댓글 작성자만 삭제 버튼
      <form action="{% url 'articles:comment_delete' article.pk comment.pk %}" method="POST">
        {% csrf_token %}
        <input type="submit" value="delete">
      </form>
    {% endif %}
  {% endfor %}
</ul>
```



#### :ocean: M: N 관계

​	Many-To-Many 관계

​	django ManyToManyField 를 통해 중개 테이블을 자동 생성

​	두 개의 모델 사이에 관계를 맺으면 `model_id` / `model2_id`  컬럼을 가진 중개테이블이 생성됨

​	한 개의 모델에서 관계를 맺으면 `from_model_id` / `from_model_id` 컬럼을 가진 중개테이블이 생성됨



#### :ocean: Like 구현 (User - Article M:N 관계)

```python
# articles/models.py

class Article(models.Model):
    ...
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    ...
```

모델에 변화가 생겼으니 migration 진행



```python
# articles/urls.py

app_name = 'articles'
urlpatterns = [
	...
    path('<int:article_pk>/likes/', views.like, name='like'),
]

```

```python
# articles/views.py

@require_POST
def like(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        # article을 좋아요 한 목록에 있으면 삭제, 그렇지 않으면 추가
        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)
        else:
            article.like_users.add(request.user)
        return redirect('articles:index')
    return redirect('accounts:login')
```

##### :heavy_check_mark: QuerySet API `exists()`

​		QuerySest에 결과가 포함되어 있으면 True를 반환, 그렇지 않으면 False

​		규모가 큰 QuerySet 컨텍스트에서 특정 개체 존재 여부와 관련된 검색에 유용



```html
# articles/index.html

  <form action="{% url 'articles:like' article.pk %}" method="POST">
    {% csrf_token %}
    {% if user in article.like_users.all %}
      <input type="submit" value="좋아요 취소">
    {% else %}
      <input type="submit" value="좋아요">
    {% endif %}
  </form>
```

user가 좋아요를 누른 목록에 있다면 좋아요 취소 버튼이 보이도록



#### :ocean: 프로필 페이지 만들기

```python
# accounts/urls.py

app_name = 'accounts'
urlpatterns = [
	...
    path('<username>/', views.profile, name='profile'),
]
```

```python
# accounts/views.py

def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person' : person,
    }
    return render(request, 'accounts/profile.html', context)
```

```html
# articles/profile.html

{% extends 'base.html' %}

{% block content %} 
  <h2>{{ person.username }} 의 프로필</h2>
  <hr>

  <h2>{{ person.username }}이 작성한 게시글</h2>
  {% for article in person.article_set.all %}
    {{ article.title }}
  {% endfor %}

  <h2>{{ person.username }}이 작성한 댓글</h2>
  {% for comment in person.comments.all %}
    {{ comment.content }}
  {% endfor %}

  <h2>{{ person.username }}이 좋아요 한 게시글</h2>
  {% for article in person.like_articles.all %}
    {{ article.title }}
  {% endfor %}
  <hr>

  <a href="{% url 'articles:index' %}">main</a>

{% endblock content %} 
```

```html
# articles/index.html

<a href="{% url 'accounts:profile' article.user.username %}">{{ article.user }}</a> # 추가
```



#### :ocean: Follow 구현 (User - User M:N 관계)

```python
# accounts/models.py

class User(AbstractUser):
    name = models.TextField()
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
```

##### :heavy_check_mark: symmetrical

​	ManyToManyField가 동일한 모델(on self)을 가리키는 젖ㅇ의에서만 사용

​	symmetrical=True(기본값)일 경우 django는 model_set 매니저를 추가하지않음

​	대칭을 원하지 않는 경우 False로 설정(ex 내 친구가 팔로우한 것을 나까지 팔로우)



모델에 변화가 생겼으니 migration 진행



```python
app_name = 'accounts'
urlpatterns = [
	...
    path('<int:user_pk>/follow/', views.follow, name='follow'),
]
```

```python
# articles/views.py

@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), pk=user_pk)
        if person != request.user:              #  내가 아닐 때만 팔로우 가능
            # 팔로우 목록에 있다면 제거
            if person.followers.filter(pk=request.user.pk).exists():
                person.followers.remove(request.user)
            else:
                person.followers.add(request.user)
        return redirect('accounts:profile', person.username)
    return redirect('accounts:login')
```

```html
# accounts/profile.html

  <p>팔로잉수 : {{ person.followings.all | length }}</p>
  <p>팔로워수 : {{ person.followers.all | length }}</p>
  {% if user != person %}
    <div>
      <form action="{% url 'accounts:follow' person.pk %}" method="POST">
        {% csrf_token %}
        {% if user in person.followers.all %}
          <input type="submit" value="팔로우 취소">
        {% else %}
          <input type="submit" value="팔로우">
        {% endif %}
      </form>
    </div>
  {% endif %}
```

