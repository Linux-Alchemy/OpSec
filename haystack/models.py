# event structure

# defining constants for events
EVENT_SSH_FAIL = "ssh_fail"
EVENT_SSH_SUCCESS = "ssh_success"
EVENT_SUDO_FAIL = "sudo_fail"
# EVENT_SUDO_SUCCESS = "sudo_success"

# define structure of the captured info for the detector later
def create_event(timestamp, event_type, username, source_ip=None, raw_line="", service="unknown"):
    return {
        "timestamp": timestamp,
        "event_type": event_type,
        "username": username,
        "source_ip": source_ip,
        "raw_line": raw_line,
        "service": service
    }
