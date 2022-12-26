## :rocket: Django REST API



#### :ocean: HTTP

* HyperText Tranfer Protocol

* 웹 상에서 컨텐츠를 전송하기 위한 약속

* HTML 문서와 같은 리소스들을 가져올 수 있도록 하는 프로토콜(규칙, 약속)

* 웹에서 이루어지는 모든 데이터 교환읜 기초

  * request, response

* 쿠키와 세션을 통해 서버 상태를 요청과 연결

* HTTP request methods

  * GET, POST, PUT, DELETE

* HTTP response status codes

  * Informational responses (1xx)

  * Successful responses (2xx)

  * Redirection messages (3xx)

  * Client error responses (4xx)

  * Server error responses (5xx)

    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status



#### :ocean: URI, URL , URN

##### URL

* 통합 자원 식별자
* 인터넷의 자원을 식별하는 유일한 주소(정보의 자원을 표현)
* 인터넷에서 자원을 식별하거나 이름을 지정하는데 사용되는 간단한 문자열
* URL, URN

##### URL

* Uniform Resoure Locator
* '웹 주소', '링크'
* 통합 자원 위치
* 네트워크 상 자원이 어디 있는지 알려주기 위한 약속

##### URN

* Uniform Resource Name
* 통합 자원 이름
* URL과 달리 자원의 위치에 영향을 받지 않는 유일한 이름 역할을 함



#### :ocean: URL

##### 구조

* Scheme(protocal) : 브라우저가 사용하는 프로토콜 (ex https)

* Host(Domain name) : 요청받는 웹 서버의 이름(ip address를 사용할수도있음)

* Port : 웹 서버상의 리소스에 접근하는데 사용되는 기술적인 문

* Path : 웹 서버 상의 리소스 경로

* Query(Identifier) : 웹 서버에 제공되는 추가적인 매개 변수 / &로 구부되는 key-value 목록

* Fragment : 브라우저에서 해당 문서의 특정 부분을 보여주기 위한 방법 

  ​					`#` 뒷부분은 요청이 서버에 보내지지 않음



#### :ocean: API

Application Programming Interface

프로그래밍 언어가 제공하는 기능을 수행할 수 있게 만든 인터페이스

##### Web API

웹 애플리케이션 개발에서 다른 서비스에 요청을 보내고 응답을 받기 위해 정의된 명세

응답 데이터타입: HTML, JSON, XML 등



#### :ocean: REST

REpresentational State Transfer

API Server를 개발하기 위한 일종의 소프트웨어 설계 방법론

##### REST의 자원과 주소의 지정 방법

* 자원(정보) : URL
* 행위 : HTTP Method (GET, POST, PUT, DELETE)
* 표현 : 결과물(JSON 형태로 제공)



#### :ocean: JSON

JavaScript Object Notation

JavaScript 표기법을 따른 단순 문자열

사람이 읽거나 쓰기 쉽고 기계가 파싱(해석, 분석)하고 만들어내기 쉬움

파이썬의 dictionary, 자바스크립트의 object처럼 C 계열의 언어가 갖고 있는 자료구조로 쉽게 변화할 수 있는 key-value형태의 구조를 갖고 있음



#### :ocean: RESTful API

REST 원리를 따라 설계한 API

프로그래밍을 통해 클라이언트의 요청에 JSON을 응답하는 서버를 구성



#### :ocean: JsonResponse

JsonResponse Objects : JSON-encoded response를 만드는 HttpResponse의 서브클래스

`safe=False` : dict 이외의 객체를 직렬화 하려면 False로 설정

```python
# 예시

response = JsonResponse({'foo': 'bar'})
response = JsonResponse([1, 2, 3], safe=False)
```



#### :ocean: Serialization

직렬화

데이터 구조나 객체 상태를 동일하거나 다른 컴퓨터 환경에 저장하고, 나중에 재구성할 수 있는 포맷으로 변화하는 과정

Serializers in Django : Queryset 및 Model Instance와 같은 복잡한 데이터를 JSON, XML 등의 유형으로 쉽게 변환할 수 있는 Python 데이터 타입으로 만들어줌

##### Django의 내장 HttpResponse 활용

```python
from django.http.response import HttpResponse
from django.core import serializers

def article(request):
    articles = Article.objects.all()
    data = serializers.serialize('json', articles)
    return HttpResponse(data, content_type='application/json')
```



##### Django REST Framework(DRF) 라이브러리 활용

사용법

```bash
$ pip install djangorestframework
```

```python
# settings.py

INSTALLED_APPS = [
    ...
    'rest_framework',
]
```



#### :ocean: Django REST Framework(DRF)

Web API 구축을 위한 강력한 Toolkit을 제공하는 라이브러리

DRF의 Serializer는 Django의 Form 및 ModelForm 클래스와 매우 유사하게 구성되고 작동함



##### ModelSerializer

Model이 필드를 어떻게 '직렬화'할 지 설정

Django에서 Model의 필드를 설정하는 것과 동일



##### READ

