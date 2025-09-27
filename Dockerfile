# Dockerfile simple para servir frontend estático con nginx
FROM nginx:alpine

# Elimina la configuración por defecto
RUN rm /etc/nginx/conf.d/default.conf

# Copia tu configuración personalizada
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia todos los archivos estáticos
COPY . /public

# Expone el puerto 8080
EXPOSE 8080

# Ejecuta nginx
CMD ["nginx", "-g", "daemon off;"]