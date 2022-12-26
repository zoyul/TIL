# :rocket: Django User!!



### :full_moon_with_face: Application 생성 및 등록

```bash
$ python manage.py startapp accounts
```

##### auth와 관련해서 django 내부적으로 accounts라는 이름으로 사용되고 있으므로 accounts로 지정하는 것을 권장



```python
# setting.py

INSTALLED_APPS = [
    'accounts',
]
```

```python
# urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]

```

```python
# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    
]
```



### :full_moon_with_face: main 페이지 만들기(index)

##### 	User 목록 내보낼거임

```python
# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),		# 추가
]
```

```python
# accounts/views.py

from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    userlist = User.objects.all()
    context = {
        'userlist': userlist
    }
    return render(request, 'accounts/index.html', context)
```

##### 	usercreationform을 보면 User를 상속받음

```html
# accounts/template/accounts/index.html

{% extends 'base.html' %}

{% block content %}
  <h2>Main</h2>
  <hr>
  {% for user in userlist %}
    <p>{{ user }}</p>
  {% endfor %}
  <hr>
{% endblock content %}
```



### :full_moon_with_face: 가입

```python
# urls.py

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),		# 추가
]
```

```python
# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    else:
        form = UserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/signup.html', context)
```

```html
# accounts/template/accounts/signup.html

{% extends 'base.html' %}

{% block content %}
  <h2>Sign up</h2>
  <hr>
  <form action="" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
  </form>
  <a href="{% url 'accounts:index' %}">main</a>
{% endblock content %}
```



##### :heavy_check_mark: index.html에 추가

```html
  <a href="{% url 'accounts:signup' %}">Signup</a>
```



### :full_moon_with_face: 로그인

##### 	AuthenticationForm 이용

```python
# accounts/urls.py

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login')					#추가
]
```

```python
# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('accounts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)
```

##### :cactus: auth_login

##### 	login이라는 django 내부 함수가 views.py 에 지정한 함수와 이름이 겹쳐서 이름을 바꾸어서 import함

##### :cactus: get_user()

##### 	AuthenticationForm의 인스턴스 메서드

##### 	유효성 검사를 통과했을 경우, 로그인 한 사용자 객체로 할당 됨

##### 	인스턴스의 유효성을 먼저 확인하고, 인스턴스가 유효할 때만 user 제공



```html
# accounts/template/accounts/login.html

{% extends 'base.html' %}

{% block content %}
  <h2>Login</h2>
  <hr>
  <form action="" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
  </form>
{% endblock content %}
```



##### :heavy_check_mark: index.html에 추가

```html
<a href="{% url 'accounts:login' %}">Login</a>
```

##### :heavy_check_mark: views.py에 signup 함수에 추가 ( 가입 후 자동 로그인 기능)

```python
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()						# 수정
            auth_login(request, user)				# 추가
            # auth_login(request, form.save())
            return redirect('accounts:index')
    else:
        form = UserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/signup.html', context)
```

##### :cactus: UserCreationFrom의 save 메서드를 보면 user를 반환함



### :full_moon_with_face: 로그아웃

```python
# accounts/urls.py

urlpatterns = [
    path('logout/', views.logout, name='logout'),			# 추가
]
```

```python
# accounts/views.py

from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_http_methods, require_POST

@require_POST
def logout(request):
    auth_logout(request)
    return redirect('accounts:index')
```



##### :heavy_check_mark: index.html 에 추가

```html
  <form action="{% url 'accounts:logout' %}" method="POST">
    {% csrf_token %}
    <input type="submit" value="logout">
  </form>
```





## :carrot: 로그인 사용자 접근 제한 !!

​	`is_authenticated ` attribute

​	`login_required` decorator

#### 	* is_authenticated 속성

##### 		User model의 속성 중 하나, 모든 User인스턴스에 대해 항상 True(AnonymousUser는 False)

```html
# accounts/index.html

{% extends 'base.html' %}

{% block content %}
  <h2>Main</h2>
  {% if request.user.is_authenticated %}
    <form action="{% url 'accounts:logout' %}" method="POST">
      {% csrf_token %}
      <input type="submit" value="logout">
    </form>
  
  {% else %}
    <a href="{% url 'accounts:signup' %}">Signup</a>
    <a href="{% url 'accounts:login' %}">Login</a>
  
  {% endif %}
  <hr>
  {% for user in userlist %}
    <p>{{ user }}</p>
  {% endfor %}
  <hr>
{% endblock content %}
```

