import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class VisionCaptioner:
    """
    This object is used to get a caption for an image using the
    endpoint of BLIP deployed on Azure.
    """

    def __init__(self):
        self._url = "https://vision-captions.purplesky-efe9a7f4.eastus.azurecontainerapps.io"  # noqa
        self._caption_endpoint = "/caption"

    @staticmethod
    def _get_image(image_url: str) -> bytes:
        """
        This method is used to get an image from a URL, either local
        or remote.

        Parameters
        ----------
        image_url : str
            The URL of the image.

        Returns
        -------
        bytes
            The image.
        """
        if image_url.startswith("http"):
            response = requests.get(image_url)
            if response.status_code != 200:
                raise Exception("Error getting image")
            return response.content
        else:
            with open(image_url, "rb") as image:
                return image.read()

    def get_caption(self, image: bytes) -> str:
        """
        This method is used to get a caption for an image using the
        endpoint of BLIP deployed on Azure.

        Parameters
        ----------
        image : bytes
            The image to get a caption for.

        Returns
        -------
        str
            The caption for the image.
        """
        # Check if the file is local or remote
        files = {"image": ("image", self._get_image(image))}
        multipart_data = MultipartEncoder(fields=files)
        headers = {
            "Accept": "application/json",
            "Content-Type": multipart_data.content_type,
        }
        response = requests.post(
            f"{self._url}/{self._caption_endpoint}",
            data=multipart_data,
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception("Error getting caption for image")
        return response.json()
