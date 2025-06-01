package com.db.lab6.service;

import com.db.lab6.dto.UserRequestDto;
import com.db.lab6.dto.UserResponseDto;
import com.db.lab6.model.User;
import com.db.lab6.repository.UserRepository;
import com.db.lab6.exception.UserAlreadyExistsException;
import com.db.lab6.exception.UserNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;

    public List<UserResponseDto> getAllUsers() {
        List<User> users = userRepository.findAll();
        return users.stream()
                .map(this::convertToResponseDto)
                .collect(Collectors.toList());
    }

    public UserResponseDto getUserById(Long id) {
        return userRepository.findById(id)
                .map(this::convertToResponseDto)
                .orElseThrow(() -> new UserNotFoundException(id));
    }

    public UserResponseDto createUser(UserRequestDto userRequestDto) {
        checkEmailUniqueness(userRequestDto.getEmail());

        User user = new User();

        user.setEmail(userRequestDto.getEmail());
        user.setPasswordHash(userRequestDto.getPasswordHash());
        user.setRole(userRequestDto.getRole());
        user.setIsActive(userRequestDto.getIsActive());

        User savedUser = userRepository.save(user);
        return convertToResponseDto(savedUser);
    }

    public UserResponseDto updateUser(Long id, UserRequestDto userRequestDto) {
        User existingUser = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException(id));

        if (!existingUser.getEmail().equals(userRequestDto.getEmail())) {
            checkEmailUniqueness(userRequestDto.getEmail());
            existingUser.setEmail(userRequestDto.getEmail());
        }

        existingUser.setPasswordHash(userRequestDto.getPasswordHash());
        existingUser.setRole(userRequestDto.getRole());
        existingUser.setIsActive(userRequestDto.getIsActive());

        User savedUser = userRepository.save(existingUser);
        return convertToResponseDto(savedUser);
    }

    public void deleteUserById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException(id));
        userRepository.delete(user);
    }

    private void checkEmailUniqueness(String email) {
        if (userRepository.findByEmail(email).isPresent()) {
            throw new UserAlreadyExistsException(email);
        }
    }

    private UserResponseDto convertToResponseDto(User user) {
        UserResponseDto dto = new UserResponseDto();
        dto.setId(user.getId());
        dto.setEmail(user.getEmail());
        dto.setPasswordHash(user.getPasswordHash());
        dto.setRole(user.getRole());
        dto.setIsActive(user.getIsActive());
        return dto;
    }
}
