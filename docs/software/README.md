# Реалізація інформаційного та програмного забезпечення

У рамках проєкту розробляється:
- SQL-скрипти для створення та початкового наповнення бази даних;
- RESTfull сервіс для керування обліковими записами користувачів системи.


## SQL-скрипти
### main.sql
```sql
  CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    passwordHash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    isActive BOOLEAN NOT NULL
);

CREATE TABLE Survey (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL,
    creationDate DATETIME NOT NULL,
    closeDate DATETIME,
    userId INT NOT NULL,
    FOREIGN KEY (userId) REFERENCES User(id) ON DELETE CASCADE
);

CREATE TABLE Question (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    isRequired BOOLEAN NOT NULL,
    `order` INT NOT NULL,
    surveyId INT NOT NULL,
    FOREIGN KEY (surveyId) REFERENCES Survey(id) ON DELETE CASCADE
);

CREATE TABLE SurveyLink (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(100) NOT NULL UNIQUE,
    isActive BOOLEAN NOT NULL,
    expiryDate DATETIME,
    clicks INT NOT NULL DEFAULT 0,
    surveyId INT NOT NULL,
    FOREIGN KEY (surveyId) REFERENCES Survey(id) ON DELETE CASCADE
);

CREATE TABLE Response (
    id INT AUTO_INCREMENT PRIMARY KEY,
    submissionDate DATETIME NOT NULL,
    isComplete BOOLEAN NOT NULL,
    surveyLinkId INT NOT NULL,
    FOREIGN KEY (surveyLinkId) REFERENCES SurveyLink(id) ON DELETE CASCADE
);

CREATE TABLE Answer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    value TEXT NOT NULL,
    responseId INT NOT NULL,
    questionId INT NOT NULL,
    FOREIGN KEY (responseId) REFERENCES Response(id) ON DELETE CASCADE,
    FOREIGN KEY (questionId) REFERENCES Question(id) ON DELETE CASCADE
);
```

### test_d.sql
```sql
  INSERT INTO User (email, passwordHash, role, isActive) VALUES
('admin@example.com', 'hash1', 'admin', TRUE),
('user1@example.com', 'hash2', 'respondent', TRUE),
('user2@example.com', 'hash3', 'respondent', TRUE);

INSERT INTO Survey (title, description, status, creationDate, closeDate, userId) VALUES
('Customer Satisfaction Survey', 'Tell us about your experience.', 'active', NOW(), NULL, 1),
('Product Feedback', 'We value your thoughts on our new product.', 'draft', NOW(), NULL, 1),
('Website Usability', 'How easy is it to use our website?', 'active', NOW(), NULL, 1);

INSERT INTO Question (text, type, isRequired, `order`, surveyId) VALUES
-- Survey 1
('How satisfied are you?', 'rating', TRUE, 1, 1),
('What can we improve?', 'text', FALSE, 2, 1),
-- Survey 2
('Is the product useful?', 'yesno', TRUE, 1, 2),
('Would you recommend it?', 'yesno', TRUE, 2, 2),
-- Survey 3
('Was the site easy to navigate?', 'yesno', TRUE, 1, 3),
('Any technical issues?', 'text', FALSE, 2, 3);

INSERT INTO SurveyLink (token, isActive, expiryDate, clicks, surveyId) VALUES
('link1', TRUE, DATE_ADD(NOW(), INTERVAL 10 DAY), 5, 1),
('link2', TRUE, DATE_ADD(NOW(), INTERVAL 5 DAY), 0, 1),
('link3', TRUE, DATE_ADD(NOW(), INTERVAL 15 DAY), 2, 2),
('link4', TRUE, DATE_ADD(NOW(), INTERVAL 7 DAY), 1, 3);

INSERT INTO Response (submissionDate, isComplete, surveyLinkId) VALUES
(NOW(), TRUE, 1),
(NOW(), TRUE, 2),
(NOW(), FALSE, 3),
(NOW(), TRUE, 4);

-- Response 1 (link1, survey 1)
INSERT INTO Answer (value, responseId, questionId) VALUES
('4', 1, 1),
('More options needed.', 1, 2);

-- Response 2 (link2, survey 1)
INSERT INTO Answer (value, responseId, questionId) VALUES
('5', 2, 1),
('Nothing to improve.', 2, 2);

-- Response 3 (link3, survey 2) — incomplete, only one answer
INSERT INTO Answer (value, responseId, questionId) VALUES
('Yes', 3, 3);

-- Response 4 (link4, survey 3)
INSERT INTO Answer (value, responseId, questionId) VALUES
('Yes', 4, 5),
('No issues', 4, 6);
```


