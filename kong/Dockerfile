FROM kong:3.9

# Add custom plugin under Kong's Lua plugin path
COPY plugins/custom /usr/local/share/lua/5.1/kong/plugins/custom

# Ensure Kong loads bundled plugins plus our custom one
ENV KONG_PLUGINS=bundled,custom

USER kong
