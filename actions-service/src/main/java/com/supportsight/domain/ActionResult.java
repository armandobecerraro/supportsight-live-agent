package com.supportsight.domain;

import java.time.Instant;

public record ActionResult(
    String actionId,
    String sessionId,
    String status,
    String output,
    String errorMessage,
    Instant executedAt
) {}
