# Dockerfile simple para servir frontend estático con nginx
FROM nginx:alpine

# Copiar configuración nginx que ya maneja CSP para Cesium
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar archivos estáticos del frontend
COPY . /public

# Exponer puerto 8080 (Railway lo requiere)
EXPOSE 8080

# Comando por defecto
CMD ["nginx", "-g", "daemon off;"]