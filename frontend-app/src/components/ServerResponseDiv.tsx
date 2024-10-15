import {
  RESPONSE_DIV_ID,
  RESPONSE_LOADING_DIV,
  RESPONSE_RECEIVED_DIV,
  GENERATED_DESIGNS_CONSUMER_CAROUSEL,
  NO_BIKES_FOUND_DIV,
  ERROR_RESPONSE_DIV,
} from "../html_element_constant_ids";
import { McdServerResponse } from "./McdServerResponse";

function LoadingDiv() {
  return (
    <div id={RESPONSE_LOADING_DIV} className="text-center">
      <div className="spinner-border loading-element" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <div className="text-xl-center">
        <h4>MCD is generating designs...</h4>
        <h5>This should not take more than 30 seconds...</h5>
      </div>
    </div>
  );
}

function NoBikesDiv() {
  return (
    <div id={NO_BIKES_FOUND_DIV} className="p-3 text-center">
      <h4>
        MCD could not generate any valid designs within the allotted time.
        Please try a different request.
      </h4>
    </div>
  );
}

function ValidBikesDiv() {
  return (
    <div id={RESPONSE_RECEIVED_DIV} className="p-3">
      <div id="carouselExampleDark" className="carousel carousel-dark slide">
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
  );
}

export function ServerResponseDiv(props: {
  mcdServerResponse: McdServerResponse;
}) {
  const optRes = props.mcdServerResponse.optimizationResponse;
  return (
    <div id={RESPONSE_DIV_ID} className="container border rounded p-3">
      <h2>Generated Designs</h2>
      <div id="loading-or-result-div" className="container p-3">
        {props.mcdServerResponse.isLoading && <LoadingDiv />}
        {optRes !== undefined && optRes.bikes.length > 0 && <ValidBikesDiv />}
        {optRes !== undefined && optRes.bikes.length === 0 && <ValidBikesDiv />}
        {props.mcdServerResponse.error !== undefined && (
          <div id={ERROR_RESPONSE_DIV} className="p-3 text-center">
            {props.mcdServerResponse.error.errorMessage}
          </div>
        )}
      </div>
    </div>
  );
}
