function renderPayments(data) {
    let paymentRow = ``, paymentRowsTemplate = ``, paymentsTemplate, paymentStatus = ``, privateClassStatus = ``;
    $.each(data, function (index, payment) {
        // status of payment
        console.log("is_disable", payment.is_disable)
        console.log("is_bought", payment.is_bought)
        if (payment.is_disable === true) {
            if (payment.is_bought === false) {
                paymentStatus = `
                    <img class="ml-1" src="/static/home/images/icons/close.svg" alt="alert" width="20px" height="20px">
                   <span class="text-danger">این دوره را از دست دادی</span>
                `
                privateClassStatus = `<a class="btn btn-info btn-sm" onclick="rayChatPrivateClass()">می خوای جبران کنی ؟</a>`
            } else {
                paymentStatus = `
                    <img class="ml-1"  src="/static/home/images/icons/tick.svg" alt="tick" width="20px" height="20px">
                    <span class="text-success">در این دوره شرکت کردی</span>
                `
                privateClassStatus = "";
            }
        } else {
            if (payment.is_bought === false) {
                paymentStatus = `
                    <img class="ml-1" src="/static/home/images/icons/alert.svg" alt="close" width="20px" height="20px">
                    <span class="text-warning">این دوره هنوز خریداری نشده</span>
                `
                privateClassStatus = "";
            } else {
                paymentStatus = `
                    <img class="ml-1" src="/static/home/images/icons/tick.svg" alt="tick" width="20px" height="20px">
                    <span class="text-success">این دوره خریداری شده</span>
                `
                privateClassStatus = "";
            }

        }
        paymentRow = `
            <tr>
                <td scope="row">${payment.title}</td>
                <td>${payment.amount}  تومان </td>
                <td> ${paymentStatus} </td>
                <td>
                    ${privateClassStatus}
                </td>
            </tr>
        `;
        paymentRowsTemplate += paymentRow;
    });

    paymentsTemplate = `
        <div class="container mt-3">
            <table class="table">
                <thead>
                <tr>
                    <th scope="col">شهریه</th>
                    <th scope="col">قیمت</th>
                    <th scope="col">وضعیت</th>
                    <th scope="col">
                        <button type="button" class="btn btn-secondary">پرداخت شهریه</button>
                    </th>
                </tr>
                </thead>
                <!-- payments rows -->
                <tbody>
                    ${paymentRowsTemplate}
                </tbody>
            </table>
        </div>
`;
    $("#payments").append(paymentsTemplate);
    $('[data-toggle="tooltip"]').tooltip()
}


function paymentsRender(code) {
    courseCode = code;
    $.ajax({
        url: `/dashboard/lessons/user-installments/${courseCode}/`,
        type: "GET",
        dataType: "json",
        success: function (data) {
            renderPayments(data);
        },
        error: function () {
            alert("خطا در بارگزاری جزوات ... صفحه را بازنشانی کنید!")
        },
    });
}


function rayChatPrivateClass() {
    let sendPrivateClassStatus = false;
    // for forget password
    // $('#forgetPasswordModal').modal('show')
    setTimeout(
        function () {
            if (!sendPrivateClassStatus) {
                let message = `
                سلام
                اینجا می تونی با مشاوره تحصیلی خودت صحبت کنی
                تا راهنماییت کنه چی جوری عقب افتادگی هاتو جبران کنی  📚
                `
                window.addEventListener('raychat_ready', function (ets) {
                    window.Raychat.sendOfflineMessage(message);
                    window.Raychat.toggle();
                    sendPrivateClassStatus = true;
                });
            }
        }, 2000);
}

// set default tooltip to hover
$.fn.tooltip.Constructor.Default.trigger = 'hover';