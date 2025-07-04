// backend/server.js
const http = require("http");
const { spawn } = require("child_process");

const server = http.createServer((req, res) => {
  if (req.method === "OPTIONS") {
    res.writeHead(204, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    });
    return res.end();
  }

  if (req.method === "POST") {
    let body = "";
    req.on("data", chunk => body += chunk);
    req.on("end", () => {
      const { image } = JSON.parse(body);
      const python = spawn("python", ["../faceemotion.py", image]);

      let result = "";
      python.stdout.on("data", data => result += data.toString());
     python.stderr.on("data", err => {
  const msg = err.toString();
  if (!msg.includes("oneDNN custom operations")) {
    console.error("Python error:", msg);
  }
});

      python.on("close", () => {
        res.writeHead(200, {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        });

        res.end(JSON.stringify({ emotion: result.trim() }));
      });
    });
  } else {
    res.writeHead(404);
    res.end();
  }
});

server.listen(3001, () => {
  console.log("✅ Server running at http://localhost:3001");
});