import {
  OptimizationController,
  RenderingController,
  GeneratedBike,
} from "./controller";

const optimizationApiUrl = "https://mcd-demo.com/api/v1/optimization";
const renderingApiUrl = "https://mcd-demo.com/api/v1/rendering";
let bikeStore = {};
const seedsFormId = "seeds-form-form";
const uploadRiderImageFormId = "upload-rider-image-form";
const specifyDimensionsFormId = "specify-rider-dimensions-form";
const responseDivId = "server-response-div";
const urlCreator = window.URL || window.webkitURL;
const optimizationController = new OptimizationController(optimizationApiUrl);
const renderingController = new RenderingController(renderingApiUrl);

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

const problemFormElements = new ExclusivelyVisibleElements([
  seedsFormId,
  uploadRiderImageFormId,
  specifyDimensionsFormId,
]);

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

function downloadBikeById(bikeId: string) {
  const downloadButton = getElementById(
    getDownloadBikeCadBtnId(bikeId)
  ) as HTMLButtonElement;

  downloadButton.innerHTML = "Downloading bike...";

  optimizationController
    .postDownloadBikeCadRequest(bikeStore[bikeId])
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
    "data:application/xml;charset=utf-8," + encodeURIComponent(text)
  );
  anchor.click();
}

function renderBikeById(bikeId: string) {
  hideRenderButton(bikeId);
  setBikeLoading(bikeId, "flex");
  renderingController
    .postRenderBikeRequest(bikeStore[bikeId])
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
  getElementById(getBikeImagesDivId(bikeId)).setAttribute(
    "style",
    "display: flex"
  );
}

function submitCustomRiderForm(optimizationType: string): void {
  resetBikeStore();
  throwIfInvalidType(optimizationType);
  submitProblemForm(uploadRiderImageFormId, (form: HTMLFormElement) =>
    submitValidCustomRiderForm(optimizationType, form)
  );
}

function submitRiderDimensionsForm(optimizationType: string): void {
  resetBikeStore();
  throwIfInvalidType(optimizationType);
  submitProblemForm(specifyDimensionsFormId, (form: HTMLFormElement) =>
    submitValidDimensionsForm(optimizationType, form)
  );
}

function submitSeedsForm(optimizationType: string): void {
  resetBikeStore();
  throwIfInvalidType(optimizationType);
  submitProblemForm(seedsFormId, (form: HTMLFormElement) =>
    submitValidSeedsForm(optimizationType, form)
  );
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

function submitValidCustomRiderForm(
  optimizationType: string,
  form: HTMLFormElement
) {
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
    optimizationController.postSeedsOptimization(
      optimizationType,
      formData.get("seedBike") as string,
      formData.get("riderImage") as string
    )
  );
}

function getNumberFrom(formData: FormData, fieldName: string): number {
  return Number(formData.get(fieldName) as string);
}

function submitValidDimensionsForm(
  optimizationType: string,
  form: HTMLFormElement
) {
  const formData = new FormData(form);
  postOptimizationForm(
    formData,
    optimizationController.postDimensionsOptimization(
      optimizationType,
      formData.get("seedBike") as string,
      {
        height: getNumberFrom(formData, "rider-height"),
        sh_height: getNumberFrom(formData, "shoulder-height"),
        hip_to_ankle: getNumberFrom(formData, "hip-ankle"),
        hip_to_knee: getNumberFrom(formData, "hip-knee"),
        shoulder_to_wrist: getNumberFrom(formData, "shoulder-wrist"),
        arm_length: getNumberFrom(formData, "arm-length"),
        torso_length: getNumberFrom(formData, "torso-length"),
        lower_leg: getNumberFrom(formData, "lower-leg"),
        upper_leg: getNumberFrom(formData, "upper-leg"),
      }
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
    optimizationController.postImageOptimization(
      optimizationType,
      formData.get("seedBike") as string,
      base64File,
      Number(formData.get("user-height") as string)
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
      renderFirstBike();
    }
  });
}

function renderFirstBike() {
  (
    getElementById(
      getRenderBikeBtnId(Object.keys(bikeStore)[0])
    ) as HTMLButtonElement
  ).click();
}

