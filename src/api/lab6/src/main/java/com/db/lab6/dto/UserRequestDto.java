package com.db.lab6.dto;

import com.db.lab6.enums.Role;
import lombok.Data;

@Data
public class UserRequestDto {
    private String email;
    private String passwordHash;
    private Role role;
    private Boolean isActive;
}
