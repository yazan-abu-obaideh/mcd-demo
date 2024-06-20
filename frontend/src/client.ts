import {
  OptimizationController,
  RenderingController,
  GeneratedBike,
} from "./controller";

import { apiRoot } from "./config";
import { getSeedBikeSelectionHtml } from "./bike_selection_form";
import { getElementById } from "./html_utils";
import { ExclusivelyVisibleElements } from "./exclusively_visible_elements"
import { readFile } from "./html_utils";
import { downloadAsTextFile } from "./html_utils";
import { getDownloadBikeCadBtnId, getBikeImgId, getBikeImagesDivId, getRenderBikeBtnId } from "./bike_element_id";
import { GENERATE_FROM_TEXT_PROMPT_ID, SEEDS_FORM_ID, UPLOAD_RIDER_IMAGE_FORM_ID, SPECIFY_DIMENSIONS_FORM_ID, TEXT_PROMPT_FORM_ID, RESPONSE_DIV_ID, SELECT_SEED_BIKE_PLACEHOLDER_SUFFIX } from "./html_element_constant_ids";
import { RESPONSE_RECEIVED_DIV, NO_BIKES_FOUND_DIV, RESPONSE_LOADING_DIV, ERROR_RESPONSE_DIV } from "./html_element_constant_ids";
import { createSpaceDiv } from "./html_utils";
import { getOriginalImageInResultId } from "./bike_element_id";
import { renderingFailedElementId } from "./bike_element_id";
import { bikeLoadingId } from "./bike_element_id";
import { GENERATED_DESIGNS_CONSUMER_CAROUSEL } from "./html_element_constant_ids";
import { generateUuid } from "./generic_utils";
import { USER_IMAGE_UPLOAD } from "./html_element_constant_ids";
import { dimensionsFormToRiderDimensions as dimensionsFormToDimensionsRequest } from "./forms";


const optimizationApiUrl = apiRoot.concat("/api/v1/optimization");
const renderingApiUrl = apiRoot.concat("/api/v1/rendering");
const optimizationController = new OptimizationController(optimizationApiUrl);
const renderingController = new RenderingController(renderingApiUrl);

let bikeStore: Map<string, GeneratedBike> = new Map();

const urlCreator = window.URL || window.webkitURL;

const resultDivElements = new ExclusivelyVisibleElements([
  RESPONSE_RECEIVED_DIV,
  NO_BIKES_FOUND_DIV,
  RESPONSE_LOADING_DIV,
  ERROR_RESPONSE_DIV,
]);

const problemFormElements = new ExclusivelyVisibleElements([
  GENERATE_FROM_TEXT_PROMPT_ID,
  SEEDS_FORM_ID,
  UPLOAD_RIDER_IMAGE_FORM_ID,
  SPECIFY_DIMENSIONS_FORM_ID,
]);

