from rest_framework.response import Response
from rest_framework.views import APIView
from config import settings
from post.models import Post
import requests
from .serializers import PhotoSerializer


class getURL(APIView):

    def post(self, request):
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v2/direct_upload"
        res = requests.post(url, headers={
                "Authorization": f"Bearer {settings.CF_TOKEN}",
        }).json()
        return Response(res)
    
class uploadImage(APIView):
      
    def post(self, request, postPk):
        
        t_post = Post.objects.get(pk=postPk)
        data = request.data.copy()
        data["post"] = t_post.pk 
        data["author"] = t_post.author.pk 
        serializer = PhotoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class getImages(APIView):
    
    def get(self, request, postPk):
        t_post = Post.objects.get(pk=postPk)
        photos = t_post.photo_set.all()
        serializer = PhotoSerializer(photos, many=True)
        
        return Response(serializer.data)
        