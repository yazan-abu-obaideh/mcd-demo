const apiUrl = "http://localhost:5000";

function submitRequest() {
  const form: HTMLFormElement = document.getElementById(
    "problem-form-form"
  ) as HTMLFormElement;
  if (form.checkValidity()) {
    optimizeSeedBike(
      {
        seat_x: -9,
        seat_y: 27,
        handle_bar_x: 16.5,
        handle_bar_y: 25.5,
        crank_length: 7,
      },
      {
        height: 75,
        sh_height: 61.09855828510818,
        hip_to_ankle: 31.167514055725047,
        hip_to_knee: 15.196207871637029,
        shoulder_to_wrist: 13.538605228960089,
        arm_len: 16.538605228960087,
        tor_len: 26.931044229383136,
        low_leg: 18.971306184088018,
        up_leg: 15.196207871637029,
      }
    );
  } else {
    form.reportValidity();
  }
}

function optimizeSeedBike(seedBike: Object, bodyDimensions: Object) {
  restfulPost(
    "/optimize",
    { "seed-bike": seedBike, "body-dimensions": bodyDimensions },
    (response) => {
      console.log(response);
    },
    (errorResponse) => {
      console.log(errorResponse);
    }
  );
}

function getHealth() {
  restfulGet(
    "/health",
    (responseJson) => {
      console.log("Success " + responseJson["status"]);
      return responseJson;
    },
    (errorResponse) => {
      console.log("Boo! " + errorResponse["message"]);
    }
  );
}

function restfulPost(
  urlSuffix: string,
  requestBody: Object,
  successHandler: (response: JSON) => void,
  errorResponseHandler: (response: JSON) => void
) {
  restfulCall(
    urlSuffix,
    JSON.stringify(requestBody),
    "POST",
    successHandler,
    errorResponseHandler
  );
}

function restfulGet(
  urlSuffix: string,
  successHandler: (response: JSON) => void,
  errorResponseHandler: (response: JSON) => void
) {
  restfulCall(urlSuffix, null, "GET", successHandler, errorResponseHandler);
}

function restfulCall(
  urlSuffix: string,
  requestBody: string | null,
  requestMethod: string,
  successHandler: (response: JSON) => void,
  errorResponseHandler: (response: JSON) => void
) {
  fetch(apiUrl.concat(urlSuffix), {
    headers: { "Content-Type": "application/json" },
    method: requestMethod,
    body: requestBody,
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

function utilizeHandler(handler: (response: JSON) => void, response: Response) {
  response.text().then((responseText) => handler(JSON.parse(responseText)));
}

// export default getHealth;