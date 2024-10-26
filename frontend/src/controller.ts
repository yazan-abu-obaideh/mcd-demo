import { optimizationApiUrl, renderingApiUrl } from "./config";

class FrontendDimensionsOptimizationRequest {
  seedBikeId: string | undefined;
  height!: number;
  sh_height!: number;
  hip_to_ankle!: number;
  hip_to_knee!: number;
  shoulder_to_wrist!: number;
  arm_length!: number;
  torso_length!: number;
  lower_leg!: number;
  upper_leg!: number;
}

class GeneratedBike {
  seedImageId!: string;
  bikeObject!: object;
  bikePerformance!: string;
}

class TextPromptOptimizationRequest {
  text_prompt!: string;
  cosine_distance_upper_bound: number | null = null;
  optimizer_population: number | null = null;
  optimizer_generations: number | null = null;
  avg_gower_weight: number | null = null;
  cfc_weight: number | null = null;
  gower_weight: number | null = null;
  diversity_weight: number | null = null;
  bonus_objective_weight: number | null = null;
  include_dataset: boolean = false;
}

class RenderingController {
  renderingApiUrl: string;

  constructor(renderingApiUrl: string) {
    this.renderingApiUrl = renderingApiUrl;
  }

  async postRenderClipsBikeRequest(bike: GeneratedBike): Promise<Response> {
    return fetch(this.renderingApiUrl.concat("/render-clips-bike"), {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: JSON.stringify({
        bike: bike.bikeObject,
      }),
    });
  }

  async postRenderBikeRequest(bike: GeneratedBike): Promise<Response> {
    return fetch(this.renderingApiUrl.concat("/render-bike-object"), {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: JSON.stringify({
        bike: bike.bikeObject,
        seedImageId: bike.seedImageId,
      }),
    });
  }
}

class OptimizationController {
  optimizationApiUrl: string;

  constructor(optimizationApiUrl: string) {
    this.optimizationApiUrl = optimizationApiUrl;
  }

  async postTextPromptOptimization(request: TextPromptOptimizationRequest): Promise<Response> {
    return await fetch(this.optimizationApiUrl.concat("/text-prompt"), {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  async postDimensionsOptimization(
    optimizationType: string,
    dimensionsRequestInches: FrontendDimensionsOptimizationRequest
  ) {
    const seedId = dimensionsRequestInches.seedBikeId;
    delete dimensionsRequestInches.seedBikeId;

    return await fetch(this.optimizationApiUrl.concat(`/${optimizationType}/optimize-dimensions`), {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: JSON.stringify({
        seedBikeId: seedId,
        riderDimensionsInches: dimensionsRequestInches,
      }),
    });
  }

  async postImageOptimization(
    optimizationType: "aerodynamics" | "ergonomics",
    seedBikeId: string,
    imageBase64: string,
    personHeight: number
  ) {
    return await fetch(this.optimizationApiUrl.concat(`/${optimizationType}/optimize-custom-rider`), {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: JSON.stringify({
        seedBikeId: seedBikeId,
        imageBase64: imageBase64,
        riderHeight: personHeight,
      }),
    });
  }

  async postSeedsOptimization(
    optimizationType: "ergonomics" | "aerodynamics",
    seedBikeId: string,
    riderImageId: string
  ): Promise<Response> {
    return await fetch(this.optimizationApiUrl.concat(`/${optimizationType}/optimize-seeds`), {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: JSON.stringify({
        seedBikeId: seedBikeId,
        riderId: riderImageId,
      }),
    });
  }

  async postDownloadBikeCadRequest(bike: GeneratedBike): Promise<Response> {
    return fetch(this.optimizationApiUrl.concat("/download-cad"), {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: JSON.stringify({
        bike: bike.bikeObject,
        seedBikeId: bike.seedImageId,
      }),
    });
  }
  async postDownloadClipsBikeCadRequest(bike: GeneratedBike): Promise<Response> {
    return fetch(this.optimizationApiUrl.concat("/download-clips-cad"), {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: JSON.stringify({
        bike: bike.bikeObject,
      }),
    });
  }
}

export {
  OptimizationController,
  FrontendDimensionsOptimizationRequest,
  GeneratedBike,
  RenderingController,
  TextPromptOptimizationRequest,
};
export const optimizationController = new OptimizationController(optimizationApiUrl);
export const renderingController = new RenderingController(renderingApiUrl);
