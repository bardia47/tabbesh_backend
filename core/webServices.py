from accounts.enums import Sms
from melipayamak import Api


class SmsWebServices:
    def send_sms(to, text, bodyId=None):
        api = Api(Sms.username.value, Sms.password.value)
        sms = api.sms()
        if bodyId is None:
            _from = Sms._from.value
            response = sms.send(to, _from, text)
        else:
            response = sms.send_by_base_number(text, to, bodyId)
        if response['Value'] == Sms.wrongNumber.value:
            return 'شماره وارد شده نامعتبر است'
        elif len(response['Value']) == 1:
            'خطایی رخ داده است . لطفا یک بار دیگر تلاش کنید یا با پشتیبان تماس بگیرید'
        else:
            return None
