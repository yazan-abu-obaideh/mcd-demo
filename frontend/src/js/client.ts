const apiUrl = "http://localhost:5000";

async function getServerHealth(): Promise<Response> {
  return await fetch(apiUrl.concat("/health"), {
    headers: { "Content-Type": "application/json" },
    method: "GET",
    // body: requestBody,
  });
}

async function postSeedBikeOptimization(
  seedBikeId: string,
  personImage: string,
  personHeight: number,
  cameraHeight: number
) {
  return await fetch(apiUrl.concat("/optimize-seed"), {
    headers: { "Content-Type": "application/json" },
    method: "POST",
    body: JSON.stringify({
      seedBikeId: seedBikeId,
      personImage: personImage,
      personHeight: personHeight,
      cameraHeight: cameraHeight,
    }),
  });
}

async function postOptimizationRequest(
  seedBike: object,
  bodyDimensions: object
): Promise<Response> {
  return await fetch(apiUrl.concat("/optimize"), {
    headers: { "Content-Type": "application/json" },
    method: "POST",
    body: JSON.stringify({
      "seed-bike": seedBike,
      "body-dimensions": bodyDimensions,
    }),
  });
}

function submitRequest() {
  const form: HTMLFormElement = document.getElementById(
    "problem-form-form"
  ) as HTMLFormElement;
  if (form.checkValidity()) {
    console.log("Valid form. Submitting request...");
    console.log(form.get("seedBike"));
    postSeedBikeOptimization(
      "1", 
      (new FormData(form)).get("user-img").toString(),
      25,
      75
    )
    .then((response) => {
      console.log(response.status);
    })
    .catch((exception) => {
      console.log("Exception occurred " + exception);
    })
    
    ;
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

// export { getServerHealth, postOptimizationRequest, postSeedBikeOptimization };
