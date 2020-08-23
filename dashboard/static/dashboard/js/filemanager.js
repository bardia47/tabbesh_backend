function activeMenu() {
    let menuTemplate = `
    <hr>
    <div id="editProfileMenu" class="row sidebar-menu active-menu">
        <img src="/static/home/images/icons/file-manager-menu.svg" alt="edit profile menu">
        <a href="">جزوه ها</a>
    </div>
    `;
    $("#sidebarMenus").append(menuTemplate);
}

// initial function
$(function () {
    // active menu
    activeMenu();

});