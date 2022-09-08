from src.editor_image_size.utils import (  # pylint: disable=import-error
    with_expanded_images,
    with_shrunken_images,
)


def test_with_shrunken_images():
    assert (
        with_shrunken_images('<img src="foo.jpg"/>')
        == '<img src="foo.jpg" data-editor-shrink="true"/>'
    )

    assert (
        with_shrunken_images('<img src="foo.jpg">')
        == '<img src="foo.jpg" data-editor-shrink="true">'
    )

    # with ">" in the src attribute
    assert (
        with_shrunken_images('<img src=">.jpg">')
        == '<img src=">.jpg" data-editor-shrink="true">'
    )

    # image tags with ">" in attributes other than src are ignored
    assert (
        with_shrunken_images('<img src="foo.jpg" class=">">')
        == '<img src="foo.jpg" class=">">'
    )

    # with regex special characters in image name
    assert (
        with_shrunken_images('<img src="++.jpg"/>')
        == '<img src="++.jpg" data-editor-shrink="true"/>'
    )


def test_with_shrunken_images_with_mutliple_images():
    assert with_shrunken_images('<img src="1.png"><img src="2.png">') == (
        '<img src="1.png" data-editor-shrink="true">'
        '<img src="2.png" data-editor-shrink="true">'
    )


def test_with_expanded_images():
    assert (
        with_expanded_images('<img src="foo.jpg" data-editor-shrink="true"/>')
        == '<img src="foo.jpg"/>'
    )

    assert (
        with_expanded_images('<img src="foo.jpg" data-editor-shrink="true">')
        == '<img src="foo.jpg">'
    )

    # with ">" in the src attribute
    assert (
        with_expanded_images('<img src=">.jpg" data-editor-shrink="true">')
        == '<img src=">.jpg">'
    )

    # image tags with ">" in attributes other than src are ignored
    assert (
        with_expanded_images('<img src="foo.jpg" class=">">')
        == '<img src="foo.jpg" class=">">'
    )

    # with regex special characters in image name
    assert (
        with_expanded_images('<img src="++.jpg" data-editor-shrink="true"/>')
        == '<img src="++.jpg"/>'
    )


def test_with_expanded_images_with_mutliple_images():
    assert with_expanded_images(
        '<img src="1.png" data-editor-shrink="true">'
        '<img src="2.png" data-editor-shrink="true">'
    ) == ('<img src="1.png"><img src="2.png">')
