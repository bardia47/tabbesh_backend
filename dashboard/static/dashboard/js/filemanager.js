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
                <td>
                    <a class="edit-document" data-course-id="${document.course}" data-sender-id="${document.sender}"  data-title="${document.title}" data-description="${document.description}"
                        style="cursor: pointer">
                        <i class="fas fa-edit text-info"></i>
                    </a>
                 </td>
                <td><a class="delete-document" data-course-id="${document.course}"style="cursor: pointer"><i class="fas fa-trash-alt text-danger"></i></a>
                </td>
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
        <div id="fileManagerTitle"  class="row mb-2">
            <div class="d-flex col-md-5 file-manager-image">
                <img src="${data.course.image}" width="50" height="50">
                <div class="ml-2">
                    <p class="m-0"><strong>${data.course.title}</strong></p>
                    <h6 class="p-0"><small>${data.course.teacher}</small></h6>         
                </div>
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
                    <th scope="col">حذف</th>
                    <th scope="col">ویرایش</th>
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
    $("#addFileButton").tooltip();
    addFileUploadButton();
    deleteDocuments();
    editDocuments();
}

function addFileUploadButton() {
    let fileUploadButtonTemplate = `
    <div  id="addFileButton" class="ml-auto" data-toggle="tooltip" data-placement="top" title="اضافه کردن جزوه">
        <img class="mt-3 mr-md-5" src="/static/home/images/icons/plus.svg" width="35" height="35">
    </div>
    `;
    $("#fileManagerTitle").append(fileUploadButtonTemplate);
    // fire modal with button
    $("#addFileButton").click(function () {
        $("#uploadModal").modal();
    });
}

// delete documents
function deleteDocuments() {
    $(".delete-document").click(function () {

    })
}

function editDocuments() {
    $(".edit-document").click(function () {
        $("#editTitle").val($(this).data("title"));
        $("#editDescription").val($(this).data("description"));
        $("#editCourse").val($(this).data("course-id"));
        $("#editSender").val($(this).data("sender-id"));
        $("#editModal").modal();
    })
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
