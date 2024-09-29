import { submitTextPromptForm } from "../declarative/client";

import { FormSelectionNavBar } from "./FormSelectionNavBar";
import { LandingHeader } from "./LandingHeader";
import { ReactElement, useState } from "react";
import { McdInputForm } from "../FormsEnum";
import { SeedsForm } from "./forms/SeedsForm";
import { UploadImageForm } from "./forms/UploadImageForm";
import { SpecifyRiderDimensionsForm } from "./forms/SpecifyRiderDimensionsForm";

function GenerateFromTextForm(): ReactElement {
  return (
    <form id="generate-from-text-form" className="m-3">
      <h3>Generate from Text Prompt</h3>
      <div className="row flex-cont">
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
      </div>
      <button
        className="btn btn-outline-danger"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#advancedOptions"
        aria-expanded="false"
        aria-controls="advancedOptions"
      >
        Show advanced options
      </button>
      <div className="collapse p-3" id="advancedOptions">
        <div className="row flex-cont">
          <div className="col-6">
            <input
              type="number"
              className="form-control"
              name="optimizer_population"
              id="optimizer_population-input"
              min="1"
              max="100"
            />
            <label className="form-label" htmlFor="optimizer_population-input">
              Bikes per generation
            </label>
          </div>
          <div className="col-6">
            <input
              type="number"
              className="form-control"
              name="optimizer_generations"
              max="60"
              min="1"
              id="optimizer_generations-input"
            />
            <label className="form-label" htmlFor="optimizer_generations-input">
              Number of generations
            </label>
          </div>
        </div>
        <div className="row flex-cont">
          <div className="col-6">
            <input
              type="number"
              className="form-control"
              name="cosine_distance_upper_bound"
              min="0.1"
              max="1"
              step="0.01"
              id="cosine_distance_upper_bound-input"
            />
            <label
              className="form-label"
              htmlFor="cosine_distance_upper_bound-input"
            >
              Cosine distance upper bound
            </label>
          </div>
          <div className="col-6">
            <input
              type="number"
              className="form-control"
              name="avg_gower_weight"
              step="0.01"
              id="avg_gower_weight-input"
            />
            <label className="form-label" htmlFor="avg_gower_weight-input">
              Average gower weight
            </label>
          </div>
        </div>
        <div className="row flex-cont">
          <div className="col-6">
            <input
              type="number"
              className="form-control"
              name="cfc_weight"
              step="0.01"
              id="cfc_weight-input"
            />
            <label className="form-label" htmlFor="cfc_weight-input">
              Counterfactual weight
            </label>
          </div>
          <div className="col-6">
            <input
              type="number"
              className="form-control"
              name="gower_weight"
              step="0.01"
              id="gower_weight-input"
            />
            <label className="form-label" htmlFor="gower_weight-input">
              Gower weight
            </label>
          </div>
        </div>
        <div className="row flex-cont">
          <div className="col-6">
            <input
              type="number"
              className="form-control"
              name="diversity_weight"
              step="0.01"
              id="diversity_weight-input"
            />
            <label className="form-label" htmlFor="diversity_weight-input">
              Diversity weight
            </label>
          </div>
          <div className="col-6">
            <input
              type="number"
              className="form-control"
              name="bonus_objective_weight"
              step="0.01"
              id="bonus_objective_weight-input"
            />
            <label
              className="form-label"
              htmlFor="bonus_objective_weight-input"
            >
              Bonus objective weight
            </label>
          </div>
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
      <div className="row flex-cont"></div>
      <div className="p-3">
        <div className="row flex-cont text-center justify-content-center">
          <button
            className="btn btn-outline-danger btn-lg w-40"
            type="button"
            id="generate-from-text-form-submit-button"
            onClick={() => submitTextPromptForm()}
          >
            Generate!
          </button>
        </div>
      </div>
    </form>
  );
}

function ServerResponseDiv() {
  return (
    <div
      id="server-response-div"
      className="container border rounded p-3"
      style={{ display: "none" }}
    >
      <h2>Generated Designs</h2>
      <div id="loading-or-result-div" className="container p-3">
        <div
          id="response-loading-div"
          className="text-center"
          style={{ display: "block" }}
        >
          <div className="spinner-border loading-element" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <div className="text-xl-center">
            <h4>MCD is generating designs...</h4>
            <h5>This should not take more than 30 seconds...</h5>
          </div>
        </div>
        <div
          id="response-received-div"
          className="p-3"
          style={{ display: "none" }}
        >
          <div
            id="carouselExampleDark"
            className="carousel carousel-dark slide"
          >
            <div
              id="generated-designs-consumer-carousel"
              className="carousel-inner"
            ></div>
            <button
              className="carousel-control-prev"
              type="button"
              data-bs-target="#carouselExampleDark"
              data-bs-slide="prev"
            >
              <span
                className="carousel-control-prev-icon"
                aria-hidden="true"
              ></span>
              <span className="visually-hidden">Previous</span>
            </button>
            <button
              className="carousel-control-next"
              type="button"
              data-bs-target="#carouselExampleDark"
              data-bs-slide="next"
            >
              <span
                className="carousel-control-next-icon"
                aria-hidden="true"
              ></span>
              <span className="visually-hidden">Next</span>
            </button>
          </div>
        </div>
        <div
          id="no-bikes-found-div"
          className="p-3 text-center"
          style={{ display: "none" }}
        >
          <h4>
            MCD could not generate any valid designs within the allotted time.
            Please try a different request.
          </h4>
        </div>
        <div
          id="error-response-div"
          className="p-3 text-center"
          style={{ display: "none" }}
        ></div>
      </div>
    </div>
  );
}

export default function McdDemoUserForm() {
  const [selectedForm, setSelectedForm] = useState(McdInputForm.SEEDS);
  return (
    <div className="non-nav-body">
      <LandingHeader />
      <FormSelectionNavBar setForm={setSelectedForm} />
      <div id="generation-forms" className="container border rounded p-3 mb-3">
        {selectedForm === McdInputForm.SEEDS && <SeedsForm />}
        {selectedForm === McdInputForm.IMAGE && <UploadImageForm />}
        {selectedForm === McdInputForm.TEXT && <GenerateFromTextForm />}
        {selectedForm === McdInputForm.DIMENSIONS && (
          <SpecifyRiderDimensionsForm />
        )}
      </div>
      <ServerResponseDiv />
    </div>
  );
}
