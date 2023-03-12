from src.image_to_text.utils import prepare_image


def test_prepare_image(image, request):
    image = request.getfixturevalue("image")
    result = prepare_image(image)
    assert result.mode == "L"
