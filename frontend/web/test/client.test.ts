import {
  OptimizationController,
  RiderDimensions,
  RenderingController,
  GeneratedBike,
} from "../src/controller";

const testTimeoutMilliseconds = 20000;

const optimizationController = new OptimizationController(
  "http://localhost:5000/api/v1/optimization"
);
const renderingController = new RenderingController(
  "http://localhost:5000/api/v1/rendering"
);


function clientTest(testName: string, testFunction: any) {
  test(testName, testFunction, testTimeoutMilliseconds);
}


clientTest("Optimize seeds and render...", async () => {
  const response: Response = await optimizationController.postSeedsOptimization(
    "ergonomics",
    "1",
    "1"
  );
  expect(
    (JSON.parse(await response.text()) as Object).hasOwnProperty("bikes")
  ).toEqual(true);
  expect(response.status).toEqual(200);
});

clientTest("Optimize dimensions...", async () => {
  const riderDimensions = new RiderDimensions();
  riderDimensions.height = 73.5;
  riderDimensions.sh_height = 60;
  riderDimensions.hip_to_ankle = 34;
  riderDimensions.hip_to_knee = 16.5;
  riderDimensions.shoulder_to_wrist = 20.5;
  riderDimensions.arm_length = 23.5;
  riderDimensions.upper_leg = 16.5;
  riderDimensions.lower_leg = 20.25;
  riderDimensions.torso_length = 23;

  const response: Response =
    await optimizationController.postDimensionsOptimization(
      "aerodynamics",
      "5",
      riderDimensions
    );
  expect(
    (JSON.parse(await response.text()) as Object).hasOwnProperty("bikes")
  ).toEqual(true);
  expect(response.status).toEqual(200);
});

clientTest("Optimize invalid image...", async () => {
  const response = await optimizationController.postImageOptimization(
    "aerodynamics",
    "1",
    "0101",
    65
  );

  expect(response.status).toEqual(400);
  expect(JSON.parse(await response.text())).toHaveProperty("message");
});

clientTest("Render bike...", async () => {
  const bike = new GeneratedBike();
  bike.bikeObject = {
    "Crank length": 175,
    "DT Length": 636.2950530025701,
    "HT Angle": 72.1,
    "HT LX": 54.3,
    "HT Length": 206.7682943434329,
    "Handlebar style": 1,
    "Headset spacers": 33.69758842393159,
    "ST Angle": 73.16557640624752,
    "ST Length": 300,
    "Saddle height": 510.92794982218373,
    "Seatpost LENGTH": 291.45431563600863,
    Stack: 565.6,
    "Stem angle": 28.592130586374434,
    "Stem length": 110.48084725204376,
  };
  bike.bikePerformance = "";
  bike.seedImageId = "3";

  const response = await renderingController.postRenderBikeRequest(bike);
  expect(response.status).toEqual(200);
  expect(await response.blob()).toBeDefined();
});
