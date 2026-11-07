# El contexto de build es la raíz del repo (ver docker-compose.yml),
# por eso todas las rutas de origen van prefijadas con apps/api/.

# --- Etapa 1: dependencias completas (dev + prod) ---
FROM node:26-alpine AS deps
WORKDIR /app
COPY apps/api/package*.json ./
RUN npm ci

# --- Etapa 2: desarrollo (usada por docker compose up) ---
FROM node:26-alpine AS dev
WORKDIR /app
ENV NODE_ENV=development
COPY --from=deps /app/node_modules ./node_modules
COPY apps/api/ ./
COPY index.html ./public/index.html
EXPOSE 3000
CMD ["npm", "run", "dev"]

# --- Etapa 3: compilación TypeScript ---
FROM node:26-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY apps/api/ ./
COPY index.html ./public/index.html
RUN npm run build

# --- Etapa 4: producción (solo dependencias de runtime + dist) ---
FROM node:26-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY apps/api/package*.json ./
RUN npm ci --omit=dev && npm cache clean --force

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/public ./public

EXPOSE 3000

CMD ["node", "dist/app.js"]
