const apiUrl = "http://localhost:5000";
const problemFormId = "problem-form-form";
const responseDivId = "server-response-div";

async function getServerHealth(): Promise<Response> {
  return await fetch(apiUrl.concat("/health"), {
    headers: { "Content-Type": "application/json" },
    method: "GET",
    // body: requestBody,
  });
}

async function postSeedBikeOptimization(
  seedBikeId: string,
  imageBase64: string,
  personHeight: number,
  cameraHeight: number
) {
  return await fetch(apiUrl.concat("/optimize-seed"), {
    headers: { "Content-Type": "application/json" },
    method: "POST",
    body: JSON.stringify({
      seedBikeId: seedBikeId,
      imageBase64: imageBase64,
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

function readFile(
  inputElementId: string,
  successHandler: (fileReader: FileReader) => void
) {
  const reader = new FileReader();
  reader.readAsArrayBuffer(getFileById(inputElementId));
  reader.onloadend = () => {
    successHandler(reader);
  };
}

function getFileById(inputElementId: string): File {
  return (document.getElementById(inputElementId) as HTMLInputElement).files[0];
}

function submitProblemForm() {
  const form: HTMLFormElement = document.getElementById(
    problemFormId
  ) as HTMLFormElement;
  if (form.checkValidity()) {
    showResponseDiv();
    submitValidForm(form);
  } else {
    showFormErrors(form);
  }
}

function showResponseDiv() {
  const responseDiv = document.getElementById(responseDivId);
  setLoading(true);
  responseDiv.setAttribute("style", "display: block;");
  responseDiv.scrollIntoView();
}

function showFormErrors(form: HTMLFormElement) {
  form.reportValidity();
}

function submitValidForm(form: HTMLFormElement) {
  readFile("user-img-upload", (reader) => {
    console.log("read file!");
    const base64File: string = arrayBufferToBase64(
      reader.result as ArrayBuffer
    );
    const formData: FormData = new FormData(form);
    postSeedBikeOptimization(formData.get("seedBike") as string, base64File, 
    Number(formData.get("user-height") as string), Number(formData.get("camera-height") as string))
      .then((response) => {
        handleOptimizationResponse(response);
      })
      .catch((exception) => {
        console.log("Exception occurred " + exception);
      });
  });
}

function handleOptimizationResponse(response: Response) {
  if (response.status == 200) {
    handleSuccessfulOptimizationResponse(response);
    
  } else {
    console.log("Failed!")
  }
}

function handleSuccessfulOptimizationResponse(response: Response) {
  response.text().then((responseText) => {
    const responseJson: object = JSON.parse(responseText);
    setLoading(false);
    document.getElementById("mcd-logs-consumer").innerHTML = logsToHtml(responseJson["logs"]);
    document.getElementById("generated-designs-consumer").innerHTML = bikesToHtml(responseJson["bikes"]);
  });
}

function setLoading(loading: boolean) {
  if (loading) {
    setResponseDivChildrenVisilbity('block', 'none');
  } else {
    setResponseDivChildrenVisilbity('none', 'block');
  }
}

function setResponseDivChildrenVisilbity(loadingDisplay: string, responseDisplay: string) {
  document.getElementById("response-loading-div")?.setAttribute("style", `display: ${loadingDisplay}`);
  document.getElementById("response-received-div")?.setAttribute("style", `display: ${responseDisplay}`);
}

function arrayBufferToBase64(arrayBuffer: ArrayBuffer) {
  let binary = "";
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


function bikesToHtml(bikes: Array<object>): string {
  let bikesHtml = "";
  bikes.forEach(bike => {
    bikesHtml += bikeToHtml(bike)
  });
  return bikesHtml;
}

function bikeToHtml(bike: object) {
  return `<div class="container text-center border rounded mb-1"> Crank Length: ${parseNumber(bike["crank_length"])} | 
    Handle Bar X: ${parseNumber(bike["handle_bar_x"])} Handle Bar Y: ${parseNumber(bike["handle_bar_y"])} 
    Seat X: ${parseNumber(bike["seat_x"])} Seat Y: ${parseNumber(bike["seat_y"])} </div>`;
}

function parseNumber(numberAsString: string): number {
  return Number(Number(numberAsString).toFixed(3));
}

function logsToHtml(logs: Array<string>): string {
  let inner = "";
  logs.forEach(logMessage => {
    inner += logMessage + "<br>"
  });
return `<p> ${inner} </p>`
}

function onShowLogs() {
    document.getElementById("collapse-logs-div")?.scrollIntoView();
}

// export { getServerHealth, postOptimizationRequest, postSeedBikeOptimization };
