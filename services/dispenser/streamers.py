import os

from time import time
from datetime import datetime, timezone

from hashlib import md5, sha1
from base64 import b64encode, encodebytes

import hmac
import grpc

import tools
logger = tools.get_logger()


class BaseStreamer(object):

    @classmethod
    def factory(cls, service):
        for streamer in cls.__subclasses__():
            if streamer.__name__.lower() == service.handler:
                return streamer(service)
        raise NotImplementedError

    def __init__(self, service):
        self._service = service

    def __repr__(self):
        return self.__class__.__name__

    def create_live_url(self, request_id, ip_address, stream_name, login):
        raise NotImplementedError

    def create_dvr_url(self, request_id, ip_address, stream_name, dvr_app, time_start, duration, force_hls, login, platform, device_class):
        logger.debug(f"DVR service \'{self._service.handler}\' is not implemented")
        return
#        raise NotImplementedError

    def create_movie_url(self, request_id, ip_address, filename, login):
        raise NotImplementedError


class CDNvideo(BaseStreamer):

    def create_live_url(self, request_id, ip_address, stream_name, login):
        expires = int(time()) + (3600 * 6)
        path, _, reminder = stream_name.strip("/").rpartition("/")
        signed = b64encode(
            md5(f"{os.environ.get('CDNVIDEO_KEY')}:{expires}:{ip_address}:/{path}".encode()).digest()
        ).decode().replace("+", "-").replace("/", "_").replace("=", "")
        return f"{self._service.address}/{path}/{reminder}?md5={signed}&e={expires}"

    def create_dvr_url(self, request_id, ip_address, stream_name, dvr_app, time_start, duration, force_hls, login, platform, device_class):
        dvr_app_stream = f"{dvr_app}/{stream_name}"
        if platform == 'moovi':
            duration_timeshift = 3600 * 3 + 600
            duration_range = 3600 * 3 + 600
        else:
            duration_timeshift = duration
            duration_range = duration
        if (time_start + duration_timeshift) > time():
            if device_class == 'SmartTV' and ((time_start + duration + 60) < time()):
                duration = abs(int(time()) - int(time_start) - 60)
                path = f"/{dvr_app_stream}/playlist_dvr_range-{time_start}-{duration}.m3u8"
            else:
                time_start = abs(int(time()) - int(time_start))
                path = f"/{dvr_app_stream}/playlist_dvr_timeshift-{time_start}-60.m3u8"
        else:
            path = f"/{dvr_app_stream}/playlist_dvr_range-{time_start}-{duration_range}.m3u8"
        url = f"{self._service.address}{path}"
        logger.debug(f"login: {login}, device_class: {device_class}, time_start: {time_start}, duration_timeshift: {duration_timeshift}")
        logger.debug(f"DVR stream URL (CDNvideo): {url}")
        return url


class CDNGCL(BaseStreamer):

    def auth(self, ip_address, path, expires):
        expires += int(time())
        secret = os.environ.get('CDNGCL_KEY')
        signed = encodebytes(md5(f"{expires}{ip_address} {secret}".encode()).digest()).decode().replace("\n", "").replace("+", "-").replace("/", "_").replace("=", "")
        return f"?md5={signed}&expires={expires}"

    def create_live_url(self, request_id, ip_address, stream_name, login):
        path = f"/{stream_name.strip('/')}"
        expires = 3600 * 6
        logger.debug(f"create_live_url: path {path}")
        return f"{self._service.address}{path}{self.auth(ip_address, path, expires)}"

    def create_dvr_url(self, request_id, ip_address, stream_name, dvr_app, time_start, duration, force_hls, login, platform, device_class):
        dvr_app_stream = f"{dvr_app}/{stream_name}"
        if platform == 'moovi':
            duration_timeshift = 3600 * 3 + 600
            duration_range = 3600 * 3 + 600
        else:
            duration_timeshift = duration
            duration_range = duration
        if (time_start + duration_timeshift) > time():
            if device_class == 'SmartTV' and ((time_start + duration + 60) < time()):
                duration = abs(int(time()) - int(time_start) - 60)
                path = f"/{dvr_app_stream}/playlist_dvr_range-{time_start}-{duration}.m3u8"
            else:
                time_start = abs(int(time()) - int(time_start))
                path = f"/{dvr_app_stream}/playlist_dvr_timeshift-{time_start}-60.m3u8"
        else:
            path = f"/{dvr_app_stream}/playlist_dvr_range-{time_start}-{duration_range}.m3u8"
        expires = duration_range
        url = f"{self._service.address}{path}{self.auth(ip_address, path, expires)}"
        logger.debug(f"login: {login}, device_class: {device_class}, time_start: {time_start}, duration_timeshift: {duration_timeshift}")
        logger.debug(f"DVR stream URL (CDN GCL): {url}")
        return url


