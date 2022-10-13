from django import forms
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from wagtail import blocks
from wagtail.blocks import CharBlock, RawHTMLBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Collection


class InlineImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(label=_("Image"))
    caption = CharBlock(required=False, label=_("Caption"))
    float = blocks.ChoiceBlock(
        required=False,
        choices=[("right", _("Right")), ("left", _("Left")), ("center", _("Center"))],
        default="right",
        label=_("Float"),
    )
    size = blocks.ChoiceBlock(
        required=False,
        choices=[("small", _("Small")), ("medium", _("Medium")), ("large", _("Large"))],
        default="small",
        label=_("Size"),
    )

    class Meta:
        icon = "image"


class InlineVideoBlock(blocks.StructBlock):
    video = EmbedBlock(label=_("Video Url"))
    caption = CharBlock(required=False, label=_("Caption"))
    float = blocks.ChoiceBlock(
        required=False,
        choices=[("right", _("Right")), ("left", _("Left")), ("center", _("Center"))],
        default="right",
        label=_("Float"),
    )
    size = blocks.ChoiceBlock(
        required=False,
        choices=[("small", _("Small")), ("medium", _("Medium")), ("large", _("Large"))],
        default="small",
        label=_("Size"),
    )

    class Meta:
        icon = "media"


class InArticleGoogleAdBlock(blocks.StructBlock):
    ad_type = blocks.ChoiceBlock(
        required=True,
        choices=[("google_ad", _("Google Ad")), ("self_serve_ad", _("Self Serve Ad"))],
        label=_("Ad type"),
    )

    class Meta:
        icon = "ab-ads"


class InlineTweetBlock(blocks.StructBlock):
    tweet_url = EmbedBlock(required=True, help_text=_("Paste the url of the tweet."))

    class Meta:
        icon = "ab-twitter"


class InlinePodcastBlock(blocks.StructBlock):
    podcast_url = EmbedBlock(
        required=True,
        help_text=_("Paste the url of the podcast. Supports spotify and soundcloud only."),
    )

    class Meta:
        icon = "ab-podcast"


class HTMLEmbedBlock(blocks.StructBlock):
    embed_html = RawHTMLBlock(
        required=True,
        help_text=_(
            "Paste embed html here. Used for embedding Facebook/Instagram posts, Apple Podcasts or any other raw html embeds."
        ),
    )

    class Meta:
        icon = "code"


class CollectionChooserBlock(blocks.FieldBlock):
    """
    Enables choosing a wagtail Collection in the streamfield.
    """

    target_model = Collection
    widget = forms.Select

    def __init__(self, required=False, label=None, help_text=None, *args, **kwargs):
        self._required = required
        self._help_text = help_text
        self._label = label
        super().__init__(*args, **kwargs)

    @cached_property
    def field(self):
        return forms.ModelChoiceField(
            queryset=self.target_model.objects.all().order_by("name"),
            widget=self.widget,
            required=self._required,
            label=self._label,
            help_text=self._help_text,
        )

    def to_python(self, value):
        """
        Convert the serialized value back into a python object.
        """
        if isinstance(value, int):
            return self.target_model.objects.get(pk=value)
        return value

    def get_prep_value(self, value):
        """
        Serialize the model in a form suitable for wagtail's JSON-ish streamfield
        """
        if isinstance(value, self.target_model):
            return value.pk
        return value


class InlineCarousalBlock(blocks.StructBlock):
    collection = CollectionChooserBlock(
        required=True, help_text=_("Choose the collection of images to be displayed as carousal.")
    )
    slides_to_show = blocks.FloatBlock(
        required=True,
        max_value=5,
        min_value=1,
        help_text=_("Select the number of images to be shown in one frame."),
    )
    slides_to_scroll = blocks.FloatBlock(
        required=True,
        max_value=5,
        min_value=1,
        help_text=_("Select the number of slides to be scrolled in one press."),
    )

    class Meta:
        icon = "image"


class InlineImageGalleryBlock(blocks.StructBlock):
    collection = CollectionChooserBlock(
        required=True, help_text=_("Choose the collection of images to be displayed as a gallery.")
    )

    class Meta:
        icon = "image"
