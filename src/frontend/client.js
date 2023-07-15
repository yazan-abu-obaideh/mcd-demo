const apiUrl = "http://localhost:5000";

function submitRequest() {
  const form = document.getElementById("problem-form-form");
  if (form.checkValidity()) {
    console.log("Submitted!");
    console.log(document.getElementById("user-height-input").value);
    console.log(document.getElementById("camera-height-input").value);
    console.log(form.elements["seedBike"].value);
  } else {
    form.reportValidity();
  }
}

function getHealth() {
  restfulGet(
    "/health",
    (responseJson) => {
      console.log("Success " + responseJson["status"]);
    },
    (errorResponse) => {
      console.log("Boo! " + errorResponse["message"]);
    }
  );
}

function restfulPost(urlSuffix, requestBody, successHandler, errorResponseHandler) {
  restfulCall(urlSuffix, JSON.stringify(requestBody), "POST", successHandler, errorResponseHandler);
}

function restfulGet(urlSuffix, successHandler, errorResponseHandler) {
  restfulCall(urlSuffix, "", "GET", successHandler, errorResponseHandler);
}

function restfulCall(urlSuffix, requestBody, requestMethod, successHandler, errorResponseHandler) {
  fetch(apiUrl.concat(urlSuffix), {
    headers: { "Content-Type": "application/json" },
    requestMethod: requestMethod,
    requestBody: requestBody
  })
    .then((response) => {
      if (200 <= response.status && response.status < 300) {
        utilizeHandler(successHandler, response);
      } else {
        utilizeHandler(errorResponseHandler, response);
      }
    })
    .catch((exception) => {
      console.log("Something went wrong: " + exception);
    });
}


function utilizeHandler(handler, response) {
  response.text().then((responseText) => handler(JSON.parse(responseText)));
}
