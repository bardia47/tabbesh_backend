import sys 
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
class Utils:
          #compress images
    def compressImage(uploadedImage):
        imageTemproary = Image.open(uploadedImage)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((20,20), Image.ANTIALIAS) 
        imageTemproary = imageTemproary.convert('RGB')
        imageTemproary.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage


    def cleanMenuCache(request):
          if request.accepted_renderer.format == 'html':
              # cache key for {% cache 10000 sidebar username %} templatetag
              key = make_template_fragment_key('sidebar', [request.user.username])
              print(cache.get(key))
              cache.delete(key)  # invalidates cached template fragment