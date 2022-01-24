from melipayamak import Api
from accounts.enums.enum_sms import SmsEnum


class SmsWebServices:
    def send_sms(to, text, bodyId=None):
        api = Api(SmsEnum.username.value, SmsEnum.password.value)
        sms = api.sms()
        if bodyId is None:
            _from = SmsEnum._from.value
            response = sms.send(to, _from, text)
        else:
            response = sms.send_by_base_number(text, to, bodyId)
        if response['Value'] == SmsEnum.wrongNumber.value:
            return 'شماره وارد شده نامعتبر است'
        elif len(response['Value']) == 1:
            'خطایی رخ داده است . لطفا یک بار دیگر تلاش کنید یا با پشتیبان تماس بگیرید'
        else:
            return None
