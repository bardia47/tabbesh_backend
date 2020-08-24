function renderStudentsList(data) {
    let studentListRowsTemplate = ``, studentListRow = ``, studentListTemplate = ``;
    if (data.students.length === 0) {
        studentListRowsTemplate = `
        <tr>
            <td class="p-3 vazir-bold" style="font-size: 15px;" colspan="6" scope="row">
                <img class="mb-2" src="/static/home/images/icons/file-manager-empty.svg" width="35"
                     height="35">
                <br>
                دانش آموزی در این کلاس ثبت نام نکرده است!
            </td>
        </tr>
        `;
    } else {
        $.each(data.students, function (index, student) {
            studentListRow = `
            <tr>
                <th style="font-family:'Vazir_Bold'" scope="row">
                <img src="${student.avatar}" width="25" height="25">
                </th>
                <td>${student.first_name}</td>
                <td>${student.last_name}</td>
                <td>${student.grade}</td>
                <td>${student.cityTitle}</td>
            </tr>
            `;
            studentListRowsTemplate += studentListRow;
        });
    }

    studentListTemplate = `
    <div class="container">
        <div class="table-responsive-sm">
            <table class="table table-hover">
                <thead>
                <tr>
                    <th scope="col"><img src="/static/home/images/icons/folder.svg" width="25" height="25"></th>
                    <th scope="col">نام</th>
                    <th scope="col">نام خانوادگی</th>
                    <th scope="col">پایه تحصیلی</th>
                    <th scope="col">استان</th>
                </tr>
                </thead>
                <tbody>
                    ${studentListRowsTemplate}
                </tbody>
            </table>
        </div>
    </div>
`;
    $("#studentsList").append(studentListTemplate);
}

function studentListRender() {

    $.ajax({
        url: "http://127.0.0.1:8000/dashboard/lessons/list/020009/",
        type: "GET",
        dataType: "json",
        success: function (data) {
            renderStudentsList(data);
        },
        error: function () {
            alert("خطا در بارگزاری دروس ... لطفا دوباره امتحان کنید!")
        },
    });
}
