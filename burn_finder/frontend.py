import cv2
from pygrabber.dshow_graph import FilterGraph

def GetActualListCams():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    try:
        devices_names = FilterGraph().get_input_devices()
    except Exception as e:
        return []
    dev_port = 0
    working_cams = []
    while dev_port < len(devices_names):
        camera = cv2.VideoCapture(dev_port)
        if camera.isOpened():
            is_reading, img = camera.read()
            if is_reading:
                working_cams.append(dev_port)
        dev_port +=1
    cams = [(devices_names[index], index) for index in working_cams]
    return cams

def GetCameraInput(device_id):
    """
    Returns the camera input.
    """
    return cv2.VideoCapture(device_id)