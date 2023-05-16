import cv2
import numpy as np
from insightface.app import FaceAnalysis

class FaceDetector():
    def __init__(self) -> None:
        self.app = FaceAnalysis(allowed_modules=['detection', 'recognition'])
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        self.identity_embedding = dict()
    

    def load_identity_embedding(self, img_path, name):
        img = cv2.imread(img_path)
        face_res = self.app.get(img)
        assert len(face_res) == 1, "Detect more than one face in identity image."
        self.identity_embedding[name] = face_res[0]["embedding"]

    def draw_on(self, img, face):
        dimg = img.copy()
        box = face.bbox.astype(np.int32)
        color = (0, 0, 255)
        cv2.rectangle(dimg, (box[0], box[1]), (box[2], box[3]), color, 2)
        return dimg
    

    def detect_face(self, target_face_img, threshold, minbbox_thre):
        assert len(self.identity_embedding) != 0, "call `load_identity_embedding` first"
        target_face_res = self.app.get(target_face_img)
        if len(target_face_res) == 0:
            return None
        cur_front_tar = None
        max_size = 0
        for tar in target_face_res:
            cur_box = tar["bbox"]
            cur_size = (cur_box[3]-cur_box[1]) * (cur_box[2]-cur_box[0])
            if cur_size > max_size:
                cur_front_tar = tar
                max_size = cur_size

        min_diff_score = 10000
        min_diff_name = None
        for name, embedding in self.identity_embedding.items():
            diff_score = np.mean(np.square(cur_front_tar['embedding'] - embedding))
            if diff_score < min_diff_score:
                min_diff_score = diff_score
                min_diff_name = name

        x1, y1, x2, y2 = cur_front_tar.bbox.astype(np.int32)
        if ((x2-x1)*(y2-y1)) < minbbox_thre:
            return None

        if min_diff_score < threshold:
            return self.draw_on(target_face_img, cur_front_tar), min_diff_name, cur_front_tar.bbox.astype(np.int32)
        else:
            return None



if __name__ == "__main__":
    d = FaceDetector()
    d.load_identity_embedding("images/IMG_7934.jpg", "Yokey") # 通过路径读取证件照
    res = d.detect_face(cv2.imread("images/zyf3.jpeg"), 1.0, 100) # 直接输入待检测图片
    if res is not None:
        cv2.imshow("Result", res[0])
        cv2.waitKey(0) 
        cv2.destroyAllWindows()
