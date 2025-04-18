from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import ForumTopic


@registry.register_document
class ForumTopicDocument(Document):
    class Index:
        name = "forumtopic"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = ForumTopic
        fields = ["title", "content"]