function renderPayments(data) {
    let paymentRow = ``, paymentRowsTemplate = ``, paymentsTemplate = ``;
    $.each(data.documents, function (index, document) {
        $("#courseId").val(document.course);
        paymentRow = `
            <tr>
                <th scope="row">مهر ماه</th>
                <td>60000 تومان</td>
                <td><img src="/static/home/images/icons/alert.svg" alt="alert"></td>
                <td class="pl-5">
                    این دوره هنوز خریداری نشده است
                </td>
            </tr>
        `;
        paymentRowsTemplate += documentRow;
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
                        <button type="button" class="btn btn-primary">انتخاب همه</button>
                    </th>
                </tr>
                </thead>
                <!-- payments rows -->
                <tbody>
                </tbody>
            </table>
        </div>
`;
    $("#fileManager").append(fileManagerTemplate);
    $('[data-toggle="tooltip"]').tooltip()
}


function paymentsRender(code) {
    courseCode = code;
    $.ajax({
        url: `/dashboard/lessons/files/${courseCode}/`,
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


// set default tooltip to hover
$.fn.tooltip.Constructor.Default.trigger = 'hover';