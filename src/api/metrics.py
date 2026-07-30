class MetricsStore:

    def __init__(self):
        self.global_stats = {
            "successful_requests": 0,
            "rate_limited_requests": 0,
            "total_tokens": 0,
            "total_latency": 0.0,
            "total_tool_calls": 0
        }

        self.per_key_stats = {}

    def _init_key(self, api_key):
        if api_key not in self.per_key_stats:
            self.per_key_stats[api_key] = {
                "successful_requests": 0,
                "rate_limited_requests": 0,
                "tokens": 0,
                "latency": 0.0,
                "tool_calls": 0
            }

    # ✅ Called only for successful (200) requests
    def record_success(self, api_key: str, latency: float, usage: dict, trace: dict):

        self._init_key(api_key)

        # ---- Global ----
        self.global_stats["successful_requests"] += 1
        self.global_stats["total_latency"] += latency
        self.global_stats["total_tokens"] += usage.get("total_tokens", 0)

        for step in trace.get("steps", []):
            self.global_stats["total_tool_calls"] += len(step.get("tool_calls", []))

        # ---- Per Key ----
        key_stats = self.per_key_stats[api_key]

        key_stats["successful_requests"] += 1
        key_stats["tokens"] += usage.get("total_tokens", 0)
        key_stats["latency"] += latency

        for step in trace.get("steps", []):
            key_stats["tool_calls"] += len(step.get("tool_calls", []))

    # ✅ Called when rate limited (429)
    def record_rate_limited(self, api_key: str):

        self._init_key(api_key)

        self.global_stats["rate_limited_requests"] += 1
        self.per_key_stats[api_key]["rate_limited_requests"] += 1

    def snapshot(self):

        avg_latency = (
            self.global_stats["total_latency"] / self.global_stats["successful_requests"]
            if self.global_stats["successful_requests"] > 0 else 0
        )

        return {
            "global": {
                "successful_requests": self.global_stats["successful_requests"],
                "rate_limited_requests": self.global_stats["rate_limited_requests"],
                "total_tokens": self.global_stats["total_tokens"],
                "avg_latency_ms": round(avg_latency * 1000, 2),
                "total_tool_calls": self.global_stats["total_tool_calls"]
            },
            "per_key": self.per_key_stats
        }


metrics_store = MetricsStore()
