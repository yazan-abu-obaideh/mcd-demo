import { GeneratedBike } from "../declarative/controller";

export class McdError {
  constructor(readonly errorMessage: string) {}
}

export const GENERIC_ERROR = new McdError("Something went wrong");

export type BikesServerResponse = {
  bikes: Array<{
    bike: GeneratedBike;
    bikePerformance: string;
  }>;
  logs?: Array<string>;
};

export class McdServerRequest {
  constructor(readonly seedBike: string) {}
}

export class OptimizationRequestState {
  static started(mcdRequest: McdServerRequest) {
    return new OptimizationRequestState(true, mcdRequest, true, undefined, undefined);
  }
  constructor(
    readonly started: boolean,
    readonly requestPayload: undefined | McdServerRequest,
    readonly isLoading: boolean,
    readonly error: McdError | undefined,
    readonly optimizationResponse: BikesServerResponse | undefined,
    readonly isClips: boolean = false
  ) {}
}
