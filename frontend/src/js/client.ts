const apiUrl = "http://localhost:5000/api/v1";
const bikeStore = {};
const problemFormId = "problem-form-form";
const responseDivId = "server-response-div";
const urlCreator = window.URL || window.webkitURL;

async function getServerHealth(): Promise<Response> {
  return await fetch(apiUrl.concat("/health"), {
    headers: { "Content-Type": "application/json" },
    method: "GET",
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

function postRenderBikeRequest(bike: object): Promise<Response> {
  return fetch(apiUrl.concat("/render-bike-object"), {
    headers: { "Content-Type": "application/json" },
    method: "POST",
    body: JSON.stringify({
      bike: bike,
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
  const outputImg = document.getElementById(
    getBikeImgId(bikeId)
  ) as HTMLImageElement;
  outputImg.src = urlCreator.createObjectURL(responseBlob);
  outputImg.setAttribute("style", "display: inline");
}

function renderBike() {
  postRenderBikeRequest({}).then((response) => {
    response.blob().then((responseBlob) => {
      let outputImg = document.getElementById("bike-img") as HTMLImageElement;
      outputImg.src = urlCreator.createObjectURL(responseBlob);
    });
  });
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
    postSeedBikeOptimization(
      formData.get("seedBike") as string,
      base64File,
      Number(formData.get("user-height") as string),
      Number(formData.get("camera-height") as string)
    )
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
    console.log("Failed!");
  }
}

function handleSuccessfulOptimizationResponse(response: Response) {
  response.text().then((responseText) => {
    const responseJson: object = JSON.parse(responseText);
    setLoading(false);
    document.getElementById("mcd-logs-consumer").innerHTML = logsToHtml(
      responseJson["logs"]
    );
    document.getElementById("generated-designs-consumer").innerHTML =
      bikesToHtml(responseJson["bikes"]);
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

function bikesToHtml(bikes: Array<object>): string {
  let bikesHtml = "";
  bikes.forEach((bike) => {
    const bikeId = persistBike(bike);
    bikesHtml += bikeToHtml(bikeId, bike);
  });
  return bikesHtml;
}

function bikeToHtml(bikeId: string, bike: object) {
  return `
  ${generateBikeDescription(bike)}
  <br>
  ${generateRenderButton(bikeId)}
    <br>
     ${generateRenderedImgElement(bikeId)}
  </div>`;
}

function generateBikeDescription(bike: object): string {
  return `<div class="container text-center border rounded mb-1 p-3"> Crank Length: ${formatNumber(
    bike["crank_length"]
  )} | 
  Handle Bar X: ${formatNumber(
    bike["handle_bar_x"]
  )} Handle Bar Y: ${formatNumber(bike["handle_bar_y"])} 
  Seat X: ${formatNumber(bike["seat_x"])} Seat Y: ${formatNumber(
    bike["seat_y"]
  )}`;
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
  document.getElementById("collapse-logs-div")?.scrollIntoView();
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

function persistBike(bike: object): string {
  const bikeId = generateUuid();
  bikeStore[bikeId] = bike;
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
  const buttonElement = document.getElementById(getBikeBtnId(bikeId));
  buttonElement?.setAttribute("style", "display: none");
}
// export { getServerHealth, postOptimizationRequest, postSeedBikeOptimization };
