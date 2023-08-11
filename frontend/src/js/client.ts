const optimizationApiUrl = "http://localhost:5000/api/v1";
const renderingApiUrl = "http://localhost:8000/api/v1/rendering";
const bikeStore = {};
const problemFormId = "problem-form-form";
const responseDivId = "server-response-div";
const urlCreator = window.URL || window.webkitURL;

class OptimizedBike {
  seedImageId: string;
  bikeObject: object;
  bikePerformance: object;
}

class ExclusivelyVisibleElements {
  // a class that encapsulates the logic of a bunch of elements where only one can be visible at a time
  constructor(elementIds: Array<string>) {
    this.elementIds = elementIds;
  }

  elementIds: Array<string>;
  showElement(id: string, elementDisplay = "block") {
    if (!this.elementIds.includes(id)) {
      throw Error("Element not found");
    }
    this.elementIds.forEach((elementId) => {
      getElementById(elementId).setAttribute("style", "display: none");
    });
    getElementById(id).setAttribute("style", `display: ${elementDisplay}`);
  }
}

const resultDivElements = new ExclusivelyVisibleElements([
  "response-received-div",
  "no-bikes-found-div",
  "response-loading-div",
  "error-response-div",
]);



async function postSeedsOptimization(
  seedBikeId: string,
  riderImageId: string
) {
  return await fetch(optimizationApiUrl.concat("/optimize-seeds"), {
    headers: { "Content-Type": "application/json" },
    method: "POST",
    body: JSON.stringify({
      seedBikeId: seedBikeId,
      riderId: riderImageId
    }),
  });
}

