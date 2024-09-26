import {
  OptimizationController,
  RenderingController,
  GeneratedBike,
  TextPromptOptimizationRequest,
} from "./controller";

import { apiRoot } from "./config";
import { getElementById } from "./html_utils";
import { ExclusivelyVisibleElements } from "./exclusively_visible_elements";
import { readFile } from "./html_utils";
import { downloadAsTextFile } from "./html_utils";
import {
  getDownloadBikeCadBtnId,
  getBikeImgId,
  getBikeImagesDivId,
  getRenderBikeBtnId,
} from "./bike_element_id";
import {
  GENERATE_FROM_TEXT_PROMPT_ID,
  SEEDS_FORM_ID,
  UPLOAD_RIDER_IMAGE_FORM_ID,
  SPECIFY_DIMENSIONS_FORM_ID,
  TEXT_PROMPT_FORM_ID,
  RESPONSE_DIV_ID,
} from "./html_element_constant_ids";
import {
  RESPONSE_RECEIVED_DIV,
  NO_BIKES_FOUND_DIV,
  RESPONSE_LOADING_DIV,
  ERROR_RESPONSE_DIV,
} from "./html_element_constant_ids";
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

const STANDARD_BIKE_INDEX = "10";

const resultDivElements = new ExclusivelyVisibleElements([
  RESPONSE_RECEIVED_DIV,
  NO_BIKES_FOUND_DIV,
  RESPONSE_LOADING_DIV,
  ERROR_RESPONSE_DIV,
]);

const problemFormElements = new ExclusivelyVisibleElements([
  SEEDS_FORM_ID,
  UPLOAD_RIDER_IMAGE_FORM_ID,
  SPECIFY_DIMENSIONS_FORM_ID,
  GENERATE_FROM_TEXT_PROMPT_ID,
]);

abstract class GenericBikeOptimizationSubmitter {
  submitForm(optimizationType: string): void {
    this.resetBikeStore();
    this.throwIfInvalidType(optimizationType);
    const form: HTMLFormElement = getElementById(
      this.formId()
    ) as HTMLFormElement;
    if (form.checkValidity()) {
      this.showResponseDiv();
      this.submitValidForm(form, optimizationType);
    } else {
      this.showFormErrors(form);
    }
  }

  abstract submitValidForm(
    form: HTMLFormElement,
    optimizationType: string
  ): void;
  abstract formId(): string;

  downloadBike(
    bikeId: string,
    downloadFunction: (bike: GeneratedBike) => Promise<Response>
  ) {
    const downloadButton = getElementById(
      getDownloadBikeCadBtnId(bikeId)
    ) as HTMLButtonElement;

    downloadButton.innerHTML = "Downloading bike...";

    downloadFunction(bikeStore.get(bikeId)!)
      .then((response) => {
        if (response.status === 200) {
          response.text().then((responseText) => {
            downloadAsTextFile(responseText, "bike.bcad");
            this.toPressedDownloadButton(
              downloadButton,
              "Downloaded successfully"
            );
          });
        } else {
          this.toPressedDownloadButton(downloadButton, "Download failed");
        }
      })
      .catch(() => {
        this.toPressedDownloadButton(downloadButton, "Download failed");
      });
  }

