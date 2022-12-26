## :rocket: Django START!!!



####  :black_small_square: 개발환경 설정

```bash
$ python -m venv venv 	# 가상환경 설정
$ source venv/scripts/activate		# 가상환경 활성화
$ pip install django				# django 설치
$ pip install -r requirements.txt	# req 에 있는 파일 설치
$ pip freeze > requirements.txt		# 설치목록 req로 보내기

# vscode에서 Interpreter 설정
```



####  :black_small_square: ​프로젝트 생성

```bash
$ django-admin startproject crud .			# 프로젝트 생성

$ python manage.py runserver	# 서버 실행 후 확인(로켓페이지=성공)
```

##### :grey_exclamation: project 생성 시 . 을 찍어 파일을 풀어줌



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



####  :black_small_square: ​추가 세팅

```python
# settings.py

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'
```
