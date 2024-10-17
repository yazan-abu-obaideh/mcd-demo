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
  constructor(
    readonly requestPayload: undefined | McdServerRequest,
    readonly isLoading: boolean,
    readonly error: McdError | undefined,
    readonly optimizationResponse: BikesServerResponse | undefined
  ) {}
}
