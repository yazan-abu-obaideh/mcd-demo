import { PropsWithChildren, ReactElement } from "react";
import { optimizationController } from "../../declarative/controller";
import BikeSelectionForm from "../BikeSelectionForm";
import { SubmitDropdown } from "./SubmitDropdown";
import { SPECIFY_DIMENSIONS_FORM_ID } from "../../html_element_constant_ids";
import { McdServerRequest, OptimizationRequestState } from "../McdServerResponse";
import { callIfValidForm, handleResponse } from "./FormUtils";
import { FrontendDimensionsOptimizationRequest } from "../../declarative/controller";
import { SEED_BIKE_DATA_NAME } from "../constants";

function FloatInputDiv(props: { name: string; labelText: string; inputId: string; initialValue: number }) {
  return (
    <div className="col-3">
      <input
        type="number"
        className="form-control"
        name={props.name}
        id={props.inputId}
        step={0.01}
        placeholder={props.initialValue.toString()}
        defaultValue={props.initialValue}
        required
      />
      <label className="form-label" htmlFor={props.inputId}>
        {props.labelText}
      </label>
    </div>
  );
}

function Row(props: PropsWithChildren): ReactElement {
  return <div className="row flex-cont"> {props.children} </div>;
}

function buildFromFormData(formData: FormData): FrontendDimensionsOptimizationRequest {
  function parseFloat(fieldName: string): number {
    return Number.parseFloat(formData.get(fieldName) as string);
  }

  const dimensionsRequest = new FrontendDimensionsOptimizationRequest();

  dimensionsRequest.arm_length = parseFloat("arm-length");
  dimensionsRequest.height = parseFloat("rider-height");
  dimensionsRequest.sh_height = parseFloat("shoulder-height");
  dimensionsRequest.hip_to_ankle = parseFloat("hip-ankle");
  dimensionsRequest.hip_to_knee = parseFloat("hip-knee");
  dimensionsRequest.shoulder_to_wrist = parseFloat("shoulder-wrist");
  dimensionsRequest.upper_leg = parseFloat("upper-leg");
  dimensionsRequest.lower_leg = parseFloat("lower-leg");
  dimensionsRequest.torso_length = parseFloat("torso-length");

  return dimensionsRequest;
}

function optimizeDimensions(
  setServerResponse: (mcdServerResponse: OptimizationRequestState) => void,
  postRequest: (dimensionsRequest: FrontendDimensionsOptimizationRequest) => Promise<Response>
) {
  const formData = new FormData(document.getElementById(SPECIFY_DIMENSIONS_FORM_ID) as HTMLFormElement);
  const bikeId = formData.get(SEED_BIKE_DATA_NAME) as string;

  const dimensionsRequest = buildFromFormData(formData);
  dimensionsRequest.seedBikeId = bikeId;

  const mcdRequest = new McdServerRequest(bikeId);
  setServerResponse(OptimizationRequestState.started(mcdRequest));

  const response = postRequest(dimensionsRequest);
  handleResponse(response, setServerResponse, mcdRequest);
}

function buildOnClickFunction(
  setServerResponse: (mcdServerResponse: OptimizationRequestState) => void,
  optimizationType: "aerodynamics" | "ergonomics"
): () => void {
  return () => {
    callIfValidForm(SPECIFY_DIMENSIONS_FORM_ID, () => {
      optimizeDimensions(setServerResponse, (dimensionsRequest) =>
        optimizationController.postDimensionsOptimization(optimizationType, dimensionsRequest)
      );
    });
  };
}

export function SpecifyRiderDimensionsForm(props: {
  setServerResponse: (mcdServerResponse: OptimizationRequestState) => void;
}) {
  return (
    <form id={SPECIFY_DIMENSIONS_FORM_ID}>
      <div id="specify-rider-dimensions-container" className="m-3">
        <h3>
          Specify rider dimensions
          <span style={{ fontSize: "small" }}>(Inches)</span>
        </h3>
        <div className="p-3">
          <Row>
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
          </Row>
          <Row>
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
          </Row>
          <Row>
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
          </Row>
          <Row>
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
          </Row>
          <Row>
            <div className="col-3" style={{ width: "50%" }}>
              <input
                type="number"
                className="form-control"
                name="torso-length"
                id="torso-length-input-specify-rider-dimensions"
                step="0.01"
                placeholder="23"
                defaultValue={23}
                required
              />
              <label className="form-label" htmlFor="torso-length-input-specify-rider-dimensions">
                Torso Length
              </label>
            </div>
          </Row>
        </div>
      </div>
      <BikeSelectionForm idSuffix={SPECIFY_DIMENSIONS_FORM_ID} />
      <SubmitDropdown
        id="1"
        ergonomicOptimizationFunction={buildOnClickFunction(props.setServerResponse, "ergonomics")}
        aerodynamicOptimizationFunction={buildOnClickFunction(props.setServerResponse, "aerodynamics")}
      />
    </form>
  );
}