class Ngenix(BaseStreamer):

    def create_live_url(self, request_id, ip_address, stream_name, login):
        path, _, reminder = stream_name.strip("/").rpartition("/")
        key = os.environ.get('NGENIX_KEY')
        if key:
            nvb = int(time()) # not valid before current time
            nva = nvb + (5 * 60) # valid for 5 minutes
            url = f"/{path}/{reminder}?nvb={nvb}&nva={nva}"
            token = f"0{hmac.new(key.encode(), url.encode(), sha1).hexdigest()[:20]}"
            return f"{self._service.address}{url}&token={token}"
        return f"{self._service.address}/{path}/{reminder}"


class Nimble(BaseStreamer):

    def AuthSign(self, request_id):
        server_time = datetime.now(timezone.utc).strftime("%m/%d/%Y %I:%M:%S %p")
        hashed = b64encode(
            md5(f"{request_id}{os.environ.get('NIMBLE_KEY')}{server_time}2".encode()).digest()
        ).decode()
        auth_sign = b64encode(
            f"hash_value={hashed}&server_time={server_time}&validminutes=2&id={request_id}".encode()
        ).decode()
        return f"?wmsAuthSign={auth_sign}&token={request_id}"

    def AuthSignNew(self, request_id, ip_address, valid_min):
        server_time = datetime.now(timezone.utc).strftime("%m/%d/%Y %I:%M:%S %p")
        hashed = b64encode(md5(f"{ip_address}{request_id}{os.environ.get('NIMBLE_KEY')}{server_time}{valid_min}".encode()).digest()).decode()
        auth_sign = b64encode(f"server_time={server_time}&hash_value={hashed}&validminutes={valid_min}&id={request_id}&checkip=true".encode()).decode()
        return f"?wmsAuthSign={auth_sign}&token={request_id}"

    def create_live_url(self, request_id, ip_address, stream_name, login):
        stream_name = stream_name.strip("/")
        if login in [ 215638 ]:
            auth_sign = self.AuthSignNew(request_id, ip_address, 2)
        else:
            auth_sign = self.AuthSign(request_id)
        return f"{self._service.address}/{stream_name}{auth_sign}"

    def create_movie_url(self, request_id, ip_address, filename, login):
        return self.create_live_url(request_id, ip_address, filename, login)

    def create_dvr_url(self, request_id, ip_address, stream_name, dvr_app, time_start, duration, force_hls, login, platform, device_class):
        dvr_app_stream = f"{dvr_app}/{stream_name}"
        if login in [ 109910 ]:
            auth_sign = self.AuthSignNew(request_id, ip_address, 2)
        else:
            auth_sign = self.AuthSign(request_id)
        if platform == 'moovi':
            duration_timeshift = 3600 * 3 + 600
            duration_range = 3600 * 3 + 600
        else:
            duration_timeshift = duration
            duration_range = duration
        if (time_start + duration_timeshift) > time():
            if device_class == 'SmartTV' and ((time_start + duration + 60) < time()):
                duration = abs(int(time()) - int(time_start) - 60)
                url = f"{self._service.address}/{dvr_app_stream}/playlist_dvr_range-{time_start}-{duration}.m3u8{auth_sign}"
            else:
                time_start = abs(int(time()) - int(time_start))
                url = f"{self._service.address}/{dvr_app_stream}/playlist_dvr_timeshift-{time_start}-60.m3u8{auth_sign}"
        else:
            url = f"{self._service.address}/{dvr_app_stream}/playlist_dvr_range-{time_start}-{duration_range}.m3u8{auth_sign}"
        logger.debug(f"login: {login}, device_class: {device_class}, time_start: {time_start}, duration_timeshift: {duration_timeshift}")
        logger.debug(f"DVR stream URL (Nimble): {url}")
        return url


class Flussonic(BaseStreamer):

    def create_live_url(self, request_id, ip_address, stream_name, login):
        return f"{self._service.address}/{stream_name}?token={request_id}"

    def create_dvr_url(self, request_id, ip_address, stream_name, dvr_app, time_start, duration, force_hls, login, platform, device_class):
        if force_hls:
            url = f"{self._service.address}/{stream_name}/archive-{time_start}-{duration}.m3u8?token={request_id}"
        else:
            url = f"{self._service.address}/{stream_name}/timeshift_abs-{time_start}.ts?token={request_id}"
        logger.debug(f"DVR stream URL (Flussonic): {url}")
        return url


if __name__ == "__main__":
    BaseStreamer.factory("nimble")
