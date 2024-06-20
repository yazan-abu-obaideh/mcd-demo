import { DimensionsOptimizationRequest } from "./controller";

export function dimensionsFormToRiderDimensions(formData: FormData): DimensionsOptimizationRequest {
    return {
        seedBikeId: formData.get("seedBike") as string,
        height: getNumberFrom(formData, "rider-height"),
        sh_height: getNumberFrom(formData, "shoulder-height"),
        hip_to_ankle: getNumberFrom(formData, "hip-ankle"),
        hip_to_knee: getNumberFrom(formData, "hip-knee"),
        shoulder_to_wrist: getNumberFrom(formData, "shoulder-wrist"),
        arm_length: getNumberFrom(formData, "arm-length"),
        torso_length: getNumberFrom(formData, "torso-length"),
        lower_leg: getNumberFrom(formData, "lower-leg"),
        upper_leg: getNumberFrom(formData, "upper-leg"),
      }
}

function getNumberFrom(formData: FormData, fieldName: string): number {
    return Number(formData.get(fieldName) as string);
  }