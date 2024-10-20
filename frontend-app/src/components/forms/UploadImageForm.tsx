import { optimizationController } from "../../declarative/client";
import { readFile } from "../../declarative/html_utils";
import { UPLOAD_RIDER_IMAGE_FORM_ID, USER_IMAGE_UPLOAD } from "../../html_element_constant_ids";
import BikeSelectionForm from "../BikeSelectionForm";
import { SEED_BIKE_DATA_NAME } from "../constants";
import { McdServerRequest, OptimizationRequestState } from "../McdServerResponse";
import { handleResponse } from "./FormUtils";
import { SubmitDropdown } from "./SubmitDropdown";

function UserHeightInputDiv() {
  return (
    <div className="row flex-cont">
      <div className="col-6">
        <input type="number" className="form-control" name="user-height" id="user-height-input" step="0.01" required />
        <label className="form-label" htmlFor="user-height-input">
          User Height (Inches)
        </label>
      </div>
    </div>
  );
}

function arrayBufferToBase64(arrayBuffer: ArrayBuffer) {
  let binary = "";
  const bytes = new Uint8Array(arrayBuffer);
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

function optimizeImage(
  setServerResponse: (mcdServerResponse: OptimizationRequestState) => void,
  postRequest: (seedBikeId: string, base64File: string, personHeight: number) => Promise<Response>
) {
  const formData = new FormData(document.getElementById(UPLOAD_RIDER_IMAGE_FORM_ID) as HTMLFormElement);
  const bikeId = formData.get(SEED_BIKE_DATA_NAME) as string;
  const userHeight = Number.parseFloat(formData.get("user-height") as string);

  readFile(USER_IMAGE_UPLOAD, (reader) => {
    const base64File: string = arrayBufferToBase64(reader.result as ArrayBuffer);

    const mcdRequest = new McdServerRequest(bikeId);
    setServerResponse(OptimizationRequestState.started(mcdRequest));

    const response = postRequest(bikeId, base64File, userHeight);
    handleResponse(response, setServerResponse, mcdRequest);
  });
}

function UploadImageInputDiv() {
  return (
    <div className="row flex-cont">
      <div className="col-6">
        <input
          className="form-control"
          type="file"
          accept=".jpg, .jpeg, .png, .svg"
          id={USER_IMAGE_UPLOAD}
          name="user-img"
          required
        />
      </div>
    </div>
  );
}

export function UploadImageForm(props: { setServerResponse: (mcdServerResponse: OptimizationRequestState) => void }) {
  return (
    <form id={UPLOAD_RIDER_IMAGE_FORM_ID}>
      <div id="upload-image-container" className="m-3">
        <h3>Upload Rider Image</h3>
        <div className="p-3">
          <UploadImageInputDiv />
          <UserHeightInputDiv />
        </div>
      </div>
      <BikeSelectionForm idSuffix={UPLOAD_RIDER_IMAGE_FORM_ID} />
      <SubmitDropdown
        id="1-upload-rider"
        ergonomicOptimizationFunction={() => {
          optimizeImage(props.setServerResponse, (seedBikeId, base64File, personHeight) =>
            optimizationController.postImageOptimization("ergonomics", seedBikeId, base64File, personHeight)
          );
        }}
        aerodynamicOptimizationFunction={() => {
          optimizeImage(props.setServerResponse, (seedBikeId, base64File, personHeight) =>
            optimizationController.postImageOptimization("aerodynamics", seedBikeId, base64File, personHeight)
          );
        }}
      />
    </form>
  );
}
