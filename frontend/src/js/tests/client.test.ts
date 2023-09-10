import { OptimizationController } from "../controller";

const optimizationController = new OptimizationController("http://localhost:5000/api/v1");


test("Optimize seeds...", async () => {
  const response: Response = await optimizationController.postSeedsOptimization("ergonomics", "1", "1");
  expect((JSON.parse((await response.text())) as Object).hasOwnProperty("bikes")).toEqual(true);
  expect(response.status).toEqual(200);
});

