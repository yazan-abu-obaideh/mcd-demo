import { BikesServerResponse, McdError, McdServerRequest, OptimizationRequestState } from "../McdServerResponse";
import { GENERIC_ERROR_RESPONSE } from "./SeedsForm";

export function handleResponse(
  response: Promise<Response>,
  setServerResponse: (mcdServerResponse: OptimizationRequestState) => void,
  mcdRequest: McdServerRequest,
  isClips: boolean = false
) {
  response
    .then((response) => {
      if (response.status !== 200) {
        response.json().then((resJson) => {
          setServerResponse(
            new OptimizationRequestState(true, mcdRequest, false, new McdError(resJson["message"]), undefined, isClips)
          );
        });
      } else {
        response.text().then((resJson) => {
          const optResponse = JSON.parse(resJson) as BikesServerResponse;
          setServerResponse(new OptimizationRequestState(true, mcdRequest, false, undefined, optResponse, isClips));
        });
      }
    })
    .catch(() => {
      setServerResponse(GENERIC_ERROR_RESPONSE);
    });
}
