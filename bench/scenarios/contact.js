import http from "k6/http";
import { check, sleep } from "k6";
import { Counter } from "k6/metrics";

const BASE = __ENV.BASE_URL || "http://localhost:80";

const rateLimited = new Counter("contact_rate_limited");
const accepted = new Counter("contact_accepted");

export const options = {
    scenarios: {
        contact: {
            executor: "constant-vus",
            vus: 10,
            duration: "30s",
        },
    },
    thresholds: {
        // Rate limit MUST engage | if not, contact_limit is broken.
        contact_rate_limited: ["count>10"],
        http_req_failed: ["rate<0.9"], // lax, many 429s expected
    },
};

export default function () {
    const payload = JSON.stringify({
        name: `Bench ${__VU}-${__ITER}`,
        email: `bench+${__VU}${__ITER}@example.com`,
        subject: "bench",
        message: "load test payload, safe to ignore",
    });
    const res = http.post(`${BASE}/api/contacts/`, payload, {
        headers: { "Content-Type": "application/json" },
    });

    if (res.status === 429) {
        rateLimited.add(1);
    } else if (res.status >= 200 && res.status < 300) {
        accepted.add(1);
    }

    check(res, {
        "status 2xx or 429 (not 5xx)": (r) => r.status < 500,
    });
    sleep(1);
}
