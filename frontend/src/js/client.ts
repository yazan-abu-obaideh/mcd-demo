const optimizationApiUrl = "http://localhost:5000/api/v1";
const renderingApiUrl = "http://localhost:8000/api/v1/rendering";
const bikeStore = {};
const problemFormId = "problem-form-form";
const responseDivId = "server-response-div";
const urlCreator = window.URL || window.webkitURL;


class OptimizedBike {
  seedImageId: string;
  bikeObject: object;
}

async function postSeedBikeOptimization(
  seedBikeId: string,
  imageBase64: string,
  personHeight: number,
  cameraHeight: number
) {
  return await fetch(optimizationApiUrl.concat("/optimize-seed"), {
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
  return await fetch(optimizationApiUrl.concat("/optimize"), {
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
  return ((getElementById(inputElementId) as HTMLInputElement).files)![0];
}

function postRenderBikeRequest(bike: OptimizedBike): Promise<Response> {
  return fetch(renderingApiUrl.concat("/render-bike-object"), {
    headers: { "Content-Type": "application/json" },
    method: "POST",
    body: JSON.stringify({
      bike: bike.bikeObject,
      seedImageId: bike.seedImageId
    }),
  });
}

function renderBikeById(bikeId: string) {
  postRenderBikeRequest(bikeStore[bikeId]).then((response) => {
    response.blob().then((responseBlob) => {
      handleRenderedBikeImage(bikeId, responseBlob);
      hideRenderButton(bikeId);
    });
  });
}

function handleRenderedBikeImage(bikeId: string, responseBlob: Blob) {
  const outputImg = getElementById(
    getBikeImgId(bikeId)
  ) as HTMLImageElement;
  outputImg.src = urlCreator.createObjectURL(responseBlob);
  outputImg.setAttribute("style", "display: inline");
}

function submitProblemForm() {
  const form: HTMLFormElement = getElementById(
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
  const responseDiv = getElementById(responseDivId);
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
    postSeedBikeOptimizationForm(formData, base64File);
  });
}

function postSeedBikeOptimizationForm(formData: FormData, base64File: string) {
  postSeedBikeOptimization(
    formData.get("seedBike") as string,
    base64File,
    Number(formData.get("user-height") as string),
    Number(formData.get("camera-height") as string)
  )
    .then((response) => {
      handleOptimizationResponse(response, formData);
    })
    .catch((exception) => {
      setLoading(false);
      getElementById("generated-designs-consumer").innerHTML =
        "<h2> Operation failed. Either you have no internet connection, or our servers are down 🥸 </h2>";
    });
}

function handleOptimizationResponse(response: Response, formData: FormData) {
  if (response.status == 200) {
    handleSuccessfulOptimizationResponse(response, formData);
  } else {
    handleFailedResponse(response);
  }
}

function handleSuccessfulOptimizationResponse(response: Response, formData: FormData) {
  response.text().then((responseText) => {
    const responseJson: object = JSON.parse(responseText);
    setLoading(false);
    getElementById("mcd-logs-consumer").innerHTML = logsToHtml(
      responseJson["logs"]
    );
    getElementById("generated-designs-consumer").innerHTML =
      persistAndBuildHtml(responseJson["bikes"], formData);
  });
}

function setLoading(loading: boolean) {
  if (loading) {
    setResponseDivChildrenVisibility("block", "none");
  } else {
    setResponseDivChildrenVisibility("none", "block");
  }
}

function setResponseDivChildrenVisibility(
  loadingDisplay: string,
  responseDisplay: string
) {
  document
    .getElementById("response-loading-div")
    ?.setAttribute("style", `display: ${loadingDisplay}`);
  document
    .getElementById("response-received-div")
    ?.setAttribute("style", `display: ${responseDisplay}`);
}

function arrayBufferToBase64(arrayBuffer: ArrayBuffer) {
  let binary = "";
  const bytes = new Uint8Array(arrayBuffer);
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

function persistAndBuildHtml(bikes: Array<object>, formData: FormData): string {
  let bikesHtml = "";
  bikes.forEach((bike) => {
    const bikeId = persistBike(bike, formData);
    bikesHtml += bikeToHtml(bikeId, bike);
  });
  return bikesHtml;
}

function bikeToHtml(bikeId: string, bike: object) {
  return `
  <div class="container text-center border rounded mb-1 p-3">
  ${generateBikeDescription(bike)}
  <br>
  ${generateRenderButton(bikeId)}
    <br>
     ${generateRenderedImgElement(bikeId)}
  </div>`;
}

function generateBikeDescription(bike: object): string {
  return `Generated Bike`;
}

function generateRenderedImgElement(bikeId: string): string {
  return `<div class="m-3 text-center"> <img class="rendered-bike-img" id='${getBikeImgId(
    bikeId
  )}' alt="rendered bike image" style="display: none"> </div>`;
}

function generateRenderButton(bikeId: string): string {
  return `<button type="button" id='${getBikeBtnId(
    bikeId
  )}' class="btn btn-danger btn-sm m-2"
  onclick='${renderBikeById.name}("${bikeId}")'> 
    Render Bike </button>
`;
}

function formatNumber(numberAsString: string): string {
  return Number(numberAsString).toFixed(3);
}

function logsToHtml(logs: Array<string>): string {
  let inner = "";
  logs.forEach((logMessage) => {
    inner += logMessage + "<br>";
  });
  return `<p> ${inner} </p>`;
}

function onShowLogs() {
  getElementById("collapse-logs-div")?.scrollIntoView();
}

function generateUuid(): string {
  const S4 = function (): string {
    return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
  };
  return (
    S4() +
    S4() +
    "-" +
    S4() +
    "-" +
    S4() +
    "-" +
    S4() +
    "-" +
    S4() +
    S4() +
    S4()
  );
}

function persistBike(bike: object, formData: FormData): string {
  const bikeId = generateUuid();
  const optimizedBike = new OptimizedBike();
  optimizedBike.bikeObject = bike;
  optimizedBike.seedImageId = formData.get("seedBike") as string;
  bikeStore[bikeId] = optimizedBike;
  return bikeId;
}

function getBikeImgId(bikeId: string) {
  // deterministic
  return `bike-img-${bikeId}`;
}

function getBikeBtnId(bikeId: string) {
  // deterministic
  return `render-bike-btn-${bikeId}`;
}

function hideRenderButton(bikeId: string) {
  const buttonElement = getElementById(getBikeBtnId(bikeId));
  buttonElement?.setAttribute("style", "display: none");
}

function handleFailedResponse(response: Response) {
  response.text().then(responseText => {
    const errorResponse = JSON.parse(responseText);
    setLoading(false);
    getElementById("generated-designs-consumer").innerHTML = 
    `<h2> Operation failed. Server responded with: ${errorResponse["message"]} </h2>`
  });
}

function getElementById(elementId: string): HTMLElement {
  return document.getElementById(elementId)!;
}

// export { getServerHealth, postOptimizationRequest, postSeedBikeOptimization };
