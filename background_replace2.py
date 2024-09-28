import cv2
import numpy as np
import math


def color_distance(rgb1,rgb2):
    r1,g1,b1 = rgb1
    r2,g2,b2 = rgb2
    r_mean = int(r1)/ 2 +int(r2) / 2
    r = int(r1) - int(r2)
    g = int(g1) - int(g2)
    b = int(b1) - int(b2)
    
    result = math.sqrt((2 + r_mean/256)*(r**2)+4*(g**2)+(2+(255-r_mean)/256)*(b**2) )
    
    return result


def open_video_file(filename):
    v = cv2.VideoCapture(filename=filename)
    # 获取视频尺寸
    w = int(v.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(v.get(cv2.CAP_PROP_FRAME_HEIGHT))
    c = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
    
    return h,w,c,v


def extract_bg_color(filename):
    h,w,c,v = open_video_file(filename=filename)         
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
            cv2.imshow("Image", imCrop)
            break
                    
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        
        # cv2.imwrite("./images/"+str(i) +"bg.png",frame)
        i = i + 1
        print("index-sum",i,c)
    
    v.release()
    return imCrop[0][0]

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
            frame_rois.append(imCrop)
            rect_rois.append(r)
            cv2.imshow("Image", imCrop)
                    
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        
        # cv2.imwrite("./images/"+str(i) +"bg.png",frame)
        i = i + 1
        print("index-sum",i,c)
    
    v.release()
    return frame_rois, rect_rois
    
    
def judge_color_distance(c1,c2):
    thresold = 250
    r_mean = color_distance(c1,c2)
    # print(r_mean)
    if r_mean < thresold:
        return True

    return False
    

def judge_color_bk(select_c1,frame_c2,bg_color):
    r_mean = color_distance(select_c1,bg_color)
    if r_mean < 20:
        return False
    
    r_mean = color_distance(select_c1,frame_c2)
    if r_mean > 250:
        return False
    
    return True

def replace(fs,rs,bg_color, filename, out_filename):
    h,w,frame_count,v = open_video_file(filename=filename)
    
    # ######################################
    fourcc_type = 'mp4v'
    fourcc = cv2.VideoWriter_fourcc(*fourcc_type)
    fps = v.get(cv2.CAP_PROP_FPS)
    vw = cv2.VideoWriter(out_filename, fourcc, fps, (w, h), True)
    # ######################################
    
    ret, frame = v.read()
    index = 0
    while ret:
        # # 读取视频帧
        for i in range(len(rs)):
            r = rs[i]
            f = fs[i]
            r_x = int(r[0])
            r_y = int(r[1])
            r_w = int(r[2])
            r_h = int(r[3])
            
            for hi in range(r_h):
                for wi in range(r_w):
                    frame_h = hi+r_y
                    frame_w = r_x+wi
                    
                    # if judge_color_distance(frame[frame_h][frame_w],f[hi][wi]):
                    if judge_color_bk(f[hi][wi],frame[frame_h][frame_w],bg_color):
                    # print(r_mean)
                    # print("------------------------>",frame_h, frame_w,hi,wi)
                    # if frame[frame_h][frame_w][0] == f[hi][wi][0] and  frame[frame_h][frame_w][1] == f[hi][wi][1] and  frame[frame_h][frame_w][2] == f[hi][wi][2]:
                        frame[frame_h][frame_w]= bg_color
                        # frame[frame_h][frame_w][1] = bg_color[1]
                        # frame[frame_h][frame_w][2] = bg_color[2]
                    else:
                        # print("no match!")
                        pass
        
        # cv2.imshow("re",frame)
        vw.write(frame)        
        
        ret, frame = v.read()
        # 检测视频是否结束
        # diff_frame = cv2.Mat(diff)
        index = index + 1
        print("index-frame_count->",index,frame_count)
        
        # if cv2.waitKey(10) & 0xFF == ord('l'):
        #     break
        
        
    v.release()
    vw.release()
    


def main(filename, out):
    # filename = "D:\\a\\00\\合集_2024-09-13_基础  价格行为\\第1期 价格行为学Price Action Al Brooks数K以及高123和低123书本结合BTC实例.mp4"
    # replace(fs=0,rs=0,bg_color=0,filename=filename,out_filename="./out.mp4")
    print("##################################################################################################################################")
    c = extract_bg_color(filename=filename)
    fs,rs = extract_bg(filename=filename)
    print("##################################################################################################################################")
    replace(fs=fs,rs=rs,bg_color=c,filename=filename,out_filename=out)
    print("##################################################################################################################################")




file = "D:\\a\\00\\合集_2024-09-13_基础  价格行为\\"
name = "第4期 价格行为学Price Action Al Brooks趋势K线回调有关量化.mp4"

out = "o3.mp4"

main(file + name,out=out )