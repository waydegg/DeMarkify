var el = x => document.getElementById(x);

function showPicker(){
    el("file-input").click();
}

function showPicked(input){
    el("upload-label").innerHTML = input.files[0].name;
    var reader = new FileReader();
    reader.onload = function(e) {
        el("image-picked").src = e.target.result();
        el("image-picked").classname = "";
    };
    reader.readAsDataURL(input.files[0]);
}

function analyze() {
    var uploadFiles = el('file-input').files;
    if (uploadFiles.length !== 1) alert("Please select a file to analyze!");

    el("analyze-button").innerHTML = "Analyzing...";
    var xhr = new XMLHttpRequest();
    var loc = window.location;
    xhr.open("POST", )
}