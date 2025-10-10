#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
图像识别工具类
提供图像对比、图像定位和文字识别功能
"""

import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ImageRecognition:
    """图像识别工具类，提供图像对比、定位和文字识别功能"""
    
    def __init__(self, tesseract_cmd=None, adb_utils=None):
        """
        初始化图像识别工具
        
        Args:
            tesseract_cmd (str, optional): Tesseract OCR引擎路径，如果已添加到环境变量则不需要指定
            adb_utils (object, optional): ADB工具实例，用于获取安卓设备屏幕截图
        """
        # 配置Tesseract OCR路径 - 优先顺序：传入参数 > 自动检测系统PATH > 默认路径
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        else:
            # 尝试自动检测系统PATH中的tesseract
            try:
                # 如果tesseract在PATH中，pytesseract通常可以直接找到它
                pytesseract.get_tesseract_version()
                logger.info("Tesseract已在系统PATH中找到")
            except Exception as e:
                # 不使用默认路径，只记录错误
                logger.error(f"未在系统PATH中找到Tesseract: {e}")
                logger.warning("请确保Tesseract已安装并添加到系统PATH中，或在实例化时传入正确的路径")
        # 存储ADB工具实例
        self.adb_utils = adb_utils
        
        # 检查Tesseract是否可用
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            logger.warning(f"Tesseract OCR初始化失败: {e}")
            logger.warning("文字识别功能可能无法使用，请确保已安装Tesseract并配置正确路径")
        
        # 检查OpenCV是否可用
        try:
            # 测试OpenCV功能
            test_img = np.zeros((10, 10), dtype=np.uint8)
            cv2.cvtColor(test_img, cv2.COLOR_GRAY2BGR)
        except Exception as e:
            raise Exception(f"OpenCV初始化失败: {e}")
            
    def set_adb_utils(self, adb_utils):
        """
        设置ADB工具实例
        
        Args:
            adb_utils (object): ADB工具实例
        """
        self.adb_utils = adb_utils
    
    def compare_images(self, image_path1, image_path2, threshold=0.9):
        """
        比较两个图像的相似度
        
        Args:
            image_path1 (str): 第一个图像路径
            image_path2 (str): 第二个图像路径
            threshold (float): 相似度阈值，范围0-1，默认0.9
        
        Returns:
            dict: 包含相似度和是否匹配的结果
        """
        try:
            # 读取图像
            img1 = cv2.imread(image_path1)
            img2 = cv2.imread(image_path2)
            
            if img1 is None or img2 is None:
                raise Exception(f"无法读取图像: {image_path1 if img1 is None else image_path2}")
            
            # 调整图像大小以匹配
            if img1.shape != img2.shape:
                img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
            
            # 转换为灰度图
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            
            # 使用ORB算法检测特征点
            orb = cv2.ORB_create()
            kp1, des1 = orb.detectAndCompute(gray1, None)
            kp2, des2 = orb.detectAndCompute(gray2, None)
            
            # 使用暴力匹配器
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)
            
            # 计算匹配点比例
            match_ratio = len(matches) / max(len(kp1), len(kp2)) if max(len(kp1), len(kp2)) > 0 else 0
            
            # 计算MSE (均方误差)
            mse = np.mean((gray1 - gray2) ** 2)
            # 归一化MSE到0-1范围，表示相似度
            mse_similarity = 1 / (1 + mse)
            
            # 综合相似度
            similarity = (match_ratio + mse_similarity) / 2
            
            return {
                'similarity': similarity,
                'is_match': similarity >= threshold,
                'match_ratio': match_ratio,
                'mse_similarity': mse_similarity
            }
            
        except Exception as e:
            logger.error(f"图像对比失败: {e}")
            raise
    
    def find_image_in_screen(self, screen_image_path, target_image_path, threshold=0.8):
        """
        在屏幕截图中查找目标图像的位置
        
        Args:
            screen_image_path (str): 屏幕截图路径
            target_image_path (str): 目标图像路径
            threshold (float): 匹配阈值，范围0-1，默认0.8
        
        Returns:
            dict: 包含是否找到、坐标和相似度的结果
        """
        try:
            # 读取图像 - 优先使用PIL来处理中文路径
            try:
                # 尝试使用PIL读取图像，然后转换为OpenCV格式
                screen_pil = Image.open(screen_image_path)
                screen_img = cv2.cvtColor(np.array(screen_pil), cv2.COLOR_RGB2BGR)
                
                target_pil = Image.open(target_image_path)
                target_img = cv2.cvtColor(np.array(target_pil), cv2.COLOR_RGB2BGR)
            except Exception as e:
                self.logger.warning(f"使用PIL读取图像失败，尝试使用OpenCV: {e}")
                # 如果PIL读取失败，尝试使用OpenCV
                screen_img = cv2.imread(screen_image_path)
                target_img = cv2.imread(target_image_path)
            
            if screen_img is None or target_img is None:
                raise Exception(f"无法读取图像: {screen_image_path if screen_img is None else target_image_path}")
            
            # 转换为灰度图以提高匹配速度
            screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
            target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
            
            # 使用模板匹配
            result = cv2.matchTemplate(screen_gray, target_gray, cv2.TM_CCOEFF_NORMED)
            
            # 获取最大匹配值和位置
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # 检查是否达到阈值
            if max_val >= threshold:
                # 计算目标图像的中心点坐标
                target_height, target_width = target_gray.shape[:2]
                top_left = max_loc
                bottom_right = (top_left[0] + target_width, top_left[1] + target_height)
                center_x = top_left[0] + target_width // 2
                center_y = top_left[1] + target_height // 2
                
                return {
                    'found': True,
                    'top_left': top_left,
                    'bottom_right': bottom_right,
                    'center': (center_x, center_y),
                    'similarity': max_val
                }
            else:
                return {
                    'found': False,
                    'similarity': max_val
                }
                
        except Exception as e:
            logger.error(f"在屏幕中查找图像失败: {e}")
            raise
    
    def ocr_image(self, image_path, lang='chi_sim+eng', config='--oem 3 --psm 6'):
        """
        识别图像中的文字，增强版
        
        Args:
            image_path (str): 图像路径
            lang (str): 语言，默认中文简体+英文
            config (str): Tesseract配置参数，默认使用OEM 3 (LSTM引擎) 和PSM 6 (假设为单个均匀块文本)
        
        Returns:
            dict: 包含识别结果和置信度的字典
        """
        # 读取图像
        img = cv2.imread(image_path)
        
        if img is None:
            raise Exception(f"无法读取图像: {image_path}")
        
        # 预处理图像以提高识别率
        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 应用高斯模糊降噪 - 使用更小的核来保留更多细节
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # 自适应阈值处理 - 调整参数以更好地保留文本细节
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17, 3
        )
        
        # 进行形态学操作，增强文字连通性
        kernel = np.ones((1, 1), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # 使用Tesseract进行OCR识别，添加额外配置提高准确率
        # --oem 3: 使用LSTM引擎
        # --psm 6: 假设为单个均匀块文本
        # -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789: 白名单
        text = pytesseract.image_to_string(thresh, lang=lang, config=config)
        
        # 获取详细数据（包括置信度）
        data = pytesseract.image_to_data(thresh, lang=lang, config=config, output_type=pytesseract.Output.DICT)
        
        # 计算平均置信度
        confidences = [int(conf) for conf in data['conf'] if conf != '-1']
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        return {
            'text': text.strip(),
            'confidence': avg_confidence,
            'details': data
        }
    
    def fuzzy_text_search(self, recognized_text, target_text, threshold=0.8):
        """
        模糊文本匹配，用于提高文字识别的容错性
        
        Args:
            recognized_text (str): 识别出的文本
            target_text (str): 目标文本
            threshold (float): 相似度阈值，范围0-1，默认0.8
        
        Returns:
            bool: 是否匹配成功
        """
        from difflib import SequenceMatcher
        
        # 转为小写进行比较
        recognized_text = recognized_text.lower()
        target_text = target_text.lower()
        
        # 精确匹配优先
        if target_text in recognized_text:
            return True
        
        # 计算相似度
        similarity = SequenceMatcher(None, recognized_text, target_text).ratio()
        if similarity >= threshold:
            return True
        
        # 检查是否包含关键词
        target_words = target_text.split()
        matched_words = 0
        for word in target_words:
            if word in recognized_text:
                matched_words += 1
        
        # 如果匹配的关键词超过一半，也认为匹配成功
        if matched_words >= len(target_words) * 0.5:
            return True
        
        return False
    
    def preprocess_image(self, image_path, output_path=None):
        """
        预处理图像以提高识别率
        
        Args:
            image_path (str): 输入图像路径
            output_path (str, optional): 输出图像路径，如果不指定则不保存
        
        Returns:
            numpy.ndarray: 预处理后的图像
        """
        try:
            # 读取图像
            img = cv2.imread(image_path)
            
            if img is None:
                raise Exception(f"无法读取图像: {image_path}")
            
            # 转换为灰度图
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 应用高斯模糊降噪
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # 自适应阈值处理
            thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # 保存处理后的图像
            if output_path:
                cv2.imwrite(output_path, thresh)
                logger.info(f"预处理后的图像已保存到: {output_path}")
            
            return thresh
            
        except Exception as e:
            logger.error(f"图像预处理失败: {e}")
            raise
    
    def capture_screen(self, save_path):
        """
        捕获安卓设备屏幕截图
        
        Args:
            save_path (str): 保存路径
        
        Returns:
            bool: 操作是否成功
        """
        try:
            if self.adb_utils:
                # 使用ADB工具获取设备截图
                success = self.adb_utils.截图(save_path)
                
                if success:
                    logger.info(f"设备屏幕截图已保存到: {save_path}")
                    return True
                else:
                    logger.error("使用ADB获取设备截图失败")
                    return False
            else:
                logger.error("未提供ADB工具实例，无法获取设备截图")
                raise Exception("未提供ADB工具实例，无法获取设备截图")
                
        except Exception as e:
            logger.error(f"捕获设备屏幕截图失败: {e}")
            raise


# 创建全局图像识别工具实例
def get_image_recognition(tesseract_cmd=None, adb_utils=None):
    """
    获取图像识别工具实例
    
    Args:
        tesseract_cmd (str, optional): Tesseract OCR引擎路径
        adb_utils (object, optional): ADB工具实例
    
    Returns:
        ImageRecognition: 图像识别工具实例
    """
    return ImageRecognition(tesseract_cmd, adb_utils)