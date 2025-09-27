# Dockerfile simple para servir frontend estático con nginx
FROM nginx:alpine

# Elimina la configuración por defecto
RUN rm /etc/nginx/conf.d/default.conf

# Copia tu configuración personalizada PRIMERO
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia SOLO los archivos necesarios para el frontend (no nginx.conf ni Dockerfile)
COPY index.html /public/
COPY css/ /public/css/
COPY js/ /public/js/
COPY images/ /public/images/
COPY fonts/ /public/fonts/
COPY libs/ /public/libs/
COPY templates/ /public/templates/
COPY source/ /public/source/

# Expone el puerto 8080
EXPOSE 8080

# Ejecuta nginx
CMD ["nginx", "-g", "daemon off;"]