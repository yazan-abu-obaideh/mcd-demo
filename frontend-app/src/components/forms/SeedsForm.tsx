import { ReactElement } from "react";
import {
  optimizationController,
  submitSeedsForm,
} from "../../declarative/client";

import person1 from "../../assets/person1.png";
import person2 from "../../assets/person2.png";
import person3 from "../../assets/person3.png";
import BikeSelectionForm from "../BikeSelectionForm";
import { SubmitDropdown } from "./SubmitDropdown";
import { SEEDS_FORM_ID } from "../../html_element_constant_ids";
import {
  GENERIC_ERROR,
  McdError,
  McdServerResponse,
  BikesServerResponse,
} from "../McdServerResponse";
import { OptimizationController } from "../../declarative/controller";
import { apiRoot } from "../../declarative/config";
import { SEED_BIKE_DATA_NAME } from "../constants";

const RIDER_DATA_NAME = "riderImage";
const LOADING = new McdServerResponse(true, undefined, undefined);
const GENERIC_ERROR_RESPONSE = new McdServerResponse(
  false,
  GENERIC_ERROR,
  undefined
);

function RiderDiv(props: {
  imageSrc: string;
  inputValue: string;
  labelText: string;
}): ReactElement {
  return (
    <div className="col seed-bike-div">
      <img
        className="seed-bike-img"
        src={props.imageSrc}
        alt={"rider-image-" + props.inputValue}
      />
      <br />
      <input
        id={"rider-image-" + props.inputValue}
        value={props.inputValue}
        name={RIDER_DATA_NAME}
        type="radio"
        className="form-check-input"
        checked
        required
      />
      <label
        className="form-check-label"
        htmlFor={"rider-image-" + props.inputValue}
      >
        {props.labelText}
      </label>
    </div>
  );
}

function stringFromFormData(dataName: string) {
  const formData = new FormData(
    document.getElementById(SEEDS_FORM_ID) as HTMLFormElement
  );
  return formData.get(dataName) as string;
}

function grabSelectedSeed(): string {
  return stringFromFormData(SEED_BIKE_DATA_NAME);
}

function grabSelectedRider(): string {
  return stringFromFormData(RIDER_DATA_NAME);
}

export function SeedsForm(props: {
  setServerResponse: (mcdServerResponse: McdServerResponse) => void;
}) {
  return (
    <form id={SEEDS_FORM_ID}>
      <div id="person-image-container" className="m-3">
        <h3>Select Rider</h3>
        <div className="row p-5">
          <RiderDiv imageSrc={person1} inputValue="1" labelText={`6'2"`} />
          <RiderDiv imageSrc={person2} inputValue="2" labelText={`5'10"`} />
          <RiderDiv imageSrc={person3} inputValue="3" labelText={` 5'1"`} />
        </div>
      </div>
      <BikeSelectionForm idSuffix={SEEDS_FORM_ID} />
      <SubmitDropdown
        id="1"
        ergonomicOptimizationFunction={() => {
          props.setServerResponse(LOADING);
          optimizationController
            .postSeedsOptimization(
              "ergonomics",
              grabSelectedSeed(),
              grabSelectedRider()
            )
            .then((response) => {
              if (response.status !== 200) {
                response.json().then((resJson) => {
                  props.setServerResponse(
                    new McdServerResponse(
                      false,
                      new McdError(resJson["message"]),
                      undefined
                    )
                  );
                });
              } else {
                response.json().then((resJson) => {
                  
                  const optResponse = JSON.parse(
                    resJson
                  ) as BikesServerResponse;
                  props.setServerResponse(
                    new McdServerResponse(false, undefined, optResponse)
                  );
                });
              }
            })
            .catch(() => {
              props.setServerResponse(GENERIC_ERROR_RESPONSE);
            });
        }}
        aerodynamicOptimizationFunction={() => {}}
      />
    </form>
  );
}
