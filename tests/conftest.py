"""Global fixture functions."""

# pylint: disable = redefined-outer-name

from collections.abc import AsyncGenerator, Generator

import aiohttp
from aioresponses import aioresponses
import pytest

from pyalarmdotcomajax import AlarmController, const as c
from pyalarmdotcomajax.devices import DEVICE_ENDPOINTS, DeviceType
from pyalarmdotcomajax.extensions import CameraSkybellControllerExtension

from .responses import get_http_body_html, get_http_body_json


@pytest.fixture  # type: ignore
def response_mocker() -> Generator:
    """Yield aioresponses."""
    with aioresponses() as mocker:
        yield mocker


@pytest.fixture  # type: ignore
@pytest.mark.asyncio  # type: ignore
async def adc_client() -> AsyncGenerator:
    """Build and return dummy controller for testing without Alarm.com API."""

    async with aiohttp.ClientSession() as websession:
        yield AlarmController(
            username="test-username",
            password="hunter2",
            websession=websession,
            twofactorcookie="test-cookie",
        )


@pytest.fixture  # type: ignore
def all_base_ok_responses(response_mocker: aioresponses) -> None:
    """Shortcut for including all mocked success responses."""

    ############
    ### META ###
    ############

    response_mocker.get(
        url=c.TROUBLECONDITIONS_URL_TEMPLATE.format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("trouble_condition_ok"),
    )
    response_mocker.get(
        url=c.IDENTITIES_URL_TEMPLATE.format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("identity_ok"),
    )

    ###############
    ### DEVICES ###
    ###############

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.SENSOR]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("sensor_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.CAMERA]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("camera_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.GARAGE_DOOR]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("garage_door_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.GATE]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("gate_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.IMAGE_SENSOR]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("image_sensor_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.IMAGE_SENSOR]["additional"][
            "recent_images"
        ].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("image_sensor_data_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.LIGHT]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("light_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.LOCK]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("lock_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.PARTITION]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("partition_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.SYSTEM]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("system_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.THERMOSTAT]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("thermostat_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.WATER_SENSOR]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("water_sensor_ok"),
    )


@pytest.fixture  # type: ignore
def all_extension_ok_responses(response_mocker: aioresponses) -> None:
    """Shortcut for including all mocked success responses."""

    ##################
    ### EXTENSIONS ###
    ##################

    response_mocker.get(
        url=CameraSkybellControllerExtension.ENDPOINT,
        status=200,
        body=get_http_body_html("camera_settings_skybell"),
    )


@pytest.fixture  # type: ignore
def skybell_missing_video_quality_field(response_mocker: aioresponses) -> None:
    """Shortcut for including all mocked success responses."""

    ##################
    ### EXTENSIONS ###
    ##################

    response_mocker.get(
        url=CameraSkybellControllerExtension.ENDPOINT,
        status=200,
        body=get_http_body_html("camera_settings_skybell_missing_video_quality_field"),
    )


@pytest.fixture  # type: ignore
def camera_no_permissions(response_mocker: aioresponses) -> None:
    """No permissions for camera."""

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.CAMERA]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("camera_no_permissions"),
    )


@pytest.fixture  # type: ignore
def all_base_ok_camera_403(response_mocker: aioresponses) -> None:
    """Shortcut for including all mocked success responses."""

    ############
    ### META ###
    ############

    response_mocker.get(
        url=c.TROUBLECONDITIONS_URL_TEMPLATE.format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("trouble_condition_ok"),
    )
    response_mocker.get(
        url=c.IDENTITIES_URL_TEMPLATE.format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("identity_ok"),
    )

    ###############
    ### DEVICES ###
    ###############

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.SENSOR]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("sensor_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.CAMERA]["primary"].format(c.URL_BASE, ""),
        status=403,
        body=get_http_body_html("404"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.GARAGE_DOOR]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("garage_door_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.GATE]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("gate_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.IMAGE_SENSOR]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("image_sensor_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.IMAGE_SENSOR]["additional"][
            "recent_images"
        ].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("image_sensor_data_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.LIGHT]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("light_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.LOCK]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("lock_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.PARTITION]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("partition_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.SYSTEM]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("system_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.THERMOSTAT]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("thermostat_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.WATER_SENSOR]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("water_sensor_ok"),
    )


@pytest.fixture  # type: ignore
def all_base_ok_camera_404(response_mocker: aioresponses) -> None:
    """Shortcut for including all mocked success responses."""

    ############
    ### META ###
    ############

    response_mocker.get(
        url=c.TROUBLECONDITIONS_URL_TEMPLATE.format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("trouble_condition_ok"),
    )
    response_mocker.get(
        url=c.IDENTITIES_URL_TEMPLATE.format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("identity_ok"),
    )

    ###############
    ### DEVICES ###
    ###############

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.SENSOR]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("sensor_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.CAMERA]["primary"].format(c.URL_BASE, ""),
        status=404,
        body=get_http_body_html("404"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.GARAGE_DOOR]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("garage_door_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.GATE]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("gate_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.IMAGE_SENSOR]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("image_sensor_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.IMAGE_SENSOR]["additional"][
            "recent_images"
        ].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("image_sensor_data_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.LIGHT]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("light_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.LOCK]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("lock_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.PARTITION]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("partition_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.SYSTEM]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("system_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.THERMOSTAT]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("thermostat_ok"),
    )

    response_mocker.get(
        url=DEVICE_ENDPOINTS[DeviceType.WATER_SENSOR]["primary"].format(c.URL_BASE, ""),
        status=200,
        body=get_http_body_json("water_sensor_ok"),
    )
