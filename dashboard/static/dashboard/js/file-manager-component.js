let uploadModal = $("#uploadModal");
let uploadModalTitle = uploadModal.find("#title");
let uploadModalDescription = uploadModal.find("#description");
let uploadModalSenderId = uploadModal.find("#senderId");
let uploadModalDocumentId = uploadModal.find("#documentId");
let uploadModalAddOrEditStatus = uploadModal.find("#addOrEditStatus");
let courseCode = "";
function renderDocuments(data) {
    let documentRowsTemplate = ``, documentRow = ``, fileManagerTemplate = ``;
    if (data.documents.length === 0) {
        documentRowsTemplate = `
        <tr>
            <td class="p-3 vazir-bold" style="font-size: 15px;" colspan="8" scope="row">
                <img class="mb-2" src="/static/home/images/icons/file-manager-empty.svg" width="35"
                     height="35">
                <br>
                متاسفانه جزوه ای یافت نشد !
            </td>
        </tr>
        `;
    } else {
        $.each(data.documents, function (index, document) {
            $("#courseId").val(document.course);
            let documentUploadDate = new persianDate(Date.parse(document.upload_date));
            documentRow = `
            <tr>
                <th style="font-family:'Vazir_Bold'" scope="row">${index + 1}</th>
                <td>${document.title}</td>
                <td>${document.sender_name}</td>
                <td>${documentUploadDate.format("LLLL")}</td>
                <td>${document.description}</td>
                <td data-toggle="tooltip" data-placement="top" title="تغییر جزوه">
                    <a class="edit-document" data-id="${document.id}" data-course-id="${document.course}" data-sender-id="${document.sender}"  data-title="${document.title}" data-description="${document.description}"
                        style="cursor: pointer">
                        <i class="fas fa-edit text-info"></i>
                    </a>
                 </td>
                <td data-toggle="tooltip" data-placement="top" title="حذف جزوه">
                    <a class="delete-document" data-course-id="${document.course}"style="cursor: pointer">
                        <i class="fas fa-trash-alt text-danger"></i>
                    </a>
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
            <div  id="addFileButton" class="ml-auto" data-toggle="tooltip" data-placement="top" title="اضافه کردن جزوه">
                <img class="mt-3 mr-md-5" src="/static/home/images/icons/plus.svg" width="35" height="35">
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
                    <th scope="col">ویرایش</th>
                    <th scope="col">حذف</th>
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
    $("#documentUploadForm").submit(function (e) {
        e.preventDefault();
        if (uploadModalAddOrEditStatus.val() === "add") {
            addDocumentAjax();
        } else {
            editDocumentAjax();
        }
    });

    addDocumentConfigure();
    editDocumentsConfigure();
    deleteDocuments();

    // reset modal
    uploadModal.on("hidden.bs.modal", function () {
        restDropZone();
    });
}


function fileManagerRender(code) {
    courseCode = code;
    $.ajax({
        url: `http://127.0.0.1:8000/dashboard/lessons/files/${courseCode}/`,
        type: "GET",
        dataType: "json",
        success: function (data) {
            $("#fileManager").empty();
            renderDocuments(data);
        },
        error: function () {
            alert("خطا در بارگزاری جزوات ... صفحه را بازنشانی کنید!")
        },
    });
}


function addDocumentConfigure() {
    // fire modal with button
    $("#addFileButton").click(function () {
        uploadModalTitle.val("");
        uploadModalDescription.val("");
        uploadModalAddOrEditStatus.val("add");

        // configure modal for edit document
        uploadModal.find(".modal-title").text("اضافه کردن جزوه ی جدید");
        uploadModal.find("#titleLabel").text("عنوان جزوه");
        uploadModal.find("#descriptionLabel").text("توضیحات جزوه");
        uploadModal.find("#fileLabel").text("فایل جدید جزوه را در این قسمت آپلود کنید.");
        uploadModal.find("#uploadSubmit").text("آپلود جزوه");
        uploadModal.modal();
    });
}


function editDocumentsConfigure() {
    $(".edit-document").click(function () {
        uploadModalTitle.val($(this).data("title"));
        uploadModalDescription.val($(this).data("description"));
        uploadModalSenderId.val($(this).data("sender-id"));
        uploadModalDocumentId.val($(this).data("id"));
        uploadModalAddOrEditStatus.val("edit");

        // configure modal for edit document
        uploadModal.find(".modal-title").text("تغییر جزوه ی آپلود شده");
        uploadModal.find("#titleLabel").text("عنوان جدید جزوه");
        uploadModal.find("#descriptionLabel").text("توضیحات جدید");
        uploadModal.find("#fileLabel").text("در صورت تغییر فایل جزوه می توانید از این قسمت استفاده کنید.");
        uploadModal.find("#uploadSubmit").text("ثبت تغییرات");
        uploadModal.modal();
    });
}

// delete documents
function deleteDocuments() {
    $(".delete-document").click(function () {

    })
}

function addDocumentAjax() {
    $.ajax({
        url: `http://127.0.0.1:8000/dashboard/lessons/files/${courseCode}/`,
        type: "POST",
        data: new FormData($("#documentUploadForm")[0]),
        processData: false,
        contentType: false,
        dataType: "json",
        beforeSend: function (xhr, settings) {
            $("#uploadModal").find("#uploadSubmit").text("در حال آپلود");
            $("#uploadLoading").show();
            $("#uploadFailedAlert").hide();
        },
        success: function (data, textStatus, xhr) {
            $("#uploadLoading").hide();
            $("#uploadModal").modal("hide");
            // render file manager with new data
            fileManagerRender(courseCode);
        },
        error: function (xhr, status, error) {
            $("#uploadLoading").hide();
            $("#uploadFailedAlert").show();
        }
    });

}


function editDocumentAjax() {
    let editFormData = new FormData($("#documentUploadForm")[0]);
    if ($("#dropUploadFiles")[0].files.length === 0) editFormData.delete("upload_document");
    $.ajax({
        url: `http://127.0.0.1:8000/dashboard/lessons/files/${courseCode}/${uploadModalDocumentId.val()}/`,
        type: "POST",
        data: editFormData,
        processData: false,
        contentType: false,
        dataType: "json",
        beforeSend: function (xhr, settings) {
            $("#uploadSubmit").text("در حل ثبت تغییرات");
            $("#uploadLoading").show();
            $("#uploadFailedAlert").hide();
        },
        success: function (data, textStatus, xhr) {
            $("#uploadLoading").hide();
            $("#uploadModal").modal("hide");
            // render file manager with new data
            fileManagerRender(courseCode);
        },
        error: function (xhr, status, error) {
            alert("خطا در تغییر جزوه ، دوباره امتحان کنید.")
            $("#uploadLoading").hide();
            $("#uploadFailedAlert").show();
        }
    });

}
