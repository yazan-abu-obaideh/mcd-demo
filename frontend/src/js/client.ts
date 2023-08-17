const optimizationApiUrl = "http://localhost:5000/api/v1";
const renderingApiUrl = "http://localhost:8000/api/v1/rendering";
let bikeStore = {};
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
  optimizationType: string,
  seedBikeId: string,
  riderImageId: string
) {
  return await fetch(
    optimizationApiUrl.concat(`/${optimizationType}/optimize-seeds`),
    {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: JSON.stringify({
        seedBikeId: seedBikeId,
        riderId: riderImageId,
      }),
    }
  );
}

async function postCustomRiderOptimization(
  optimizationType: string,
  seedBikeId: string,
  imageBase64: string,
  personHeight: number,
  cameraHeight: number
) {
  return await fetch(
    optimizationApiUrl.concat(`/${optimizationType}/optimize-custom-rider`),
    {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: JSON.stringify({
        seedBikeId: seedBikeId,
        imageBase64: imageBase64,
        personHeight: personHeight,
        cameraHeight: cameraHeight,
      }),
    }
  );
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

function postDownloadBikeCadRequest(bike: OptimizedBike): Promise<Response> {
  return fetch(optimizationApiUrl.concat("/download-cad"), {
    headers: { "Content-Type": "application/json" },
    method: "POST",
    body: JSON.stringify({
      bike: bike.bikeObject,
      seedBikeId: bike.seedImageId,
    }),
  });
}

function downloadBikeById(bikeId: string) {
  const downloadButton = getElementById(
    getDownloadBikeCadBtnId(bikeId)
  ) as HTMLButtonElement;

  downloadButton.innerHTML = "Downloading bike...";

  postDownloadBikeCadRequest(bikeStore[bikeId])
    .then((response) => {
      if (response.status == 200) {
        response.text().then((responseText) => {
          download(responseText);
          toPressedDownloadButton(downloadButton, "Downloaded successfully");
        });
      } else {
        toPressedDownloadButton(downloadButton, "Download failed");
      }
    })
    .catch((error) => {
      toPressedDownloadButton(downloadButton, "Download failed");
    });
}

function toPressedDownloadButton(
  downloadButton: HTMLButtonElement,
  textContent: string
) {
  downloadButton.innerHTML = textContent;
  downloadButton.setAttribute(
    "class",
    downloadButton.getAttribute("class")!.replace("btn-danger", "btn-dark")
  );
  downloadButton.disabled = true;
}

function download(text: string) {
  const anchor = document.createElement("a");
  anchor.setAttribute("download", "bike.bcad");
  anchor.setAttribute(
    "href",
    "data:applcation/xml;charset=utf-8," + encodeURIComponent(text)
  );
  anchor.click();
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

function submitCustomRiderForm(optimizationType: string): void {
  throwIfInvalidType(optimizationType);
  submitProblemForm(problemFormId, 
    (form: HTMLFormElement) => submitValidCustomRiderForm(optimizationType, form));
}

function submitSeedsForm(optimizationType: string): void {
  resetBikeStore();
  throwIfInvalidType(optimizationType);
  submitProblemForm(problemFormId, 
    (form: HTMLFormElement) => submitValidSeedsForm(optimizationType, form));
}

function resetBikeStore() {
  bikeStore = {};
}

function submitProblemForm(
  formId: string,
  validSubmissionFunction: CallableFunction
): void {
  const form: HTMLFormElement = getElementById(formId) as HTMLFormElement;
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

function submitValidCustomRiderForm(optimizationType:string, form: HTMLFormElement) {
  readFile("user-img-upload", (reader) => {
    const base64File: string = arrayBufferToBase64(
      reader.result as ArrayBuffer
    );
    const formData: FormData = new FormData(form);
    postCustomRiderOptimizationForm(optimizationType, formData, base64File);
  });
}

function submitValidSeedsForm(optimizationType: string, form: HTMLFormElement) {
  const formData = new FormData(form);
  postOptimizationForm(
    formData,
    postSeedsOptimization(
      optimizationType,
      formData.get("seedBike") as string,
      formData.get("riderImage") as string
    )
  );
}

function postCustomRiderOptimizationForm(
  optimizationType: string,
  formData: FormData,
  base64File: string
) {
  postOptimizationForm(
    formData,
    postCustomRiderOptimization(
      optimizationType,
      formData.get("seedBike") as string,
      base64File,
      Number(formData.get("user-height") as string),
      Number(formData.get("camera-height") as string)
    )
  );
}

function postOptimizationForm(
  formData: FormData,
  responsePromise: Promise<Response>
) {
  responsePromise
    .then((response) => {
      handleOptimizationResponse(response, formData);
    })
    .catch((exception) => {
      showGenericError();
    });
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
      (getElementById(getRenderBikeBtnId(Object.keys(bikeStore)[0])) as HTMLButtonElement).click();
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
    const bikeItem = bikeToCarouselItem(index, bikeId, bikes[index], bikes.length);
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

function bikeToCarouselItem(index: number, bikeId: string, bike: object, totalBikes: number) {
  const optimizedBikeDiv = document.createElement("div");
  optimizedBikeDiv.setAttribute(
    "class",
    "container text-center border rounded carousel-item mb-1 p-5 optimized-bike-div"
  );
  optimizedBikeDiv.appendChild(generateBikeDescription(index, bike, totalBikes));
  optimizedBikeDiv.appendChild(
    generatePerformanceElement(bike["bikePerformance"])
  );
  optimizedBikeDiv.appendChild(document.createElement("br"));
  optimizedBikeDiv.appendChild(createBikeLoadingElement(bikeId));
  optimizedBikeDiv.appendChild(createRenderingFailedElement(bikeId));
  optimizedBikeDiv.appendChild(generateRenderButton(bikeId));
  optimizedBikeDiv.appendChild(generateRenderedImgElement(bikeId));
  optimizedBikeDiv.appendChild(generateDownloadCadButton(bikeId));
  optimizedBikeDiv.appendChild(document.createElement("br"));
  return optimizedBikeDiv;
}

function generateBikeDescription(index: number, bike: object, totalBikes: number): HTMLElement {
  const element = document.createElement("h4");
  element.textContent = `Generated Bike ${index + 1}/${totalBikes}`;
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

function generateRenderButton(bikeId: string): HTMLElement {
  return generateBikeActionButton(
    bikeId,
    getRenderBikeBtnId,
    "Render bike",
    renderBikeById.name
  );
}

function generateDownloadCadButton(bikeId: string): HTMLElement {
  return generateBikeActionButton(
    bikeId,
    getDownloadBikeCadBtnId,
    "Download CAD",
    downloadBikeById.name
  );
}

function generateBikeActionButton(
  bikeId: string,
  idGenerator: CallableFunction,
  textContent: string,
  onClickFunctionName: string
): HTMLElement {
  const buttonCssClasses = "btn btn-outline-danger btn-lg";
  const button = document.createElement("button");
  button.setAttribute("class", buttonCssClasses);
  button.setAttribute("id", idGenerator(bikeId));
  button.setAttribute("onClick", `${onClickFunctionName}("${bikeId}")`);
  button.textContent = textContent;
  return button;
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

function getRenderBikeBtnId(bikeId: string) {
  // deterministic
  return `render-bike-btn-${bikeId}`;
}

function getDownloadBikeCadBtnId(bikeId: string) {
  // deterministic
  return `download-cad-bike-btn-${bikeId}`;
}

function hideRenderButton(bikeId: string) {
  const buttonElement = getElementById(getRenderBikeBtnId(bikeId));
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
    "text-center bike-render-inner-element-div flex-column"
  );
  bikeLoadingDiv.setAttribute("style", "display: none;");

  const innerDiv = document.createElement("div");
  innerDiv.setAttribute("class", "spinner-border loading-element");
  const labelDiv = document.createElement("div");
  labelDiv.textContent = "Rendering bike...";

  bikeLoadingDiv.appendChild(innerDiv);
  bikeLoadingDiv.appendChild(labelDiv);
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

function generatePerformanceElement(bikePerformance: object): HTMLElement {
  const div = document.createElement("h5");
  div.textContent = JSON.stringify(bikePerformance).replace('"', "").replace('"', "");
  return div;
}

function throwIfInvalidType(optimizationType: string) {
  if (!["aerodynamics", "ergonomics"].includes(optimizationType)) {
    throw Error(`Invalid optimization type ${optimizationType}`);
  }
}
// export { getServerHealth, postOptimizationRequest, postSeedBikeOptimization };
