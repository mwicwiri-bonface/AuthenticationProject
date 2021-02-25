from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.conf import settings
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDER_TYPES = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('o', 'Other')
)


class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_sessions', on_delete=models.CASCADE)
    session = models.OneToOneField(Session, related_name='user_sessions', on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.user, self.session.session_key)


class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model."""

    def create_user(self, email, username, password=None):
        """Creates a user profile object."""

        if not email:
            raise ValueError('Users must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)

        user.user_id = -1
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        """Creates and saves a new superuser with given details."""

        user = self.create_user(email=email, username=username, password=password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, null=True)
    email = models.EmailField(_('email'), unique=True)
    gender = models.CharField(
        choices=GENDER_TYPES,
        default='m',
        max_length=2,
        null=True,
        blank=True
    )
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    is_staff = models.BooleanField(_('Staff'), default=False, help_text=_('Means the user has staff privileges, '
                                                                          'when activated'))
    is_superuser = models.BooleanField(_('Super User'), default=False, help_text=_('Means the user has admin'
                                                                                   ' privileges, when activated'))
    is_active = models.BooleanField(_('Status'), default=False, help_text=_('When activated, allows user to login'
                                                                            'when deactivated means user registration '
                                                                            'is not approved'))
    is_archive = models.BooleanField(_('Archive'), default=False, help_text=_('When activated, means use cannot login'))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def has_module_perms(self, app_label):
        return self.is_superuser

    @staticmethod
    def _allow_edit(obj=None):
        if not obj:
            return True
        return not (obj.is_superuser or obj.staff)

    def has_perm(self, request, obj=None):
        return True

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Users/profile_pictures/%Y/%m/', default="Users/profile_pictures/default.jpg")
    bio = models.TextField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=CustomUser)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
