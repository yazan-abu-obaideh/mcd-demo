import { submitCustomRiderForm } from "../../declarative/client";
import BikeSelectionForm from "../BikeSelectionForm";
import { SubmitDropdown } from "./SubmitDropdown";

function UserHeightInputDiv() {
  return (
    <div className="row flex-cont">
      <div className="col-6">
        <input
          type="number"
          className="form-control"
          name="user-height"
          id="user-height-input"
          step="0.01"
          required
        />
        <label className="form-label" htmlFor="user-height-input">
          User Height (Inches)
        </label>
      </div>
    </div>
  );
}

function UploadImageInputDiv() {
  return (
    <div className="row flex-cont">
      <div className="col-6">
        <input
          className="form-control"
          type="file"
          accept=".jpg, .jpeg, .png, .svg"
          id="user-img-upload"
          name="user-img"
          required
        />
      </div>
    </div>
  );
}

export function UploadImageForm() {
  return (
    <form id="upload-rider-image-form">
      <div id="upload-image-container" className="m-3">
        <h3>Upload Rider Image</h3>
        <div className="p-3">
          <UploadImageInputDiv />
          <UserHeightInputDiv />
        </div>
      </div>
      <div id="upload-rider-image-form-seed-bike-placeholder">
        <BikeSelectionForm idSuffix="upload-rider-image-form" />
      </div>
      <SubmitDropdown
        id="1-upload-rider"
        typedSubmissionFunction={submitCustomRiderForm}
      />
    </form>
  );
}
