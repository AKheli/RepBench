let toggle_visibility = function (id) {
    var e = document.getElementById(id);
    if (e.style.display == 'block')
        e.style.display = 'none';
    else
        e.style.display = 'block';
}


let toggles = Array.from(document.getElementsByClassName("myToggle"));
toggles.forEach((element, i) => {
    element["on"] = i === 0; // set first toggle to on
    element["primary"] = false;
});

toggles.forEach(element => {

    element.addEventListener("click", function (e) {
        element.primary = true;

        if (element.id === "repair-toggle" && element.primary === true
            && injectedSeries && injectedSeries.length < 1) {
            console.log("clicked repair");
            element.primary = false;
            element.click();
        } else {
            element.on = !element.on;
            toggles.forEach(other => {
                if (other.on && !other.primary) {
                    other.click();
                }
            });
            element.primary = false;
        }

    })
})

let collapseRepairToggle = function () {
    let repairToggle = document.getElementById("repair-toggle");
    if (repairToggle.on) {
        repairToggle.click();
    }
}


