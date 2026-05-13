# ========================================
# STAGE 1: Builder (node environment)
# In real React projects this would be:
# npm install && npm run build
# Here we just copy the static file
# ========================================
FROM node:20-alpine AS builder

WORKDIR /build

# Simulate build step (copy static assets)
COPY index.html .

# In real React: 
# COPY package*.json ./
# RUN npm ci
# COPY . .
# RUN npm run build

# ========================================
# STAGE 2: Runtime — nginx serves frontend
# Final image: only nginx + built files
# No node.js in production image!
# ========================================
FROM nginx:alpine AS runtime

# Remove default nginx page
RUN rm -rf /usr/share/nginx/html/*

# Copy built frontend from builder stage
COPY --from=builder /build/index.html /usr/share/nginx/html/

# Copy custom nginx config (handles API proxy)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget -qO- http://localhost/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
