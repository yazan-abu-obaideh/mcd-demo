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
      imageBase64: personImage,
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

    const reader = new FileReader();

    let file = (document.getElementById("user-img-upload") as HTMLInputElement).files[0];
    console.log(file.name);
    console.log("Type: ")
    console.log(typeof(file));

    reader.readAsArrayBuffer(file);

    reader.onloadend = function() {
      // Encode the file as a Base64 string
      console.log("read file!")
      const base64File: string = arrayBufferToBase64(reader.result as ArrayBuffer);
      postSeedBikeOptimization(
        "1",
        base64File,
        25,
        75
      )
      .then((response) => {
        console.log(response.status);
      })
      .catch((exception) => {
        console.log("Exception occurred " + exception);
      })  
    }
    console.log("Valid form. Submitting request...");
    
    ;
  } else {
    form.reportValidity();
  }
}

function arrayBufferToBase64(arrayBuffer: ArrayBuffer) {
  let binary = '';
  const bytes = new Uint8Array(arrayBuffer);
  const len = bytes.byteLength;

  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }

  return btoa(binary);
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
