import http from "node:http";
import https from "node:https";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Simple .env parser without dependencies
function loadEnv() {
  const envPath = path.join(__dirname, ".env");
  if (fs.existsSync(envPath)) {
    const lines = fs.readFileSync(envPath, "utf-8").split("\n");
    for (let line of lines) {
      line = line.trim();
      if (line && !line.startsWith("#") && line.includes("=")) {
        const [k, ...rest] = line.split("=");
        const v = rest.join("=").trim().replace(/^['"]|['"]$/g, "");
        if (!process.env[k.trim()]) {
          process.env[k.trim()] = v;
        }
      }
    }
  }
}
loadEnv();

const PORT = process.env.PORT || 8080;
const DECART_API_BASE = process.env.DECART_API_BASE || "https://api.decart.ai/v1";

const MIME_TYPES = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon"
};

const server = http.createServer(async (req, res) => {
  const setCors = () => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization, x-api-key");
  };

  setCors();

  if (req.method === "OPTIONS") {
    res.statusCode = 204;
    return res.end();
  }

  const reqUrl = new URL(req.url, `http://${req.headers.host}`);

  // Endpoint: GET /api/config
  if (req.method === "GET" && (reqUrl.pathname === "/api/config" || reqUrl.pathname === "/api/health")) {
    const hasKey = Boolean(process.env.DECART_API_KEY && process.env.DECART_API_KEY.trim());
    res.writeHead(200, { "Content-Type": "application/json" });
    return res.end(JSON.stringify({
      status: "ok",
      hasServerApiKey: hasKey,
      model: "lucy-vton-3.5",
      defaultSpeed: process.env.DECART_SPEED || "fast"
    }));
  }

  // Endpoint: POST /api/realtime-token
  if (req.method === "POST" && reqUrl.pathname === "/api/realtime-token") {
    let bodyData = "";
    req.on("data", chunk => { bodyData += chunk; });
    req.on("end", async () => {
      let body = {};
      try {
        if (bodyData) body = JSON.parse(bodyData);
      } catch (e) {
        console.warn("Failed to parse request JSON", e);
      }

      const apiKey = (body.apiKey || process.env.DECART_API_KEY || "").trim();
      if (!apiKey) {
        res.writeHead(400, { "Content-Type": "application/json" });
        return res.end(JSON.stringify({
          error: "No Decart API Key provided. Set DECART_API_KEY in .env or enter in UI."
        }));
      }

      const payload = JSON.stringify({
        expiresIn: body.expiresIn || 3600,
        allowedModels: ["lucy-vton-3.5"]
      });

      const options = {
        hostname: "api.decart.ai",
        port: 443,
        path: "/v1/client/tokens",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(payload),
          "x-api-key": apiKey,
          "User-Agent": "Decart-Lucy-VTON-Node/1.0"
        }
      };

      const decartReq = https.request(options, (decartRes) => {
        let respData = "";
        decartRes.on("data", chunk => { respData += chunk; });
        decartRes.on("end", () => {
          res.writeHead(decartRes.statusCode, { "Content-Type": "application/json" });
          res.end(respData);
          if (decartRes.statusCode === 200) {
            console.log("[OK] Minted Decart client token via Node.js server");
          } else {
            console.error(`[Error] Decart API error ${decartRes.statusCode}: ${respData}`);
          }
        });
      });

      decartReq.on("error", (e) => {
        res.writeHead(500, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: "Network error contacting Decart API", details: e.message }));
      });

      decartReq.write(payload);
      decartReq.end();
    });
    return;
  }

  // Static File Serving
  let filePath = path.join(__dirname, reqUrl.pathname === "/" ? "index.html" : reqUrl.pathname);
  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    filePath = path.join(__dirname, "index.html");
  }

  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || "application/octet-stream";

  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(404, { "Content-Type": "text/plain" });
      return res.end("Not Found");
    }
    res.writeHead(200, { "Content-Type": contentType });
    res.end(content);
  });
});

server.listen(PORT, () => {
  console.log(`\n======================================================`);
  console.log(`  mir.ai — Realtime WebRTC Virtual Try-On Studio`);
  console.log(`  Model: ${process.env.DECART_MODEL || "lucy-vton-3.6"}`);
  console.log(`  URL: http://localhost:${PORT}`);
  console.log(`  Backend API Key: ${process.env.DECART_API_KEY ? "CONFIGURED" : "NOT SET (Use .env or UI)"}`);
  console.log(`======================================================\n`);
});
