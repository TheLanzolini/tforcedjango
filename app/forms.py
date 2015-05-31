"""
Definition of forms.
"""

from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

try:
    from django.utils.timezone import now
except ImportError:
    from datetime.datetime import now  # noqa

from podcasting.utils.widgets import CustomAdminThumbnailWidget

from app.utils.twitter import can_tweet
from app.models import Profile, Episode, Show
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.instance.pk and self.instance.user:
            self.fields['user'].initial = self.instance.username
        else:
            self.fields['user'] = forms.ModelChoiceField(queryset=User.objects.filter(profile=None))
        if self.instance.pk and not self.instance.user:
            self.fields['placeheld'].required = True
            self.fields['placeheld'].initial = True
            self.fields['placeheld'].widget = forms.BooleanField({ 'checked': 'true', 'disabled': 'disabled'})
            self.fields['placeholderName'].required = True

    #fullname = forms.C
    class Meta:
        model = Profile
        fields = [ 'user',
                  'userLevel', 
                  'firstName', 
                  'lastName', 
                  'birthday',
                  'lanzobotpts',
                  'avatar',
                  'city',
                  'placeheld',
                  'placeholderName',
                  'bio']

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        user = cleaned_data.get("user")
        placeheld = cleaned_data.get("placeheld")
        pName = cleaned_data.get("placeholderName")
        if not user:
            if not placeheld:
                self.add_error(ValidationError(_('Select a username or mark the Placeheld field as true.'), code='invalid'), params = None)
            pass
        pass
        return cleaned_data         


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class BaseShowForm(forms.ModelForm):

    original_image = forms.ImageField(
        widget=CustomAdminThumbnailWidget,
        help_text=Show._meta.get_field("original_image").help_text)

    publish = forms.BooleanField(
        required=False,
        help_text=_("Checking this will publish this show on the site, no turning back."),
    )



    class Meta:
        model = Show
        fields = [
            "original_image",
            "author_text",
            "owner",
            "editor_email",
            "webmaster_email",
            "title", "subtitle", "description",
            "twitter_tweet_prefix",
            "feedburner", "itunes",
            "keywords", "organization", "license",
            "explicit", "link",
            "on_itunes",
            "publish",
            "members",
        ]
        if "taggit" in settings.INSTALLED_APPS:
            fields.append("tags")


class ShowAddForm(BaseShowForm):

    def clean_publish(self):
        if self.cleaned_data["publish"]:
            self.instance.published = now()


class ShowChangeForm(BaseShowForm):

    def __init__(self, *args, **kwargs):
        super(ShowChangeForm, self).__init__(*args, **kwargs)
        self.fields["publish"].initial = bool(self.instance.published)

    def clean_publish(self):
        # clean_publish is called twice, skip the first time when instance is unset
        if not self.instance.pk:
            return
        # do nothing if already published
        if self.instance.published:
            return
        if self.cleaned_data["publish"]:
            self.instance.published = now()


class BaseEpisodeForm(forms.ModelForm):

    original_image = forms.ImageField(
        widget=CustomAdminThumbnailWidget,
        help_text=Episode._meta.get_field("original_image").help_text)

    publish = forms.BooleanField(
        required=False,
        help_text=_("Checking this will publish this episode on the site, no turning back."),
    )

    if can_tweet():
        tweet = forms.BooleanField(
            required=False,
            help_text=_("Checking this will send out a tweet announcing the episode."))

    class Meta:
        model = Episode
        fields = [
            "original_image",
            "author_text",
            "title", "subtitle",
            "description",
            "tracklist",
            "url",
            "youtube_url",
            "image_url",
            "hours", "minutes", "seconds",
            "publish",
            "url",
            "mime",
            "size",
            "bitrate",
            "sample",
            "channel",
            "duration",
            "members",
        ]
        if "taggit" in settings.INSTALLED_APPS:
            fields.append("tags")
        extra_fields_itunes = [
            "keywords",
            "explicit",
            "block",
        ]
        required_fields_itunes = [
            "author_text",
            "subtitle",
            "description",
            "original_image",
            "keywords",
            "explicit",
        ]

    def save(self):
        instance = self.instance
        if instance.pk:
            membersAdded = True
            #nummembers = len(instance.members.all())
            untaggedMembers = instance.members.exclude(user__username__in=[item.get('name') for item in instances.tags.all().values('name')])
            for member in untaggedMembers:
                instance.tags.add(member.username)
        instance = super(BaseEpisodeForm, self).save()
        if not membersAdded:
            untaggedmembers = instance.members.exclude(user__username__in=[item.get('name') for item in instances.tags.all().values('name')])
            for member in untaggedMembers:
                instance.tags.add(member.username)
        if can_tweet() and self.cleaned_data["tweet"]:
            instance.tweet()

        return instance

    def validate_published(self):
        if not self.instance.enclosure_set.count() or not self.instance.embedmedia_set.count():
            raise forms.ValidationError(
                _("An episode must have at least one enclosure or media file before publishing.\n "
                  "Uncheck, save this episode, and add an encoslure before publishing."))
        elif not self.instance.is_show_published:
            raise forms.ValidationError(_("The show for this episode is not yet published"))
        self.instance.published = now()


