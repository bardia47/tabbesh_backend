from enum import Enum
class RoleCodes(Enum):
    STUDENT='1'
    ADMIN='2'
    TEACHER='3'

class Sms(Enum):
    username='09357727769'
    password='8794'
    signupText='با سلام و احترام خدمت شما پیشگامی عزیز رمز  عبور شما برابر با {} می باشد لطفا پس از ورد به سایت در قسمت پروفایل آن را تعویض نمایید'
    wrongNumber='11'
    _from = '50001060690571'

