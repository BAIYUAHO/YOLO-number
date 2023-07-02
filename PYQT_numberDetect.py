import platform

import random

import PyQt5
from PyCameraList.camera_device import list_video_devices

import numpy as np
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from PyQt5.QtCore import QUrl
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *

import argparse
import os
import sys
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn

import dir_change

from utils.general import scale_boxes
from utils.augmentations import letterbox

import datetime

import time

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:  # 模块的查询路径列表
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.experimental import attempt_load
from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box, plot_one_box
from utils.torch_utils import select_device, smart_inference_mode


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'weights/best.pt',
                        help='model path or triton URL')
    parser.add_argument('--source', type=str, default='0', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--data', type=str,
                        default=ROOT / './numberParameter.yaml',
                        help='(optional) dataset.yaml path')
    # parser.add_argument('--source', type=str, default='0', help='source')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640],
                        help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int,
                        help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default=ROOT / 'runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    parser.add_argument('--vid-stride', type=int, default=1, help='video frame-rate stride')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    print_args(vars(opt))
    return opt

    # self.rece_send = receAndsend()


class number_detect0():
    def __init__(self):
        #   ui 可以随意取名
        self.ui = QUiLoader().load("D:\\Python\\YOLO-number\\num_detect.ui")
        self.b = 1
        self.Cap = 0
        self.n = 1
        self.player = QMediaPlayer()

        self.img0 = 0
        self.img1 = 1
        self.path = 0

        # 设置 QMediaPlayer 的内容为 QMediaContent 对象
        self.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/Welcome.wav")))
        self.player.play()
        # tab1
        self.ui.tab1_btn_openPic.clicked.connect(self.open_image_detect1)
        self.ui.tab1_btn_openCam.clicked.connect(self.open_cam1)
        self.ui.tab1_btn_realtime.clicked.connect(self.realtime_detect)
        self.realtime_detect0 = realtime_detect()
        self.ui.tab1_btn_detectPic.clicked.connect(self.detect_pic)
        self.detect_pic0 = detect_pic()
        self.ui.tab1_btn_close.clicked.connect(self.detect_close)
        self.tab1_table = False
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 将列调整到跟内容大小相匹配
        self.ui.tableWidget.showGrid()
        self.ui.tableWidget.setFrameShape(QFrame.Box)
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget.setRowHeight(0, 30)

        # tab2
        self.ui.tab2_btn_openPic.clicked.connect(self.open_image_detect2)
        self.ui.tab2_btn_openCam.clicked.connect(self.open_cam2)
        self.ui.tab2_btn_detectPic.clicked.connect(self.detect_pic2)
        self.detect_pic2 = detect_pic2()
        self.my_list3 = []
        self.ui.tab2_btn_realtime.clicked.connect(self.realtime_detect2)
        self.realtime_detect2 = realtime_detect2()
        self.ui.tab2_btn_close.clicked.connect(self.detect_close2)

        # tab3
        self.ui.tab3_btn_openPic.clicked.connect(self.open_image_detect3)
        self.ui.tab3_btn_openCam.clicked.connect(self.open_cam3)
        self.ui.tab3_btn_detectPic.clicked.connect(self.detect_pic3)
        self.detect_pic3 = detect_pic3()
        self.ui.tab3_btn_realtime.clicked.connect(self.realtime_detect3)
        self.realtime_detect3 = realtime_detect3()
        self.ui.tab3_btn_close.clicked.connect(self.detect_close3)

        # tab4
        self.ui.tab4_btn_detectPic.clicked.connect(self.detect_pic4)
        self.detect_pic4 = detect_pic4()
        self.tab4_table = False
        self.ui.tab4_btn_openCam.clicked.connect(self.open_cam4)
        self.ui.tab4_btn_closeCam.clicked.connect(self.detect_close4)
        self.ui.tab4_btn_realtime.clicked.connect(self.realtime_detect4)
        self.realtime_detect4 = realtime_detect4()




        self.ui.tab4_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 将列调整到跟内容大小相匹配
        self.ui.tab4_tableWidget.showGrid()
        self.ui.tab4_tableWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.ui.tab4_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tab4_tableWidget.setRowHeight(0, 30)
        self.ui.tab5_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 将列调整到跟内容大小相匹配
        self.ui.tab5_tableWidget.showGrid()
        self.ui.tab5_tableWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.ui.tab5_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tab5_tableWidget.setRowHeight(0, 30)

        # tab5
        font = QFont()
        font.setPointSize(24)  # 设置字体大小
        self.ui.tab5_label_1.setFont(font)
        self.ui.tab5_label_1.setStyleSheet("color: red;")  # 设置字体颜色
        self.ui.tab5_label_2.setFont(font)
        self.ui.tab5_label_2.setStyleSheet("color: red;")  # 设置字体颜色
        self.ui.tab5_label_4.setFont(font)
        self.ui.tab5_label_4.setStyleSheet("color: red;")  # 设置字体颜色
        self.ui.tab5_label_5.setFont(font)
        self.ui.tab5_label_5.setStyleSheet("color: red;")  # 设置字体颜色
        self.ui.tab5_label_6.setFont(font)
        self.ui.tab5_label_6.setStyleSheet("color: red;")  # 设置字体颜色
        self.ui.tab5_label_7.setFont(font)
        self.ui.tab5_label_7.setStyleSheet("color: red;")  # 设置字体颜色
        self.ui.tab5_label_8.setFont(font)
        self.ui.tab5_label_8.setStyleSheet("color: red;")  # 设置字体颜色
        self.ui.tab5_label_3.setFont(font)
        self.ui.tab5_label_3.setStyleSheet("color: red;")  # 设置字体颜色
        self.ui.tab5_btn_add.clicked.connect(self.rand_add)
        self.rand_add = rand_add()
        self.ui.tab5_btn_sub.clicked.connect(self.rand_sub)
        self.rand_sub = rand_sub()
        self.ui.tab5_btn_mul.clicked.connect(self.rand_mul)
        self.rand_mul = rand_mul()
        self.ui.tab5_btn_division.clicked.connect(self.rand_division)
        self.rand_division = rand_division()
        self.ui.tab5_btn_openCam.clicked.connect(self.open_cam5)
        self.ui.tab5_btn_detectPic.clicked.connect(self.detect_pic5)
        self.detect_pic5 = detect_pic5()
        self.ui.tab5_btn_closeCam.clicked.connect(self.detect_close5)
        self.ui.tab5_btn_realtime.clicked.connect(self.realtime_detect5)
        self.realtime_detect5= realtime_detect5()

        self.r_add = 0
        self.r_sub = 0
        self.r_mul = 0
        self.r_division = 0
        # self.ui.tab5_btn_detectPic.clicked.connect(self.detect_pic5)
        # self.detect_pic5 = detect_pic5()

        self.source = " "

    def run2(self,
             weights=ROOT / 'best.pt',  # model path or triton URL
             source=ROOT / '',  # file/dir/URL/glob/screen/0(webcam)
             data=ROOT / 'oilsealParameter.yaml',  # dataset.yaml path
             imgsz=(640, 640),  # inference size (height, width)
             conf_thres=0.25,  # confidence threshold
             iou_thres=0.45,  # NMS IOU threshold
             max_det=1000,  # maximum detections per image
             device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
             view_img=False,  # show results
             save_txt=False,  # save results to *.txt
             save_conf=False,  # save confidences in --save-txt labels
             save_crop=False,  # save cropped prediction boxes
             nosave=False,  # do not save images/videos
             classes=None,  # filter by class: --class 0, or --class 0 2 3
             agnostic_nms=False,  # class-agnostic NMS
             augment=False,  # augmented inference
             visualize=False,  # visualize features
             update=False,  # update all models
             project=ROOT / 'runs/detect',  # save results to project/name
             name='exp',  # save results to project/name
             exist_ok=False,  # existing project/name ok, do not increment
             line_thickness=3,  # bounding box thickness (pixels)
             hide_labels=False,  # hide labels
             hide_conf=False,  # hide confidences
             half=False,  # use FP16 half-precision inference
             dnn=False,  # use OpenCV DNN for ONNX inference
             vid_stride=1,  # video frame-rate stride
             ):
        number_detect.my_list3 = []
        source = str(number_detect.source)
        save_img = not nosave and not source.endswith('.txt')  # save inference images
        is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
        is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
        webcam = source.isnumeric() or source.endswith('.streams') or (is_url and not is_file)
        screenshot = source.lower().startswith('screen')
        if is_url and is_file:
            source = check_file(source)  # download
        # Directories
        if webcam:
            save_dir = Path(project) / name  # increment run 存放检测结果
        else:
            save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run 存放检测结果
        (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir 存放txt文件
        # Dataloader
        bs = 1  # batch_size
        if webcam:
            view_img = check_imshow(warn=True)
            dataset = LoadStreams('1', img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
            bs = len(dataset)
        elif screenshot:
            dataset = LoadScreenshots(source, img_size=imgsz, stride=stride, auto=pt)
        else:
            dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        # dataset = LoadImages('0', img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        vid_path, vid_writer = [None] * bs, [None] * bs
        # Run inference
        model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
        seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
        for path, im, im0s, vid_cap, s in dataset:
            with dt[0]:
                im = torch.from_numpy(im).to(model.device)
                im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
                im /= 255  # 0 - 255 to 0.0 - 1.0
                if len(im.shape) == 3:
                    im = im[None]  # expand for batch dim

            # Inference
            with dt[1]:
                visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
                pred = model(im, augment=augment, visualize=visualize)

            # NMS
            with dt[2]:
                pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

            # Second-stage classifier (optional)
            # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

            # Process predictions
            for i, det in enumerate(pred):  # per image
                seen += 1
                if webcam:  # batch_size >= 1
                    p, im0, frame = path[i], im0s[i].copy(), dataset.count
                    s += f'{i}: '
                else:
                    p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

                p = Path(p)  # to Path
                save_path = str(save_dir / p.name)  # im.jpg
                txt_path = str(save_dir / 'labels' / p.stem) + (
                    '' if dataset.mode == 'image' else f'_{frame}')  # im.txt
                s += '%gx%g ' % im.shape[2:]  # print string

                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                imc = im0.copy() if save_crop else im0  # for save_crop
                annotator = Annotator(im0, line_width=line_thickness, example=str(names))
                listttt = []
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, 5].unique():
                        n = (det[:, 5] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                        if save_txt:  # Write to file
                            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(
                                -1).tolist()  # normalized xywh
                            line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                            with open(f'{txt_path}.txt', 'a') as f:
                                f.write(('%g ' * len(line)).rstrip() % line + '\n')
                        if save_img or save_crop or view_img:  # Add bbox to image
                            c = int(cls)  # integer class
                            label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                            box0 = annotator.box_label(xyxy, label, color=colors(c, True))
                            listttt.append(label + ':' + str(box0))
                            # print('lllll', listttt)
                        if save_crop:
                            save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)
                    if source != '1':
                        my_list = []

                        my_dict = {}
                        for l in listttt:
                            num = l.index(':')
                            q = l[num + 1:]
                            my_dict[q] = l[0]
                            my_list.append(int(q))
                        my_list.sort()
                        for q in my_list:
                            number_detect.my_list3.append(my_dict[str(q)])
                        num_stationary = len(my_list)
                # Stream results
                im0 = annotator.result()
                if source == '1':
                    # number_detect.im0 = cv2.flip(im0, 1)
                    return im0
                # if view_img:
                #     if sys.platform.system() == 'Linux' and p not in windows:
                #         windows.append(p)
                #         cv2.namedWindow(str(p),
                #                         cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                #         cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])

                # cv2.imshow(str(p), im0)
                # cv2.waitKey(1)  # 1 millisecond

                # Save results (image with detections)
                # if 0:
                # # if save_img:
                #     if dataset.mode == 'image':
                #         cv2.imwrite(save_path, im0)
                #     else:  # 'video' or 'stream'
                #         if vid_path[i] != save_path:  # new video
                #             vid_path[i] = save_path
                #             if isinstance(vid_writer[i], cv2.VideoWriter):
                #                 vid_writer[i].release()  # release previous video writer
                #             if vid_cap:  # video
                #                 fps = vid_cap.get(cv2.CAP_PROP_FPS)
                #                 w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                #                 h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                #             else:  # stream
                #                 fps, w, h = 30, im0.shape[1], im0.shape[0]
                #             save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                #             vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                #         vid_writer[i].write(im0)

            # Print time (inference-only)
            # LOGGER.info(f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")
            # info = f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms"
            # # print(info)
            # if source != '1':
            #     if number_detect.tab1_table == True:
            #         str1 = 'jpg'
            #         n = info.index(str1)
            #         info2 = info[n:]
            #         curr_time = datetime.datetime.now()
            #         time_now = datetime.datetime.strftime(curr_time, '%H:%M:%S')
            #         row_count = number_detect.ui.tableWidget.rowCount()
            #         number_detect.ui.tableWidget.insertRow(row_count)
            #         number_detect.ui.tableWidget.setItem(row_count, 0, QtWidgets.QTableWidgetItem(str(time_now)))
            #         number_detect.ui.tableWidget.item(row_count, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #         number_detect.ui.tableWidget.verticalScrollBar().setSliderPosition(row_count + 2)
            #         if 'Pencil' in info2 or 'Eraser' in info2 or 'Scale' in info2 or 'Sharpener' in info2:
            #             item = QtWidgets.QTableWidgetItem(str('stationary_Num'))
            #             item.setForeground(QtGui.QColor(255, 0, 0))
            #             number_detect.ui.tableWidget.setItem(row_count, 5,
            #                                                  QtWidgets.QTableWidgetItem(str(num_stationary)))
            #             number_detect.ui.tableWidget.item(row_count, 5).setTextAlignment(
            #                 Qt.AlignHCenter | Qt.AlignVCenter)
            #         if 'Pencil' in info2:
            #             item = QtWidgets.QTableWidgetItem(str('pencil'))
            #             item.setForeground(QtGui.QColor(255, 0, 0))
            #             number_detect.ui.tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('√')))
            #             number_detect.ui.tableWidget.item(row_count, 2).setTextAlignment(
            #                 Qt.AlignHCenter | Qt.AlignVCenter)
            #         if 'Eraser' in info2:
            #             item = QtWidgets.QTableWidgetItem(str('eraser'))
            #             item.setForeground(QtGui.QColor(255, 0, 0))
            #             number_detect.ui.tableWidget.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str('√')))
            #             number_detect.ui.tableWidget.item(row_count, 3).setTextAlignment(
            #                 Qt.AlignHCenter | Qt.AlignVCenter)
            #         if 'Scale' in info2:
            #             item = QtWidgets.QTableWidgetItem(str('scale'))
            #             item.setForeground(QtGui.QColor(255, 0, 0))
            #             number_detect.ui.tableWidget.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str('√')))
            #             number_detect.ui.tableWidget.item(row_count, 4).setTextAlignment(
            #                 Qt.AlignHCenter | Qt.AlignVCenter)
            #         if 'Sharpener' in info2:
            #             item = QtWidgets.QTableWidgetItem(str('sharpener'))
            #             item.setForeground(QtGui.QColor(255, 0, 0))
            #             # j += 1
            #             number_detect.ui.tableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str('√')), )
            #             number_detect.ui.tableWidget.item(row_count, 1).setTextAlignment(
            #                 Qt.AlignHCenter | Qt.AlignVCenter)
            # # Print results
            # t = tuple(x.t / seen * 1E3 for x in dt)  # speeds per image
            # LOGGER.info(
            #     f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
            # if save_txt or save_img:
            #     s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
            #     LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
            # if update:
            #     strip_optimizer(weights[0])  # update model (to fix SourceChangeWarning)

    def run0(self,
             weights=ROOT / 'best.pt',  # model path or triton URL
             source=ROOT / '',  # file/dir/URL/glob/screen/0(webcam)
             data=ROOT / 'oilsealParameter.yaml',  # dataset.yaml path
             imgsz=(640, 640),  # inference size (height, width)
             conf_thres=0.25,  # confidence threshold
             iou_thres=0.45,  # NMS IOU threshold
             max_det=1000,  # maximum detections per image
             device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
             view_img=False,  # show results
             save_txt=False,  # save results to *.txt
             save_conf=False,  # save confidences in --save-txt labels
             save_crop=False,  # save cropped prediction boxes
             nosave=False,  # do not save images/videos
             classes=None,  # filter by class: --class 0, or --class 0 2 3
             agnostic_nms=False,  # class-agnostic NMS
             augment=False,  # augmented inference
             visualize=False,  # visualize features
             update=False,  # update all models
             project=ROOT / 'runs/detect',  # save results to project/name
             name='exp',  # save results to project/name
             exist_ok=False,  # existing project/name ok, do not increment
             line_thickness=3,  # bounding box thickness (pixels)
             hide_labels=False,  # hide labels
             hide_conf=False,  # hide confidences
             half=False,  # use FP16 half-precision inference
             dnn=False,  # use OpenCV DNN for ONNX inference
             vid_stride=1,  # video frame-rate stride
             ):
        number_detect.b = 1
        number_detect.my_list3 = []
        source = str(number_detect.source)
        save_img = not nosave and not source.endswith('.txt')  # save inference images
        is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
        is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
        webcam = source.isnumeric() or source.endswith('.streams') or (is_url and not is_file)
        screenshot = source.lower().startswith('screen')
        if is_url and is_file:
            source = check_file(source)  # download
        # Directories
        if webcam:
            save_dir = Path(project) / name  # increment run 存放检测结果
        else:
            save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run 存放检测结果
        (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True,
                                           exist_ok=True)  # make dir 存放txt文件
        # Dataloader
        bs = 1  # batch_size
        if webcam:
            view_img = check_imshow(warn=True)
            dataset = LoadStreams('1', img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
            bs = len(dataset)
        elif screenshot:
            dataset = LoadScreenshots(source, img_size=imgsz, stride=stride, auto=pt)
        else:
            dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        # dataset = LoadImages('0', img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        vid_path, vid_writer = [None] * bs, [None] * bs
        # Run inference
        model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
        seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
        for path, im, im0s, vid_cap, s in dataset:
            with dt[0]:
                im = torch.from_numpy(im).to(model.device)
                im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
                im /= 255  # 0 - 255 to 0.0 - 1.0
                if len(im.shape) == 3:
                    im = im[None]  # expand for batch dim

            # Inference
            with dt[1]:
                visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
                pred = model(im, augment=augment, visualize=visualize)

            # NMS
            with dt[2]:
                pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms,
                                           max_det=max_det)

            # Process predictions
            for i, det in enumerate(pred):  # per image
                seen += 1
                if webcam:  # batch_size >= 1
                    p, im0, frame = path[i], im0s[i].copy(), dataset.count
                    s += f'{i}: '
                else:
                    p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

                p = Path(p)  # to Path
                save_path = str(save_dir / p.name)  # im.jpg
                txt_path = str(save_dir / 'labels' / p.stem) + (
                    '' if dataset.mode == 'image' else f'_{frame}')  # im.txt
                s += '%gx%g ' % im.shape[2:]  # print string

                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                imc = im0.copy() if save_crop else im0  # for save_crop
                annotator = Annotator(im0, line_width=line_thickness, example=str(names))
                listttt = []
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, 5].unique():
                        n = (det[:, 5] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                        if save_txt:  # Write to file
                            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(
                                -1).tolist()  # normalized xywh
                            line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                            with open(f'{txt_path}.txt', 'a') as f:
                                f.write(('%g ' * len(line)).rstrip() % line + '\n')
                        if save_img or save_crop or view_img:  # Add bbox to image
                            c = int(cls)  # integer class
                            label = None if hide_labels else (
                                names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                            box0 = annotator.box_label(xyxy, label, color=colors(c, True))
                            listttt.append(label + ':' + str(box0))
                            # print('lllll', listttt)
                        if save_crop:
                            save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg',
                                         BGR=True)

                    my_list = []

                    my_dict = {}
                    for l in listttt:
                        num = l.index(':')
                        q = l[num + 1:]
                        my_dict[q] = l[0]
                        my_list.append(int(q))
                    my_list.sort()
                    for q in my_list:
                        number_detect.my_list3.append(my_dict[str(q)])
                    num_stationary = len(my_list)
                # Stream results
                im0 = annotator.result()
                if source == '1':
                    im0 = cv2.flip(im0, 1)

                # Save results (image with detections)
                if save_img:
                    if dataset.mode == 'image':
                        cv2.imwrite(save_path, im0)
                    else:  # 'video' or 'stream'
                        if vid_path[i] != save_path:  # new video
                            vid_path[i] = save_path
                            if isinstance(vid_writer[i], cv2.VideoWriter):
                                vid_writer[i].release()  # release previous video writer
                            if vid_cap:  # video
                                fps = vid_cap.get(cv2.CAP_PROP_FPS)
                                w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            else:  # stream
                                fps, w, h = 30, im0.shape[1], im0.shape[0]
                            save_path = str(
                                Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                            vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps,
                                                            (w, h))
                        vid_writer[i].write(im0)

            # Print time (inference-only)
            LOGGER.info(f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")
            info = f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms"
            # print(info)

            if number_detect.tab1_table == True:

                info2 = info[:]
                print(info2)
                curr_time = datetime.datetime.now()
                time_now = datetime.datetime.strftime(curr_time, '%H:%M:%S')
                row_count = number_detect.ui.tableWidget.rowCount()
                number_detect.ui.tableWidget.insertRow(row_count)
                number_detect.ui.tableWidget.setItem(row_count, 0,
                                                     QtWidgets.QTableWidgetItem(str(time_now)))
                number_detect.ui.tableWidget.item(row_count, 0).setTextAlignment(
                    Qt.AlignHCenter | Qt.AlignVCenter)
                number_detect.ui.tableWidget.verticalScrollBar().setSliderPosition(row_count + 2)
                if 'Pencil' in info2 or 'Eraser' in info2 or 'Scale' in info2 or 'Sharpener' in info2:
                    item = QtWidgets.QTableWidgetItem(str('stationary_Num'))
                    item.setForeground(QtGui.QColor(255, 0, 0))
                    number_detect.ui.tableWidget.setItem(row_count, 5,
                                                         QtWidgets.QTableWidgetItem(
                                                             str(num_stationary)))
                    number_detect.ui.tableWidget.item(row_count, 5).setTextAlignment(
                        Qt.AlignHCenter | Qt.AlignVCenter)
                if 'Pencil' in info2:
                    item = QtWidgets.QTableWidgetItem(str('pencil'))
                    item.setForeground(QtGui.QColor(255, 0, 0))
                    number_detect.ui.tableWidget.setItem(row_count, 2,
                                                         QtWidgets.QTableWidgetItem(str('√')))
                    number_detect.ui.tableWidget.item(row_count, 2).setTextAlignment(
                        Qt.AlignHCenter | Qt.AlignVCenter)
                if 'Eraser' in info2:
                    item = QtWidgets.QTableWidgetItem(str('eraser'))
                    item.setForeground(QtGui.QColor(255, 0, 0))
                    number_detect.ui.tableWidget.setItem(row_count, 3,
                                                         QtWidgets.QTableWidgetItem(str('√')))
                    number_detect.ui.tableWidget.item(row_count, 3).setTextAlignment(
                        Qt.AlignHCenter | Qt.AlignVCenter)
                if 'Scale' in info2:
                    item = QtWidgets.QTableWidgetItem(str('scale'))
                    item.setForeground(QtGui.QColor(255, 0, 0))
                    number_detect.ui.tableWidget.setItem(row_count, 4,
                                                         QtWidgets.QTableWidgetItem(str('√')))
                    number_detect.ui.tableWidget.item(row_count, 4).setTextAlignment(
                        Qt.AlignHCenter | Qt.AlignVCenter)
                if 'Sharpener' in info2:
                    item = QtWidgets.QTableWidgetItem(str('sharpener'))
                    item.setForeground(QtGui.QColor(255, 0, 0))
                    # j += 1
                    number_detect.ui.tableWidget.setItem(row_count, 1,
                                                         QtWidgets.QTableWidgetItem(str('√')), )
                    number_detect.ui.tableWidget.item(row_count, 1).setTextAlignment(
                        Qt.AlignHCenter | Qt.AlignVCenter)
            # Print results
            t = tuple(x.t / seen * 1E3 for x in dt)  # speeds per image
            LOGGER.info(
                f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
            if save_txt or save_img:
                s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
                LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
            if update:
                strip_optimizer(weights[0])  # update model (to fix SourceChangeWarning)

            number_detect.img1 = im0
            return 0

    def rand_add(self):
        self.rand_add.start()

    def rand_sub(self):
        self.rand_sub.start()

    def rand_mul(self):
        self.rand_mul.start()

    def rand_division(self):
        self.rand_division.start()

    # 实时检测线程接口1
    def realtime_detect(self):
        self.realtime_detect0.start()

    # 实时检测线程接口2
    def realtime_detect2(self):
        self.realtime_detect2.start()

    # 实时检测线程接口3
    def realtime_detect3(self):
        self.realtime_detect3.start()

    # 实时检测线程接口4
    def realtime_detect4(self):
        self.realtime_detect4.start()

    # 实时检测线程接口5
    def realtime_detect5(self):
        self.realtime_detect5.start()
    # 拍照检测线程接口1
    def detect_pic(self):
        number_detect.tab1_table = True
        number_detect.tab4_table = False
        self.detect_pic0.start()

    # 拍照检测线程接口2
    def detect_pic2(self):
        self.detect_pic2.start()

    # 拍照检测线程接口3
    def detect_pic3(self):
        self.detect_pic3.start()

    # 拍照检测线程接口3
    def detect_pic4(self):
        self.detect_pic4.start()

    # 拍照检测线程接口5
    def detect_pic5(self):
        self.detect_pic5.start()

    # 相机打开成功1
    def open_cam1(self):
        l1 = []
        number_detect.b = 1
        number_detect.Cap = cv2.VideoCapture(number_detect.n, cv2.CAP_DSHOW)  # 相机
        cameras = dict(list_video_devices())
        for i in cameras:
            l1.append(i)
        if number_detect.n in l1:
            reply = QMessageBox.question(number_detect.ui, 'Notification', 'The camera is opened successfully！')
            if reply == 'StandardButton.Yes':
                pass
        else:
            reply = QMessageBox.question(number_detect.ui, 'Notification', 'The camera failed to open, please check the camera and reconnect!')
            if reply == 'StandardButton.Yes':
                pass
        print('eeeeeeeee', number_detect.b)

    # 确认相机打开成功2
    def open_cam2(self):
        l1 = []
        number_detect.b = 1
        number_detect.Cap = cv2.VideoCapture(number_detect.n, cv2.CAP_DSHOW)  # 相机
        cameras = dict(list_video_devices())
        for i in cameras:
            l1.append(i)
        if number_detect.n in l1:
            reply = QMessageBox.question(number_detect.ui, 'Notification', 'The camera is opened successfully！')
            if reply == 'StandardButton.Yes':
                pass
        else:
            reply = QMessageBox.question(number_detect.ui, 'Notification', 'The camera failed to open, please check the camera and reconnect!')
            if reply == 'StandardButton.Yes':
                pass

    # 确认相机打开成功3
    def open_cam3(self):
        l1 = []
        number_detect.b = 1
        number_detect.Cap = cv2.VideoCapture(number_detect.n, cv2.CAP_DSHOW)  # 相机
        cameras = dict(list_video_devices())
        for i in cameras:
            l1.append(i)
        if number_detect.n in l1:
            reply = QMessageBox.question(number_detect.ui, 'Notification', 'The camera is opened successfully！')
            if reply == 'StandardButton.Yes':
                pass
        else:
            reply = QMessageBox.question(number_detect.ui, 'Notification', 'The camera failed to open, please check the camera and reconnect!')
            if reply == 'StandardButton.Yes':
                pass

    # 确认相机打开成功4
    def open_cam4(self):
        l1 = []
        number_detect.b = 1
        number_detect.Cap = cv2.VideoCapture(number_detect.n, cv2.CAP_DSHOW)  # 相机
        cameras = dict(list_video_devices())
        for i in cameras:
            l1.append(i)
        if number_detect.n in l1:
            reply = QMessageBox.question(number_detect.ui, 'Notification', 'The camera is opened successfully！')
            if reply == 'StandardButton.Yes':
                pass
        else:
            reply = QMessageBox.question(number_detect.ui, 'Notification', 'The camera failed to open, please check the camera and reconnect!')
            if reply == 'StandardButton.Yes':
                pass

    # 确认相机打开成功5
    def open_cam5(self):
        l1 = []
        number_detect.b = True
        number_detect.Cap = cv2.VideoCapture(number_detect.n, cv2.CAP_DSHOW)  # 相机
        cameras = dict(list_video_devices())
        for i in cameras:
            l1.append(i)
        if number_detect.n in l1:
            reply = QMessageBox.question(number_detect.ui, 'Notification', 'The camera is opened successfully！')
            if reply == 'StandardButton.Yes':
                pass
        else:
            reply = QMessageBox.question(number_detect.ui, 'Notification', 'The camera failed to open, please check the camera and reconnect!')
            if reply == 'StandardButton.Yes':
                pass

    # 打开图片检测
    def open_image_detect(self):
        # 获取图像的路径
        number_detect.path = QFileDialog.getOpenFileName(self.ui, "选取文件夹", "./")[0]
        number_detect.source = str(number_detect.path)
        number_detect.run0(**vars(opt))
        # img3 = cv2.flip(number_detect.img1, 1)
        img3 = cv2.resize(number_detect.img1, (448, 336))
        img2 = QImage(img3.data, img3.shape[1], img3.shape[0], QImage.Format_BGR888)
        # 将图像显示在QLabel中
        return img2

    # 打开图片检测在tab1显示
    def open_image_detect1(self):
        number_detect.tab1_table = True
        number_detect.tab4_table = False
        img =number_detect.open_image_detect()
        img0 = QPixmap(str(number_detect.path))
        label_size = number_detect.ui.label_1.size()
        scaled_pixmap = img0.scaled(label_size, Qt.KeepAspectRatio)
        number_detect.ui.label_1.setPixmap(scaled_pixmap)
        number_detect.ui.label_2.setPixmap(QPixmap.fromImage(img))
    # 打开图片检测在tab2显示
    def open_image_detect2(self):
        img = number_detect.open_image_detect()
        img0 = QPixmap(str(number_detect.path))
        label_size = number_detect.ui.tab2_label_dis_img_2.size()
        scaled_pixmap = img0.scaled(label_size, Qt.KeepAspectRatio)
        number_detect.ui.tab2_label_dis_img_2.setPixmap(scaled_pixmap)
        number_detect.ui.tab2_label_dis_img.setPixmap(QPixmap.fromImage(img))


    # 打开图片检测在tab3显示
    def open_image_detect3(self):
        img = number_detect.open_image_detect()
        img0 = QPixmap(str(number_detect.path))
        label_size = number_detect.ui.tab3_label_dis_img_2.size()
        scaled_pixmap = img0.scaled(label_size, Qt.KeepAspectRatio)
        number_detect.ui.tab3_label_dis_img_2.setPixmap(scaled_pixmap)
        number_detect.ui.tab3_label_dis_img.setPixmap(QPixmap.fromImage(img))

    # tab1 关闭检测
    def detect_close(self):

        # if number_detect.b == False:
        #     number_detect.realtime_detect0.terminate()

        # if number_detect.b == True:
        number_detect.Cap.release()
        number_detect.b = 0
        # print('cccccccccccc', number_detect.b)

    # tab2 关闭检测
    def detect_close2(self):
        number_detect.Cap.release()
        number_detect.b = 0
        # Cam.release()
        # if number_detect.b == True:
        #     number_detect.Cap.release()
        #     number_detect.b = False

    # tab3 关闭检测
    def detect_close3(self):
        number_detect.Cap.release()
        number_detect.b = 0
        # # Cam.release()
        #
        # if number_detect.b == True:
        #     number_detect.Cap.release()
        #     number_detect.b = False

    # tab4关闭检测
    def detect_close4(self):
        number_detect.Cap.release()
        number_detect.b = 0

    # tab5 关闭检测
    def detect_close5(self):
        number_detect.Cap.release()
        number_detect.b = 0


# 加法
class rand_add(QThread):
    def run(self):
        num = random.randint(0, 10)
        num2 = random.randint(0, 10)
        number_detect.ui.tab5_label_6.setText(str(num))
        number_detect.ui.tab5_label_7.setText(str('+'))
        number_detect.ui.tab5_label_8.setText(str(num2))
        number_detect.r_add = num + num2
        time.sleep(0.3)


class rand_sub(QThread):
    def run(self):
        num = random.randint(0, 10)
        num2 = random.randint(0, num)
        number_detect.ui.tab5_label_6.setText(str(num))
        number_detect.ui.tab5_label_7.setText(str('-'))
        number_detect.ui.tab5_label_8.setText(str(num2))
        number_detect.r_sub = num - num2
        time.sleep(0.3)


class rand_mul(QThread):
    def run(self):
        num = random.randint(0, 10)
        num2 = random.randint(0, 10)
        number_detect.ui.tab5_label_6.setText(str(num))
        number_detect.ui.tab5_label_7.setText(str('*'))
        number_detect.ui.tab5_label_8.setText(str(num2))
        number_detect.r_mul = num * num2
        time.sleep(0.3)


class rand_division(QThread):
    def run(self):
        num = random.randint(1, 99)
        l1 = []
        for i in range(1, num):
            if num % i == 0:
                l1.append(i)
        len0 = len(l1)
        num2 = random.randint(0, len0 - 1)
        num3 = l1[num2]
        number_detect.ui.tab5_label_6.setText(str(num))
        number_detect.ui.tab5_label_7.setText(str('/'))
        number_detect.ui.tab5_label_8.setText(str(num3))

        number_detect.r_division = int(num / num3)
        time.sleep(0.3)


# 拍照检测线程1
class detect_pic(QThread):
    def run(self):
        # print('bbbbbbbbbb', number_detect.b)

        # if number_detect.b == False:
        #     # number_detect.Cap.release()
        #     number_detect.realtime_detect0.terminate()
        #     number_detect.realtime_detect0.terminate()
        #     time.sleep(0.1)
        #     number_detect.Cap.release()
        #     time.sleep(0.2)
        number_detect.b = 2
        # if number_detect.b == True:
        #     # number_detect.Cap.release()
        #     number_detect.Cap = cv2.VideoCapture(number_detect.n, cv2.CAP_DSHOW)  # 相机
        #     img_savedir0 = 'D:\\Python\\YOLO-number\\data\\takepic_detect'
        #     len00 = len(os.listdir(img_savedir0))
        #     img_savedir = 'D:\\Python\\YOLO-number\\data\\takepic_detect\\' + str(len00) + '.jpg'
        #     # number_detect.Cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
        #     ret, frame = number_detect.Cap.read()
        #     number_detect.b = True
        #     print('ret', ret)
        #     if ret:
        #         # frame = cv2.flip(frame, 1)
        #         # 将图像从BGR格式转换为RGB格式
        #         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #         cv2.imwrite(img_savedir, frame_rgb)
        #         time.sleep(0.1)
        #     number_detect.source = str(img_savedir)
        #     number_detect.run2(**vars(opt))
        #     path2 = "./runs/detect"
        #     len0 = len(os.listdir(path2))
        #     if len0 == 1:
        #         path3 = path2 + '/' + 'exp'
        #     else:
        #         path3 = path2 + '/' + 'exp' + str(len0)
        #
        #     file1 = os.listdir(path3)[0]
        #     path4 = path3 + '/' + str(file1)
        #     print(path4)
        #     img0 = QPixmap(str(path4))
        #     label2_size = number_detect.ui.label_2.size()
        #     scaled_pixmap = img0.scaled(label2_size, Qt.KeepAspectRatio)
        #     number_detect.ui.label_2.setPixmap(scaled_pixmap)


# 拍照检测线程2
class detect_pic2(QThread):
    def run(self):
        # number_detect.b = 2
        # if number_detect.b == False:
        #     number_detect.realtime_detect2.terminate()
        #     time.sleep(0.2)
        #     number_detect.Cap.release()
        #     time.sleep(0.2)
        #     number_detect.Cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        number_detect.b = 2
        # if number_detect.b == True:
        #     img_savedir0 = 'D:\\Python\\YOLO-number\\data\\takepic_detect'
        #     len00 = len(os.listdir(img_savedir0))
        #     img_savedir = 'D:\\Python\\YOLO-number\\data\\takepic_detect\\' + str(len00) + '.jpg'
        #
        #     ret, frame = number_detect.Cap.read()
        #     if ret:
        #         # frame = cv2.flip(frame, 1)
        #         # 将图像从BGR格式转换为RGB格式
        #         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #         cv2.imwrite(img_savedir, frame_rgb)
        #         time.sleep(0.1)
        #     number_detect.source = str(img_savedir)
        #     number_detect.run2(**vars(opt))
        #     path2 = "D://Python//YOLO-number//runs//detect"
        #     len0 = len(os.listdir(path2))
        #     if len0 == 1:
        #         path3 = path2 + '//' + 'exp'
        #     else:
        #         path3 = path2 + '//' + 'exp' + str(len0)
        #
        #     file1 = os.listdir(path3)[0]
        #     path4 = path3 + '/' + str(file1)
        #     print(path4)
        #     img0 = QPixmap(str(path4))
        #     label_size = number_detect.ui.tab2_label_dis_img.size()
        #     scaled_pixmap = img0.scaled(label_size, Qt.KeepAspectRatio)
        #     number_detect.ui.tab2_label_dis_img.setPixmap(scaled_pixmap)
            # 只有检测到一个类别且一个目标时才显示在tab2_label_dis_num中
            # if len(number_detect.my_list3) == 1:
            #     s = str(number_detect.my_list3[0])
            #     number_detect.ui.tab2_label_dis_num.setText(s)
            #     if s == '0':
            #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
            #         number_detect.player.play()
            #     elif s == '1':
            #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
            #         number_detect.player.play()
            #     elif s == '2':
            #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
            #         number_detect.player.play()
            #     elif s == '3':
            #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
            #         number_detect.player.play()
            #     elif s == '4':
            #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
            #         number_detect.player.play()
            #     elif s == '5':
            #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
            #         number_detect.player.play()
            #     elif s == '6':
            #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
            #         number_detect.player.play()
            #     elif s == '7':
            #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
            #         number_detect.player.play()
            #     elif s == '8':
            #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
            #         number_detect.player.play()
            #     elif s == '9':
            #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
            #         number_detect.player.play()
            #     elif s == '+':
            #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/plus.wav")))
            #         number_detect.player.play()
            #     elif s == '-':
            #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/minus.wav")))
            #         number_detect.player.play()
            #     elif s == '*':
            #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/times.wav")))
            #         number_detect.player.play()
            #     elif s == '/':
            #         number_detect.player.setMedia(
            #             QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/divided by.wav")))
            #         number_detect.player.play()
            #     elif s == '=':
            #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/equals.wav")))
            #         number_detect.player.play()
            #     font = QFont()
            #     font.setPointSize(24)  # 设置字体大小
            #     number_detect.ui.tab2_label_dis_num.setFont(font)
            #     number_detect.ui.tab2_label_dis_num.setStyleSheet("color: red;")  # 设置字体颜色


# 拍照检测线程3
class detect_pic3(QThread):
    def run(self):

        # if number_detect.b == False:
        #     number_detect.realtime_detect0.terminate()
        #     time.sleep(0.1)
        #     number_detect.Cap.release()
        #     time.sleep(0.2)
        #     number_detect.Cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        #     time.sleep(0.2)
        number_detect.b = 2
        # if number_detect.b == True:
        #
        #     img_savedir0 = 'D:\\Python\\YOLO-number\\data\\takepic_detect'
        #     len00 = len(os.listdir(img_savedir0))
        #     img_savedir = 'D:\\Python\\YOLO-number\\data\\takepic_detect\\' + str(len00) + '.jpg'
        #     ret, frame = number_detect.Cap.read()
        #
        #     if ret:
        #         # frame = cv2.flip(frame, 1)
        #         # 将图像从BGR格式转换为RGB格式
        #         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #         cv2.imwrite(img_savedir, frame_rgb)
        #         time.sleep(0.1)
        #     number_detect.source = str(img_savedir)
        #     number_detect.run2(**vars(opt))
        #     path2 = "D:\\Python\\YOLO-number\\runs\\detect\\"
        #     len0 = len(os.listdir(path2))
        #     if len0 == 1:
        #         path3 = path2 + 'exp'
        #     else:
        #         path3 = path2 + 'exp' + str(len0)
        #     print(path3)
        #     file1 = os.listdir(path3)[0]
        #     path4 = path3 + '\\' + str(file1)
        #     print(path4)
        #     img0 = QPixmap(str(path4))
        #     label_size = number_detect.ui.tab3_label_dis_img.size()
        #     scaled_pixmap = img0.scaled(label_size, Qt.KeepAspectRatio)
        #     number_detect.ui.tab3_label_dis_img.setPixmap(scaled_pixmap)
        #     # 只有检测到一个类别且一个目标时才显示在tab2_label_dis_num中
        #     if len(number_detect.my_list3) == 1:
        #         s = str(number_detect.my_list3[0])
        #         number_detect.ui.tab3_label_dis_symbol.setText(s)
        #         font = QFont()
        #         font.setPointSize(24)  # 设置字体大小
        #         number_detect.ui.tab3_label_dis_symbol.setFont(font)
        #         number_detect.ui.tab3_label_dis_symbol.setStyleSheet("color: red;")  # 设置字体颜色


# 拍照检测线程4
class detect_pic4(QThread):
    def run(self):
        number_detect.b = 2
        # if number_detect.b == True:
        #     number_detect.Cap.release()
        #     time.sleep(0.2)
        # img_savedir0 = 'D:\\Python\\YOLO-number\\data\\takepic_detect'
        # len00 = len(os.listdir(img_savedir0))
        # img_savedir = 'D:\\Python\\YOLO-number\\data\\takepic_detect\\' + str(len00) + '.jpg'
        #
        # ret, frame = number_detect.Cap.read()
        # if ret:
        #     # frame = cv2.flip(frame, 1)
        #     # 将图像从BGR格式转换为RGB格式
        #     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #     cv2.imwrite(img_savedir, frame_rgb)
        #     time.sleep(0.1)
        # number_detect.source = str(img_savedir)
        # number_detect.run2(**vars(opt))
        # path2 = "D:\\Python\\YOLO-number\\runs\\detect\\"
        # len0 = len(os.listdir(path2))
        # if len0 == 1:
        #     path3 = path2 + 'exp'
        # else:
        #     path3 = path2 + 'exp' + str(len0)
        # print(path3)
        # file1 = os.listdir(path3)[0]
        # path4 = path3 + '\\' + str(file1)
        # print(path4)
        # img0 = QPixmap(str(path4))
        # curr_time = datetime.datetime.now()
        # time_now = datetime.datetime.strftime(curr_time, '%H:%M:%S')
        #
        # row_count = number_detect.ui.tab4_tableWidget.rowCount()
        #
        # number_detect.ui.tab4_tableWidget.insertRow(row_count)
        # number_detect.ui.tab4_tableWidget.setItem(row_count, 0, QtWidgets.QTableWidgetItem(str(time_now)))
        # number_detect.ui.tab4_tableWidget.item(row_count, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #
        # font = QFont()
        # font.setPointSize(24)  # 设置字体大小
        # number_detect.ui.tab4_label_1.setFont(font)
        # number_detect.ui.tab4_label_1.setStyleSheet("color: red;")  # 设置字体颜色
        #
        # number_detect.ui.tab4_label_2.setFont(font)
        # number_detect.ui.tab4_label_2.setStyleSheet("color: red;")  # 设置字体颜色
        #
        # number_detect.ui.tab4_label_3.setFont(font)
        # number_detect.ui.tab4_label_3.setStyleSheet("color: red;")  # 设置字体颜色
        #
        # number_detect.ui.tab4_label_4.setFont(font)
        # number_detect.ui.tab4_label_4.setStyleSheet("color: red;")  # 设置字体颜色
        #
        # number_detect.ui.tab4_label_5.setFont(font)
        # number_detect.ui.tab4_label_5.setStyleSheet("color: red;")  # 设置字体颜色
        # label_size = number_detect.ui.tab4_label_dis_img.size()
        # scaled_pixmap = img0.scaled(label_size, Qt.KeepAspectRatio)
        # number_detect.ui.tab4_label_dis_img.setPixmap(scaled_pixmap)
        # list = number_detect.my_list3
        # # print('list', list)
        # # len0 = len(list)
        # s1, s2, s3, s4, s5 = '+', '-', '*', '/', '='
        # # if list[0] == s1 or list[0] == s2 or list[0] == s3 or list[0] == s4 or list[0] == s5:
        # #     reply = QMessageBox.question(number_detect.ui, '信息提示', '算式书写错误，请重新书写并检测！')
        # #     if reply == 'StandardButton.Yes':
        # #         pass
        # if 1:
        #     number_detect.ui.tab4_label_4.setText(s5)
        #     if s1 in list:  # 加法
        #
        #         n0 = list.index(s1)
        #         number_detect.ui.tab4_label_2.setText(s1)
        #
        #         txt1 = list[:n0]
        #         if len(txt1) > 1:
        #             x = str(int(txt1[0]) * 10 + int(txt1[1]))
        #         else:
        #             x = str(int(txt1[0]))
        #
        #         number_detect.ui.tab4_label_1.setText(x)
        #         txt2 = list[n0 + 1:]
        #         if len(txt2) > 1:
        #             x2 = str(int(txt2[0]) * 10 + int(txt2[1]))
        #         else:
        #             x2 = str(int(txt2[0]))
        #         number_detect.ui.tab4_label_3.setText(x2)
        #
        #         x3 = str(int(x) + int(x2))
        #         number_detect.ui.tab4_label_5.setText(x3)
        #         formula = str(x) + '+' + str(x2)
        #         item = QtWidgets.QTableWidgetItem(str('mathe formul'))
        #         item.setForeground(QtGui.QColor(255, 0, 0))
        #         number_detect.ui.tab4_tableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(formula)))
        #         number_detect.ui.tab4_tableWidget.item(row_count, 1).setTextAlignment(
        #             Qt.AlignHCenter | Qt.AlignVCenter)
        #         if 1:
        #             item = QtWidgets.QTableWidgetItem(str('result'))
        #             item.setForeground(QtGui.QColor(255, 0, 0))
        #
        #             number_detect.ui.tab4_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(x3)), )
        #             number_detect.ui.tab4_tableWidget.item(row_count, 2).setTextAlignment(
        #                 Qt.AlignHCenter | Qt.AlignVCenter)
        #
        #     elif s2 in list:  # 减法
        #
        #         n0 = list.index(s2)
        #         number_detect.ui.tab4_label_2.setText(s2)
        #         txt1 = list[:n0]
        #         if len(txt1) > 1:
        #             x = str(int(txt1[0]) * 10 + int(txt1[1]))
        #         else:
        #             x = str(int(txt1[0]))
        #         number_detect.ui.tab4_label_1.setText(x)
        #         txt2 = list[n0 + 1:]
        #         if len(txt2) > 1:
        #             x2 = str(int(txt2[0]) * 10 + int(txt2[1]))
        #         else:
        #             x2 = str(int(txt2[0]))
        #         number_detect.ui.tab4_label_3.setText(x2)
        #         x3 = str(int(x) - int(x2))
        #         number_detect.ui.tab4_label_5.setText(x3)
        #         formula = str(x) + '-' + str(x2)
        #         item = QtWidgets.QTableWidgetItem(str('mathe formul'))
        #         item.setForeground(QtGui.QColor(255, 0, 0))
        #         number_detect.ui.tab4_tableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(formula)))
        #         number_detect.ui.tab4_tableWidget.item(row_count, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #         if 1:
        #             item = QtWidgets.QTableWidgetItem(str('result'))
        #             item.setForeground(QtGui.QColor(255, 0, 0))
        #             number_detect.ui.tab4_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(x3)), )
        #             number_detect.ui.tab4_tableWidget.item(row_count, 2).setTextAlignment(
        #                 Qt.AlignHCenter | Qt.AlignVCenter)
        #
        #     elif s3 in list:  # 乘法
        #
        #         n0 = list.index(s3)
        #
        #         number_detect.ui.tab4_label_2.setText(s3)
        #         txt1 = list[:n0]
        #         if len(txt1) > 1:
        #             x = str(int(txt1[0]) * 10 + int(txt1[1]))
        #         else:
        #             x = str(int(txt1[0]))
        #         number_detect.ui.tab4_label_1.setText(x)
        #         txt2 = list[n0 + 1:]
        #         if len(txt2) > 1:
        #             x2 = str(int(txt2[0]) * 10 + int(txt2[1]))
        #         else:
        #             x2 = str(int(txt2[0]))
        #         number_detect.ui.tab4_label_3.setText(x2)
        #
        #         x3 = str(int(x) * int(x2))
        #         number_detect.ui.tab4_label_5.setText(x3)
        #         formula = str(x) + '*' + str(x2)
        #         item = QtWidgets.QTableWidgetItem(str('mathe formul'))
        #         item.setForeground(QtGui.QColor(255, 0, 0))
        #         number_detect.ui.tab4_tableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(formula)))
        #         number_detect.ui.tab4_tableWidget.item(row_count, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #         if 1:
        #             item = QtWidgets.QTableWidgetItem(str('result'))
        #             item.setForeground(QtGui.QColor(255, 0, 0))
        #             number_detect.ui.tab4_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(x3)), )
        #             number_detect.ui.tab4_tableWidget.item(row_count, 2).setTextAlignment(
        #                 Qt.AlignHCenter | Qt.AlignVCenter)
        #
        #     elif s4 in list:  # 除法
        #
        #         n0 = list.index(s4)
        #
        #         number_detect.ui.tab4_label_2.setText(s4)
        #         txt1 = list[:n0]
        #         if len(txt1) > 1:
        #             x = str(txt1[0] * 10 + txt1[1])
        #         else:
        #             x = str(txt1[0])
        #         number_detect.ui.tab4_label_1.setText(x)
        #
        #         txt2 = list[n0 + 1:]
        #         if len(txt2) > 1:
        #             x2 = str(int(txt2[0]) * 10 + int(txt2[1]))
        #         else:
        #             x2 = str(int(txt2[0]))
        #         number_detect.ui.tab4_label_3.setText(x2)
        #         x3 = str(int(x) / int(x2))
        #         number_detect.ui.tab4_label_5.setText(x3)
        #         formula = str(x) + '/' + str(x2)
        #         item = QtWidgets.QTableWidgetItem(str('mathe formul'))
        #         item.setForeground(QtGui.QColor(255, 0, 0))
        #         number_detect.ui.tab4_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(formula)))
        #         number_detect.ui.tab4_tableWidget.item(row_count, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #         if 1:
        #             item = QtWidgets.QTableWidgetItem(str('result'))
        #             item.setForeground(QtGui.QColor(255, 0, 0))
        #             number_detect.ui.tab4_tableWidget.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(x3)), )
         #             number_detect.ui.tab4_tableWidget.item(row_count, 3).setTextAlignment(
        #                 Qt.AlignHCenter | Qt.AlignVCenter)
        # if s1 in list:
        #     if int(x[0]) == 0:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x[0]) == 1:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x[0]) == 2:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x[0]) == 3:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x[0]) == 4:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x[0]) == 5:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x[0]) == 6:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x[0]) == 7:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x[0]) == 8:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x[0]) == 9:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #
        #     number_detect.player.setMedia(
        #         QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/plus.wav")))
        #     number_detect.player.play()
        #     time.sleep(1)
        #
        #     if int(x2[0]) == 0:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x2[0]) == 1:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x2[0]) == 2:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x2[0]) == 3:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x2[0]) == 4:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x2[0]) == 5:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x2[0]) == 6:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x2[0]) == 7:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x2[0]) == 8:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x2[0]) == 9:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/equals.wav")))
        #     number_detect.player.play()
        #     time.sleep(1)
        #
        #     if int(x3[0]) == 0:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x3[0]) == 1:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x3[0]) == 2:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x3[0]) == 3:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x3[0]) == 4:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x3[0]) == 5:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x3[0]) == 6:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x3[0]) == 7:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x3[0]) == 8:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)
        #     elif int(x3[0]) == 9:
        #         number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
        #         number_detect.player.play()
        #         time.sleep(1)


# 拍照检测线程5
class detect_pic5(QThread):
    def run(self):
        number_detect.b = 2
        # if number_detect.b == True:
        #     number_detect.Cap.release()
        #     time.sleep(0.2)
        # img_savedir0 = 'D:\\Python\\YOLO-number\\data\\takepic_detect'
        # len00 = len(os.listdir(img_savedir0))
        # img_savedir = 'D:\\Python\\YOLO-number\\data\\takepic_detect\\' + str(len00) + '.jpg'
        # ret, frame = number_detect.Cap.read()
        # if ret:
        #     # frame = cv2.flip(frame, 1)
        #     # 将图像从BGR格式转换为RGB格式
        #     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #     cv2.imwrite(img_savedir, frame_rgb)
        #     time.sleep(0.1)
        # number_detect.source = str(img_savedir)
        # number_detect.run2(**vars(opt))
        # path2 = "D:\\Python\\YOLO-number\\runs\\detect\\"
        # len0 = len(os.listdir(path2))
        # if len0 == 1:
        #     path3 = path2 + 'exp'
        # else:
        #     path3 = path2 + 'exp' + str(len0)
        # print(path3)
        # file1 = os.listdir(path3)[0]
        # path4 = path3 + '\\' + str(file1)
        # print(path4)
        # img0 = QPixmap(str(path4))
        # curr_time = datetime.datetime.now()
        # time_now = datetime.datetime.strftime(curr_time, '%H:%M:%S')
        # row_count = number_detect.ui.tab5_tableWidget.rowCount()
        # number_detect.ui.tab5_tableWidget.insertRow(row_count)
        # number_detect.ui.tab5_tableWidget.setItem(row_count, 0, QtWidgets.QTableWidgetItem(str(time_now)))
        # number_detect.ui.tab5_tableWidget.item(row_count, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #
        # font = QFont()
        # font.setPointSize(24)  # 设置字体大小
        # number_detect.ui.tab5_label_1.setFont(font)
        # number_detect.ui.tab5_label_1.setStyleSheet("color: red;")  # 设置字体颜色
        #
        # number_detect.ui.tab5_label_2.setFont(font)
        # number_detect.ui.tab5_label_2.setStyleSheet("color: red;")  # 设置字体颜色
        #
        # number_detect.ui.tab5_label_3.setFont(font)
        # number_detect.ui.tab4_label_3.setStyleSheet("color: red;")  # 设置字体颜色
        #
        # number_detect.ui.tab5_label_4.setFont(font)
        # number_detect.ui.tab5_label_4.setStyleSheet("color: red;")  # 设置字体颜色
        #
        # number_detect.ui.tab5_label_5.setFont(font)
        # number_detect.ui.tab5_label_5.setStyleSheet("color: red;")  # 设置字体颜色
        #
        # label_size = number_detect.ui.tab5_label_dis_img.size()
        # scaled_pixmap = img0.scaled(label_size, Qt.KeepAspectRatio)
        # number_detect.ui.tab5_label_dis_img.setPixmap(scaled_pixmap)
        # list = number_detect.my_list3
        # # print('list', list)
        # # len0 = len(list)
        # s1, s2, s3, s4, s5 = '+', '-', '*', '/', '='
        # # if list[0] == s1 or list[0] == s2 or list[0] == s3 or list[0] == s4 or list[0] == s5:
        # #     reply = QMessageBox.question(number_detect.ui, '信息提示', '算式书写错误，请重新书写并检测！')
        # #     if reply == 'StandardButton.Yes':
        # #         pass
        # if 1:
        #     number_detect.ui.tab5_label_4.setText(s5)
        #     if (s1 in list) and (s5 in list):  # 加法
        #         n4 = list.index(s5)
        #         n0 = list.index(s1)
        #         number_detect.ui.tab5_label_2.setText(s1)
        #         txt1 = list[:n0]
        #         if len(txt1) > 1:
        #             x = str(int(txt1[0]) * 10 + int(txt1[1]))
        #         else:
        #             x = str(int(txt1[0]))
        #         number_detect.ui.tab5_label_1.setText(x)
        #         txt2 = list[n0 + 1:n4]
        #         if len(txt2) > 1:
        #             x2 = str(int(txt2[0]) * 10 + int(txt2[1]))
        #         else:
        #             x2 = str(int(txt2[0]))
        #         number_detect.ui.tab5_label_3.setText(x2)
        #         txt3 = list[n4 + 1:]
        #         if len(txt3) == 1:
        #             x3 = str(int(txt3[0]))
        #
        #         elif len(txt3) == 2:
        #             x3 = str(int(txt3[0]) * 10 + int(txt3[1]))
        #         elif len(txt3) == 3:
        #             x3 = str(int(txt3[0]) * 100 + int(txt3[1]) * 10 + int(txt3[2]))
        #         elif len(txt3) == 4:
        #             x3 = str(int(txt3[0]) * 1000 + int(txt3[1]) * 100 + int(txt3[2]) * 10 + int(txt3[3]))
        #
        #         # x3 = str(int(x) + int(x2))
        #         number_detect.ui.tab5_label_5.setText(x3)
        #         formula = str(x) + s1 + str(x2) + s5 + str(x3)
        #         item = QtWidgets.QTableWidgetItem(str('mathe formul'))
        #         item.setForeground(QtGui.QColor(255, 0, 0))
        #         number_detect.ui.tab5_tableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(formula)))
        #         number_detect.ui.tab5_tableWidget.item(row_count, 1).setTextAlignment(
        #             Qt.AlignHCenter | Qt.AlignVCenter)
        #         if int(x3) == number_detect.r_add:
        #             item = QtWidgets.QTableWidgetItem(str('result'))
        #             item.setForeground(QtGui.QColor(255, 0, 0))
        #
        #             number_detect.ui.tab5_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('√')), )
        #             number_detect.ui.tab5_tableWidget.item(row_count, 2).setTextAlignment(
        #                 Qt.AlignHCenter | Qt.AlignVCenter)
        #         else:
        #             item = QtWidgets.QTableWidgetItem(str('result'))
        #             item.setForeground(QtGui.QColor(255, 0, 0))
        #
        #             number_detect.ui.tab5_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('x')), )
        #             number_detect.ui.tab5_tableWidget.item(row_count, 2).setTextAlignment(
        #                 Qt.AlignHCenter | Qt.AlignVCenter)
        #
        #     elif (s2 in list) and (s5 in list):  # 减法
        #         n4 = list.index(s5)
        #         n0 = list.index(s2)
        #         number_detect.ui.tab5_label_2.setText(s2)
        #         txt1 = list[:n0]
        #         if len(txt1) > 1:
        #             x = str(int(txt1[0]) * 10 + int(txt1[1]))
        #         else:
        #             x = str(int(txt1[0]))
        #         number_detect.ui.tab5_label_1.setText(x)
        #         txt2 = list[n0 + 1:n4]
        #         if len(txt2) > 1:
        #             x2 = str(int(txt2[0]) * 10 + int(txt2[1]))
        #         else:
        #             x2 = str(int(txt2[0]))
        #         number_detect.ui.tab5_label_3.setText(x2)
        #         txt3 = list[n4 + 1:]
        #         if len(txt3) == 1:
        #             x3 = str(int(txt3[0]))
        #
        #         elif len(txt3) == 2:
        #             x3 = str(int(txt3[0]) * 10 + int(txt3[1]))
        #         elif len(txt3) == 3:
        #             x3 = str(int(txt3[0]) * 100 + int(txt3[1]) * 10 + int(txt3[2]))
        #         elif len(txt3) == 4:
        #             x3 = str(int(txt3[0]) * 1000 + int(txt3[1]) * 100 + int(txt3[2]) * 10 + int(txt3[3]))
        #         number_detect.ui.tab5_label_5.setText(x3)
        #         formula = str(x) + s2 + str(x2) + s5 + str(x3)
        #         item = QtWidgets.QTableWidgetItem(str('mathe formul'))
        #         item.setForeground(QtGui.QColor(255, 0, 0))
        #         number_detect.ui.tab5_tableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(formula)))
        #         number_detect.ui.tab5_tableWidget.item(row_count, 1).setTextAlignment(
        #             Qt.AlignHCenter | Qt.AlignVCenter)
        #         if int(x3) == number_detect.r_sub:
        #             item = QtWidgets.QTableWidgetItem(str('result'))
        #             item.setForeground(QtGui.QColor(255, 0, 0))
        #             number_detect.ui.tab5_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('√')), )
        #             number_detect.ui.tab5_tableWidget.item(row_count, 2).setTextAlignment(
        #                 Qt.AlignHCenter | Qt.AlignVCenter)
        #         else:
        #             item = QtWidgets.QTableWidgetItem(str('result'))
        #             item.setForeground(QtGui.QColor(255, 0, 0))
        #
        #             number_detect.ui.tab5_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('x')), )
        #             number_detect.ui.tab5_tableWidget.item(row_count, 2).setTextAlignment(
        #                 Qt.AlignHCenter | Qt.AlignVCenter)
        #
        #     elif (s3 in list) and (s5 in list):  # 乘法
        #         n4 = list.index(s5)
        #         n0 = list.index(s3)
        #
        #         number_detect.ui.tab5_label_2.setText(s3)
        #         txt1 = list[:n0]
        #         if len(txt1) > 1:
        #             x = str(int(txt1[0]) * 10 + int(txt1[1]))
        #         else:
        #             x = str(int(txt1[0]))
        #         number_detect.ui.tab5_label_1.setText(x)
        #         txt2 = list[n0 + 1:]
        #         if len(txt2) > 1:
        #             x2 = str(int(txt2[0]) * 10 + int(txt2[1]))
        #         else:
        #             x2 = str(int(txt2[0]))
        #         number_detect.ui.tab5_label_3.setText(x2)
        #         txt3 = list[n4 + 1:]
        #         if len(txt3) == 1:
        #             x3 = str(int(txt3[0]))
        #         elif len(txt3) == 2:
        #             x3 = str(int(txt3[0]) * 10 + int(txt3[1]))
        #         elif len(txt3) == 3:
        #             x3 = str(int(txt3[0]) * 100 + int(txt3[1]) * 10 + int(txt3[2]))
        #         elif len(txt3) == 4:
        #             x3 = str(int(txt3[0]) * 1000 + int(txt3[1]) * 100 + int(txt3[2]) * 10 + int(txt3[3]))
        #         number_detect.ui.tab5_label_5.setText(x3)
        #         formula = str(x) + '*' + str(x2) + s5 + str(x3)
        #         item = QtWidgets.QTableWidgetItem(str('mathe formul'))
        #         item.setForeground(QtGui.QColor(255, 0, 0))
        #         number_detect.ui.tab5_tableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(formula)))
        #         number_detect.ui.tab5_tableWidget.item(row_count, 1).setTextAlignment(
        #             Qt.AlignHCenter | Qt.AlignVCenter)
        #         if int(x3) == number_detect.r_mul:
        #             item = QtWidgets.QTableWidgetItem(str('result'))
        #             item.setForeground(QtGui.QColor(255, 0, 0))
        #             number_detect.ui.tab5_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('√')), )
        #             number_detect.ui.tab5_tableWidget.item(row_count, 2).setTextAlignment(
        #                 Qt.AlignHCenter | Qt.AlignVCenter)
        #         else:
        #             item = QtWidgets.QTableWidgetItem(str('result'))
        #             item.setForeground(QtGui.QColor(255, 0, 0))
        #
        #             number_detect.ui.tab5_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('x')), )
        #             number_detect.ui.tab5_tableWidget.item(row_count, 2).setTextAlignment(
        #                 Qt.AlignHCenter | Qt.AlignVCenter)
        #
        #     elif (s4 in list) and (s5 in list):  # 除法
        #         n4 = list.index(s5)
        #         n0 = list.index(s4)
        #         number_detect.ui.tab5_label_2.setText(s4)
        #         txt1 = list[:n0]
        #         if len(txt1) > 1:
        #             x = str(int(txt1[0]) * 10 + int(txt1[1]))
        #         else:
        #             x = str(int(txt1[0]))
        #         number_detect.ui.tab5_label_1.setText(x)
        #
        #         txt2 = list[n0 + 1:n4]
        #         if len(txt2) > 1:
        #             x2 = str(int(txt2[0]) * 10 + int(txt2[1]))
        #         else:
        #             x2 = str(int(txt2[0]))
        #         number_detect.ui.tab5_label_3.setText(x2)
        #         txt3 = list[n4 + 1:]
        #         if len(txt3) == 1:
        #             x3 = str(int(txt3[0]))
        #
        #         elif len(txt3) == 2:
        #             x3 = str(int(txt3[0]) * 10 + int(txt3[1]))
        #         elif len(txt3) == 3:
        #             x3 = str(int(txt3[0]) * 100 + int(txt3[1]) * 10 + int(txt3[2]))
        #         elif len(txt3) == 4:
        #             x3 = str(int(txt3[0]) * 1000 + int(txt3[1]) * 100 + int(txt3[2]) * 10 + int(txt3[3]))
        #
        #         number_detect.ui.tab5_label_5.setText(x3)
        #         formula = str(x) + s4 + str(x2) + s5 + str(x3)
        #         item = QtWidgets.QTableWidgetItem(str('mathe formul'))
        #         item.setForeground(QtGui.QColor(255, 0, 0))
        #         number_detect.ui.tab5_tableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(formula)))
        #         number_detect.ui.tab5_tableWidget.item(row_count, 1).setTextAlignment(
        #             Qt.AlignHCenter | Qt.AlignVCenter)
        #         if int(x3) == number_detect.r_division:
        #             item = QtWidgets.QTableWidgetItem(str('result'))
        #             item.setForeground(QtGui.QColor(255, 0, 0))
        #             number_detect.ui.tab5_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('√')), )
        #             number_detect.ui.tab5_tableWidget.item(row_count, 2).setTextAlignment(
        #                 Qt.AlignHCenter | Qt.AlignVCenter)
        #         else:
        #             item = QtWidgets.QTableWidgetItem(str('result'))
        #             item.setForeground(QtGui.QColor(255, 0, 0))
        #             number_detect.ui.tab5_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('x')), )
        #             number_detect.ui.tab5_tableWidget.item(row_count, 2).setTextAlignment(
        #                 Qt.AlignHCenter | Qt.AlignVCenter)


# 实时检测线程1
class realtime_detect(QThread):
    def run(self):

        number_detect.source = 1

        while 1:
            img0 = number_detect.run2(**vars(opt))
            # img = cv2.flip(img0, 1)
            # img = cv2.resize(img, (448, 336))
            # img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
            # # 将图像显示在QLabel中
            # number_detect.ui.label_1.setPixmap(QPixmap.fromImage(img))
            if number_detect.b == 2:
                number_detect.run0(**vars(opt))

                img3 = cv2.flip(number_detect.img1, 1)
                img3 = cv2.resize(img3, (448, 336))
                img2 = QImage(img3.data, img3.shape[1], img3.shape[0], QImage.Format_BGR888)
                # 将图像显示在QLabel中
                number_detect.ui.label_2.setPixmap(QPixmap.fromImage(img2))
            elif number_detect.b == 0:
                return 0
            img = cv2.resize(img0, (448, 336))
            img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_BGR888)
            # 将图像显示在QLabel中
            number_detect.ui.label_1.setPixmap(QPixmap.fromImage(img))


# 实时检测线程2
class realtime_detect2(QThread):
    def run(self):
        number_detect.source = 1

        while 1:
            img0 = number_detect.run2(**vars(opt))
            # img = cv2.flip(img0, 1)
            # img = cv2.resize(img, (448, 336))
            # img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
            # # 将图像显示在QLabel中
            # number_detect.ui.label_1.setPixmap(QPixmap.fromImage(img))
            if number_detect.b == 2:
                number_detect.run0(**vars(opt))

                img3 = cv2.flip(number_detect.img1, 1)
                img3 = cv2.resize(img3, (448, 336))
                img2 = QImage(img3.data, img3.shape[1], img3.shape[0], QImage.Format_BGR888)
                # 将图像显示在QLabel中
                number_detect.ui.tab2_label_dis_img.setPixmap(QPixmap.fromImage(img2))
                if len(number_detect.my_list3) == 1:
                    s = str(number_detect.my_list3[0])
                    number_detect.ui.tab2_label_dis_num.setText(s)
                    if s == '0':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
                        number_detect.player.play()
                    elif s == '1':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                        number_detect.player.play()
                    elif s == '2':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                        number_detect.player.play()
                    elif s == '3':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                        number_detect.player.play()
                    elif s == '4':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                        number_detect.player.play()
                    elif s == '5':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                        number_detect.player.play()
                    elif s == '6':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                        number_detect.player.play()
                    elif s == '7':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                        number_detect.player.play()
                    elif s == '8':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                        number_detect.player.play()
                    elif s == '9':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                        number_detect.player.play()
                    elif s == '+':
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/plus.wav")))
                        number_detect.player.play()
                    elif s == '-':
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/minus.wav")))
                        number_detect.player.play()
                    elif s == '*':
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/times.wav")))
                        number_detect.player.play()
                    elif s == '/':
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/divided by.wav")))
                        number_detect.player.play()
                    elif s == '=':
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/equals.wav")))
                        number_detect.player.play()
                    font = QFont()
                    font.setPointSize(24)  # 设置字体大小
                    number_detect.ui.tab2_label_dis_num.setFont(font)
                    number_detect.ui.tab2_label_dis_num.setStyleSheet("color: red;")  # 设置字体颜色
            elif number_detect.b == 0:
                return 0
            img = cv2.resize(img0, (448, 336))
            img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_BGR888)
            # 将图像显示在QLabel中
            number_detect.ui.tab2_label_dis_img_2.setPixmap(QPixmap.fromImage(img))


# 实时检测线程3
class realtime_detect3(QThread):
    def run(self):
        number_detect.source = 1

        while 1:
            img0 = number_detect.run2(**vars(opt))
            # img = cv2.flip(img0, 1)
            # img = cv2.resize(img, (448, 336))
            # img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
            # # 将图像显示在QLabel中
            # number_detect.ui.label_1.setPixmap(QPixmap.fromImage(img))
            if number_detect.b == 2:
                number_detect.run0(**vars(opt))

                img3 = cv2.flip(number_detect.img1, 1)
                img3 = cv2.resize(img3, (448, 336))
                img2 = QImage(img3.data, img3.shape[1], img3.shape[0], QImage.Format_BGR888)
                # 将图像显示在QLabel中
                number_detect.ui.tab3_label_dis_img.setPixmap(QPixmap.fromImage(img2))
                if len(number_detect.my_list3) == 1:
                    s = str(number_detect.my_list3[0])
                    number_detect.ui.tab3_label_dis_symbol.setText(s)
                    if s == '0':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
                        number_detect.player.play()
                    elif s == '1':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                        number_detect.player.play()
                    elif s == '2':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                        number_detect.player.play()
                    elif s == '3':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                        number_detect.player.play()
                    elif s == '4':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                        number_detect.player.play()
                    elif s == '5':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                        number_detect.player.play()
                    elif s == '6':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                        number_detect.player.play()
                    elif s == '7':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                        number_detect.player.play()
                    elif s == '8':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                        number_detect.player.play()
                    elif s == '9':
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                        number_detect.player.play()
                    elif s == '+':
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/plus.wav")))
                        number_detect.player.play()
                    elif s == '-':
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/minus.wav")))
                        number_detect.player.play()
                    elif s == '*':
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/times.wav")))
                        number_detect.player.play()
                    elif s == '/':
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/divided by.wav")))
                        number_detect.player.play()
                    elif s == '=':
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/equals.wav")))
                        number_detect.player.play()
                    font = QFont()
                    font.setPointSize(24)  # 设置字体大小
                    number_detect.ui.tab3_label_dis_symbol.setFont(font)
                    number_detect.ui.tab3_label_dis_symbol.setStyleSheet("color: red;")  # 设置字体颜色
            elif number_detect.b == 0:
                return 0
            img = cv2.resize(img0, (448, 336))
            img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_BGR888)
            # 将图像显示在QLabel中
            number_detect.ui.tab3_label_dis_img_2.setPixmap(QPixmap.fromImage(img))