async function postCustomRiderOptimization(
  seedBikeId: string,
  imageBase64: string,
  personHeight: number,
  cameraHeight: number
) {
  return await fetch(optimizationApiUrl.concat("/optimize-custom-rider"), {
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
  return (getElementById(inputElementId) as HTMLInputElement).files![0];
}

function postRenderBikeRequest(bike: OptimizedBike): Promise<Response> {
  return fetch(renderingApiUrl.concat("/render-bike-object"), {
    headers: { "Content-Type": "application/json" },
    method: "POST",
    body: JSON.stringify({
      bike: bike.bikeObject,
      seedImageId: bike.seedImageId,
    }),
  });
}

function renderBikeById(bikeId: string) {
  hideRenderButton(bikeId);
  setBikeLoading(bikeId, "flex");
  postRenderBikeRequest(bikeStore[bikeId])
    .then((response) => {
      if (response.status == 200) {
        handleSuccessfulRenderResponse(response, bikeId);
      } else {
        showRenderError(bikeId);
      }
    })
    .catch((error) => {
      console.log(error);
      showRenderError(bikeId);
    })
    .finally(() => setBikeLoading(bikeId, "none"));
}

function showRenderError(bikeId: string) {
  getElementById(renderingFailedElementId(bikeId)).setAttribute(
    "style",
    "display: flex"
  );
}

function handleSuccessfulRenderResponse(response: Response, bikeId: string) {
  response.blob().then((responseBlob) => {
    handleRenderedBikeImage(bikeId, responseBlob);
  });
}

function setBikeLoading(bikeId: string, display: string): void {
  document
    .getElementById(bikeLoadingId(bikeId))!
    .setAttribute("style", `display: ${display}`);
}

function handleRenderedBikeImage(bikeId: string, responseBlob: Blob) {
  const outputImg = getElementById(getBikeImgId(bikeId)) as HTMLImageElement;
  outputImg.src = urlCreator.createObjectURL(responseBlob);
  outputImg.setAttribute("style", "display: inline");
}

function submitCustomRiderForm(): void {
  submitProblemForm(problemFormId, submitValidCustomRiderForm);
}

function submitSeedsForm(): void {
  submitProblemForm(problemFormId, submitValidSeedsForm)
}


function submitProblemForm(formId: string, validSubmissionFunction: CallableFunction): void {
  const form: HTMLFormElement = getElementById(
    formId
  ) as HTMLFormElement;
  if (form.checkValidity()) {
    showResponseDiv();
    validSubmissionFunction(form);
  } else {
    showFormErrors(form);
  }
}

function showResponseDiv() {
  const responseDiv = getElementById(responseDivId);
  setLoading();
  responseDiv.setAttribute("style", "display: block;");
  responseDiv.scrollIntoView();
}

function showFormErrors(form: HTMLFormElement) {
  form.reportValidity();
}

function submitValidCustomRiderForm(form: HTMLFormElement) {
  readFile("user-img-upload", (reader) => {
    const base64File: string = arrayBufferToBase64(
      reader.result as ArrayBuffer
    );
    const formData: FormData = new FormData(form);
    postCustomRiderOptimizationForm(formData, base64File);
  });
}

function submitValidSeedsForm(form: HTMLFormElement) {
  const formData = new FormData(form);
  postOptimizationForm(
    formData, postSeedsOptimization(
      formData.get("seedBike") as string,
      formData.get("riderImage") as string
    )
  )
}


function postCustomRiderOptimizationForm(formData: FormData, base64File: string) {
  postOptimizationForm(formData, postCustomRiderOptimization(
    formData.get("seedBike") as string,
    base64File,
    Number(formData.get("user-height") as string),
    Number(formData.get("camera-height") as string)
  ));
}

function postOptimizationForm(formData: FormData, responsePromise: Promise<Response>) {
  responsePromise.then((response) => {
    handleOptimizationResponse(response, formData);
  })
  .catch((exception) => {
    showGenericError();
  })
}


function handleOptimizationResponse(response: Response, formData: FormData) {
  if (response.status == 200) {
    handleSuccessfulOptimizationResponse(response, formData);
  } else {
    handleFailedResponse(response);
  }
}

function handleSuccessfulOptimizationResponse(
  response: Response,
  formData: FormData
) {
  response.text().then((responseText) => {
    const responseJson: object = JSON.parse(responseText);
    if (responseJson["bikes"].length == 0) {
      resultDivElements.showElement("no-bikes-found-div");
    } else {
      showGeneratedBikes(responseJson, formData);
    }
  });
}

function showGeneratedBikes(responseJson: object, formData: FormData) {
  resultDivElements.showElement("response-received-div");
  getElementById("mcd-logs-consumer").innerHTML = logsToHtml(
    responseJson["logs"]
  );
  getElementById("generated-designs-consumer-carousel").innerHTML =
    persistAndBuildCarouselItems(responseJson["bikes"], formData).innerHTML;
}

function setLoading() {
  resultDivElements.showElement("response-loading-div");
}

function setResponseDivChildrenVisibility(loadingDisplay: string) {
  document
    .getElementById("response-loading-div")
    ?.setAttribute("style", `display: ${loadingDisplay}`);
}

function arrayBufferToBase64(arrayBuffer: ArrayBuffer) {
  let binary = "";
  const bytes = new Uint8Array(arrayBuffer);
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

function persistAndBuildCarouselItems(
  bikes: Array<object>,
  formData: FormData
): HTMLDivElement {
  const bikesHtml = document.createElement("div");
  for (let index = 0; index < bikes.length; index++) {
    const bikeId = persistBike(bikes[index], formData);
    const bikeItem = bikeToCarouselItem(index, bikeId, bikes[index]);
    activateFirst(index, bikeItem);
    bikesHtml.appendChild(bikeItem);
  }
  return bikesHtml;
}

function activateFirst(index: number, bikeItem: HTMLDivElement) {
  if (index == 0) {
    bikeItem.setAttribute("class", bikeItem.getAttribute("class") + " active");
  }
}

function bikeToCarouselItem(index: number, bikeId: string, bike: object) {
  const optimizedBikeDiv = document.createElement("div");
  optimizedBikeDiv.setAttribute(
    "class",
    "container text-center border rounded carousel-item mb-1 p-5 optimized-bike-div"
  );
  optimizedBikeDiv.appendChild(generateBikeDescription(index, bike));
  optimizedBikeDiv.appendChild(document.createElement("br"));
  optimizedBikeDiv.appendChild(createBikeLoadingElement(bikeId));
  optimizedBikeDiv.appendChild(createRenderingFailedElement(bikeId));
  optimizedBikeDiv.appendChild(generateRenderButton(bikeId));
  optimizedBikeDiv.appendChild(document.createElement("br"));
  optimizedBikeDiv.appendChild(generateRenderedImgElement(bikeId));
  return optimizedBikeDiv;
}

function generateBikeDescription(index: number, bike: object): HTMLElement {
  const element = document.createElement("h4");
  element.textContent = `Generated Bike ${index + 1}`;
  return element;
}

function generateRenderedImgElement(bikeId: string): HTMLDivElement {
  const imageDiv = document.createElement("div");
  imageDiv.setAttribute("class", "m-3 text-center");
  const image = document.createElement("img");
  image.setAttribute("class", "rendered-bike-img");
  image.setAttribute("id", getBikeImgId(bikeId));
  image.setAttribute("alt", "rendered bike image");
  image.setAttribute("style", "display: none");
  imageDiv.appendChild(image);
  return imageDiv;
}

function generateRenderButton(bikeId: string): HTMLDivElement {
  const div = document.createElement("div");
  div.setAttribute("class", "bike-render-inner-element-div");
  div.setAttribute("id", getBikeBtnId(bikeId));
  const button = document.createElement("button");
  button.setAttribute("class", "btn btn-danger btn-lg");
  button.setAttribute("onClick", `${renderBikeById.name}("${bikeId}")`);
  button.textContent = "Render Bike";
  div.appendChild(button);
  return div;
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
  optimizedBike.bikeObject = bike["bike"];
  optimizedBike.bikePerformance = bike["bikePerformance"];
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
  response.text().then((responseText) => {
    try {
      handleJsonFailedResponse(responseText);
    } catch {
      showGenericError();
    }
  });
}

function showGenericError() {
  resultDivElements.showElement("error-response-div");
  getElementById("error-response-div").innerHTML =
    "<h3> Something went wrong. </h3>";
}

function handleJsonFailedResponse(responseText: string) {
  const errorResponse = JSON.parse(responseText);
  resultDivElements.showElement("error-response-div");
  getElementById(
    "error-response-div"
  ).innerHTML = `<h3> Operation failed. Server responded with: ${errorResponse["message"]} </h3>`;
}

function getElementById(elementId: string): HTMLElement {
  return document.getElementById(elementId)!;
}

function createBikeLoadingElement(bikeId: string): HTMLDivElement {
  const bikeLoadingDiv = document.createElement("div");
  bikeLoadingDiv.setAttribute("id", bikeLoadingId(bikeId));
  bikeLoadingDiv.setAttribute(
    "class",
    "text-center bike-render-inner-element-div"
  );
  bikeLoadingDiv.setAttribute("style", "display: none;");

  const innerDiv = document.createElement("div");
  innerDiv.setAttribute("class", "spinner-border loading-element");

  bikeLoadingDiv.appendChild(innerDiv);
  return bikeLoadingDiv;
}

function bikeLoadingId(bikeId: string): string {
  return `bike-loading-element-${bikeId}`;
}

function createRenderingFailedElement(bikeId: string): HTMLElement {
  const div = document.createElement("div");
  div.setAttribute("class", "bike-render-inner-element-div");
  div.setAttribute("id", renderingFailedElementId(bikeId));
  div.setAttribute("style", "display: none");
  div.innerHTML = "<h4> Rendering failed... </h4>";
  return div;
}

function renderingFailedElementId(bikeId: string): string {
  return `bike-rendering-failed-${bikeId}`;
}

// export { getServerHealth, postOptimizationRequest, postSeedBikeOptimization };
