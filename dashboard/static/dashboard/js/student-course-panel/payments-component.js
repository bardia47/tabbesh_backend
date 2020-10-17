function renderPayments(data) {
    let paymentRow = ``, paymentRowsTemplate = ``, paymentsTemplate, paymentStatus = ``, privateClassStatus = ``;
    $.each(data.installments, function (index, payment) {
        // status of payment
        if (payment.is_bought === false && payment.is_disable === true) {
            privateClassStatus = `<a class="btn btn-info btn-sm" onclick="rayChatPrivateClass()">می خوای جبران کنی ؟</a>`
        }
        paymentRow = `
            <tr>
                <td scope="row">${payment.title}</td>
                <td class="${messageClass(payment)}">${payment.message}</td>
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
                    <th scope="col">وضعیت</th>
                    <th scope="col">
                        <a onclick="sessionStorage.setItem('totalId' , '[${data.id}]')" type="button" class="btn btn-secondary btn-sm" href="/payment/shopping-cart/">پرداخت شهریه</a>
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


function messageClass(payment){
    if (payment.is_bought === true) return "text-success"
    else{
        if (payment.is_disable === false) return "text-danger"
        else return "text-warning"
    }
}

// set default tooltip to hover
$.fn.tooltip.Constructor.Default.trigger = 'hover';