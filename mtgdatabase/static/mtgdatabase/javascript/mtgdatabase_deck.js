document.addEventListener("DOMContentLoaded", function(e) {
    var coll = document.getElementsByClassName("collapsible");
    var counter;

    for (counter = 0; counter < coll.length; counter++) {
        coll[counter].addEventListener("click", function() {
            this.classList.toggle("active");
            var deckContent = this.nextElementSibling;
            if (deckContent.style.display === "block") {
                deckContent.style.display = "none";
            } else {
                deckContent.style.display = "block";    
            }
        });
    }
});