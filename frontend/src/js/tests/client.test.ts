import { getServerHealth, postOptimizationRequest, postSeedBikeOptimization } from "../client";

test("Health response...", async () => {
  const responseText: string = await (await getServerHealth()).text();
  expect(JSON.parse(responseText)).toEqual({ status: "UP" });
});

test("Optimization response", async () => {
  let responseObject = JSON.parse(
    await (
      await postOptimizationRequest(
        {
          seat_x: -9,
          seat_y: 27,
          handle_bar_x: 16.5,
          handle_bar_y: 25.5,
          crank_length: 7,
        },
        {
          height: 75,
          sh_height: 61.09855828510818,
          hip_to_ankle: 31.167514055725047,
          hip_to_knee: 15.196207871637029,
          shoulder_to_wrist: 13.538605228960089,
          arm_len: 16.538605228960087,
          tor_len: 26.931044229383136,
          low_leg: 18.971306184088018,
          up_leg: 15.196207871637029,
        }
      )
    ).text()
  );
  expect(responseObject).toBeInstanceOf(Array);
});

test("seed bike optimization response", async () => {
  let responseObject = JSON.parse(
    await (
      await postSeedBikeOptimization(
        {
          seat_x: -9,
          seat_y: 27,
          handle_bar_x: 16.5,
          handle_bar_y: 25.5,
          crank_length: 7,
        },
        {
          height: 75,
          sh_height: 61.09855828510818,
          hip_to_ankle: 31.167514055725047,
          hip_to_knee: 15.196207871637029,
          shoulder_to_wrist: 13.538605228960089,
          arm_len: 16.538605228960087,
          tor_len: 26.931044229383136,
          low_leg: 18.971306184088018,
          up_leg: 15.196207871637029,
        },
        15,
        25
      )
    ).text()
  );
  expect(responseObject).toBeInstanceOf(Array);
});

