class FrontendDimensionsOptimizationRequest {
  seedBikeId: string;
  height: number;
  sh_height: number;
  hip_to_ankle: number;
  hip_to_knee: number;
  shoulder_to_wrist: number;
  arm_length: number;
  torso_length: number;
  lower_leg: number;
  upper_leg: number;
}

class GeneratedBike {
  seedImageId: string;
  bikeObject: object;
  bikePerformance: string;
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
        bike: bike.bikeObject
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

  async postTextPromptOptimization(textPrompt: string): Promise<Response> {
    return await fetch(this.optimizationApiUrl.concat("/text-prompt"), {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: JSON.stringify({
        textPrompt: textPrompt,
      }),
    });
  }

  async postDimensionsOptimization(
    optimizationType: string,
    dimensionsRequestInches: FrontendDimensionsOptimizationRequest
  ) {
    const seedId = dimensionsRequestInches.seedBikeId;
    delete dimensionsRequestInches.seedBikeId;

    return await fetch(
      this.optimizationApiUrl.concat(
        `/${optimizationType}/optimize-dimensions`
      ),
      {
        headers: { "Content-Type": "application/json" },
        method: "POST",
        body: JSON.stringify({
          seedBikeId: seedId,
          riderDimensionsInches: dimensionsRequestInches,
        }),
      }
    );
  }

  async postImageOptimization(
    optimizationType: string,
    seedBikeId: string,
    imageBase64: string,
    personHeight: number
  ) {
    return await fetch(
      this.optimizationApiUrl.concat(
        `/${optimizationType}/optimize-custom-rider`
      ),
      {
        headers: { "Content-Type": "application/json" },
        method: "POST",
        body: JSON.stringify({
          seedBikeId: seedBikeId,
          imageBase64: imageBase64,
          riderHeight: personHeight,
        }),
      }
    );
  }

  async postSeedsOptimization(
    optimizationType: string,
    seedBikeId: string,
    riderImageId: string
  ): Promise<Response> {
    return await fetch(
      this.optimizationApiUrl.concat(`/${optimizationType}/optimize-seeds`),
      {
        headers: { "Content-Type": "application/json" },
        method: "POST",
        body: JSON.stringify({
          seedBikeId: seedBikeId,
          riderId: riderImageId,
        }),
      }
    );
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
}

export {
  OptimizationController,
  FrontendDimensionsOptimizationRequest,
  GeneratedBike,
  RenderingController,
};
