class SecurityConfig:
    SECRET_KEY = 'tvGKGnxE_6xmhUHCAir1Vw'
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "8ed-0B6Exefz5esP4lx2jg"
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    WTF_CSRF_ENABLED = False
    JWT_SECRET_KEY = '4rLpZyB4kjDCAAwq2av_9w'
    SECURITY_PASSWORD_SINGLE_HASH = False
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379