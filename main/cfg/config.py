class _Config(object):
    # JWT
    JWT_SECRET_KEY = 'A very very secret key!'

    # MySQL Database
    MYSQL_URL = 'mysql://root:123456@localhost:3306/just_blog'

    # Google Login Secret
    GOOGLE_CLIENT_ID = "106660850039-0qrna09hm090hl6n6k9g01ao77fijt2l.apps.googleusercontent.com"
    GOOGLE_PROJECT_ID = "just-blog-namdaoduy"
    GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_TOKEN_URI = "https://www.googleapis.com/oauth2/v3/token"
    GOOGLE_CERT_URL = "https://www.googleapis.com/oauth2/v1/certs"
    GOOGLE_CLIENT_SECRET = "kdhw2N_30s2p8oUvnOJUtfL0"
    GOOGLE_JAVASCRIPT_ORIGIN = "http://localhost:3002"
    GOOGLE_TOKEN_VERIFY_STRING = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s"