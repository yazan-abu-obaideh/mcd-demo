class RiderDimensions {
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



class OptimizationController {

    optimizationApiUrl: string;

    constructor(optimizationApiUrl: string) {
        this.optimizationApiUrl = optimizationApiUrl;
    }

    async postDimensionsOptimization(optimizationType: string,
      seedBikeId: string,
      riderDimensionsInches: RiderDimensions     
      ) {
        return await fetch(
          optimizationApiUrl.concat(`/${optimizationType}/optimize-dimensions`),
          {
            headers: { "Content-Type": "application/json" },
            method: "POST",
            body: JSON.stringify({
              seedBikeId: seedBikeId,
              riderDimensionsInches: riderDimensionsInches,
            }),
          }
        );      
    }

    async postSeedsOptimization(optimizationType: string,
        seedBikeId: string,
        riderImageId: string): Promise<Response> {
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
}


export { OptimizationController };
