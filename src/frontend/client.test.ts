import getHealth from "./client";


test('adds 1 + 2 to equal 3', () => {
    expect(getHealth()).toBe({"status": "UP"});
  });
  