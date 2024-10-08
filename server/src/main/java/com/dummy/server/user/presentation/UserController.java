package com.dummy.server.user.presentation;

import com.dummy.server.oauth.CurrentUser;
import com.dummy.server.oauth.CustomUsernamePasswordAuthenticationToken;
import com.dummy.server.oauth.TokenProvider;
import com.dummy.server.oauth.UserPrincipal;
import com.dummy.server.user.application.UserService;
import com.dummy.server.user.dto.AuthResponse;
import com.dummy.server.user.dto.LoginRequest;
import com.dummy.server.user.dto.UserProfileResponse;
import com.dummy.server.user.dto.UserResisterRequest;
import io.swagger.v3.oas.annotations.Operation;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {
    private final AuthenticationManager authenticationManager;
    private final UserService userService;
    private final TokenProvider tokenProvider;

    @PostMapping("/login")
    @Operation(summary = "로그인" ,description = "")
    public ResponseEntity<AuthResponse> authenticateUser(@Valid @RequestBody LoginRequest loginRequest) {

        Authentication authentication = authenticationManager.authenticate(
                new CustomUsernamePasswordAuthenticationToken(
                        loginRequest.email(),
                        loginRequest.password()
                )
        );

        SecurityContextHolder.getContext().setAuthentication(authentication);

        String token = tokenProvider.createToken(authentication);
        return ResponseEntity.ok(AuthResponse.builder()
                    .accessToken(token)
                    .tokenType("Bearer")
                    .build());
    }

    @PostMapping("/signup")
    @Operation(summary = "회원가입"
            ,description = "이메일 형식으로 기입 할것.\n" +
            "비밀번호는 6~20자 사이\n" +
            "닉네임은 2~30자 사이로 입력해주세요.(중복 불가)")
    public ResponseEntity<String> registerUser(@Valid @RequestBody UserResisterRequest registrationDto) {
        String result = userService.createUser(registrationDto);
        return ResponseEntity.ok(result);
    }

    @GetMapping("/me")
    @PreAuthorize("hasRole('USER')")
    @Operation(summary = "내 정보 확인", description = "")
    public ResponseEntity<UserProfileResponse> getCurrentUser(@CurrentUser UserPrincipal userPrincipal) {
        UserProfileResponse currentUser = userService.getCurrentUser(userPrincipal);
        return ResponseEntity.ok(currentUser);
    }

}
