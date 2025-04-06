import pytest
from django.template import Context, Template
from mindjunkies.courses.templatetags import courses_tags


@pytest.mark.django_db
def test_markdown_filter():
    """Test the markdown filter."""
    markdown_text = "# This is a heading"
    template_code = "{% load courses_tags %}{{ markdown_text|markdown }}"
    template = Template(template_code)
    context = Context({"markdown_text": markdown_text})
    rendered = template.render(context)

    assert "<h1>" in rendered
    assert "<h1>This is a heading</h1>" in rendered


@pytest.mark.django_db
def test_times_filter():
    """Test the times filter."""
    template_code = "{% load courses_tags %}{% for i in 5|times %}{{ i }}{% endfor %}"
    template = Template(template_code)
    context = Context({})
    rendered = template.render(context)

    assert rendered == "01234"


@pytest.mark.django_db
def test_subtract_filter():
    """Test the subtract filter."""
    template_code = "{% load courses_tags %}{{ 10|subtract:4 }}"
    template = Template(template_code)
    context = Context({})
    rendered = template.render(context)

    assert rendered == "6"
