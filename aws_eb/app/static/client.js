var el = x => document.getElementById(x);

function showPicker() {
  el("file-input").click();
}

function showPicked(input) {
  el("upload-label").innerHTML = input.files[0].name;
  var reader = new FileReader();
  reader.onload = function(e) {
    el("image-picked").src = e.target.result;
    el("image-picked").className = "";
  };
  reader.readAsDataURL(input.files[0]);
}

function analyzeJS() {

  var testData = "Some data...";
  var uploadFiles = el("file-input").files;

  if(uploadFiles.length !== 1) alert("Please select a file to analyze!");
  el("analyze-button").innerHTML = "Analyzing...";

  var entry = {
    image_data: uploadFiles,
    message: testData
  };

  console.log("ENTRY:")
  console.log(entry);

  // fetch method for POST and GET requests
  fetch(`${window.origin}/analyze`, {
    method: "POST",
    body: uploadFiles[0],
    cache: "no-cache",
    headers: new Headers({"content-type": "application/json"})
  }).then(function(response){
    el("analyze-button").innerHTML = "Analyze";

    if(response.status !== 200){
      console.log(`There was a problem. Status code: ${response.status}`);
      
      return;
    }
    response.json().then(function(data){
      el("result-label").innerHTML = `Generated URL = ${data["url"]}`
      console.log(`RESPONSE:`);
      console.log(data);
    });
  }).catch(function(error){
    console.log("Fetch error: " + error);
  });
}


