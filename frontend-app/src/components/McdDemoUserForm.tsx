import { FormSelectionNavBar } from "./FormSelectionNavBar";
import { LandingHeader } from "./LandingHeader";
import { useState } from "react";
import { McdInputForm } from "../FormsEnum";
import { SeedsForm } from "./forms/SeedsForm";
import { UploadImageForm } from "./forms/UploadImageForm";
import { SpecifyRiderDimensionsForm } from "./forms/SpecifyRiderDimensionsForm";
import { GenerateFromTextForm } from "./forms/GenerateFromTextForm";
import { ERROR_RESPONSE_DIV, GENERATED_DESIGNS_CONSUMER_CAROUSEL, NO_BIKES_FOUND_DIV, RESPONSE_DIV_ID, RESPONSE_LOADING_DIV, RESPONSE_RECEIVED_DIV } from "../html_element_constant_ids";

function ServerResponseDiv() {
  return (
    <div
      id={RESPONSE_DIV_ID}
      className="container border rounded p-3"
      style={{ display: "none" }}
    >
      <h2>Generated Designs</h2>
      <div id="loading-or-result-div" className="container p-3">
        <div
          id={RESPONSE_LOADING_DIV}
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
          id={RESPONSE_RECEIVED_DIV}
          className="p-3"
          style={{ display: "none" }}
        >
          <div
            id="carouselExampleDark"
            className="carousel carousel-dark slide"
          >
            <div
              id={GENERATED_DESIGNS_CONSUMER_CAROUSEL}
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
          id={NO_BIKES_FOUND_DIV}
          className="p-3 text-center"
          style={{ display: "none" }}
        >
          <h4>
            MCD could not generate any valid designs within the allotted time.
            Please try a different request.
          </h4>
        </div>
        <div
          id={ERROR_RESPONSE_DIV}
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
