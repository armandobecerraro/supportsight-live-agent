package com.supportsight.domain;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "action_logs")
public class ActionLog {
    @Id @GeneratedValue(strategy = GenerationType.UUID)
    private String id;
    private String sessionId;
    private String actionId;
    private String actionType;
    private String status;
    @Column(length = 5000)
    private String output;
    @Column(length = 1000)
    private String errorMessage;
    private Instant executedAt = Instant.now();

    public ActionLog() {}
    public ActionLog(String sessionId, String actionId, String actionType,
                     String status, String output, String errorMessage) {
        this.sessionId = sessionId; this.actionId = actionId;
        this.actionType = actionType; this.status = status;
        this.output = output; this.errorMessage = errorMessage;
    }
    // Getters
    public String getId() { return id; }
    public String getSessionId() { return sessionId; }
    public String getActionId() { return actionId; }
    public String getStatus() { return status; }
    public String getOutput() { return output; }
    public String getErrorMessage() { return errorMessage; }
    public Instant getExecutedAt() { return executedAt; }
}
