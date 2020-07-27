// convert persian and arabic numbers to english numbers
function persianToEnglishNumbers(convertedNumbers) {
    const persianNumbers = [/۰/g, /۱/g, /۲/g, /۳/g, /۴/g, /۵/g, /۶/g, /۷/g, /۸/g, /۹/g];
    const arabicNumbers = [/٠/g, /١/g, /٢/g, /٣/g, /٤/g, /٥/g, /٦/g, /٧/g, /٨/g, /٩/g];
    if (typeof convertedNumbers === 'string') {
        for (let i = 0; i < 10; i++) {
            convertedNumbers = convertedNumbers.replace(persianNumbers[i], i).replace(arabicNumbers[i], i);
        }
    }
    return convertedNumbers;
}


document.addEventListener("DOMContentLoaded", function () {
    let elements = document.getElementsByTagName("INPUT");
    for (let i = 0; i < elements.length; i++) {
        elements[i].oninvalid = function (e) {
            e.target.setCustomValidity("");
            if (!e.target.validity.valid) {
                e.target.setCustomValidity("این مورد اجباری می باشد.");
            }
        };
        elements[i].oninput = function (e) {
            e.target.setCustomValidity("");
        };
    }
});


document.addEventListener("DOMContentLoaded", function () {
    let elements = document.getElementsByTagName("SELECT");
    for (let i = 0; i < elements.length; i++) {
        elements[i].oninvalid = function (e) {
            e.target.setCustomValidity("");
            if (!e.target.validity.valid) {
                e.target.setCustomValidity("لطفا یکی از موارد را انتخاب کنید.");
            }
        };
        elements[i].oninput = function (e) {
            e.target.setCustomValidity("");
        };
    }
});