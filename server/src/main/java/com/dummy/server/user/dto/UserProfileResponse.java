package com.dummy.server.user.dto;

import lombok.Builder;

@Builder
public record UserProfileResponse(
        String employeeNumber,
        String nickname,
        String email
) {
}
