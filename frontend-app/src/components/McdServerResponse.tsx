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
};

export class McdServerResponse {
  constructor(
    readonly isLoading: boolean,
    readonly error: McdError | undefined,
    readonly optimizationResponse: BikesServerResponse | undefined
  ) {}
}
