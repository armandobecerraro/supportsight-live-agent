package com.supportsight.domain;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record ActionRequest(
    @NotBlank @Size(max = 36) String sessionId,
    @NotBlank @Size(max = 36) String actionId,
    @NotBlank @Size(max = 200) String actionType,
    @Size(max = 1000) String parameters
) {}
