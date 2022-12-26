from django.shortcuts import get_object_or_404
from .models import Article, Comment

from .serializers import ArticleSerializer, CommentSerializer
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

# @api_view(['POST'])
# def create(request):
#     if request.method == 'POST':
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def create(request):
    if request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def delete(request, pk):
    if request.method == 'DELETE':
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response({'message': '삭제되었습니다'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def update(request, pk):
    if request.method == 'PUT':
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

@api_view(['POST'])        
def comment_create(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def comment_delete(request, comment_pk):
    if request.method == 'DELETE':
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        return Response({'message': '삭제되었습니다'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def comments_list(request, article_pk):
    if request.method == 'GET':
        article = get_object_or_404(Article, pk=article_pk)
        comments = article.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

@api_view(['PUT'])
def comment_update(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)