# uploader/oidc.py

from django.contrib.auth.mixins import LoginRequiredMixin

class OIDCLoginRequiredMixin(LoginRequiredMixin):
    """
    A simple LoginRequiredMixin. For this standalone project, it just ensures
    a user is logged in via the standard Django session, which OIDC will create.
    """
    pass