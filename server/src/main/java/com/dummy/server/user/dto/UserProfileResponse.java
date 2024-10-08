package com.dummy.server.user.dto;

import lombok.Builder;

@Builder
public record UserProfileResponse(
        String nickname,
        String email
) {
}
