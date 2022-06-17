from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response



from hitchapi.models.Tag import Tag
from hitchapi.serializers.tag_serializer import TagSerializer


class TagView(ViewSet):
    
    def list(self, request):
        
        tags = Tag.objects.all()
        
        serializer = TagSerializer(tags, many =True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)