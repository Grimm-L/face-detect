from detect.ai.db import access_db_to_json, parse_menu_info_from_redis
from detect.ai.detect_face_mutiple import *
import os

class Front:
    def __init__(self, face_dir="../images") -> None:
        self.d = FaceDetector()
        self.menu = None
        self.menu_info = None
        self.load_face_menu(face_dir)
        self.frame_cnt = 0
        self.last_face = None
        self.last_bbox = None

    def load_face_menu(self, face_dir):
        for files in os.listdir(face_dir):
            self.d.load_identity_embedding(os.path.join(face_dir, files), files.split('.')[0])
            print(f"Add face {files}")

    def is_bbox_move(self, bbox, fix_bbox_thre=100):
        m = 0
        for i in range(len(bbox)):
            m = max(m, abs(bbox[i]-self.last_bbox[i]))
        return m > fix_bbox_thre

    def get_face_menu(self, img, face_thre, fix_bbox_thre, fix_frame_thre, minbbox_thre=100):
        img = cv2.imdecode(np.frombuffer(img, np.uint8), -1)
        
        # In case of grayScale images the len(img.shape) == 2
        if len(img.shape) > 2 and img.shape[2] == 4:
            #convert the image from RGBA2RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        res = self.d.detect_face(img, face_thre, minbbox_thre)
        if res is None:
            return None # 没有检测到任何人脸
        tar_img, face_id, bbox = res

        if face_id != self.last_face or self.is_bbox_move(bbox, fix_bbox_thre):
            self.frame_cnt = 0
            self.last_face = face_id
            self.last_bbox = bbox  
        else:
            self.frame_cnt += 1
            self.last_bbox = bbox
            if self.frame_cnt > fix_frame_thre: # 假设摄像头是60帧
                access_db_to_json(face_id)
                self.menu = parse_menu_info_from_redis()
                return self.menu
            # elif self.frame_cnt > fix_frame_thre/2:
            #     self.menu, self.menu_info = self.db.get_menu_info(face_id)
        return None


if __name__ == '__main__': 
    f = Front()
    import cv2

    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Real Time', cv2.WINDOW_NORMAL)
    while cap.isOpened():
        ret, frame = cap.read()
        tar_img, menu, menu_info = f.get_face_menu(frame, face_thre=1.0, fix_bbox_thre=100, fix_frame_thre=5)  # 1.0閾值，1.0表示MSE，小於1.0顯示框
        if menu:
            print(menu)
            print(menu_info)
        cv2.imshow("Real Time", tar_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
