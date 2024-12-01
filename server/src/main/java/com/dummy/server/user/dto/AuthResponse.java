package com.dummy.server.user.dto;

import lombok.Builder;

@Builder
public record AuthResponse(
        String accessToken,
        String tokenType
) {
}
