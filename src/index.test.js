const { describe, it } = require("node:test");
const assert = require("node:assert");
const http = require("node:http");
const app = require("./index");

function request(method, path) {
  return new Promise((resolve, reject) => {
    const server = app.listen(0, () => {
      const { port } = server.address();
      const req = http.request({ hostname: "localhost", port, path, method }, (res) => {
        let body = "";
        res.on("data", (chunk) => { body += chunk; });
        res.on("end", () => {
          server.close();
          try {
            resolve(JSON.parse(body));
          } catch {
            resolve(body);
          }
        });
      });
      req.on("error", (err) => {
        server.close();
        reject(err);
      });
      req.end();
    });
  });
}

describe("Express API", () => {
  it("GET / returns hello message", async () => {
    const data = await request("GET", "/");
    assert.strictEqual(data.message, "Hello from Open ORC!");
  });

  it("GET /health returns ok", async () => {
    const data = await request("GET", "/health");
    assert.strictEqual(data.status, "ok");
  });

  it("GET /api/users returns users array", async () => {
    const data = await request("GET", "/api/users");
    assert.strictEqual(data.length, 2);
    assert.strictEqual(data[0].name, "Alice");
  });
});
