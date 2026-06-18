# Imagen oficial de Nginx, versión alpine = aún más ligera que slim
FROM nginx:alpine

# Eliminamos la configuración por defecto que trae la imagen
RUN rm /etc/nginx/conf.d/default.conf

# Copiamos nuestra configuración personalizada
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