# 实时检测线程4
class realtime_detect4(QThread):
    @property
    def run(self):

        number_detect.source = 1

        while 1:
            img0 = number_detect.run2(**vars(opt))
            # img = cv2.flip(img0, 1)
            # img = cv2.resize(img, (448, 336))
            # img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
            # # 将图像显示在QLabel中
            # number_detect.ui.label_1.setPixmap(QPixmap.fromImage(img))
            if number_detect.b == 2:
                number_detect.run0(**vars(opt))

                img3 = cv2.flip(number_detect.img1, 1)
                img3 = cv2.resize(img3, (448, 336))
                img2 = QImage(img3.data, img3.shape[1], img3.shape[0], QImage.Format_BGR888)
                # 将图像显示在QLabel中
                number_detect.ui.tab4_label_dis_img_2.setPixmap(QPixmap.fromImage(img2))
                curr_time = datetime.datetime.now()
                time_now = datetime.datetime.strftime(curr_time, '%H:%M:%S')

                row_count = number_detect.ui.tab4_tableWidget.rowCount()

                number_detect.ui.tab4_tableWidget.insertRow(row_count)
                number_detect.ui.tab4_tableWidget.setItem(row_count, 0, QtWidgets.QTableWidgetItem(str(time_now)))
                number_detect.ui.tab4_tableWidget.item(row_count, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                font = QFont()
                font.setPointSize(24)  # 设置字体大小
                number_detect.ui.tab4_label_1.setFont(font)
                number_detect.ui.tab4_label_1.setStyleSheet("color: red;")  # 设置字体颜色

                number_detect.ui.tab4_label_2.setFont(font)
                number_detect.ui.tab4_label_2.setStyleSheet("color: red;")  # 设置字体颜色

                number_detect.ui.tab4_label_3.setFont(font)
                number_detect.ui.tab4_label_3.setStyleSheet("color: red;")  # 设置字体颜色

                number_detect.ui.tab4_label_4.setFont(font)
                number_detect.ui.tab4_label_4.setStyleSheet("color: red;")  # 设置字体颜色

                number_detect.ui.tab4_label_5.setFont(font)
                number_detect.ui.tab4_label_5.setStyleSheet("color: red;")  # 设置字体颜色
                # label_size = number_detect.ui.tab4_label_dis_img.size()
                # scaled_pixmap = img0.scaled(label_size, Qt.KeepAspectRatio)
                # number_detect.ui.tab4_label_dis_img.setPixmap(scaled_pixmap)
                list = number_detect.my_list3
                # print('list', list)
                # len0 = len(list)
                s1, s2, s3, s4, s5 = '+', '-', '*', '/', '='
                # if list[0] == s1 or list[0] == s2 or list[0] == s3 or list[0] == s4 or list[0] == s5:
                #     reply = QMessageBox.question(number_detect.ui, '信息提示', '算式书写错误，请重新书写并检测！')
                #     if reply == 'StandardButton.Yes':
                #         pass
                if 1:
                    number_detect.ui.tab4_label_4.setText(s5)
                    if s1 in list:  # 加法

                        n0 = list.index(s1)
                        number_detect.ui.tab4_label_2.setText(s1)

                        txt1 = list[:n0]
                        if len(txt1) > 1:
                            x = str(int(txt1[0]) * 10 + int(txt1[1]))
                        else:
                            x = str(int(txt1[0]))

                        number_detect.ui.tab4_label_1.setText(x)
                        txt2 = list[n0 + 1:]
                        if len(txt2) > 1:
                            x2 = str(int(txt2[0]) * 10 + int(txt2[1]))
                        else:
                            x2 = str(int(txt2[0]))
                        number_detect.ui.tab4_label_3.setText(x2)

                        x3 = str(int(x) + int(x2))
                        number_detect.ui.tab4_label_5.setText(x3)
                        formula = str(x) + '+' + str(x2)
                        item = QtWidgets.QTableWidgetItem(str('mathe formul'))
                        item.setForeground(QtGui.QColor(255, 0, 0))
                        number_detect.ui.tab4_tableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(formula)))
                        number_detect.ui.tab4_tableWidget.item(row_count, 1).setTextAlignment(
                            Qt.AlignHCenter | Qt.AlignVCenter)
                        if 1:
                            item = QtWidgets.QTableWidgetItem(str('result'))
                            item.setForeground(QtGui.QColor(255, 0, 0))

                            number_detect.ui.tab4_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(x3)), )
                            number_detect.ui.tab4_tableWidget.item(row_count, 2).setTextAlignment(
                                Qt.AlignHCenter | Qt.AlignVCenter)

                    elif s2 in list:  # 减法

                        n0 = list.index(s2)
                        number_detect.ui.tab4_label_2.setText(s2)
                        txt1 = list[:n0]
                        if len(txt1) > 1:
                            x = str(int(txt1[0]) * 10 + int(txt1[1]))
                        else:
                            x = str(int(txt1[0]))
                        number_detect.ui.tab4_label_1.setText(x)
                        txt2 = list[n0 + 1:]
                        if len(txt2) > 1:
                            x2 = str(int(txt2[0]) * 10 + int(txt2[1]))
                        else:
                            x2 = str(int(txt2[0]))
                        number_detect.ui.tab4_label_3.setText(x2)
                        x3 = str(int(x) - int(x2))
                        number_detect.ui.tab4_label_5.setText(x3)
                        formula = str(x) + '-' + str(x2)
                        item = QtWidgets.QTableWidgetItem(str('mathe formul'))
                        item.setForeground(QtGui.QColor(255, 0, 0))
                        number_detect.ui.tab4_tableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(formula)))
                        number_detect.ui.tab4_tableWidget.item(row_count, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        if 1:
                            item = QtWidgets.QTableWidgetItem(str('result'))
                            item.setForeground(QtGui.QColor(255, 0, 0))
                            number_detect.ui.tab4_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(x3)), )
                            number_detect.ui.tab4_tableWidget.item(row_count, 2).setTextAlignment(
                                Qt.AlignHCenter | Qt.AlignVCenter)

                    elif s3 in list:  # 乘法

                        n0 = list.index(s3)

                        number_detect.ui.tab4_label_2.setText(s3)
                        txt1 = list[:n0]
                        if len(txt1) > 1:
                            x = str(int(txt1[0]) * 10 + int(txt1[1]))
                        else:
                            x = str(int(txt1[0]))
                        number_detect.ui.tab4_label_1.setText(x)
                        txt2 = list[n0 + 1:]
                        if len(txt2) > 1:
                            x2 = str(int(txt2[0]) * 10 + int(txt2[1]))
                        else:
                            x2 = str(int(txt2[0]))
                        number_detect.ui.tab4_label_3.setText(x2)

                        x3 = str(int(x) * int(x2))
                        number_detect.ui.tab4_label_5.setText(x3)
                        formula = str(x) + '*' + str(x2)
                        item = QtWidgets.QTableWidgetItem(str('mathe formul'))
                        item.setForeground(QtGui.QColor(255, 0, 0))
                        number_detect.ui.tab4_tableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(formula)))
                        number_detect.ui.tab4_tableWidget.item(row_count, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        if 1:
                            item = QtWidgets.QTableWidgetItem(str('result'))
                            item.setForeground(QtGui.QColor(255, 0, 0))
                            number_detect.ui.tab4_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(x3)), )
                            number_detect.ui.tab4_tableWidget.item(row_count, 2).setTextAlignment(
                                Qt.AlignHCenter | Qt.AlignVCenter)

                    elif s4 in list:  # 除法

                        n0 = list.index(s4)

                        number_detect.ui.tab4_label_2.setText(s4)
                        txt1 = list[:n0]
                        if len(txt1) > 1:
                            x = str(txt1[0] * 10 + txt1[1])
                        else:
                            x = str(txt1[0])
                        number_detect.ui.tab4_label_1.setText(x)

                        txt2 = list[n0 + 1:]
                        if len(txt2) > 1:
                            x2 = str(int(txt2[0]) * 10 + int(txt2[1]))
                        else:
                            x2 = str(int(txt2[0]))
                        number_detect.ui.tab4_label_3.setText(x2)
                        x3 = str(int(x) / int(x2))
                        number_detect.ui.tab4_label_5.setText(x3)
                        formula = str(x) + '/' + str(x2)
                        item = QtWidgets.QTableWidgetItem(str('mathe formul'))
                        item.setForeground(QtGui.QColor(255, 0, 0))
                        number_detect.ui.tab4_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(formula)))
                        number_detect.ui.tab4_tableWidget.item(row_count, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        if 1:
                            item = QtWidgets.QTableWidgetItem(str('result'))
                            item.setForeground(QtGui.QColor(255, 0, 0))
                            number_detect.ui.tab4_tableWidget.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(x3)), )
                            number_detect.ui.tab4_tableWidget.item(row_count, 3).setTextAlignment(
                                Qt.AlignHCenter | Qt.AlignVCenter)
                # 语音播报
                #-------------------------------------------------------------------------------------------------------------------------------

                if s1 in list:
                    if int(x) == 0:  # 加数
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 1:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 2:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 3:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 4:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 5:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 6:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 7:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 8:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 9:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 10:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/10.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 11:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/11.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 12:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/12.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 13:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/13.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 14:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/14.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 15:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/15.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 16:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/16.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 17:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/17.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 18:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/18.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 19:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/19.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif 20 <= int(x) < 30:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 30 <= int(x) < 40:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 40 <= int(x) < 50:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 50 <= int(x) < 60:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 60 <= int(x) < 70:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 70 <= int(x) < 80:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 80 <= int(x) < 90:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 90 <= int(x) < 100:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif int(x) == 100:
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/100.wav")))
                        number_detect.player.play()
                        time.sleep(1)

                    # 加号
                    number_detect.player.setMedia(
                        QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/plus.wav")))
                    number_detect.player.play()
                    time.sleep(1)
                    # 被加数
                    if int(x2) == 0:  # 加数
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 1:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 2:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 3:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 4:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 5:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 6:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 7:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 8:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 9:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 10:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/10.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 11:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/11.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 12:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/12.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 13:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/13.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 14:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/14.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 15:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/15.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 16:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/16.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 17:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/17.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 18:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/18.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 19:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/19.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif 20 <= int(x2) < 30:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 30 <= int(x2) < 40:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 40 <= int(x2) < 50:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 50 <= int(x2) < 60:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 60 <= int(x2) < 70:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 70 <= int(x2) < 80:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 80 <= int(x2) < 90:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 90 <= int(x2) < 100:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif int(x2) == 100:
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/100.wav")))
                        number_detect.player.play()
                        time.sleep(1)

                    # = 号
                    number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/equals.wav")))
                    number_detect.player.play()
                    time.sleep(1)

                    # 结果
                    if int(x3) == 0:  # 加数
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 1:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 2:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 3:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 4:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 5:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 6:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 7:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 8:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 9:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 10:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/10.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 11:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/11.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 12:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/12.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 13:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/13.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 14:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/14.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 15:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/15.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 16:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/16.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 17:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/17.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 18:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/18.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 19:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/19.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif 20 <= int(x3) < 30:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 30 <= int(x3) < 40:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 40 <= int(x3) < 50:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 50 <= int(x3) < 60:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 60 <= int(x3) < 70:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 70 <= int(x3) < 80:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 80 <= int(x3) < 90:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 90 <= int(x3) < 100:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif int(x3) == 100:
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/100.wav")))
                        number_detect.player.play()
                        time.sleep(1)

                        # ------------------------------------------------------------------------------------------------------------------------------
                if s2 in list:
                    if int(x) == 0:  # 减数
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 1:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 2:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 3:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 4:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 5:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 6:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 7:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 8:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 9:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 10:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/10.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 11:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/11.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 12:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/12.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 13:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/13.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 14:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/14.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 15:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/15.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 16:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/16.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 17:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/17.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 18:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/18.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 19:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/19.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif 20 <= int(x) < 30:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 30 <= int(x) < 40:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 40 <= int(x) < 50:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 50 <= int(x) < 60:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 60 <= int(x) < 70:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 70 <= int(x) < 80:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 80 <= int(x) < 90:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 90 <= int(x) < 100:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif int(x) == 100:
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/100.wav")))
                        number_detect.player.play()
                        time.sleep(1)

                    # 减号
                    number_detect.player.setMedia(
                        QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/minus.wav")))
                    number_detect.player.play()
                    time.sleep(1)
                    # 被减数
                    if int(x2) == 0:  # 减数
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 1:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 2:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 3:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 4:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 5:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 6:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 7:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 8:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 9:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 10:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/10.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 11:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/11.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 12:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/12.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 13:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/13.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 14:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/14.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 15:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/15.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 16:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/16.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 17:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/17.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 18:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/18.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 19:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/19.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif 20 <= int(x2) < 30:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 30 <= int(x2) < 40:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 40 <= int(x2) < 50:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 50 <= int(x2) < 60:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 60 <= int(x2) < 70:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 70 <= int(x2) < 80:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 80 <= int(x2) < 90:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 90 <= int(x2) < 100:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif int(x2) == 100:
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/100.wav")))
                        number_detect.player.play()
                        time.sleep(1)

                    # = 号
                    number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/equals.wav")))
                    number_detect.player.play()
                    time.sleep(1)

                    # 结果
                    if int(x3) == 0:  # 减数
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 1:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 2:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 3:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 4:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 5:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 6:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 7:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 8:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 9:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 10:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/10.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 11:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/11.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 12:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/12.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 13:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/13.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 14:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/14.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 15:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/15.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 16:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/16.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 17:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/17.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 18:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/18.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 19:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/19.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif 20 <= int(x3) < 30:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 30 <= int(x3) < 40:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 40 <= int(x3) < 50:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 50 <= int(x3) < 60:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 60 <= int(x3) < 70:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 70 <= int(x3) < 80:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 80 <= int(x3) < 90:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 90 <= int(x3) < 100:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif int(x3) == 100:
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/100.wav")))
                        number_detect.player.play()
                        time.sleep(1)

                        # ------------------------------------------------------------------------------------------------------------------------------
                if s3 in list:
                    if int(x) == 0:  # 乘数
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 1:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 2:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 3:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 4:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 5:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 6:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 7:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 8:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 9:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 10:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/10.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 11:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/11.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 12:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/12.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 13:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/13.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 14:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/14.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 15:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/15.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 16:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/16.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 17:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/17.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 18:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/18.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 19:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/19.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif 20 <= int(x) < 30:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 30 <= int(x) < 40:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 40 <= int(x) < 50:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 50 <= int(x) < 60:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 60 <= int(x) < 70:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 70 <= int(x) < 80:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 80 <= int(x) < 90:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 90 <= int(x) < 100:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif int(x) == 100:
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/100.wav")))
                        number_detect.player.play()
                        time.sleep(1)

                    # 乘号
                    number_detect.player.setMedia(
                        QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/times.wav")))
                    number_detect.player.play()
                    time.sleep(1)
                    # 被乘数
                    if int(x2) == 0:  # 乘数
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 1:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 2:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 3:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 4:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 5:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 6:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 7:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 8:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 9:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 10:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/10.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 11:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/11.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 12:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/12.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 13:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/13.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 14:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/14.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 15:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/15.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 16:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/16.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 17:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/17.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 18:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/18.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 19:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/19.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif 20 <= int(x2) < 30:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 30 <= int(x2) < 40:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 40 <= int(x2) < 50:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 50 <= int(x2) < 60:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 60 <= int(x2) < 70:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 70 <= int(x2) < 80:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 80 <= int(x2) < 90:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 90 <= int(x2) < 100:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif int(x2) == 100:
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/100.wav")))
                        number_detect.player.play()
                        time.sleep(1)

                    # = 号
                    number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/equals.wav")))
                    number_detect.player.play()
                    time.sleep(1)

                    # 结果
                    if int(x3) == 0:  # 乘数
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 1:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 2:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 3:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 4:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 5:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 6:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 7:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 8:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 9:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 10:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/10.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 11:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/11.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 12:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/12.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 13:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/13.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 14:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/14.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 15:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/15.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 16:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/16.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 17:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/17.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 18:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/18.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 19:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/19.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif 20 <= int(x3) < 30:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 30 <= int(x3) < 40:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 40 <= int(x3) < 50:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 50 <= int(x3) < 60:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 60 <= int(x3) < 70:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 70 <= int(x3) < 80:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 80 <= int(x3) < 90:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 90 <= int(x3) < 100:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif int(x3) == 100:
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/100.wav")))
                        number_detect.player.play()
                        time.sleep(1)

                        # ------------------------------------------------------------------------------------------------------------------------------
                if s4 in list:
                    if int(x) == 0:  # 除数
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 1:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 2:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 3:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 4:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 5:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 6:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 7:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 8:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 9:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 10:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/10.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 11:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/11.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 12:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/12.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 13:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/13.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 14:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/14.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 15:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/15.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 16:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/16.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 17:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/17.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 18:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/18.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x) == 19:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/19.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif 20 <= int(x) < 30:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 30 <= int(x) < 40:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 40 <= int(x) < 50:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 50 <= int(x) < 60:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 60 <= int(x) < 70:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 70 <= int(x) < 80:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 80 <= int(x) < 90:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 90 <= int(x) < 100:
                        if int(x) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif int(x) == 100:
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/100.wav")))
                        number_detect.player.play()
                        time.sleep(1)

                    # 除号
                    number_detect.player.setMedia(
                        QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/divided by.wav")))
                    number_detect.player.play()
                    time.sleep(1)
                    # 被除数
                    if int(x2) == 0:  # 除数
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 1:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 2:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 3:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 4:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 5:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 6:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 7:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 8:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 9:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 10:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/10.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 11:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/11.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 12:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/12.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 13:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/13.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 14:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/14.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 15:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/15.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 16:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/16.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 17:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/17.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 18:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/18.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x2) == 19:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/19.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif 20 <= int(x2) < 30:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 30 <= int(x2) < 40:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 40 <= int(x2) < 50:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 50 <= int(x2) < 60:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 60 <= int(x2) < 70:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 70 <= int(x2) < 80:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 80 <= int(x2) < 90:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 90 <= int(x2) < 100:
                        if int(x2) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x2) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif int(x2) == 100:
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/100.wav")))
                        number_detect.player.play()
                        time.sleep(1)

                    # = 号
                    number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/equals.wav")))
                    number_detect.player.play()
                    time.sleep(1)

                    # 结果
                    if int(x3) == 0:  # 除数
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/0.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 1:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 2:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 3:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 4:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 5:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 6:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 7:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 8:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 9:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 10:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/10.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 11:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/11.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 12:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/12.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 13:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/13.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 14:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/14.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 15:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/15.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 16:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/16.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 17:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/17.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 18:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/18.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif int(x3) == 19:
                        number_detect.player.setMedia(QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/19.wav")))
                        number_detect.player.play()
                        time.sleep(1)
                    elif 20 <= int(x3) < 30:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/20.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 30 <= int(x3) < 40:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/30.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 40 <= int(x3) < 50:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/40.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 50 <= int(x3) < 60:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/50.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 60 <= int(x3) < 70:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/60.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 70 <= int(x3) < 80:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/70.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 80 <= int(x3) < 90:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/80.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif 90 <= int(x3) < 100:
                        if int(x3) % 10 == 0:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 1:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/1.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 2:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/2.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 3:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/3.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 4:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/4.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 5:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/5.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 6:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/6.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 7:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/7.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 8:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/8.wav")))
                            number_detect.player.play()
                            time.sleep(1)
                        elif int(x3) % 10 == 9:
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/90.wav")))
                            number_detect.player.play()
                            time.sleep(0.9)
                            number_detect.player.setMedia(
                                QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/9.wav")))
                            number_detect.player.play()
                            time.sleep(1)

                    elif int(x3) == 100:
                        number_detect.player.setMedia(
                            QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile("./numwav/100.wav")))
                        number_detect.player.play()
                        time.sleep(1)

                        # ------------------------------------------------------------------------------------------------------------------------------


            elif number_detect.b == 0:
                return 0
            img = cv2.resize(img0, (448, 336))
            img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_BGR888)
            # 将图像显示在QLabel中
            number_detect.ui.tab4_label_dis_img.setPixmap(QPixmap.fromImage(img))


# 实时检测线程5
class realtime_detect5(QThread):
    def run(self):
        number_detect.source = 1
        while 1:
            img0 = number_detect.run2(**vars(opt))
            # img = cv2.flip(img0, 1)
            # img = cv2.resize(img, (448, 336))
            # img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
            # # 将图像显示在QLabel中
            # number_detect.ui.label_1.setPixmap(QPixmap.fromImage(img))
            if number_detect.b == 2:
                number_detect.run0(**vars(opt))

                img3 = cv2.flip(number_detect.img1, 1)
                img3 = cv2.resize(img3, (448, 336))
                img2 = QImage(img3.data, img3.shape[1], img3.shape[0], QImage.Format_BGR888)
                # 将图像显示在QLabel中
                number_detect.ui.tab5_label_dis_img_2.setPixmap(QPixmap.fromImage(img2))

                curr_time = datetime.datetime.now()
                time_now = datetime.datetime.strftime(curr_time, '%H:%M:%S')
                row_count = number_detect.ui.tab5_tableWidget.rowCount()
                number_detect.ui.tab5_tableWidget.insertRow(row_count)
                number_detect.ui.tab5_tableWidget.setItem(row_count, 0, QtWidgets.QTableWidgetItem(str(time_now)))
                number_detect.ui.tab5_tableWidget.item(row_count, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                font = QFont()
                font.setPointSize(24)  # 设置字体大小
                number_detect.ui.tab5_label_1.setFont(font)
                number_detect.ui.tab5_label_1.setStyleSheet("color: red;")  # 设置字体颜色

                number_detect.ui.tab5_label_2.setFont(font)
                number_detect.ui.tab5_label_2.setStyleSheet("color: red;")  # 设置字体颜色

                number_detect.ui.tab5_label_3.setFont(font)
                number_detect.ui.tab4_label_3.setStyleSheet("color: red;")  # 设置字体颜色

                number_detect.ui.tab5_label_4.setFont(font)
                number_detect.ui.tab5_label_4.setStyleSheet("color: red;")  # 设置字体颜色

                number_detect.ui.tab5_label_5.setFont(font)
                number_detect.ui.tab5_label_5.setStyleSheet("color: red;")  # 设置字体颜色

                # label_size = number_detect.ui.tab5_label_dis_img.size()
                # scaled_pixmap = img0.scaled(label_size, Qt.KeepAspectRatio)
                # number_detect.ui.tab5_label_dis_img.setPixmap(scaled_pixmap)
                list = number_detect.my_list3
                # print('list', list)
                # len0 = len(list)
                s1, s2, s3, s4, s5 = '+', '-', '*', '/', '='
                # if list[0] == s1 or list[0] == s2 or list[0] == s3 or list[0] == s4 or list[0] == s5:
                #     reply = QMessageBox.question(number_detect.ui, '信息提示', '算式书写错误，请重新书写并检测！')
                #     if reply == 'StandardButton.Yes':
                #         pass
                if 1:
                    number_detect.ui.tab5_label_4.setText(s5)
                    if (s1 in list) and (s5 in list):  # 加法
                        n4 = list.index(s5)
                        n0 = list.index(s1)
                        number_detect.ui.tab5_label_2.setText(s1)
                        txt1  = list[:n0]
                        if len(txt1) > 1:
                            x = str(int(txt1[0]) * 10 + int(txt1[1]))
                        else:
                            x = str(int(txt1[0]))
                        number_detect.ui.tab5_label_1.setText(x)
                        txt2 = list[n0 + 1:n4]
                        if len(txt2) > 1:
                            x2 = str(int(txt2[0]) * 10 + int(txt2[1]))
                        else:
                            x2 = str(int(txt2[0]))
                        number_detect.ui.tab5_label_3.setText(x2)
                        txt3 = list[n4 + 1:]
                        if len(txt3) == 1:
                            x3 = str(int(txt3[0]))

                        elif len(txt3) == 2:
                            x3 = str(int(txt3[0]) * 10 + int(txt3[1]))
                        elif len(txt3) == 3:
                            x3 = str(int(txt3[0]) * 100 + int(txt3[1]) * 10 + int(txt3[2]))
                        elif len(txt3) == 4:
                            x3 = str(int(txt3[0]) * 1000 + int(txt3[1]) * 100 + int(txt3[2]) * 10 + int(txt3[3]))

                        # x3 = str(int(x) + int(x2))
                        number_detect.ui.tab5_label_5.setText(x3)
                        formula = str(x) + s1 + str(x2) + s5 + str(x3)
                        item = QtWidgets.QTableWidgetItem(str('mathe formul'))
                        item.setForeground(QtGui.QColor(255, 0, 0))
                        number_detect.ui.tab5_tableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(formula)))
                        number_detect.ui.tab5_tableWidget.item(row_count, 1).setTextAlignment(
                            Qt.AlignHCenter | Qt.AlignVCenter)
                        if int(x3) == number_detect.r_add:
                            item = QtWidgets.QTableWidgetItem(str('result'))
                            item.setForeground(QtGui.QColor(255, 0, 0))

                            number_detect.ui.tab5_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('√')), )
                            number_detect.ui.tab5_tableWidget.item(row_count, 2).setTextAlignment(
                                Qt.AlignHCenter | Qt.AlignVCenter)
                        else:
                            item = QtWidgets.QTableWidgetItem(str('result'))
                            item.setForeground(QtGui.QColor(255, 0, 0))

                            number_detect.ui.tab5_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('x')), )
                            number_detect.ui.tab5_tableWidget.item(row_count, 2).setTextAlignment(
                                Qt.AlignHCenter | Qt.AlignVCenter)

                    elif (s2 in list) and (s5 in list):  # 减法
                        n4 = list.index(s5)
                        n0 = list.index(s2)
                        number_detect.ui.tab5_label_2.setText(s2)
                        txt1 = list[:n0]
                        if len(txt1) > 1:
                            x = str(int(txt1[0]) * 10 + int(txt1[1]))
                        else:
                            x = str(int(txt1[0]))
                        number_detect.ui.tab5_label_1.setText(x)
                        txt2 = list[n0 + 1:n4]
                        if len(txt2) > 1:
                            x2 = str(int(txt2[0]) * 10 + int(txt2[1]))
                        else:
                            x2 = str(int(txt2[0]))
                        number_detect.ui.tab5_label_3.setText(x2)
                        txt3 = list[n4 + 1:]
                        if len(txt3) == 1:
                            x3 = str(int(txt3[0]))

                        elif len(txt3) == 2:
                            x3 = str(int(txt3[0]) * 10 + int(txt3[1]))
                        elif len(txt3) == 3:
                            x3 = str(int(txt3[0]) * 100 + int(txt3[1]) * 10 + int(txt3[2]))
                        elif len(txt3) == 4:
                            x3 = str(int(txt3[0]) * 1000 + int(txt3[1]) * 100 + int(txt3[2]) * 10 + int(txt3[3]))
                        number_detect.ui.tab5_label_5.setText(x3)
                        formula = str(x) + s2 + str(x2) + s5 + str(x3)
                        item = QtWidgets.QTableWidgetItem(str('mathe formul'))
                        item.setForeground(QtGui.QColor(255, 0, 0))
                        number_detect.ui.tab5_tableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(formula)))
                        number_detect.ui.tab5_tableWidget.item(row_count, 1).setTextAlignment(
                            Qt.AlignHCenter | Qt.AlignVCenter)
                        if int(x3) == number_detect.r_sub:
                            item = QtWidgets.QTableWidgetItem(str('result'))
                            item.setForeground(QtGui.QColor(255, 0, 0))
                            number_detect.ui.tab5_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('√')), )
                            number_detect.ui.tab5_tableWidget.item(row_count, 2).setTextAlignment(
                                Qt.AlignHCenter | Qt.AlignVCenter)
                        else:
                            item = QtWidgets.QTableWidgetItem(str('result'))
                            item.setForeground(QtGui.QColor(255, 0, 0))

                            number_detect.ui.tab5_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('x')), )
                            number_detect.ui.tab5_tableWidget.item(row_count, 2).setTextAlignment(
                                Qt.AlignHCenter | Qt.AlignVCenter)

                    elif (s3 in list) and (s5 in list):  # 乘法
                        n4 = list.index(s5)
                        n0 = list.index(s3)

                        number_detect.ui.tab5_label_2.setText(s3)
                        txt1 = list[:n0]
                        if len(txt1) > 1:
                            x = str(int(txt1[0]) * 10 + int(txt1[1]))
                        else:
                            x = str(int(txt1[0]))
                        number_detect.ui.tab5_label_1.setText(x)
                        txt2 = list[n0 + 1:]
                        if len(txt2) > 1:
                            x2 = str(int(txt2[0]) * 10 + int(txt2[1]))
                        else:
                            x2 = str(int(txt2[0]))
                        number_detect.ui.tab5_label_3.setText(x2)
                        txt3 = list[n4 + 1:]
                        if len(txt3) == 1:
                            x3 = str(int(txt3[0]))
                        elif len(txt3) == 2:
                            x3 = str(int(txt3[0]) * 10 + int(txt3[1]))
                        elif len(txt3) == 3:
                            x3 = str(int(txt3[0]) * 100 + int(txt3[1]) * 10 + int(txt3[2]))
                        elif len(txt3) == 4:
                            x3 = str(int(txt3[0]) * 1000 + int(txt3[1]) * 100 + int(txt3[2]) * 10 + int(txt3[3]))
                        number_detect.ui.tab5_label_5.setText(x3)
                        formula = str(x) + '*' + str(x2) + s5 + str(x3)
                        item = QtWidgets.QTableWidgetItem(str('mathe formul'))
                        item.setForeground(QtGui.QColor(255, 0, 0))
                        number_detect.ui.tab5_tableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(formula)))
                        number_detect.ui.tab5_tableWidget.item(row_count, 1).setTextAlignment(
                            Qt.AlignHCenter | Qt.AlignVCenter)
                        if int(x3) == number_detect.r_mul:
                            item = QtWidgets.QTableWidgetItem(str('result'))
                            item.setForeground(QtGui.QColor(255, 0, 0))
                            number_detect.ui.tab5_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('√')), )
                            number_detect.ui.tab5_tableWidget.item(row_count, 2).setTextAlignment(
                                Qt.AlignHCenter | Qt.AlignVCenter)
                        else:
                            item = QtWidgets.QTableWidgetItem(str('result'))
                            item.setForeground(QtGui.QColor(255, 0, 0))

                            number_detect.ui.tab5_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('x')), )
                            number_detect.ui.tab5_tableWidget.item(row_count, 2).setTextAlignment(
                                Qt.AlignHCenter | Qt.AlignVCenter)

                    elif (s4 in list) and (s5 in list):  # 除法
                        n4 = list.index(s5)
                        n0 = list.index(s4)
                        number_detect.ui.tab5_label_2.setText(s4)
                        txt1 = list[:n0]
                        if len(txt1) > 1:
                            x = str(int(txt1[0]) * 10 + int(txt1[1]))
                        else:
                            x = str(int(txt1[0]))
                        number_detect.ui.tab5_label_1.setText(x)

                        txt2 = list[n0 + 1:n4]
                        if len(txt2) > 1:
                            x2 = str(int(txt2[0]) * 10 + int(txt2[1]))
                        else:
                            x2 = str(int(txt2[0]))
                        number_detect.ui.tab5_label_3.setText(x2)
                        txt3 = list[n4 + 1:]
                        if len(txt3) == 1:
                            x3 = str(int(txt3[0]))

                        elif len(txt3) == 2:
                            x3 = str(int(txt3[0]) * 10 + int(txt3[1]))
                        elif len(txt3) == 3:
                            x3 = str(int(txt3[0]) * 100 + int(txt3[1]) * 10 + int(txt3[2]))
                        elif len(txt3) == 4:
                            x3 = str(int(txt3[0]) * 1000 + int(txt3[1]) * 100 + int(txt3[2]) * 10 + int(txt3[3]))

                        number_detect.ui.tab5_label_5.setText(x3)
                        formula = str(x) + s4 + str(x2) + s5 + str(x3)
                        item = QtWidgets.QTableWidgetItem(str('mathe formul'))
                        item.setForeground(QtGui.QColor(255, 0, 0))
                        number_detect.ui.tab5_tableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(formula)))
                        number_detect.ui.tab5_tableWidget.item(row_count, 1).setTextAlignment(
                            Qt.AlignHCenter | Qt.AlignVCenter)
                        if int(x3) == number_detect.r_division:
                            item = QtWidgets.QTableWidgetItem(str('result'))
                            item.setForeground(QtGui.QColor(255, 0, 0))
                            number_detect.ui.tab5_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('√')), )
                            number_detect.ui.tab5_tableWidget.item(row_count, 2).setTextAlignment(
                                Qt.AlignHCenter | Qt.AlignVCenter)
                        else:
                            item = QtWidgets.QTableWidgetItem(str('result'))
                            item.setForeground(QtGui.QColor(255, 0, 0))
                            number_detect.ui.tab5_tableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str('x')), )
                            number_detect.ui.tab5_tableWidget.item(row_count, 2).setTextAlignment(
                                Qt.AlignHCenter | Qt.AlignVCenter)
            img = cv2.resize(img0, (448, 336))
            img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_BGR888)
            # 将图像显示在QLabel中
            number_detect.ui.tab5_label_dis_img.setPixmap(QPixmap.fromImage(img))


def main(opt):
    check_requirements(exclude=('tensorboard', 'tgop'))


if __name__ == "__main__":
    weights = str('best.pt')  # model path or triton URL
    device = ''  # cuda device, i.e. 0 or 0,1,2,3 or cpu
    dnn = False,  # use OpenCV DNN for ONNX inference
    data = 'numberParameter.yaml'  # dataset.yaml path
    half = False  # use FP16 half-precision inference
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt

    # cameras = dict(list_video_devices())
    # n = 0  # 相机编号选择
    # Cam = cv2.VideoCapture(n, cv2.CAP_DSHOW)  # 相机

    app = QApplication([])
    number_detect = number_detect0()  # 主窗口对象
    opt = parse_opt()
    main(opt)
    number_detect.ui.show()
    app.exec()
    number_detect.Cap.release()
    number_detect.realtime_detect0.terminate()
