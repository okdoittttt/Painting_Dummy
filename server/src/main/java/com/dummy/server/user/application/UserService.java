package com.dummy.server.user.application;

import com.dummy.server.exception.BadRequestException;
import com.dummy.server.oauth.UserPrincipal;
import com.dummy.server.user.domain.User;
import com.dummy.server.user.dto.UserProfileResponse;
import com.dummy.server.user.dto.UserResisterRequest;
import com.dummy.server.user.repository.UserRepository;
import lombok.AllArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public String createUser(UserResisterRequest registrationDto) {
        if (userRepository.findByEmail(registrationDto.email()).isPresent())
            throw new BadRequestException("Email address already in use.");
        if (userRepository.findByNickname(registrationDto.nickname()).isPresent())
            throw new BadRequestException("Nickname already in use.");

        User newUser = User.builder()
                .email(registrationDto.email())
                .password(passwordEncoder.encode(registrationDto.password()))
                .nickname(registrationDto.nickname())
                .build();

        userRepository.save(newUser);

        return "success create user";
    }

    public UserProfileResponse getCurrentUser(UserPrincipal userPrincipal) {
        User user = userRepository.findById(userPrincipal.getId())
                .orElseThrow(() -> new BadRequestException("토큰 확인해보십쇼"));
        return UserProfileResponse.builder()
                .email(user.getEmail())
                .nickname(user.getNickname())
                .build();
    }
}