##### 로그인 되어있으면 로그아웃 버튼만 보이고 로그아웃 되어있으면 signup, login 링크 보임



```python
# views.py

def login(request):
    if request.user.is_authenticated:			# 맨 위에 추가
        return redirect('accounts:index')
    
def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')		# 맨 위체 추가
```

##### 로그인 상태라면 더이상 로그인X main으로 보내기



```python
# views.py

@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)    
    return redirect('accounts:index')
```

##### 로그인 상태인 유저만 로그아웃 가능



#### * login_required decorator

##### 	사용자가 로그인 되어있지 않으면, settings.LOGIN_URL에 설정된 경로로 redirect함

##### 	LOGIN_URL의 기본값은 '/accounts/'

##### 	사용자가 로그인되어 있으면 정상적으로 view함수 실행

##### 	인증 성공 시 사용자가 redirect 되어야하는 경로는 'next'라는 쿼리 문자열 매개 변수에 저장됨

##### 	ex) /accounts/login/?next=/articles/create/

```python
# articles/views.py

from django.contrib.auth.decorators import login_required

@login_required	
@require_http_methods(['GET', 'POST'])
def create(request):
	pass

@login_required								# 근데 문제발생
@require_POST
def delete(request, pk):
	pass

@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
	pass
```

##### :cactus: 비로그인 상태에서 게시글 삭제를 시도할 경우

##### 	redirect로 로그인 페이지로 이동 -> 로그인 시도 -> 405 오류

##### 	로그인 이후 next 매개변수에 따라 해당 함수로 redirect하는데 이때 method는 GET이다

##### 	require_POST에서 걸려버림!! (아래 코드로 해결)

##### 	* login_required는 GET method reqeust를 처리할 수 있는 곳에서만 작성!!

```python
# articles/views.py

@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        article =  get_object_or_404(Article, pk=pk)
        article.delete()
    return redirect('articles:index')
```



```python
# accounts/views.py

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'accounts:index')
			# 마지막줄 수정
```

##### login.html의 action값 비우기

##### 현재 URL로(next parameter가 있는) 요청을 보내기 위해



### :full_moon_with_face: 회원 탈퇴

```python
# accounts/urls.py

urlpatterns = [
    path('delete/', views.delete, name='delete'),
]
```

```python
# accounts/views.py

@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('accounts:index')
```



##### :heavy_check_mark: index.html에 추가

```html
<form action="{% url 'accounts:delete' %}" method="POST">
    {% csrf_token %}
    <input type="submit" value="회원탈퇴">
</form>
```



### :full_moon_with_face: 회원정보 수정

```python
# accounts/urls.py

urlpatterns = [
    path('update/' , views.update, name='update'),				# 추가
]
```

```python
# accounts/forms.py			# 파일 생성

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',)
```

##### 	회원정보 수정 form에 내가 원하는 field만 내보내기 위해 custom form을 생성

```python
# accounts/views.py

from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm

@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)
```

```html
# accounts/update.html

{% extends 'base.html' %}

{% block content %}
<h1>회원정보 수정</h1>
<hr>
<form action="" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="수정">
</form>
<a href="{% url 'accounts:index' %}">main</a>

{% endblock content %}
```



##### :heavy_check_mark: index.html에 추가

```html
<a href="{% url 'accounts:update' %}">회원정보 수정</a>
```





### :full_moon_with_face: 비밀번호 수정

```python
# accounts/urls.py

urlpatterns = [
    path('password/', views.change_password, name='change_password'),	#추가
]
```

```python
# accounts/views.py

from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)
```

```python
# accounts/change_password.html

{% extends 'base.html' %}

{% block content %}
  <h1>비밀번호 변경</h1>
  <form action="{% url 'accounts:change_password' %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
  </form>
{% endblock content %}
```





##### :heavy_check_mark: index.html에 추가

```html
<a href="{% url 'accounts:change_password' %}">비밀번호 수정</a>
```
