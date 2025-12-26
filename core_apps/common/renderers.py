import json
from typing import Any, Optional, Union

from django.utils.translation import gettext_lazy as _
from rest_framework.renderers import JSONRenderer


class GenericJSONRenderer(JSONRenderer):
    charset = "utf-8"
    object_label = "object"

    def render(
        self,
        data: Any,
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[str] = None,
    ) -> Union[bytes, str]:

        #renderer_context has
        #renderer_context = {
        #      "request": < Request object >,
        #       "response": < Response tatus = 200 >,
        #       "view": < UserDetailView instance >,
        #       "args": (),
        #       "kwargs": {"id": 1},
        #       }


        if renderer_context is None:
            renderer_context = {}

        view = renderer_context.get("view")

        #hasattr(object, "name") checks whether an object has a particular attribute or not.
        if hasattr(view, "object_label"):
            object_label = view.object_label
        else:
            object_label = self.object_label

        response = renderer_context.get("response")
        if not response:
            raise ValueError(_("Response not found in renderer context"))

        status_code = response.status_code

        errors = data.get("errors", None)

        if errors is not None:
            return super(GenericJSONRenderer, self).render(data)
        #The reason is because the error message should be simple and clear that's why we don't use our custom renderer here
        #This line converts the response data into JSON and encodes it as UTF-8 bytes so Django REST Framework can send it as an HTTP response.
        #This is normal behaviour
        #All API responses are converted to bytes before being sent over HTTP.
        return json.dumps({"status_code": status_code, object_label: data}).encode(
            self.charset
        )