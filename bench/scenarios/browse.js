import http from "k6/http";
import { check, sleep, group } from "k6";
import { Trend } from "k6/metrics";

const BASE = __ENV.BASE_URL || "http://localhost:80";

const pageLatency = new Trend("browse_page_latency", true);

export const options = {
    scenarios: {
        browse: {
            executor: "ramping-vus",
            startVUs: 0,
            stages: [
                { duration: "30s", target: 25 },
                { duration: "90s", target: 50 },
                { duration: "30s", target: 0 },
            ],
            gracefulRampDown: "15s",
        },
    },
    thresholds: {
        http_req_failed: ["rate<0.01"],
        http_req_duration: ["p(95)<500", "p(99)<1500"],
        browse_page_latency: ["p(95)<800"],
    },
};

export default function () {
    group("home", () => {
        const res = http.get(`${BASE}/`);
        pageLatency.add(res.timings.duration);
        check(res, { "home 200": (r) => r.status === 200 });
    });
    sleep(1);

    group("projects-list", () => {
        const res = http.get(`${BASE}/projects`);
        pageLatency.add(res.timings.duration);
        check(res, { "projects 200": (r) => r.status === 200 });
    });
    sleep(1);

    group("projects-api", () => {
        const res = http.get(`${BASE}/api/projects/`);
        check(res, {
            "api 200": (r) => r.status === 200,
            "api json": (r) => r.headers["Content-Type"]?.includes("json"),
        });
    });
    sleep(0.5);
}
