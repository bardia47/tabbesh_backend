import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re


class ImageUtils:
    # compress images
    # if width = height we don't need both
    def compressImage(uploadedImage, **extra_fields):
        imageTemproary = Image.open(uploadedImage)
        if 'width' in extra_fields:
            x = extra_fields['width']
            if 'height' in extra_fields:
                y = extra_fields['height']
            else:
                y = x
            imageTemproary = imageTemproary.resize((x, y), Image.ANTIALIAS)
        outputIoStream = BytesIO()
        #  imageTemproaryResized = imageTemproary.resize((20, 20), Image.ANTIALIAS)
        imageTemproary = imageTemproary.convert('RGB')
        imageTemproary.save(outputIoStream, format='JPEG', quality=60)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage

    def renameImage(uploadedImage, name):
        uploadedImage.name = re.sub('.+?(?=\.)', name, uploadedImage.name)
        return uploadedImage

    def renameAndCompressImage(uploadedImage, name, **extra_fields):
        image = ImageUtils.renameImage(uploadedImage, name)
        return ImageUtils.compressImage(image, **extra_fields)


class CacheUtils:
    # clean cache used for menu
    def cleanMenuCache(request):
        if request.accepted_renderer.format == 'html':
            # cache key for {% cache 10000 sidebar username %} templatetag
            key = make_template_fragment_key('sidebar', [request.user.username])
            cache.delete(key)  # invalidates cached template fragment


class TextUtils:
    def convert_list_to_string(list, seperator=','):
        return seperator.join(list)

    def replacer(old_text, string_list):
        # i = 0
        # counter = '{' + str(i) + '}'
        # while old_text.find(counter) != -1:
        #     if string_list[i] is not None:
        #         old_text = old_text.replace(counter, str(string_list[i]))
        #     else:
        #         old_text = old_text.replace(counter, "")
        #     i = i + 1
        #     counter = '{' + str(i) + '}'
        return old_text.format(*string_list)


# SEND emails with this class
class EmailUtils:
    def sending_email(text, receiver, sender, sender_password):
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = 'subject'
            message["From"] = sender
            message["To"] = receiver
            # Create the plain-text (it isn't force to use it) and HTML version of your message
            html = text
            # Turn these into plain/html MIMEText objects
            part = MIMEText(html, "html")
            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part)
            # Create secure connection with server and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender, sender_password)
                server.sendmail(
                    sender, receiver, message.as_string()
                )
        except:
            return {'message': 'try again.'}

# this is not used now
# class DateUtils:
#     def month_difference(start_date, end_date):
#         start_date_jalali = jdatetime.datetime.fromgregorian(datetime=start_date).strftime("%Y-%m-%d")
#         end_date_jalali = jdatetime.datetime.fromgregorian(datetime=end_date).strftime("%Y-%m-%d")
#         year_different = int(end_date_jalali[:4]) - int(start_date_jalali[:4])
#         month_different = int(end_date_jalali[5:7]) - int(start_date_jalali[5:7]) + (12 * (year_different))
#         day_different = int(end_date_jalali[7:]) - int(start_date_jalali[7:])
#         if (day_different > 16):
#             month_different -= 1
#         elif (day_different < -16):
#             month_different += 1
#         if (month_different == 0):
#             month_different += 1
#         return month_different
