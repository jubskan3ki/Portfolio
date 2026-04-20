import http from "k6/http";
import { check, sleep } from "k6";

const BASE = __ENV.BASE_URL || "http://localhost:80";

export const options = {
    scenarios: {
        sustained: {
            executor: "constant-vus",
            vus: 5,
            duration: "15m",
        },
    },
    thresholds: {
        http_req_failed: ["rate<0.005"],
        http_req_duration: ["p(95)<500"],
    },
};

const PATHS = ["/", "/projects", "/api/projects/", "/api/stacks/", "/api/experiences/", "/blog"];

export default function () {
    const url = `${BASE}${PATHS[Math.floor(Math.random() * PATHS.length)]}`;
    const res = http.get(url);
    check(res, { "2xx": (r) => r.status >= 200 && r.status < 300 });
    sleep(2);
}
