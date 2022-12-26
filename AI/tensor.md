### Tensor



#### 벡터, 행렬, 텐서

스칼라 : 차원이 없는 값 (하나의 숫자)

벡터 : 1차원으로 구성된 값 (일반적으로 일차원 배열)

행렬(Matrix) : 2차원으로 구성된 값

텐서(Tensor) : 3차원으로 구성된 값



#### Tensor shape

*  2D Tensor

   |t| = (Batch size, dim)

   ![img](https://wikidocs.net/images/page/52460/tensor3.PNG)

*  3D Tensor

   |t| = (batch size, width, height)

   ![img](https://wikidocs.net/images/page/52460/tensor5.PNG)



##### 1. tensor의 차원과 형태

```python
X = torch.rand(3, 4, 5)
print(X.dim())      # 3
print(X.shape)      # shape, size 는 동일한 용도 shape은 변수 size는 메서드
print(X.size())     # size는 x의 shape을 반환하는 함수

# torch.Size([3, 4, 5])
```



##### 3. Mul과 Matmul의 차이

`matmul` : matrix사이즈가 다를 때

`mul` : matrix사이즈가 동일할 때

```python
X = torch.rand(3, 5)
Y = torch.rand(5, 2)

D = X.matmul(Y)     # 행렬의 곱
print(D)
print(D.shape)					# torch.Size([3, 2])
```

```python
X = torch.rand(3, 5)
Y = torch.rand(3, 5)

D = X.mul(Y)       # matrix사이즈가 동일할 때

print(D)
print(X*Y)          # 값이 똑같음
print(D.shape)				# torch.Size([3, 5])
```

```python
X = torch.rand(3, 2, 5) # 2x5 행렬이 3개가 있는 tensor
Y = torch.rand(3, 5, 3) 

D = X.matmul(Y)     # (2x5) X (5x2)가 3개로 나옴 대응하는 행렬끼리 병렬로 곱해줌
print(D)
print(D.shape)				# torch.Size([3, 2, 3])
```



##### 3. Broadcasting

tensor끼리 계산할 때 크기가 다르면 크기를 맞춰 계산해줌

X 의 shape이 [100,1,20] , Y 의 shape 이  [100,40 ,20] 일 때,  X의 두번째 차원인 1을 Y의 두번째 차원 40에 맞춰 X의 값들을 반복 복제해 크기를 조절해줌

디버깅할 때 오류를 잡는 것이 어려우니 주의해야함



##### 4. shape

```python
X = torch.rand(3, 2, 5)
print(X.shape)
print(X.view(3, 19).shape)  # 2x5 를 10으로 뒤에 행렬을 10개의 벡터로 봐라
```

`shape` : # 2x5 를 10으로 뒤에 행렬을 10개의 벡터로 봐라X = torch.rand(3, 5)



##### 5. axis

다차원 텐서에 해당 함수 연산을 어떤 축으로 적용할지

![다차원 배열에서 axis(축)의 의미](https://taewanmerepo.github.io/2017/09/numpy_axis/axis.jpg)

다차원 배열에서의 axis(축)의 의미

http://taewan.kim/post/numpy_sum_axis/



##### 6. squeeze & unsqueeze

특정 차원이 1인 경우 축소시키거나 차원을 확장시킬 때

[100, 1, 20] > [100, 20]



##### 7. type casting



##### 8. concatenate

두 개 이상의 텐서들을 지정된 축으로 쌓아서 더 큰 텐서를 만드는 함수

concatenate하는 축을 제외하고는 모두 같은 크기를 가져야함