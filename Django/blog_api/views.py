from rest_framework import generics, viewsets, filters, permissions
from blog.models import Post
from .serializers import PostSerializer
# from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAdminUser, DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser

from blog_api import serializers

# class PostUserWritePermission(BasePermission):
#   message = 'Editting posts is restricted to the author only.'

#   def has_object_permission(self, request, view, obj):
#     if request.method in SAFE_METHODS:
#       return True

#     return obj.author == request.user

class PostList(viewsets.ModelViewSet):
  serializer_class = PostSerializer
  queryset = Post.postobjects.all()

class PostDetail(generics.RetrieveAPIView):
  serializer_class = PostSerializer

  def get_object(self, queryset=None, **kwargs):
    item = self.kwargs.get('pk')
    return get_object_or_404(Post, slug=item)

class PostListDetailFilter(generics.ListAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  filter_backends = [filters.SearchFilter]
  search_fields = ['^slug']

  # '^' - Starts-with search
  # '=' - Exact matches
  # '@' - Full-text search (Only postgres)
  # '$' - Regex Search

# Admin
# class CreatePost(generics.CreateAPIView):
#   permission_classes = [permissions.IsAuthenticated]
#   queryset = Post.objects.all()
#   serializer_class = PostSerializer

class CreatePost(APIView):
  permissions_classes = [permissions.IsAuthenticated]
  parser_classes = [MultiPartParser, FormParser]

  def post(self, request, format=None):
    print(request.data)
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminPostDetail(generics.RetrieveAPIView):
  permission_classes = [permissions.IsAuthenticated]
  queryset = Post.objects.all()
  serializer_class = PostSerializer

class EditPost(generics.UpdateAPIView):
  permission_classes = [permissions.IsAuthenticated]
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  
class DeletePost(generics.RetrieveDestroyAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = PostSerializer
  queryset = Post.objects.all()

# class PostList(viewsets.ViewSet):
#   permission_classes = [IsAuthenticated]
#   queryset = Post.postobjects.all()

#   def list(self, request):
#     serializer_class = PostSerializer(self.queryset, many=True)
#     return Response(serializer_class.data)

#   def retrieve(self, request, pk=None):
#     post = get_object_or_404(self.queryset, pk=pk)
#     serializer_class = PostSerializer(post)
#     return Response(serializer_class.data)



# class PostList(generics.ListCreateAPIView):
#   permission_classes = [IsAuthenticated]
#   queryset = Post.postobjects.all()
#   serializer_class = PostSerializer

# class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
#   permission_classes = [PostUserWritePermission]
#   queryset = Post.objects.all()
#   serializer_class = PostSerializer