function showGeneratedBikes(responseJson: object, formData: FormData) {
  resultDivElements.showElement("response-received-div");
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
    const bikeItem = bikeToCarouselItem(
      index,
      bikeId,
      bikes[index],
      bikes.length
    );
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

function bikeToCarouselItem(
  index: number,
  bikeId: string,
  bike: object,
  totalBikes: number
) {
  const optimizedBikeDiv = document.createElement("div");
  optimizedBikeDiv.setAttribute(
    "class",
    "container text-center border rounded carousel-item mb-1 p-5 optimized-bike-div"
  );
  optimizedBikeDiv.appendChild(
    generateBikeDescription(index, bike, totalBikes)
  );
  optimizedBikeDiv.appendChild(
    generatePerformanceElement(bike["bikePerformance"])
  );
  optimizedBikeDiv.appendChild(document.createElement("br"));
  optimizedBikeDiv.appendChild(createBikeLoadingElement(bikeId));
  optimizedBikeDiv.appendChild(createRenderingFailedElement(bikeId));
  optimizedBikeDiv.appendChild(generateRenderButton(bikeId));
  optimizedBikeDiv.appendChild(generateRenderedImgElement(bikeId));
  optimizedBikeDiv.appendChild(createSpaceDiv());
  optimizedBikeDiv.appendChild(generateDownloadCadButton(bikeId));
  return optimizedBikeDiv;
}

function generateBikeDescription(
  index: number,
  bike: object,
  totalBikes: number
): HTMLElement {
  const element = document.createElement("h4");
  element.textContent = `Generated Bike ${index + 1}/${totalBikes}`;
  return element;
}

function generateRenderedImgElement(bikeId: string): HTMLDivElement {
  const imagesDiv = document.createElement("div");
  const renderedImgDiv = createResultImgDiv();
  const originalImgDiv = createResultImgDiv();

  imagesDiv.setAttribute("class", "text-center p-5 row");
  imagesDiv.setAttribute("id", getBikeImagesDivId(bikeId));
  imagesDiv.setAttribute("style", "display: none");
  const renderedImg = document.createElement("img");

  const originalImg = document.createElement("img");
  originalImg.src = `../assets/bike${
    (bikeStore[bikeId] as GeneratedBike).seedImageId
  }.png`;
  originalImg.setAttribute("class", "original-bike-img-in-result");
  originalImg.setAttribute("id", getOriginalImageInResultId(bikeId));

  renderedImg.setAttribute("class", "rendered-bike-img");
  renderedImg.setAttribute("id", getBikeImgId(bikeId));
  renderedImg.setAttribute("alt", "rendered bike image");

  renderedImgDiv.appendChild(renderedImg);
  renderedImgDiv.appendChild(getImageLabel("Generated", getBikeImgId(bikeId)));

  originalImgDiv.appendChild(originalImg);
  originalImgDiv.appendChild(
    getImageLabel("Original", getOriginalImageInResultId(bikeId))
  );

  imagesDiv.appendChild(originalImgDiv);
  imagesDiv.appendChild(renderedImgDiv);
  return imagesDiv;
}

function getImageLabel(textContent: string, htmlFor: string) {
  const label = document.createElement("label");
  label.textContent = textContent;
  label.htmlFor = htmlFor;
  label.setAttribute("style", "display: block");
  return label;
}

function createResultImgDiv() {
  const renderedImgDiv = document.createElement("div");
  renderedImgDiv.setAttribute("class", "col bike-img-div-in-result");
  return renderedImgDiv;
}

function generateRenderButton(bikeId: string): HTMLElement {
  return generateBikeActionButton(
    bikeId,
    getRenderBikeBtnId,
    "Render bike",
    renderBikeById.name
  );
}

function showForm(formId: string) {
  problemFormElements.showElement(formId);
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
  const generatedBike = new GeneratedBike();
  generatedBike.bikeObject = bike["bike"];
  generatedBike.bikePerformance = bike["bikePerformance"];
  generatedBike.seedImageId = formData.get("seedBike") as string;
  bikeStore[bikeId] = generatedBike;
  return bikeId;
}

function getBikeImgId(bikeId: string) {
  // deterministic
  return `bike-img-${bikeId}`;
}

function getBikeImagesDivId(bikeId: string) {
  return `bike-img-div-result-${bikeId}`;
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
  div.textContent = JSON.stringify(bikePerformance)
    .replace('"', "")
    .replace('"', "");
  return div;
}

function throwIfInvalidType(optimizationType: string) {
  if (!["aerodynamics", "ergonomics"].includes(optimizationType)) {
    throw Error(`Invalid optimization type ${optimizationType}`);
  }
}

function createSpaceDiv(): HTMLDivElement {
  const spaceDiv = document.createElement("div");
  spaceDiv.setAttribute("style", "height: 5px");
  return spaceDiv;
}

function getOriginalImageInResultId(bikeId: string): string {
  return `original-img-in-result-${bikeId}`;
}
export {
  showForm,
  submitSeedsForm,
  submitCustomRiderForm,
  submitRiderDimensionsForm,
  renderBikeById,
  downloadBikeById,
};
