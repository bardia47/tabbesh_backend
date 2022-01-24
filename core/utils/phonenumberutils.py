class PhoneNumberUtils:

    @staticmethod
    def normilize_phone_number(phone_number):
        if phone_number.startswith('+98'):
            phone_number = "0" + phone_number[3:]
        elif not phone_number.startswith('0'):
            phone_number = "0" + phone_number
        return phone_number
