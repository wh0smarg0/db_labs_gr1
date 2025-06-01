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
