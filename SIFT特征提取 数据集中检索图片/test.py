import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

def extract_sift_features(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(img, None)
    return descriptors

def image_retrieval(input_image, dataset_folder, top_n=5):
    input_features = extract_sift_features(input_image)

    image_paths = os.listdir(dataset_folder)
    similarity_scores = []
    for image_path in image_paths:
        full_path = os.path.join(dataset_folder, image_path)
        image_features = extract_sift_features(full_path)
        if image_features is not None and input_features is not None:
            similarity = cosine_similarity(input_features, image_features)
            if not np.isnan(similarity[0][0]):
                similarity_scores.append((full_path, similarity[0][0]))

    # 根据相似度对结果进行排序
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    
    # 返回前top_n个相似图片路径
    similar_images = [path for path, _ in similarity_scores[:top_n]]
    return similar_images

# 示例用法
input_image = 'data/1.png'
dataset_folder = 'data/'
similar_images = image_retrieval(input_image, dataset_folder)
print(similar_images)

