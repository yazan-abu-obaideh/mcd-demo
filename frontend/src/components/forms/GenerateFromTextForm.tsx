import { ReactElement } from "react";
import { optimizationController } from "../../declarative/controller";
import { TEXT_PROMPT_FORM_ID } from "../../html_element_constant_ids";
import { TextPromptOptimizationRequest } from "../../declarative/controller";
import { handleResponse } from "./FormUtils";
import { McdServerRequest, OptimizationRequestState } from "../McdServerResponse";

const ADVANCED_OPTIONS_ID = "advancedOptions";
const STANDARD_BIKE_INDEX = "10";

function IntegerInputDiv(props: { name: string; labelText: string; min: number; max: number }) {
  const inputId = props.name + "-input";
  return (
    <div className="col-6">
      <input type="number" className="form-control" name={props.name} id={inputId} min={props.min} max={props.max} />
      <label className="form-label" htmlFor={inputId}>
        {props.labelText}
      </label>
    </div>
  );
}

function BoundedFloatInputDiv(props: { name: string; labelText: string; min: number; max: number }) {
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
        <IntegerInputDiv name="optimizer_population" min={1} max={100} labelText="Bikes per generation" />
        <IntegerInputDiv name="optimizer_generations" min={1} max={60} labelText="Number of generations" />
      </div>
      <div className="row flex-cont">
        <BoundedFloatInputDiv
          name="cosine_distance_upper_bound"
          labelText="Cosine distance upper bound"
          min={0.1}
          max={1}
        />
        <FloatInputDiv name="avg_gower_weight" labelText="Average gower weight" />
      </div>
      <div className="row flex-cont">
        <FloatInputDiv name="cfc_weight" labelText="Counterfactual weight" />
        <FloatInputDiv name="gower_weight" labelText="Gower weight" />
      </div>
      <div className="row flex-cont">
        <FloatInputDiv name="diversity_weight" labelText="Diversity weight" />
        <FloatInputDiv name="bonus_objective_weight" labelText="Bonus objective weight" />
      </div>
      <div className="row flex-cont">
        <div className="col-6">
          <input type="checkbox" name="include_dataset" id="include_dataset-input" />
          <label className="form-label" htmlFor="include_dataset-input">
            Include dataset
          </label>
        </div>
      </div>
    </div>
  );
}

function GenerateButton(props: { setServerResponse: (mcdServerResponse: OptimizationRequestState) => void }) {
  return (
    <button
      className="btn btn-outline-danger btn-lg w-40"
      type="button"
      id={TEXT_PROMPT_FORM_ID.concat("-submit-button")}
      onClick={() => {
        const formData = new FormData(document.getElementById(TEXT_PROMPT_FORM_ID) as HTMLFormElement);
        const request = new TextPromptOptimizationRequest();

        function getOrDefault<T>(label: string, parser: (string: string) => T) {
          const value = formData.get(label) as string;
          return value === undefined || value === null ? null : parser(value);
        }

        request.text_prompt = formData.get("bike-description") as string;
        request.optimizer_population = getOrDefault("optimizer_population", Number.parseInt);
        request.optimizer_generations = getOrDefault("optimizer_generations", Number.parseInt);
        request.avg_gower_weight = getOrDefault("avg_gower_weight", Number.parseFloat);
        request.bonus_objective_weight = getOrDefault("bonus_objective_weight", Number.parseFloat);
        request.cfc_weight = getOrDefault("cfc_weight", Number.parseFloat);
        request.cosine_distance_upper_bound = getOrDefault("cosine_distance_upper_bound", Number.parseFloat);
        request.diversity_weight = getOrDefault("diversity_weight", Number.parseFloat);
        request.gower_weight = getOrDefault("gower_weight", Number.parseFloat);
        request.include_dataset = getOrDefault("include_dataset", (val) => "true" === val.toLowerCase())!;

        const response = optimizationController.postTextPromptOptimization(request);
        handleResponse(response, props.setServerResponse, new McdServerRequest(STANDARD_BIKE_INDEX), true);
      }}
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
      <input type="text" className="form-control" name="bike-description" id="bike-description-input" required />
      <label className="form-label" htmlFor="bike-description-input">
        Bike Description
      </label>
    </div>
  );
}

export function GenerateFromTextForm(props: {
  setServerResponse: (mcdServerResponse: OptimizationRequestState) => void;
}): ReactElement {
  return (
    <form id={TEXT_PROMPT_FORM_ID} className="m-3">
      <h3>Generate from Text Prompt</h3>
      <div className="row flex-cont">
        <BikeDescriptionInput />
      </div>
      <ShowAdvancedOptionsButton />
      <AdvancedOptions />
      <div className="row flex-cont"></div>
      <div className="p-3">
        <div className="row flex-cont text-center justify-content-center">
          <GenerateButton setServerResponse={props.setServerResponse} />
        </div>
      </div>
    </form>
  );
}
