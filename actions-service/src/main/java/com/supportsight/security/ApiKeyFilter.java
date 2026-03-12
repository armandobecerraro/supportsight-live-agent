package com.supportsight.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.filter.OncePerRequestFilter;
import java.io.IOException;
import java.util.Collections;

public class ApiKeyFilter extends OncePerRequestFilter {

    private final String validApiKey;

    public ApiKeyFilter(String validApiKey) {
        this.validApiKey = validApiKey;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain)
            throws ServletException, IOException {
        String path = req.getRequestURI();
        if (path.contains("/health") || path.contains("/actuator")) {
            chain.doFilter(req, res);
            return;
        }
        String key = req.getHeader("X-API-Key");
        if (validApiKey.equals(key)) {
            var auth = new UsernamePasswordAuthenticationToken("service", null, Collections.emptyList());
            SecurityContextHolder.getContext().setAuthentication(auth);
        }
        chain.doFilter(req, res);
    }
}
