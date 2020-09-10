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
import jdatetime
import jdatetime

class Utils:
    # compress images
    def compressImage(uploadedImage):
        imageTemproary = Image.open(uploadedImage)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((20, 20), Image.ANTIALIAS)
        imageTemproary = imageTemproary.convert('RGB')
        imageTemproary.save(outputIoStream, format='JPEG', quality=60)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage

    # clean cache used for menu
    def cleanMenuCache(request):
        if request.accepted_renderer.format == 'html':
            # cache key for {% cache 10000 sidebar username %} templatetag
            key = make_template_fragment_key('sidebar', [request.user.username])
            cache.delete(key)  # invalidates cached template fragment


class TextUtils:
    def convert_list_to_string(list, seperator=','):
        """ Convert list to string, by joining all item in list with given separator.
            Returns the concatenated string """
        return seperator.join(list)

    def replacer(old_text, string_list):
        i = 0
        counter = '{' + str(i) + '}'
        while old_text.find(counter) != -1:
            if string_list[i] is not None:
                old_text = old_text.replace(counter, str(string_list[i]))
            else:
                old_text = old_text.replace(counter, "")
            i = i + 1
            counter = '{' + str(i) + '}'
        return old_text


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

# use get_field_display for this !
# get choice name from choice list
# class ChoiceUtils:
#     def get_choice_name(key, choice_types):
#         for choice, value in choice_types:
#             if choice == key:
#                 return value


#
class DateUtils:
    def month_difference( start_date , end_date ):
        start_date_jalali=jdatetime.datetime.fromgregorian(datetime=start_date).strftime("%Y-%m-%d")
        end_date_jalali = jdatetime.datetime.fromgregorian(datetime=end_date).strftime("%Y-%m-%d")
        year_different=int(end_date_jalali[:4]) - int(start_date_jalali[:4])
        month_different= int(end_date_jalali[5:7])-int(start_date_jalali[5:7]) + (12 * (year_different))
        day_different=int(end_date_jalali[7:])-int(start_date_jalali[7:])
        if (day_different>16):
            month_different -=1
        elif (day_different<-16):
            month_different += 1
        if (month_different==0):
            month_different += 1
        return month_different