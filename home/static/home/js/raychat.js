!function () {
    function t() {
        let t = document.createElement("script");
        t.type = "text/javascript", t.async = !0, localStorage.getItem("rayToken") ? t.src = "https://app.raychat.io/scripts/js/" + o + "?rid=" + localStorage.getItem("rayToken") + "&href=" + window.location.href : t.src = "https://app.raychat.io/scripts/js/" + o;
        let e = document.getElementsByTagName("script")[0];
        e.parentNode.insertBefore(t, e)
    }

    let e = document, a = window, o = "ce734f53-a0ca-4300-9bd8-436ac0acd84d";
    "complete" == e.readyState ? t() : a.attachEvent ? a.attachEvent("onload", t) : a.addEventListener("load", t, !1)
}();
