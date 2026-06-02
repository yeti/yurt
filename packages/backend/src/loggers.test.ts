import { getRequestLogger, logger, runWithRequestLogger } from "~/loggers";

describe("getRequestLogger", () => {
  it("returns global logger when called outside request context", () => {
    expect(getRequestLogger()).toBe(logger);
  });

  it("returns child logger with requestId inside runWithRequestLogger", () => {
    runWithRequestLogger(() => {
      const reqLogger = getRequestLogger();
      expect(reqLogger).not.toBe(logger);

      const bindings = reqLogger.bindings();
      expect(bindings).toHaveProperty("requestId");
      expect(typeof bindings.requestId).toBe("string");
      expect(bindings.requestId.length).toBeGreaterThan(0);
    });
  });

  it("produces different requestIds for different runs", () => {
    let id1: string | undefined;
    let id2: string | undefined;

    runWithRequestLogger(() => {
      id1 = getRequestLogger().bindings().requestId as string;
    });

    runWithRequestLogger(() => {
      id2 = getRequestLogger().bindings().requestId as string;
    });

    expect(id1).toBeDefined();
    expect(id2).toBeDefined();
    expect(id1).not.toBe(id2);
  });

  it("maintains separate loggers in concurrent async contexts", async () => {
    const ids: string[] = [];

    await Promise.all(
      Array.from(
        { length: 5 },
        () =>
          new Promise<void>((resolve) => {
            runWithRequestLogger(async () => {
              // Yield to the event loop so contexts overlap
              await new Promise((r) => setTimeout(r, 10));
              ids.push(getRequestLogger().bindings().requestId as string);
              resolve();
            });
          })
      )
    );

    expect(ids).toHaveLength(5);
    expect(new Set(ids).size).toBe(5);
  });
});
