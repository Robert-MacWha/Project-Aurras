//? react to titlebar buttons being pressed
document.getElementById('btn-min').addEventListener("click", () => { 
    window.api.request("titlebar", "minimize");
});

document.getElementById('btn-max').addEventListener("click", () => { 
    window.api.request("titlebar", "maximize");
});

document.getElementById('btn-exit').addEventListener("click", () => { 
    window.api.request("titlebar", "exit");
});

//? also initialize any tooltips (just putting this here so I don't ever have a page without it)
$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});