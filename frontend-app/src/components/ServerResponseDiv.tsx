import {
  RESPONSE_DIV_ID,
  RESPONSE_LOADING_DIV,
  NO_BIKES_FOUND_DIV,
  ERROR_RESPONSE_DIV,
} from "../html_element_constant_ids";
import { McdServerResponse } from "./McdServerResponse";
import { ValidBikesDiv } from "./ValidBikesDiv";

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

function BikesDiv(props: { mcdServerResponse: McdServerResponse }) {
  const empty =
    props.mcdServerResponse.optimizationResponse?.bikes.length === 0;
  const returnValue = empty ? (
    <NoBikesDiv />
  ) : (
    <ValidBikesDiv mcdServerResponse={props.mcdServerResponse} />
  );
  return returnValue;
}

export function ServerResponseDiv(props: {
  mcdServerResponse: McdServerResponse;
}) {
  const optRes = props.mcdServerResponse.optimizationResponse;
  const validResponse = optRes !== undefined;
  return (
    <div id={RESPONSE_DIV_ID} className="container border rounded p-3">
      <h2>Generated Designs</h2>
      <div id="loading-or-result-div" className="container p-3">
        {props.mcdServerResponse.isLoading && <LoadingDiv />}
        {validResponse && (
          <BikesDiv mcdServerResponse={props.mcdServerResponse} />
        )}
        {props.mcdServerResponse.error !== undefined && (
          <div id={ERROR_RESPONSE_DIV} className="p-3 text-center">
            {props.mcdServerResponse.error.errorMessage}
          </div>
        )}
      </div>
    </div>
  );
}
