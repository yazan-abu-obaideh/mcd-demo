import { ReactElement } from "react";
import { submitTextPromptForm } from "../../declarative/client";
import { GENERATE_FROM_TEXT_PROMPT_ID } from "../../html_element_constant_ids";

const ADVANCED_OPTIONS_ID = "advancedOptions";

function IntegerInputDiv(props: {
  name: string;
  labelText: string;
  min: number;
  max: number;
}) {
  const inputId = props.name + "-input";
  return (
    <div className="col-6">
      <input
        type="number"
        className="form-control"
        name={props.name}
        id={inputId}
        min={props.min}
        max={props.max}
      />
      <label className="form-label" htmlFor={inputId}>
        {props.labelText}
      </label>
    </div>
  );
}
function BoundedFloatInputDiv(props: {
  name: string;
  labelText: string;
  min: number;
  max: number;
}) {
  const inputId = props.name + "-input";
  return (
    <div className="col-6">
      <input
        type="number"
        className="form-control"
        name={props.name}
        id={inputId}
        step={0.01}
        min={props.min}
        max={props.max}
      />
      <label className="form-label" htmlFor={inputId}>
        {props.labelText}
      </label>
    </div>
  );
}

function FloatInputDiv(props: { name: string; labelText: string }) {
  return (
    <BoundedFloatInputDiv
      name={props.name}
      labelText={props.labelText}
      min={Number.NEGATIVE_INFINITY}
      max={Number.POSITIVE_INFINITY}
    />
  );
}

function AdvancedOptions() {
  return (
    <div className="collapse p-3" id={ADVANCED_OPTIONS_ID}>
      <div className="row flex-cont">
        <IntegerInputDiv
          name="optimizer_population"
          min={1}
          max={100}
          labelText="Bikes per generation"
        />
        <IntegerInputDiv
          name="optimizer_generations"
          min={1}
          max={60}
          labelText="Number of generations"
        />
      </div>
      <div className="row flex-cont">
        <BoundedFloatInputDiv
          name="cosine_distance_upper_bound"
          labelText="Cosine distance upper bound"
          min={0.1}
          max={1}
        />
        <FloatInputDiv
          name="avg_gower_weight"
          labelText="Average gower weight"
        />
      </div>
      <div className="row flex-cont">
        <FloatInputDiv name="cfc_weight" labelText="Counterfactual weight" />
        <FloatInputDiv name="gower_weight" labelText="Gower weight" />
      </div>
      <div className="row flex-cont">
        <FloatInputDiv name="diversity_weight" labelText="Diversity weight" />
        <FloatInputDiv
          name="bonus_objective_weight"
          labelText="Bonus objective weight"
        />
      </div>
      <div className="row flex-cont">
        <div className="col-6">
          <input
            type="checkbox"
            name="include_dataset"
            id="include_dataset-input"
          />
          <label className="form-label" htmlFor="include_dataset-input">
            Include dataset
          </label>
        </div>
      </div>
    </div>
  );
}

function GenerateButton() {
  return (
    <button
      className="btn btn-outline-danger btn-lg w-40"
      type="button"
      // "generate-from-text-form-submit-button"
      id={GENERATE_FROM_TEXT_PROMPT_ID.concat("-submit-button")}
      onClick={() => submitTextPromptForm()}
    >
      Generate!
    </button>
  );
}

function ShowAdvancedOptionsButton() {
  return (
    <button
      className="btn btn-outline-danger"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target={`#`.concat(ADVANCED_OPTIONS_ID)}
      aria-expanded="false"
      aria-controls={ADVANCED_OPTIONS_ID}
    >
      Show advanced options
    </button>
  );
}

function BikeDescriptionInput() {
  return (
    <div className="col-6">
      <input
        type="text"
        className="form-control"
        name="bike-description"
        id="bike-description-input"
        required
      />
      <label className="form-label" htmlFor="bike-description-input">
        Bike Description
      </label>
    </div>
  );
}

export function GenerateFromTextForm(): ReactElement {
  return (
    <form id={GENERATE_FROM_TEXT_PROMPT_ID} className="m-3">
      <h3>Generate from Text Prompt</h3>
      <div className="row flex-cont">
        <BikeDescriptionInput />
      </div>
      <ShowAdvancedOptionsButton />
      <AdvancedOptions />
      <div className="row flex-cont"></div>
      <div className="p-3">
        <div className="row flex-cont text-center justify-content-center">
          <GenerateButton />
        </div>
      </div>
    </form>
  );
}
