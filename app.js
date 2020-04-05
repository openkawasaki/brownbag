//ons.bootstrap();

// CordovaのAPIを呼び出す準備が整った
ons.ready(function() {
    console.log("ons.ready");
});

//--------------------------
// for sidemenu & pushpage
//--------------------------
window.fn = {};

window.fn.toggleMenu = function () {
    document.getElementById('appSplitter').right.toggle();
};

window.fn.loadView = function (index) {
    document.getElementById('appTabbar').setActiveTab(index);
    document.getElementById('sidemenu').close();
};

window.fn.loadLink = function (url) {
    window.open(url, '_blank');
};

window.fn.pushPage = function (page, anim) {
    if (anim) {
        document.getElementById('appNavigator').pushPage(page.id, { data: { title: page.title }, animation: anim });
    } else {
        document.getElementById('appNavigator').pushPage(page.id, { data: { title: page.title } });
    }
};

//--------------------------
// アクティブなタブが変わる前に発火します。
//--------------------------
document.addEventListener('prechange', function(event) {
    // ラベル設定
    document.querySelector('ons-toolbar .center')
        .innerHTML = event.tabItem.getAttribute('label');
});

//--------------------------
// initイベント
//--------------------------
document.addEventListener("init", function(event) {
    var page = event.target;
    if (page.id === "home-page") {
        console.log("home-page");
    } else if (page.id === "list-page") {
        console.log("list-page");
    } else if (page.id === "map-page") {
        console.log("map-page");
    } else if (page.id === "info-page") {
        console.log("info-page");
    } else if (page.id === "setting-page") {
        console.log("setting-page");
    }
});

