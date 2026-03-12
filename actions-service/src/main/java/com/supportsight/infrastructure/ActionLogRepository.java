package com.supportsight.infrastructure;

import com.supportsight.domain.ActionLog;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ActionLogRepository extends JpaRepository<ActionLog, String> {
    List<ActionLog> findBySessionIdOrderByExecutedAtDesc(String sessionId);
}
