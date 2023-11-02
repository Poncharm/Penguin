from pylsl import StreamInlet, resolve_stream
import time


def get_inlet(stream_name):
    streams = resolve_stream()
    for stream in streams:
        if stream.name() == stream_name:
            return StreamInlet(stream)
    raise RuntimeError(f"No stream found with name {stream_name}")



def get_power_lsl(inlet):
    speed, timestamp = inlet.pull_sample()
    return speed[0]
