
let toggle_visibility= function(id){
   var e = document.getElementById(id);
   if(e.style.display == 'block')
      e.style.display = 'none';
   else
      e.style.display = 'block';
}



let toggles = Array.from(document.getElementsByClassName("myToggle"));
        toggles.forEach((element,i)=> {
            element["on"] = i === 0;
            element["primary"] = false;
        });

        toggles.forEach(element => {
            element.addEventListener("click", function (input) {
                element.on = !element.on;
                element.primary = true;
                toggles.forEach(other => {
                    if (other.on && !other.primary) {
                        other.click();
                    }
                });
                element.primary = false;
            })
        })
