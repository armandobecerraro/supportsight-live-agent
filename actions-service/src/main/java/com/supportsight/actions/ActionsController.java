package com.supportsight.actions;

import com.supportsight.domain.ActionRequest;
import com.supportsight.domain.ActionResult;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.util.List;

@RestController
@RequestMapping("/actions")
public class ActionsController {

    private static final Logger log = LoggerFactory.getLogger(ActionsController.class);
    private final ActionExecutorService executor;

    public ActionsController(ActionExecutorService executor) {
        this.executor = executor;
    }

    @PostMapping("/execute")
    public ResponseEntity<ActionResult> execute(@Valid @RequestBody ActionRequest request) {
        log.info("Executing action type={} session={}", request.actionType(), request.sessionId());
        ActionResult result = executor.execute(request);
        return ResponseEntity.ok(result);
    }

    @GetMapping("/allowed-types")
    public ResponseEntity<List<String>> allowedTypes() {
        return ResponseEntity.ok(ActionExecutorService.ALLOWED_ACTION_TYPES);
    }

    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("{\"status\":\"ok\",\"service\":\"actions-service\"}");
    }
}