function downloadBikeById(bikeId: string) {
  const downloadButton = getElementById(
    getDownloadBikeCadBtnId(bikeId)
  ) as HTMLButtonElement;

  downloadButton.innerHTML = "Downloading bike...";

  optimizationController
    .postDownloadBikeCadRequest(bikeStore.get(bikeId))
    .then((response) => {
      if (response.status == 200) {
        response.text().then((responseText) => {
          downloadAsTextFile(responseText, "bike.bcad");
          toPressedDownloadButton(downloadButton, "Downloaded successfully");
        });
      } else {
        toPressedDownloadButton(downloadButton, "Download failed");
      }
    })
    .catch(() => {
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

function renderBikeById(bikeId: string) {
  hideRenderButton(bikeId);
  setBikeLoading(bikeId, "flex");
  renderingController
    .postRenderBikeRequest(bikeStore.get(bikeId))
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
  submitProblemForm(UPLOAD_RIDER_IMAGE_FORM_ID, (form: HTMLFormElement) =>
    submitValidCustomRiderForm(optimizationType, form)
  );
}

function submitTextPromptForm(): void {
  resetBikeStore();
  submitProblemForm(TEXT_PROMPT_FORM_ID, (form: HTMLFormElement) => {
    submitValidTextPromptForm(form)
  })
}

function submitRiderDimensionsForm(optimizationType: string): void {
  resetBikeStore();
  throwIfInvalidType(optimizationType);
  submitProblemForm(SPECIFY_DIMENSIONS_FORM_ID, (form: HTMLFormElement) =>
    submitValidDimensionsForm(optimizationType, form)
  );
}

function submitSeedsForm(optimizationType: string): void {
  resetBikeStore();
  throwIfInvalidType(optimizationType);
  submitProblemForm(SEEDS_FORM_ID, (form: HTMLFormElement) =>
    submitValidSeedsForm(optimizationType, form)
  );
}

function resetBikeStore() {
  bikeStore = new Map();
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
  const responseDiv = getElementById(RESPONSE_DIV_ID);
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
  readFile(USER_IMAGE_UPLOAD, (reader) => {
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
    getSeedBikeId(formData),
    optimizationController.postSeedsOptimization(
      optimizationType,
      formData.get("seedBike") as string,
      formData.get("riderImage") as string
    )
  );
}



function submitValidTextPromptForm(form: HTMLFormElement) {
  const formData = new FormData(form);
  postOptimizationForm(
    getSeedBikeId(formData),
    optimizationController.postTextPromptOptimization(
      formData.get("bike-description") as string
    )
  )
}

function submitValidDimensionsForm(
  optimizationType: string,
  form: HTMLFormElement
) {
  const formData = new FormData(form);
  postOptimizationForm(
    getSeedBikeId(formData),
    optimizationController.postDimensionsOptimization(
      optimizationType,
      dimensionsFormToDimensionsRequest(formData)
    )
  );
}

function postCustomRiderOptimizationForm(
  optimizationType: string,
  formData: FormData,
  base64File: string
) {
  postOptimizationForm(
    getSeedBikeId(formData),
    optimizationController.postImageOptimization(
      optimizationType,
      formData.get("seedBike") as string,
      base64File,
      Number(formData.get("user-height") as string)
    )
  );
}

function postOptimizationForm(
  seedBikeId: string,
  responsePromise: Promise<Response>,
) {
  responsePromise
    .then((response) => {
      handleOptimizationResponse(response, seedBikeId);
    })
    .catch((exception) => {
      showGenericError();
    });
}

function getSeedBikeId(formData: FormData): string {
  return formData.get("seedBike") as string;
}

function handleOptimizationResponse(response: Response, seedBikeId: string) {
  if (response.status == 200) {
    handleSuccessfulOptimizationResponse(response, seedBikeId);
  } else {
    handleFailedResponse(response);
  }
}

function handleSuccessfulOptimizationResponse(
  response: Response,
  seedBikeId: string
) {
  response.text().then((responseText) => {
    const responseJson: object = JSON.parse(responseText);
    if (responseJson["bikes"].length == 0) {
      resultDivElements.showElement(NO_BIKES_FOUND_DIV);
    } else {
      showGeneratedBikes(responseJson, seedBikeId);
      renderFirstBike();
    }
  });
}

function renderFirstBike() {
  const firstBikeId = bikeStore.keys().next().value;
  (
    getElementById(
      getRenderBikeBtnId(firstBikeId)
    ) as HTMLButtonElement
  ).click();
}

function showGeneratedBikes(responseJson: object, seedBikeId: string) {
  resultDivElements.showElement(RESPONSE_RECEIVED_DIV);
  getElementById(GENERATED_DESIGNS_CONSUMER_CAROUSEL).innerHTML =
    persistAndBuildCarouselItems(responseJson["bikes"], seedBikeId).innerHTML;
}

function setLoading() {
  resultDivElements.showElement(RESPONSE_LOADING_DIV);
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
  seedBikeId: string
): HTMLDivElement {
  const bikesHtml = document.createElement("div");
  for (let index = 0; index < bikes.length; index++) {
    const bikeId = persistBike(bikes[index], seedBikeId);
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
  originalImg.src = `../assets/bike${bikeStore.get(bikeId).seedImageId
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

function showForm(formId: string, hasSelectSeedBikeDiv: boolean) {
  problemFormElements.showElement(formId);
  fillInSelectSeedBikePlaceholder(formId);
}

function fillInSelectSeedBikePlaceholder(formId: string) {
  const selectSeedBikeDiv = document.getElementById(formId.concat(SELECT_SEED_BIKE_PLACEHOLDER_SUFFIX));
  if (selectSeedBikeDiv !== null) {
    const notAlreadyCreated = selectSeedBikeDiv.innerHTML.trim() === "";
    if (notAlreadyCreated) {
      selectSeedBikeDiv.innerHTML = getSeedBikeSelectionHtml(formId);
    }
  }
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

function persistBike(bike: object, seedBikeId: string): string {
  const bikeId = generateUuid();
  const generatedBike = new GeneratedBike();
  generatedBike.bikeObject = bike["bike"];
  generatedBike.bikePerformance = bike["bikePerformance"];
  generatedBike.seedImageId = seedBikeId;
  bikeStore.set(bikeId, generatedBike);
  return bikeId;
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

  const errorResponseDiv = getElementById(ERROR_RESPONSE_DIV);
  errorResponseDiv.innerHTML = "";

  resultDivElements.showElement(ERROR_RESPONSE_DIV);

  const errorHeader = document.createElement("h3")
  errorHeader.textContent = "Something went wrong."

  errorResponseDiv.appendChild(errorHeader);
}

function handleJsonFailedResponse(responseText: string) {
  const errorResponse = JSON.parse(responseText);
  resultDivElements.showElement(ERROR_RESPONSE_DIV);
  getElementById(
    ERROR_RESPONSE_DIV
  ).innerHTML = `<h3> Operation failed. Server responded with: ${errorResponse["message"]} </h3>`;
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

function createRenderingFailedElement(bikeId: string): HTMLElement {
  const div = document.createElement("div");
  div.setAttribute("class", "bike-render-inner-element-div");
  div.setAttribute("id", renderingFailedElementId(bikeId));
  div.setAttribute("style", "display: none");
  div.innerHTML = "<h4> Rendering failed... </h4>";
  return div;
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

export {
  showForm,
  submitSeedsForm,
  submitTextPromptForm,
  submitCustomRiderForm,
  submitRiderDimensionsForm,
  renderBikeById,
  downloadBikeById,
};
