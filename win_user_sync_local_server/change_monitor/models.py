from django.db import models


class RefreshToken(models.Model):
    token = models.CharField(max_length=2560)
    expires_in = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_valid():
        refresh_token = RefreshToken.objects.latest('created_at')
        # Check if token is expired
        if refresh_token.created_at + timezone.timedelta(seconds=refresh_token.expires_in) < timezone.now():
            refresh_token = token_obtainer.get_refresh_token()

    def __str__(self):
        return self.token


