import { submitRiderDimensionsForm } from "../../declarative/client";
import BikeSelectionForm from "../BikeSelectionForm";
import { SubmitDropdown } from "./SubmitDropdown";

function FloatInputDiv(props: {
  name: string;
  labelText: string;
  inputId: string;
  initialValue: number;
}) {
  return (
    <div className="col-3">
      <input
        type="number"
        className="form-control"
        name={props.name}
        id={props.inputId}
        step={0.01}
        value={props.initialValue}
        placeholder={props.initialValue.toString()}
        required
      />
      <label className="form-label" htmlFor={props.inputId}>
        {props.labelText}
      </label>
    </div>
  );
}

export function SpecifyRiderDimensionsForm() {
  return (
    <form id="specify-rider-dimensions-form">
      <div id="specify-rider-dimensions-container" className="m-3">
        <h3>
          Specify rider dimensions
          <span style={{ fontSize: "small" }}>(Inches)</span>
        </h3>
        <div className="p-3">
          <div className="row flex-cont">
            <FloatInputDiv
              name="rider-height"
              inputId="user-height-input-specify-rider-dimensions"
              initialValue={73.5}
              labelText="Height"
            />
            <FloatInputDiv
              name="shoulder-height"
              inputId="shoulder-height-input"
              initialValue={60}
              labelText="Shoulder Height"
            />
          </div>
          <div className="row flex-cont">
            <FloatInputDiv
              name="hip-ankle"
              inputId="hip-ankle-input-specify-rider-dimensions"
              initialValue={34}
              labelText="Hip to Ankle"
            />
            <FloatInputDiv
              name="hip-knee"
              inputId="hip-knee-input-specify-rider-dimensions"
              initialValue={16.5}
              labelText="Hip to Knee"
            />
          </div>
          <div className="row flex-cont">
            <FloatInputDiv
              name="shoulder-wrist"
              inputId="shoulder-wrist-input-specify-rider-dimensions"
              initialValue={20.5}
              labelText="Shoulder to wrist"
            />
            <FloatInputDiv
              name="arm-length"
              inputId="arm-length-input-specify-rider-dimensions"
              initialValue={23.5}
              labelText="Arm Length"
            />
          </div>
          <div className="row flex-cont">
            <FloatInputDiv
              name="upper-leg"
              inputId="upper-leg-input-specify-rider-dimensions"
              initialValue={16.5}
              labelText="Upper Leg"
            />
            <FloatInputDiv
              name="lower-leg"
              inputId="lower-leg-input-specify-rider-dimensions"
              initialValue={20.25}
              labelText="Lower Leg"
            />
          </div>
          <div className="row flex-cont">
            <div className="col-3" style={{ width: "50%" }}>
              <input
                type="number"
                className="form-control"
                name="torso-length"
                id="torso-length-input-specify-rider-dimensions"
                step="0.01"
                placeholder="23"
                value="23"
                required
              />
              <label
                className="form-label"
                htmlFor="torso-length-input-specify-rider-dimensions"
              >
                Torso Length
              </label>
            </div>
          </div>
        </div>
      </div>
      <div id="specify-rider-dimensions-form-seed-bike-placeholder">
        <BikeSelectionForm idSuffix="specify-rider-dimensions-form" />
      </div>
      <SubmitDropdown
        id="1-specify-rider-dimensions"
        typedSubmissionFunction={submitRiderDimensionsForm}
      />
    </form>
  );
}