class EpisodeChangeForm(BaseEpisodeForm):

    def __init__(self, *args, **kwargs):
        super(EpisodeChangeForm, self).__init__(*args, **kwargs)
        self.fields["publish"].initial = bool(self.instance.published)

    def clean_publish(self):
        # clean_publish is called twice, skip the first time when instance is unset
        if not self.instance.pk:
            return
        # do nothing if already published
        if self.instance.published:
            return
        if self.cleaned_data["publish"]:
            self.validate_published()


class EpisodeITunesChangeForm(EpisodeChangeForm):
    def __init__(self, *args, **kwargs):
        super(EpisodeITunesChangeForm, self).__init__(*args, **kwargs)
        for key in self.Meta.required_fields_itunes:
            self.fields[key].required = True

    class Meta(EpisodeChangeForm.Meta):
        fields = EpisodeChangeForm.Meta.fields + EpisodeChangeForm.Meta.extra_fields_itunes


class EpisodeAddForm(BaseEpisodeForm):

    def clean_publish(self):
        if self.cleaned_data["publish"]:
            self.validate_published()


class EpisodeITunesAddForm(EpisodeAddForm):
    def __init__(self, *args, **kwargs):
        super(EpisodeITunesAddForm, self).__init__(*args, **kwargs)
        for key in self.Meta.required_fields_itunes:
            self.fields[key].required = True

    class Meta(EpisodeAddForm.Meta):
        fields = EpisodeAddForm.Meta.fields + EpisodeAddForm.Meta.extra_fields_itunes



class AdminShowForm(forms.ModelForm):

    publish = forms.BooleanField(
        label=_("publish"),
        required=False,
        help_text=_("Checking this will publish this show on the site, no turning back."),
    )

    class Meta:
        model = Show
        fields = [
            #"sites",
            "original_image",
            "author_text",
            "owner",
            "editor_email",
            "webmaster_email",
            "title", "subtitle", "description",
            "twitter_tweet_prefix",
            "feedburner", "itunes",
            "keywords", "organization", "license",
            "explicit", "link",
            "on_itunes",
            "publish",
        ]
        if "taggit" in settings.INSTALLED_APPS:
            fields.append("tags")

    def __init__(self, *args, **kwargs):
        super(AdminShowForm, self).__init__(*args, **kwargs)
        self.fields["publish"].initial = bool(self.instance.published)

    def clean_publish(self):
        # clean_publish is called twice, skip the first time when instance is unset
        if not self.instance.pk:
            return
        # do nothing if already published
        if self.instance.published:
            return
        if self.cleaned_data["publish"]:
            self.instance.published = now()


class AdminEpisodeForm(forms.ModelForm):

    publish = forms.BooleanField(
        label=_("publish"),
        required=False,
        help_text=_("Checking this will publish this episode on the site, no turning back."))

    if can_tweet():
        tweet = forms.BooleanField(
            required=False,
            help_text=_("Checking this will send out a tweet announcing the episode."))

    class Meta:
        model = Episode
        fields = [
            "shows",
            "original_image",
            "members",
            "author_text",
            "title", "subtitle",
            "description",
            "tracklist",
            "hours", "minutes", "seconds",
            "publish",
            "keywords",
            "explicit",
            "block",
        ]
        if "taggit" in settings.INSTALLED_APPS:
            fields.append("tags")

    def __init__(self, *args, **kwargs):
        super(AdminEpisodeForm, self).__init__(*args, **kwargs)
        self.fields["publish"].initial = bool(self.instance.published)

    def validate_published(self):
        '''if not self.instance.enclosure_set.count() and not self.instance.embedmedia_set.count():
            raise forms.ValidationError(
                _("An episode must have at least one enclosure or media file before publishing.\n "
                  "Uncheck, save this episode, and add an encoslure before publishing."))
        elif not self.instance.is_show_published:
            raise forms.ValidationError(_("The show for this episode is not yet published"))'''
        self.instance.published = now()

    def clean_publish(self):
        # clean_publish is called twice, skip the first time when instance is unset
        if not self.instance.pk:
            return
        # do nothing if already published
        if self.instance.published:
            return
        if self.cleaned_data["publish"]:
            self.validate_published()

    def save(self):
        episode = super(AdminEpisodeForm, self).save(commit=False)
        duration = (episode.hours *3600) + (episode.minutes * 60) + episode.seconds
        episode.duration = duration #Point left off
        episode.size = 0 #TODO JF This is a hack we need to determine the size from URL?
        episode.save()

        if can_tweet() and self.cleaned_data["tweet"]:
            episode.tweet()

        return episode
