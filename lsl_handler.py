from pylsl import StreamInlet, resolve_stream
import threading

class LSLHandler:
    def __init__(self, stream_name=None):
        self.inlet = None
        if stream_name:
            self.set_stream(stream_name)
        self.current_fire_rate = None
        self.thread = None
        self.running = False

    @staticmethod
    def get_inlet(stream_name):
        streams = resolve_stream()
        for stream in streams:
            if stream.name() == stream_name:
                return StreamInlet(stream)
        raise RuntimeError(f"No stream found with name {stream_name}")

    def set_stream(self, stream_name):
        self.stop()  # Stop the current stream (if it's running)
        self.inlet = self.get_inlet(stream_name)

    def get_power_lsl(self):
        speed, _ = self.inlet.pull_sample()
        return speed[0]

    def get_current_fire_rate(self):
        return self.current_fire_rate

    def update_fire_rate(self):
        while self.running:
            speed = self.get_power_lsl()
            self.current_fire_rate = speed

    def start(self):
        self.stop()  # Stop the current stream (if it's running)
        self.thread = threading.Thread(target=self.update_fire_rate)
        self.running = True
        self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()
                self.thread = None  # Reset the thread to None after stopping it

    def get_available_streams(self):
        streams = resolve_stream()
        return [stream.name() for stream in streams]

    def is_running(self):
        return self.running