```python
# articles/serializers.py				# 파일 생성

from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'
```

:heavy_check_mark: ` fields = '__all__'` : 직렬화 할 필드 적기

```python
# articles/views.py

from .serializers import ArticleSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def index(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    serializer = ArticleSerializer(article)
    if request.method == 'GET':
        return Response(serializer.data)
```

:heavy_check_mark: `many=True` : 단일 인스턴스 대신 QuerySet 등을 직렬화하기 위해서는 serializer를 인스턴스화 할 때, many=True를 키워드 인자로 전달해야함

:heavy_check_mark: `api_view` : view 함수가 응답해야 하는 HTTP 메서드의 목록을 리스트의 인자로 받음

​	DRF 에서는 선택이 아닌 필수로 작성해야함



##### CREATE

```python
# articles/views.py

@api_view(['POST'])
def create(request):
    if request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

```

:heavy_check_mark: `raiser_exception` : Raising an excaption on invalid data

​	`is_valid()`는 유효성 검사 오류가 있는 경우 serializers.ValidationError 예외를 발생시키는 선택적 raise_exception인자 사용 가능

​	DRF에서 제공하는 기본 예외 처리기에 의해 자동으로처리되며 기본적으로 HTTP status code 400을 반환

:heavy_check_mark: `status` : status 모듈에 HTTP status code 집합이 모두 포함되어 있음



##### UPDATE

```python
# articles/views.py

@api_view(['PUT'])
def update(request, pk):
    if request.method == 'PUT':
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
```



##### DELETE

```python
# articles/view.py

@api_view(['DELETE'])
def delete(request, pk):
    if request.method == 'DELETE':
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response({'message': '삭제되었습니다'}, status=status.HTTP_204_NO_CONTENT)
```



#### :ocean: 1:N DRF

##### READ

```python
# articles/serializers.py

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article',)
```

:heavy_check_mark: `read_only` : form-data 로 넣지 않을 필드



##### :blue_book: 특정 게시물에 작성된 댓글 목록

:one: view 함수에서 따로 작성

```python
# articles/views.py

@api_view(['GET'])
def comments_list(request, article_pk):
    if request.method == 'GET':
        article = get_object_or_404(Article, pk=article_pk)
        comments = article.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
```

:heavy_check_mark: `comment_set` : models.py 에서 related_name 으로 변경 가능



:two: PrimaryKeyRelatedField

```python
# article/serializers.py

class ArticleSerializer(serializers.ModelSerializer):
    comment_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
```

:heavy_check_mark: `comment_set` : models.py 에서 related_name 으로 변경 가능

:heavy_check_mark: article detail을 get 할 때 comment_set 이 함께 나옴

​	id값만 나옴 (ex. comment_set: [1, 2, 3])



:three: Nested relationships

​	모델 관계상으로 참조된 대상은 참조하는 대상의 표현(응답)에 포함되거나 중첩(nested) 될 수 있음

​	이러한 중첩된 관계는 serializers를 필드로 사용하여 표현할 수 있음

```python
# article/serializers.py

from rest_framework import serializers
from .models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article',)

class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'

```

:heavy_check_mark: 참조할 필드는 무조건 위에 먼저 정의 되어야 함

:heavy_check_mark: CommentSerializer 에서 정의한 필드가 그대로 나옴

```
"comment_set": [
        {
            "id": 7,
            "content": "333111",
            "created_at": "2021-12-26T02:49:56.223032+09:00",
            "updated_at": "2021-12-26T02:49:56.223032+09:00",
            "article": 1
        },
		...
    ],
```



:blue_book: 특정 게시글에 작성된 댓글의 개수 구하기

​	별도의 값을 위한 필드를 사용하려는 경우 직접 필드 작성

```python
# articles/serializers.py

class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
```

:heavy_check_mark: `source` :필드를 채우는 데 사용할 속성의 이름

​	점 표기법(dot notation)을 사용하여 속성 탐색

​	comment_set이라는필드에 `.count` 을 통해 댓글 개수 파악 가능

​	`.count` 는 built-in Queryset API 중 하나

:heavy_check_mark: 특정 필들르 override 혹은 추가한 경우 `read_only_fields` shorcut으로 사용 불가능

​	무조건 `read_only=True` 를 해줘야함



##### CREATE

```python
# articles/views.py

@api_view(['POST'])        
def comments_create(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
```



##### UPDATE

```python
# articles/views.py

@api_view(['PUT'])
def comment_update(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
```



##### DELETE

```python
# articles/views.py

@api_view(['DELETE'])
def comments_delete(request, comment_pk):
    if request.method == 'DELETE':
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        return Response({'message': '삭제되었습니다'}, status=status.HTTP_204_NO_CONTENT)
```



#### :ocean: User와 1:N DRF

```python
# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = '__all__'
```

```python
# articles/serializers.py

from rest_framework import serializers
from .models import Article, Comment
from accounts.serializers import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
```

```python
# articles/views.py

@api_view(['POST'])
def create(request):
    if request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
```

