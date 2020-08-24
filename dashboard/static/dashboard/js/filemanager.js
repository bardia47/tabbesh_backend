function renderDocuments(data) {
    let documentRowsTemplate = ``, documentRow = ``, fileManagerTemplate = ``;
    if (data.documents.length === 0) {
        documentRowsTemplate = `
        <tr>
            <td class="p-3 vazir-bold" style="font-size: 15px;" colspan="6" scope="row">
                <img class="mb-2" src="/static/home/images/icons/file-manager-empty.svg" width="35"
                     height="35">
                <br>
                متاسفانه جزوه ای یافت نشد !
            </td>
        </tr>
        `;
    } else {
        $.each(data.documents, function (index, document) {
            documentRow = `
            <tr>
                <th style="font-family:'Vazir_Bold'" scope="row">${index + 1}</th>
                <td>${document.title}</td>
                <td>${document.sender_name}</td>
                <td>${document.upload_date_decorated}</td>
                <td>${document.description}</td>
                <td style="text-align:center"><a href="${document.upload_document}" target="_blank">
                    <img src="/static/home/images/icons/download.svg" width="20" height="20"></a>
                </td>
            </tr>
            `;
            documentRowsTemplate += documentRow;
        });
    }

    fileManagerTemplate = `
    <div class="container">
        <div class="row mb-2">
            <div class="col-md-1 file-manager-image">
                <img src="${data.course.image}" width="50" height="50">
            </div>
            <div class="col-md-3 file-manager title">
                <p class="m-0"><strong>${data.course.title}</strong></p>
                <h6 class="p-0"><small>${data.course.teacher}</small></h6>
            </div>


        </div>
        <div class="table-responsive-sm">
            <table class="table table-hover">
                <thead>
                <tr>
                    <th scope="col"><img src="/static/home/images/icons/folder.svg" width="25" height="25"></th>
                    <th scope="col">عنوان</th>
                    <th scope="col">فرستنده</th>
                    <th scope="col">تاریخ</th>
                    <th scope="col">توضیحات</th>
                    <th scope="col">دانلود</th>
                </tr>
                </thead>
                <tbody>
                    ${documentRowsTemplate}
                </tbody>
            </table>
        </div>
    </div>
`;
    $("#fileManager").append(fileManagerTemplate);
}

function fileManagerRender() {

    $.ajax({
        url: "http://127.0.0.1:8000/dashboard/lessons/files/020009/",
        type: "GET",
        dataType: "json",
        success: function (data) {
            renderDocuments(data);
        },
        error: function () {
            alert("خطا در بارگزاری دروس ... لطفا دوباره امتحان کنید!")
        },
    });
}
