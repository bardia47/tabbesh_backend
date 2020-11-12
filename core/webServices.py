from accounts.enums import Sms
from melipayamak import Api
from zarinpal import enums
import logging
import requests

logger = logging.getLogger("django")


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


def create_sky_room_obj(obj):
    flag = False
    # write request
    try:
        data = {"action": "createUser",
                "params":
                    {"username": str(obj.phone_number),
                     "password": "12345678",
                     "nickname": str(obj.__str__()),
                     "status": 1,
                     "is_public": False}}
        response = requests.post(enums.SkyRoom.url.value + enums.SkyRoom.api_key.value, json=data)
        response_check = response.json()
        # error code is related to our system and conflict with another username
        if 'error_code' in response_check and response_check['error_code'] > 12:
            flag = True
            logger.error("creating this user in skyroom has a problem" + str(response_check))
        # error code is related to sky room web service
        if 'error_code' in response_check and response_check['error_code'] < 13:
            logger.error("Web service have a problem" + str(response_check))
            sendSms = SmsWebServices.send_sms(enums.SkyRoom.phone_number.value, "skyroom has a problem" + str(response_check), None)
            if sendSms is not None:
                logger.error("danger: " + sendSms)
        if not response_check['ok']:
            raise Exception
        else:
            return enums.SkyRoom.success.value
    except:
        if flag:
            # report to user there is a problem
            return enums.SkyRoom.have_error.value
        else:
            return enums.SkyRoom.no_error.value
