FROM node:24-alpine

WORKDIR /app

# The backend uses only Node.js built-in modules.
ENV NODE_ENV=production

# Copy application code
COPY --chown=node:node . .
USER node

# Expose port
EXPOSE 5000

CMD ["node", "server.js"]
