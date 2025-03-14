import time
import uuid

from authlib.jose import jwt


class JaaSJwtBuilder:
    """The JaaSJwtBuilder class helps with the generation of the JaaS JWT."""

    EXP_TIME_DELAY_SEC = 7200  # Used as a delay for the exp claim value.

    NBF_TIME_DELAY_SEC = 10  # Used as a delay for the nbf claim value.

    def __init__(self) -> None:
        self.header = {"alg": "RS256"}
        self.user_claims = {}
        self.feature_claims = {}
        self.payload_claims = {}

    def with_defaults(self):
        """Returns the JaaSJwtBuilder with default valued claims."""
        return (
            self.with_exp_time(int(time.time() + JaaSJwtBuilder.EXP_TIME_DELAY_SEC))
            .with_nbf_time(int(time.time() - JaaSJwtBuilder.NBF_TIME_DELAY_SEC))
            .with_live_streaming_enabled(True)
            .with_recording_enabled(True)
            .with_outbound_call_enabled(True)
            .with_sip_outbound_call_enabled(True)
            .with_transcription_enabled(True)
            .with_moderator(True)
            .with_room_name("*")
            .with_user_id(str(uuid.uuid4()))
        )

    def with_api_key(self, api_key):
        """Returns the JaaSJwtBuilder with the kid claim(apiKey) set."""

        self.header["kid"] = api_key
        return self

    def with_user_avatar(self, avatar_url):
        """Returns the JaaSJwtBuilder with the avatar claim set."""

        self.user_claims["avatar"] = avatar_url
        return self

    def with_moderator(self, is_moderator):
        """Returns the JaaSJwtBuilder with the moderator claim set."""

        self.user_claims["moderator"] = "true" if is_moderator else "false"
        return self

    def with_user_name(self, user_name):
        """Returns the JaaSJwtBuilder with the name claim set."""

        self.user_claims["name"] = user_name
        return self

    def with_user_email(self, user_email):
        """Returns the JaaSJwtBuilder with the email claim set."""

        self.user_claims["email"] = user_email
        return self

    def with_live_streaming_enabled(self, is_enabled):
        """Returns the JaaSJwtBuilder with the livestreaming claim set."""

        self.feature_claims["livestreaming"] = "true" if is_enabled else "false"
        return self

    def with_recording_enabled(self, is_enabled):
        """Returns the JaaSJwtBuilder with the recording claim set."""

        self.feature_claims["recording"] = "true" if is_enabled else "false"
        return self

    def with_transcription_enabled(self, is_enabled):
        """Returns the JaaSJwtBuilder with the transcription claim set."""

        self.feature_claims["transcription"] = "true" if is_enabled else "false"
        return self

    def with_sip_outbound_call_enabled(self, is_enabled):
        """Returns the JaaSJwtBuilder with the transcription claim set."""

        self.feature_claims["sip-outbound-call"] = "true" if is_enabled else "false"
        return self

    def with_outbound_call_enabled(self, is_enabled):
        """Returns the JaaSJwtBuilder with the outbound-call claim set."""

        self.feature_claims["outbound-call"] = "true" if is_enabled else "false"
        return self

    def with_exp_time(self, exp_time):
        """
        Returns the JaaSJwtBuilder with exp claim set. Use the defaults, you won't have to change this value too much.
        """

        self.payload_claims["exp"] = exp_time
        return self

    def with_nbf_time(self, nbf_time):
        """
        Returns the JaaSJwtBuilder with nbf claim set. Use the defaults, you won't have to change this value too much.
        """

        self.payload_claims["nbfTime"] = nbf_time
        return self

    def with_room_name(self, room_name):
        """Returns the JaaSJwtBuilder with room claim set."""

        self.payload_claims["room"] = room_name
        return self

    def with_app_id(self, app_id):
        """Returns the JaaSJwtBuilder with the sub_claim set."""
        self.payload_claims["sub"] = app_id
        return self

    def with_user_id(self, user_id):
        """Returns the JaaSJwtBuilder with the id claim set."""

        self.user_claims["id"] = user_id
        return self

    def sign_with(self, key):
        """Returns a signed JWT."""

        context = {"user": self.user_claims, "features": self.feature_claims}
        self.payload_claims["context"] = context
        self.payload_claims["iss"] = "chat"
        self.payload_claims["aud"] = "jitsi"
        return jwt.encode(self.header, self.payload_claims, key)