## RESTfull сервіс
Сервіс для виконання основних операцій над обліковими записами користувачів системи був розроблений на базі 
Spring Boot, який є фреймворком Java. У проєкті використовуються такі залежності:
- Spring Web;
- Spring Data JPA;
- MySQL Driver;
- Flyway Migration;
- SpringDoc OpenAPI Starter WebMVC UI;
- Lombok.

Керування базою даних survey_db здійснуюється за допомогою СКРБД MySQL. Підключення до неї описане у файлі `application.yaml`:
``` yaml
spring:
  application:
    name: lab6
  datasource:
    url: jdbc:mysql://localhost:3306/survey_db?useSSL=false&serverTimezone=UTC
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.MySQLDialect

springdoc:
  api-docs:
    path: /api/v1/docs
```

### Структура директорій сервісу
```
src
└───main
	├───java
	│   └───com
	│       └───db
	│           └───lab6
	│               │   StartApplication.java
	│               │
	│               ├───config
	│               │       ApiError.java
	│               │       GlobalExceptionHandler.java
	│               │
	│               ├───controller
	│               │       UserController.java
	│               │
	│               ├───dto
	│               │       UserRequestDto.java
	│               │       UserResponseDto.java
	│               │
	│               ├───enums
	│               │       Role.java
	│               │
	│               ├───exception
	│               │       UserAlreadyExistsException.java
	│               │       UserNotFoundException.java
	│               │
	│               ├───model
	│               │       User.java
	│               │
	│               ├───repository
	│               │       UserRepository.java
	│               │
	│               └───service
	│                       UserService.java
	│
	└───resources
		│   application.yaml
		│
		└───db
			└───migration
					V1__create_tables.sql
					V2__insert_initial_data.sql
```

Основними шарами, які реалізовані в проєкті, є:
- модель (містить сутності, що відображають структуру таблиць реляційної БД);
- контролер (отримує HTTP-запити, обробляє їх за допомогою сервісів та повертає клієнту відповіді);
- сервіс (відповідає за виконання бізнес-логіки);
- репозиторій (містить інтерфейси, які взаємодіють з базою даних за допомогою Spring Data JPA).

### Модель
``` java
package com.db.lab6.model;

import com.db.lab6.enums.Role;
import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Entity
@Table(name = "app_user")
@Data
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 50)
    @Email(message = "Email should be valid")
    @NotBlank(message = "Email is required")
    @Size(max = 50, message = "Email cannot be longer than 50 characters")
    private String email;

    @Column(nullable = false, length = 60)
    @NotBlank(message = "Password hash is required")
    @Size(max = 60, message = "Password hash cannot be longer than 60 characters")
    private String passwordHash;

    @Column(nullable = false, length = 20)
    @Enumerated(EnumType.STRING)
    @NotNull(message = "Role is required")
    private Role role;

    @Column(nullable = false)
    @NotNull(message = "isActive flag is required")
    private Boolean isActive;
}
```

### Контролер
``` java
package com.db.lab6.controller;

import com.db.lab6.dto.UserRequestDto;
import com.db.lab6.dto.UserResponseDto;
import com.db.lab6.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping
    public ResponseEntity<List<UserResponseDto>> getAllUsers() {
        List<UserResponseDto> users = userService.getAllUsers();
        return ResponseEntity.ok(users);
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserResponseDto> getUserById(@PathVariable Long id) {
        UserResponseDto user = userService.getUserById(id);
        return ResponseEntity.ok(user);
    }

    @PostMapping
    public ResponseEntity<UserResponseDto> createUser(@Valid @RequestBody UserRequestDto userRequestDto) {
        UserResponseDto createdUser = userService.createUser(userRequestDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdUser);
    }

    @PutMapping("/{id}")
    public ResponseEntity<UserResponseDto> updateUser(
            @PathVariable Long id,
            @Valid @RequestBody UserRequestDto userRequestDto) {
        UserResponseDto updatedUser = userService.updateUser(id, userRequestDto);
        return ResponseEntity.ok(updatedUser);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        userService.deleteUserById(id);
        return ResponseEntity.noContent().build();
    }
}
```

### Сервіс
``` java
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
```

### Репозиторій
``` java
package com.db.lab6.repository;

import com.db.lab6.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
}
```
