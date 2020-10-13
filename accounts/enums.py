from enum import Enum


class PrivateCourse(Enum):
    MEMBERSHIP = '07'


class RoleCodes(Enum):
    STUDENT = '1'
    ADMIN = '2'
    TEACHER = '3'


class InstallmentModelEnum(Enum):
    installmentDateBefore = 10
    installmentIsBought='در این دوره شرکت کرده اید'
    installmentIsExpired = 'این دوره را از دست داده اید'
    installmentIsNotBought='این دوره هنوز خریداری نشده است'

class Sms(Enum):
    username = '09357727769'
    password = '8794'
    # signupText = 'با سلام و احترام خدمت شما تابشی عزیز رمز عبور شما برابر با {} می باشد لطفا پس از ورود به سایت در قسمت پروفایل آن را تعویض نمایید'
    signupBodyId = 20677
    wrongNumber = '11'
    _from = '50004000772777'

    increaseCreditText = 'با سلام و احترام اعتبار شما {0}  تومان افزایش یافت و هم اکنون برابر با {1} میباشد.برای دریافت با پشتیبان تماس بگیرید. تابش'


class Email(Enum):
    tethaEmail = 'tetha.nine@gmail.com'
    testEmail = 'bardiatethatest@gmail.com'
    testPassword = 'tetha12345678'
    schadulerTestText = """\
                <html>
                  <body>
                       <br> نام درس :
                     """ + "{0}" + """<br/>
                  </body>
                </html>
                """


class AdminEnums(Enum):
    forgetPasswordHtml = """\
    <button type="button" id="sendPass" value="{0}">
                      ارسال
                </button>
                """
