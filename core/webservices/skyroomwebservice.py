import logging
import requests
from core.enums.enum_skyroom import SkyRoomEnum
from core.webservices.sms_sender import SmsWebServices

logger = logging.getLogger("django")


class SkyRoomWebService:
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
            response = requests.post(SkyRoomEnum.url.value + SkyRoomEnum.api_key.value, json=data)
            response_check = response.json()
            # error code is related to our system and conflict with another username
            if 'error_code' in response_check and response_check['error_code'] > 12:
                flag = True
                logger.error("creating this user in skyroom has a problem" + str(response_check))
            # error code is related to sky room web service
            if 'error_code' in response_check and response_check['error_code'] < 13:
                logger.error("Web service have a problem" + str(response_check))
                sendSms = SmsWebServices.send_sms(SkyRoomEnum.phone_number.value,
                                                  "skyroom has a problem" + str(response_check), None)
                if sendSms is not None:
                    logger.error("danger: " + sendSms)
            if not response_check['ok']:
                raise Exception
            else:
                return SkyRoomEnum.success.value
        except:
            if flag:
                # report to user there is a problem
                return SkyRoomEnum.have_error.value
            else:
                return SkyRoomEnum.no_error.value
