package com.db.lab6.config;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import lombok.Data;

import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.Map;

@Data
@JsonPropertyOrder({"timestamp", "status", "message", "path", "errors"})
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ApiError {

    private ZonedDateTime timestamp;
    private int status;
    private String message;
    private String path;
    private Map<String, String> errors;

    public ApiError(int status, String message, String path) {
        this.timestamp = ZonedDateTime.now(ZoneOffset.UTC);
        this.status = status;
        this.message = message;
        this.path = path;
    }

    public ApiError(int status, String message, String path, Map<String, String> errors) {
        this.timestamp = ZonedDateTime.now(ZoneOffset.UTC);
        this.status = status;
        this.message = message;
        this.path = path;
        this.errors = errors;
    }
}
