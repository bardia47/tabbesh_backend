import sys 
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

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

class TextUtils:
    def convert_list_to_string(list, seperator=','):
            """ Convert list to string, by joining all item in list with given separator.
                Returns the concatenated string """
            return seperator.join(list)

    def replacer(old_text,string_list):
        i=0
        counter='{'+str(i)+'}'
        while(old_text.find(counter)!=-1):
          if (string_list[i] is not None):
              old_text= old_text.replace(counter,str(string_list[i]))
          else :
            old_text = old_text.replace(counter, "")
          i=i+1
          counter = '{' + str(i) + '}'
        return old_text