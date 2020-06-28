from datetime import datetime
from django.db import models


class DecodedJWT(models.Model):
    """
    The purpose of this class is to store the two JWT claims and the Payload.

    It was mainly created for debugging purposes and to simulate
    a server that would consume the request data and store to a database.
    """

    iat = models.IntegerField()
    jti = models.TextField()
    payload = models.TextField()

    def __str__(self):
        return f"JWT Issued at { datetime.fromtimestamp(self.iat).strftime('%B %d %Y, %H:%M:%S') } with the Payload: { self.payload }"