  toPressedDownloadButton(
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

  renderBikeById(bikeId: string) {
    this.renderBike(bikeId, (bike: GeneratedBike) =>
      renderingController.postRenderBikeRequest(bike)
    );
  }

  downloadBikeById(bikeId: string) {
    this.downloadBike(bikeId, (bike: GeneratedBike) =>
      optimizationController.postDownloadBikeCadRequest(bike)
    );
  }

  renderClipsBike(bikeId: string) {
    this.renderBike(bikeId, (bike: GeneratedBike) =>
      renderingController.postRenderClipsBikeRequest(bike)
    );
  }
  downloadClipsBike(bikeId: string) {
    this.downloadBike(bikeId, (bike: GeneratedBike) =>
      optimizationController.postDownloadClipsBikeCadRequest(bike)
    );
  }

  renderBike(
    bikeId: string,
    renderingCall: (bike: GeneratedBike) => Promise<Response>
  ) {
    this.hideRenderButton(bikeId);
    this.setBikeLoading(bikeId, "flex");
    renderingCall(bikeStore.get(bikeId)!)
      .then((response) => {
        if (response.status === 200) {
          this.handleSuccessfulRenderResponse(response, bikeId);
        } else {
          this.showRenderError(bikeId);
        }
      })
      .catch((error) => {
        console.log(error);
        this.showRenderError(bikeId);
      })
      .finally(() => this.setBikeLoading(bikeId, "none"));
  }

  showRenderError(bikeId: string) {
    getElementById(renderingFailedElementId(bikeId)).setAttribute(
      "style",
      "display: flex"
    );
  }

  handleSuccessfulRenderResponse(response: Response, bikeId: string) {
    response.blob().then((responseBlob) => {
      this.handleRenderedBikeImage(bikeId, responseBlob);
    });
  }

  setBikeLoading(bikeId: string, display: string): void {
    document
      .getElementById(bikeLoadingId(bikeId))!
      .setAttribute("style", `display: ${display}`);
  }

  handleRenderedBikeImage(bikeId: string, responseBlob: Blob) {
    const outputImg = getElementById(getBikeImgId(bikeId)) as HTMLImageElement;
    outputImg.src = urlCreator.createObjectURL(responseBlob);
    getElementById(getBikeImagesDivId(bikeId)).setAttribute(
      "style",
      "display: flex"
    );
  }

  submitTextPromptForm(): void {
    this.resetBikeStore();
    const form: HTMLFormElement = getElementById(
      TEXT_PROMPT_FORM_ID
    ) as HTMLFormElement;
    if (form.checkValidity()) {
      this.showResponseDiv();
      this.submitValidTextPromptForm(form);
    } else {
      this.showFormErrors(form);
    }
  }

  resetBikeStore() {
    bikeStore = new Map();
  }

  showResponseDiv() {
    const responseDiv = getElementById(RESPONSE_DIV_ID);
    this.setLoading();
    responseDiv.setAttribute("style", "display: block;");
    responseDiv.scrollIntoView();
  }

  showFormErrors(form: HTMLFormElement) {
    form.reportValidity();
  }

  submitValidTextPromptForm(form: HTMLFormElement) {
    const formData = new FormData(form);
    const request = new TextPromptOptimizationRequest();

    function getOrDefault<T>(label: string, parser: (string: string) => T) {
      const value = formData.get(label) as string;
      return value === undefined || value === null ? null : parser(value);
    }

    request.text_prompt = formData.get("bike-description") as string;
    request.optimizer_population = getOrDefault(
      "optimizer_population",
      Number.parseInt
    )!;
    request.optimizer_generations = getOrDefault(
      "optimizer_generations",
      Number.parseInt
    )!;
    request.avg_gower_weight = getOrDefault(
      "avg_gower_weight",
      Number.parseFloat
    )!;
    request.bonus_objective_weight = getOrDefault(
      "bonus_objective_weight",
      Number.parseFloat
    )!;
    request.cfc_weight = getOrDefault("cfc_weight", Number.parseFloat)!;
    request.cosine_distance_upper_bound = getOrDefault(
      "cosine_distance_upper_bound",
      Number.parseFloat
    )!;
    request.diversity_weight = getOrDefault(
      "diversity_weight",
      Number.parseFloat
    )!;
    request.gower_weight = getOrDefault("gower_weight", Number.parseFloat)!;
    request.include_dataset = getOrDefault(
      "include_dataset",
      (val) => "true" === val.toLowerCase()
    )!;

    this.postOptimizationForm(
      STANDARD_BIKE_INDEX,
      optimizationController.postTextPromptOptimization(request),
      "submitter.renderClipsBike",
      "submitter.downloadClipsBike"
    );
  }

  postCustomRiderOptimizationForm(
    optimizationType: string,
    formData: FormData,
    base64File: string
  ) {
    this.postOptimizationForm(
      this.getSeedBikeId(formData),
      optimizationController.postImageOptimization(
        optimizationType,
        formData.get("seedBike") as string,
        base64File,
        Number(formData.get("user-height") as string)
      )
    );
  }

  postOptimizationForm(
    seedBikeId: string,
    responsePromise: Promise<Response>,
    renderingFunction = "submitter.renderBikeById",
    downloadFunction = "submitter.downloadBikeById"
  ) {
    responsePromise
      .then((response) => {
        this.handleOptimizationResponse(
          response,
          seedBikeId,
          renderingFunction,
          downloadFunction
        );
      })
      .catch((exception) => {
        this.showGenericError();
      });
  }

  getSeedBikeId(formData: FormData): string {
    return formData.get("seedBike") as string;
  }

  handleOptimizationResponse(
    response: Response,
    seedBikeId: string,
    renderingFunction: string,
    downloadFunction: string
  ) {
    if (response.status === 200) {
      this.handleSuccessfulOptimizationResponse(
        response,
        seedBikeId,
        renderingFunction,
        downloadFunction
      );
    } else {
      this.handleFailedResponse(response);
    }
  }

  handleSuccessfulOptimizationResponse(
    response: Response,
    seedBikeId: string,
    renderingFunction: string,
    downloadFunction: string
  ) {
    response.text().then((responseText) => {
      const responseJson: {
        bikes: Array<{ bike: GeneratedBike; bikePerformance: string }>;
      } = JSON.parse(responseText);
      if (responseJson["bikes"].length === 0) {
        resultDivElements.showElement(NO_BIKES_FOUND_DIV);
      } else {
        this.showGeneratedBikes(
          responseJson,
          seedBikeId,
          renderingFunction,
          downloadFunction
        );
        this.renderFirstBike();
      }
    });
  }

  renderFirstBike() {
    const firstBikeId = bikeStore.keys().next().value;
    (
      getElementById(getRenderBikeBtnId(firstBikeId)) as HTMLButtonElement
    ).click();
  }

  showGeneratedBikes(
    responseJson: {
      bikes: Array<{ bike: GeneratedBike; bikePerformance: string }>;
    },
    seedBikeId: string,
    renderingFunction: string,
    downloadFunction: string
  ) {
    resultDivElements.showElement(RESPONSE_RECEIVED_DIV);
    getElementById(GENERATED_DESIGNS_CONSUMER_CAROUSEL).innerHTML =
      this.persistAndBuildCarouselItems(
        responseJson["bikes"],
        seedBikeId,
        renderingFunction,
        downloadFunction
      ).innerHTML;
  }

  setLoading() {
    resultDivElements.showElement(RESPONSE_LOADING_DIV);
  }

  arrayBufferToBase64(arrayBuffer: ArrayBuffer) {
    let binary = "";
    const bytes = new Uint8Array(arrayBuffer);
    for (let i = 0; i < bytes.byteLength; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
  }

  persistAndBuildCarouselItems(
    bikes: Array<{ bike: GeneratedBike; bikePerformance: string }>,
    seedBikeId: string,
    renderingFunction: string,
    downloadFunction: string
  ): HTMLDivElement {
    const bikesHtml = document.createElement("div");
    for (let index = 0; index < bikes.length; index++) {
      const bikeId = this.persistBike(bikes[index], seedBikeId);
      const bikeItem = this.bikeToCarouselItem(
        index,
        bikeId,
        bikes[index],
        bikes.length,
        renderingFunction,
        downloadFunction
      );
      this.activateFirst(index, bikeItem);
      bikesHtml.appendChild(bikeItem);
    }
    return bikesHtml;
  }

  activateFirst(index: number, bikeItem: HTMLDivElement) {
    if (index === 0) {
      bikeItem.setAttribute(
        "class",
        bikeItem.getAttribute("class") + " active"
      );
    }
  }

  bikeToCarouselItem(
    index: number,
    bikeId: string,
    bike: { bikePerformance: string },
    totalBikes: number,
    renderingFunction: string,
    downloadFunction: string
  ) {
    const optimizedBikeDiv = document.createElement("div");
    optimizedBikeDiv.setAttribute(
      "class",
      "container text-center border rounded carousel-item mb-1 p-5 optimized-bike-div"
    );
    optimizedBikeDiv.appendChild(
      this.generateBikeDescription(index, bike, totalBikes)
    );
    optimizedBikeDiv.appendChild(
      this.generatePerformanceElement(bike["bikePerformance"])
    );
    optimizedBikeDiv.appendChild(document.createElement("br"));
    optimizedBikeDiv.appendChild(this.createBikeLoadingElement(bikeId));
    optimizedBikeDiv.appendChild(this.createRenderingFailedElement(bikeId));
    optimizedBikeDiv.appendChild(
      this.generateRenderButton(bikeId, renderingFunction)
    );
    optimizedBikeDiv.appendChild(this.generateRenderedImgElement(bikeId));
    optimizedBikeDiv.appendChild(createSpaceDiv());
    optimizedBikeDiv.appendChild(
      this.generateDownloadCadButton(bikeId, downloadFunction)
    );
    return optimizedBikeDiv;
  }

  generateBikeDescription(
    index: number,
    bike: object,
    totalBikes: number
  ): HTMLElement {
    const element = document.createElement("h4");
    element.textContent = `Generated Bike ${index + 1}/${totalBikes}`;
    return element;
  }

  generateRenderedImgElement(bikeId: string): HTMLDivElement {
    const imagesDiv = document.createElement("div");
    const renderedImgDiv = this.createResultImgDiv();
    const originalImgDiv = this.createResultImgDiv();

    imagesDiv.setAttribute("class", "text-center p-5 row");
    imagesDiv.setAttribute("id", getBikeImagesDivId(bikeId));
    imagesDiv.setAttribute("style", "display: none");
    const renderedImg = document.createElement("img");

    const originalImg = document.createElement("img");
    originalImg.src = `../mcd/assets/bike${
      bikeStore.get(bikeId)!.seedImageId
    }.png`;
    originalImg.setAttribute("class", "original-bike-img-in-result");
    originalImg.setAttribute("id", getOriginalImageInResultId(bikeId));

    renderedImg.setAttribute("class", "rendered-bike-img");
    renderedImg.setAttribute("id", getBikeImgId(bikeId));
    renderedImg.setAttribute("alt", "rendered bike image");

    renderedImgDiv.appendChild(renderedImg);
    renderedImgDiv.appendChild(
      this.getImageLabel("Generated", getBikeImgId(bikeId))
    );

    originalImgDiv.appendChild(originalImg);
    originalImgDiv.appendChild(
      this.getImageLabel("Original", getOriginalImageInResultId(bikeId))
    );

    imagesDiv.appendChild(originalImgDiv);
    imagesDiv.appendChild(renderedImgDiv);
    return imagesDiv;
  }

  getImageLabel(textContent: string, htmlFor: string) {
    const label = document.createElement("label");
    label.textContent = textContent;
    label.htmlFor = htmlFor;
    label.setAttribute("style", "display: block");
    return label;
  }

  createResultImgDiv() {
    const renderedImgDiv = document.createElement("div");
    renderedImgDiv.setAttribute("class", "col bike-img-div-in-result");
    return renderedImgDiv;
  }

  generateRenderButton(bikeId: string, renderingFunction: string): HTMLElement {
    return this.generateBikeActionButton(
      bikeId,
      getRenderBikeBtnId,
      "Render bike",
      renderingFunction
    );
  }

  showForm(formId: string) {
    problemFormElements.showElement(formId);
  }

  generateDownloadCadButton(
    bikeId: string,
    downloadFunction: string
  ): HTMLElement {
    return this.generateBikeActionButton(
      bikeId,
      getDownloadBikeCadBtnId,
      "Download CAD",
      downloadFunction
    );
  }

  generateBikeActionButton(
    bikeId: string,
    idGenerator: CallableFunction,
    textContent: string,
    onClickFunction: string
  ): HTMLElement {
    const buttonCssClasses = "btn btn-outline-danger btn-lg";
    const button = document.createElement("button");
    button.setAttribute("class", buttonCssClasses);
    button.setAttribute("id", idGenerator(bikeId));
    button.textContent = textContent;
    button.setAttribute("onclick", `${onClickFunction}("${bikeId}")`);
    return button;
  }

  persistBike(
    bike: { bike: GeneratedBike; bikePerformance: string },
    seedBikeId: string
  ): string {
    const bikeId = generateUuid();
    const generatedBike = new GeneratedBike();
    generatedBike.bikeObject = bike["bike"];
    generatedBike.bikePerformance = bike["bikePerformance"];
    generatedBike.seedImageId = seedBikeId;
    bikeStore.set(bikeId, generatedBike);
    return bikeId;
  }

  hideRenderButton(bikeId: string) {
    const buttonElement = getElementById(getRenderBikeBtnId(bikeId));
    buttonElement?.setAttribute("style", "display: none");
  }

  handleFailedResponse(response: Response) {
    response.text().then((responseText) => {
      try {
        this.handleJsonFailedResponse(responseText);
      } catch {
        this.showGenericError();
      }
    });
  }

  showGenericError() {
    const errorResponseDiv = getElementById(ERROR_RESPONSE_DIV);
    errorResponseDiv.innerHTML = "";

    resultDivElements.showElement(ERROR_RESPONSE_DIV);

    const errorHeader = document.createElement("h3");
    errorHeader.textContent = "Something went wrong.";

    errorResponseDiv.appendChild(errorHeader);
  }

  handleJsonFailedResponse(responseText: string) {
    const errorResponse = JSON.parse(responseText);
    resultDivElements.showElement(ERROR_RESPONSE_DIV);
    getElementById(
      ERROR_RESPONSE_DIV
    ).innerHTML = `<h3> Operation failed. Server responded with: ${errorResponse["message"]} </h3>`;
  }

  createBikeLoadingElement(bikeId: string): HTMLDivElement {
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

  createRenderingFailedElement(bikeId: string): HTMLElement {
    const div = document.createElement("div");
    div.setAttribute("class", "bike-render-inner-element-div");
    div.setAttribute("id", renderingFailedElementId(bikeId));
    div.setAttribute("style", "display: none");
    div.innerHTML = "<h4> Rendering failed... </h4>";
    return div;
  }

  generatePerformanceElement(bikePerformance: string): HTMLElement {
    const div = document.createElement("h5");
    div.textContent = JSON.stringify(bikePerformance)
      .replace('"', "")
      .replace('"', "");
    return div;
  }

  throwIfInvalidType(optimizationType: string) {
    if (!["aerodynamics", "ergonomics"].includes(optimizationType)) {
      throw Error(`Invalid optimization type ${optimizationType}`);
    }
  }
}

class BikeOptimizationSubmitter extends GenericBikeOptimizationSubmitter {
  submitValidForm(form: HTMLFormElement, optimizationType: string) {
    throw new Error("Method not implemented.");
  }
  formId(): string {
    throw new Error("Method not implemented.");
  }
  submitForm(optimizationType: string): void {
    throw new Error("Method not implemented.");
  }
}

class SeedsSubmitter extends GenericBikeOptimizationSubmitter {
  submitValidSeedsForm(optimizationType: string, form: HTMLFormElement) {
    const formData = new FormData(form);
    this.postOptimizationForm(
      this.getSeedBikeId(formData),
      optimizationController.postSeedsOptimization(
        optimizationType,
        formData.get("seedBike") as string,
        formData.get("riderImage") as string
      )
    );
  }
  submitValidForm(form: HTMLFormElement, optimizationType: string) {
    this.submitValidSeedsForm(optimizationType, form);
  }
  formId(): string {
    return SEEDS_FORM_ID;
  }
}

class CustomerRidersSubmitter extends GenericBikeOptimizationSubmitter {
  submitValidCustomRiderForm(optimizationType: string, form: HTMLFormElement) {
    readFile(USER_IMAGE_UPLOAD, (reader) => {
      const base64File: string = this.arrayBufferToBase64(
        reader.result as ArrayBuffer
      );
      const formData: FormData = new FormData(form);
      this.postCustomRiderOptimizationForm(
        optimizationType,
        formData,
        base64File
      );
    });
  }
  submitValidForm(form: HTMLFormElement, optimizationType: string) {
    this.submitValidCustomRiderForm(optimizationType, form);
  }
  formId(): string {
    return UPLOAD_RIDER_IMAGE_FORM_ID;
  }
}
class DimensionsSubmitter extends GenericBikeOptimizationSubmitter {
  submitValidDimensionsForm(optimizationType: string, form: HTMLFormElement) {
    const formData = new FormData(form);
    this.postOptimizationForm(
      this.getSeedBikeId(formData),
      optimizationController.postDimensionsOptimization(
        optimizationType,
        dimensionsFormToDimensionsRequest(formData)
      )
    );
  }
  submitValidForm(form: HTMLFormElement, optimizationType: string) {
    this.submitValidDimensionsForm(optimizationType, form);
  }
  formId(): string {
    return SPECIFY_DIMENSIONS_FORM_ID;
  }
}

const submitter = new BikeOptimizationSubmitter();
const seedsSubmitter = new SeedsSubmitter();
const customerRidersSubmitter = new CustomerRidersSubmitter();
const dimensionsSubmitter = new DimensionsSubmitter();

function showForm(arg1: string) {
  submitter.showForm(arg1);
}

function submitSeedsForm(arg1: string) {
  seedsSubmitter.submitForm(arg1);
}

function submitTextPromptForm() {
  submitter.submitTextPromptForm();
}

function submitCustomRiderForm(arg1: string) {
  customerRidersSubmitter.submitForm(arg1);
}

function submitRiderDimensionsForm(arg1: string) {
  dimensionsSubmitter.submitForm(arg1);
}

function renderBikeById(arg1: string) {
  submitter.renderBikeById(arg1);
}

function downloadBikeById(arg1: string) {
  submitter.downloadBikeById(arg1);
}

document.addEventListener("DOMContentLoaded", () => {
  showForm("seeds-form-form");
});

export {
  submitter,
  showForm,
  submitSeedsForm,
  submitTextPromptForm,
  submitCustomRiderForm,
  submitRiderDimensionsForm,
  renderBikeById,
  downloadBikeById,
};
