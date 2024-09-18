import cv2
import numpy as np

def open_video_file(filename):
    v = cv2.VideoCapture(filename=filename)
    # 获取视频尺寸
    w = int(v.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(v.get(cv2.CAP_PROP_FRAME_HEIGHT))
    c = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
    
    return h,w,c,v


def extract_bg_color(filename):
    h,w,c,v = open_video_file(filename=filename) 
    frame_rois = []
    rect_rois = []
        
    print(h,w,c)
    
    ret, pre_frame = v.read()
    i = 0
    imCrop = []
    while ret:
        # 读取视频帧
        ret, frame = v.read()
        # 检测视频是否结束
        # diff_frame = cv2.Mat(diff)
        
        if not ret:
            break
        # diff_frame = cv2.absdiff(pre_frame,frame)
        
        cv2.imshow("color",frame)        
        # if cv2.waitKey(1) == "q":
        #     break
        # else:
        
        if cv2.waitKey(100) & 0xFF == ord('s'):
            r = cv2.selectROI("color",frame)
            cv2.waitKey(0)    
            imCrop = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]  
            print(r)
            frame_rois.push(imCrop)
            rect_rois.push(r)
            cv2.imshow("Image", imCrop)
            break
                    
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        
        # cv2.imwrite("./images/"+str(i) +"bg.png",frame)       
        
        i = i + 1
        print("index-sum",i,c)
    
    v.release()
    return imCrop[0] 

def extract_bg(filename):
    h,w,c,v = open_video_file(filename=filename) 
    frame_rois = []
    rect_rois = []
        
    print(h,w,c)
    
    ret, pre_frame = v.read()
    i = 0
    while ret:
        # 读取视频帧
        ret, frame = v.read()
        # 检测视频是否结束
        # diff_frame = cv2.Mat(diff)
        
        if not ret:
            break
        # diff_frame = cv2.absdiff(pre_frame,frame)
        
        cv2.imshow("frame",frame)        
        # if cv2.waitKey(1) == "q":
        #     break
        # else:
        
        if cv2.waitKey(100) & 0xFF == ord('s'):
            r = cv2.selectROI("frame",frame)
            cv2.waitKey(0)    
            imCrop = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]  
            print(r)
            frame_rois.push(imCrop)
            rect_rois.push(r)
            cv2.imshow("Image", imCrop)
                    
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        
        # cv2.imwrite("./images/"+str(i) +"bg.png",frame)       
        
        i = i + 1
        print("index-sum",i,c)
    
    v.release()
    return frame_rois, rect_rois
    
    

def replace(fs,rs,bg_color, out_filename):
    h,w,c,v = open_video_file(filename=filename)
    fourcc_type = 'mp4v'
    fourcc = cv2.VideoWriter_fourcc(*fourcc_type)    
    fps = v.get(cv2.CAP_PROP_FPS)
    vw = cv2.VideoWriter(out_filename, fourcc, fps, (w, h), True)
    
    
    ret, frame = v.read()
    i = 0
    while ret:
        # 读取视频帧
        for i in range(len(rs)):
            r = rs[i]
            f = fs[i]
            ori = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]  
            for h in range(int(r[3]))):
                for w in range(int(r[2])):
                    l = h * int(r[2]) + w
                    if ori[l] == f[l]:
                        ori[l] = bg_color
            
            frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])] = ori

        vw.write(frame)        
        
        ret, frame = v.read()
        # 检测视频是否结束
        # diff_frame = cv2.Mat(diff)
        i = i + 1
        print("index-sum",i,c)
        
    v.release()
    vw.release()
    
    
filename = "D:\\a\\00\\合集_2024-09-13_基础  价格行为\\第1期 价格行为学Price Action Al Brooks数K以及高123和低123书本结合BTC实例.mp4"
c = extract_bg_color(filename=filename)
fs,rs = extract_bg(filename=filename)
replace(fs=fs,rs=rs,out_filename="./out.mp4")
print("##################################################################################################################################")
