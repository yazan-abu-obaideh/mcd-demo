import getServerHealth from "../client";


test('Health response...', async () => {
  const responseText: string = await (await getServerHealth()).text();
    expect((JSON.parse(responseText))).toEqual({status: "UP"});
  });

  test('Adding numbers...', () => {
    expect(5 + 5).toBe(10);
  })

  