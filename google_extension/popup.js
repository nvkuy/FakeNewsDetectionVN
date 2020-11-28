const server_address = '127.0.0.1';
const port = '5000';

function showResult(prediction) {
  // prediction = -1: đang xử lí
  if (prediction < 0) {
    document.getElementById("result").style.visibility = "hidden";
    document.getElementById("loader").style.visibility = "visible";
  } else {
    document.getElementById("result").style.visibility = "visible";
    document.getElementById("loader").style.visibility = "hidden";
    document.getElementById("prediction").innerHTML = prediction + "%";
  }
}

chrome.tabs.query({active: true, currentWindow: true}, tabs => {
  let url = tabs[0].url;
  getPrediction(url);
  // console.log(url);
  // chrome.tabs.sendMessage(tabs[0].id, {url_target: url}, function(response) {
  //   // console.log(response.result);
  // });
});

// chrome.runtime.onMessage.addListener(
//   function(request, sender, sendResponse) {
//     // console.log(request.url_target);
//     // sendResponse({result: 100});
//   });

function getPrediction(url) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      res = (parseFloat(this.responseText) * 100).toFixed(1);
      // console.log(res);
      showResult(res);
    }
  };
  xhttp.open("GET", ("http://" + server_address + ":" + port + "/cn?url=" + url), true);
  xhttp.send();
}

window.onload = function() {
  showResult(-1);
}