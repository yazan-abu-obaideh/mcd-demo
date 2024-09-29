import { ReactElement } from "react";
import { submitSeedsForm } from "../../declarative/client";

import person1 from "../../assets/person1.png";
import person2 from "../../assets/person2.png";
import person3 from "../../assets/person3.png";
import BikeSelectionForm from "../BikeSelectionForm";
import { SubmitDropdown } from "./SubmitDropdown";

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
        name="riderImage"
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

export function SeedsForm() {
  return (
    <form id="seeds-form-form">
      <div id="person-image-container" className="m-3">
        <h3>Select Rider</h3>
        <div className="row p-5">
          <RiderDiv imageSrc={person1} inputValue="1" labelText={`6'2"`} />
          <RiderDiv imageSrc={person2} inputValue="2" labelText={`5'10"`} />
          <RiderDiv imageSrc={person3} inputValue="3" labelText={` 5'1"`} />
        </div>
      </div>
      <div id="seeds-form-form-seed-bike-placeholder">
        <BikeSelectionForm idSuffix="seeds-form-form" />
      </div>
      <SubmitDropdown typedSubmissionFunction={submitSeedsForm} id="1" />
    </form>
  );
}
