import torch
import cv2

models={
'yolo5n' : torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True),
# "yolo5s" : torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True),
# "yolo5m" : torch.hub.load('ultralytics/yolov5', 'yolov5m', pretrained=True),
# "yolo5l" : torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True),
# "yolo5x" : torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)
}
defaultModelType='yolo5n'

def extractObjects(objectString):
    objlist = []
    objects = str(objectString).split('\n')[0].split(',')
    for i in objects[0].split(' ')[4:]:
        objlist.append(i)
    for obj in objects[1:]:
        for i in obj.split()[1:]:
            objlist.append(i)
    return objlist

def detectimage(imagepath,modeltype=defaultModelType):
    img = cv2.imread(imagepath)
    results = models[modeltype](img)
    for i in results.render():
        cv2.imwrite(imagepath,i)
    return [imagepath,extractObjects(str(results))]

def detectvideo(videopath,modeltype=defaultModelType):
    objList=[]
    c=0
    cap = cv2.VideoCapture(videopath)
    framerate=cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frames=[]
    while cap.isOpened():
        c+=1
        ret, frame = cap.read()
        if not ret:
            break
        if c%10==0:
            results = models[modeltype](frame)
            for i in extractObjects(str(results)):
                objList.append(i)
            frame = results.render()[0]
            frames.append(frame)

    out = cv2.VideoWriter(videopath,cv2.VideoWriter_fourcc(*'mp4v'),framerate,(width,height))
    for frame in frames:
        out.write(frame)
    out.release()
    return [videopath, list(set(objList))]


