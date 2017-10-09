import sys
import os
import codecs
from PIL import Image
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QLabel,
                             QHBoxLayout, QVBoxLayout, QTextEdit, QComboBox,
                             QFileDialog, QGraphicsScene, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

class MainWidget(QWidget):
    file = ''
    pixmap = None
    frame_info_list = []
    balloon_info_list = []
    face_info_list = []
    body_info_list = []

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.initUI()
        self.px = None
        self.py = None
        self.points = []
        self.psets = []

    def initUI(self):
        self.resize(1280, 960)

        self.txtFile = QLineEdit()
        self.txtFile.setReadOnly(True)
        self.btnFile = QPushButton('参照...')
        self.btnFile.clicked.connect(self.show_image_dialog)
        hb1 = QHBoxLayout()
        hb1.addWidget(self.txtFile)
        hb1.addWidget(self.btnFile)
        
        self.combo = QComboBox(self)
        self.combo.addItem("コマ")
        self.combo.addItem("台詞")
        self.combo.addItem("キャラ顔")
        self.combo.addItem("キャラ全体")
       
        # コマのときの入力フォーマット        
        frame_id = QLabel('Frame_ID')
        area = QLabel('Area')
        framing = QLabel('枠の有無')

        self.idEditFr = QLineEdit()
        self.areaEditFr = QLineEdit()
        self.framingEditFr = QLineEdit()

        self.grid = QVBoxLayout()
        self.groupBox = QGroupBox("コマ")
        self.orivbox = QVBoxLayout()

        layout1 = QHBoxLayout()
        layout1.addWidget(frame_id)
        layout1.addWidget(self.idEditFr)

        layout2 = QHBoxLayout()
        layout2.addWidget(area)
        layout2.addWidget(self.areaEditFr)
        
        layout3 = QHBoxLayout()
        layout3.addWidget(framing)
        layout3.addWidget(self.framingEditFr)
        
        # 台詞のときの入力フォーマット 
        frame_id = QLabel('Frame_ID')
        area = QLabel('Area')
        content = QLabel('Content')
        balloon = QLabel('Ballon_id')
        speaker = QLabel('Speaker_No')

        self.idEditBa = QLineEdit()
        self.areaEditBa = QLineEdit()
        self.contentEditBa = QLineEdit()
        self.balloonEditBa = QLineEdit()
        self.speakerEditBa = QLineEdit()

        self.BalloonGroupBox = QGroupBox("台詞")
        self.orivbox2 = QVBoxLayout()

        layout4 = QHBoxLayout()
        layout4.addWidget(frame_id)
        layout4.addWidget(self.idEditBa)

        layout5 = QHBoxLayout()
        layout5.addWidget(area)
        layout5.addWidget(self.areaEditBa)
        
        layout6 = QHBoxLayout()
        layout6.addWidget(content)
        layout6.addWidget(self.contentEditBa)
        
        layout7 = QHBoxLayout()
        layout7.addWidget(balloon)
        layout7.addWidget(self.balloonEditBa)
        
        layout8 = QHBoxLayout()
        layout8.addWidget(speaker)
        layout8.addWidget(self.speakerEditBa)
        
        # キャラ顔のときの入力フォーマット 
        frame_id = QLabel('Frame_ID')
        chara_id = QLabel('Character_ID')
        chara_no = QLabel('Character_No.')
        area = QLabel('Area')
        aspect = QLabel('Aspect')
        face_direction = QLabel('Face_Direction')

        self.idEditFa = QLineEdit()
        self.charaidEditFa = QLineEdit()
        self.charanoEditFa = QLineEdit()
        self.areaEditFa = QLineEdit()
        self.aspectEditFa = QLineEdit()
        self.directionEditFa = QLineEdit()

        self.FaceGroupBox = QGroupBox("キャラ顔")
        self.orivbox3 = QVBoxLayout()

        layout9 = QHBoxLayout()
        layout9.addWidget(frame_id)
        layout9.addWidget(self.idEditFa)
        
        layout10 = QHBoxLayout()
        layout10.addWidget(chara_id)
        layout10.addWidget(self.charaidEditFa)
        
        layout11 = QHBoxLayout()
        layout11.addWidget(chara_no)
        layout11.addWidget(self.charanoEditFa)

        layout12 = QHBoxLayout()
        layout12.addWidget(area)
        layout12.addWidget(self.areaEditFa)
        
        layout13 = QHBoxLayout()
        layout13.addWidget(aspect)
        layout13.addWidget(self.aspectEditFa)
        
        layout14 = QHBoxLayout()
        layout14.addWidget(face_direction)
        layout14.addWidget(self.directionEditFa)
        
        # キャラ全体のときの入力フォーマット 
        frame_id = QLabel('Frame_ID')
        chara_id = QLabel('Character_ID')
        area = QLabel('Area')
        motion = QLabel('Motion_id')

        self.idEditBo = QLineEdit()
        self.charaidEditBo = QLineEdit()
        self.areaEditBo = QLineEdit()
        self.motionEditBo = QLineEdit()

        self.BodyGroupBox = QGroupBox("キャラ全体")
        self.orivbox4 = QVBoxLayout()

        layout16 = QHBoxLayout()
        layout16.addWidget(frame_id)
        layout16.addWidget(self.idEditBo)
        
        layout17 = QHBoxLayout()
        layout17.addWidget(chara_id)
        layout17.addWidget(self.charaidEditBo)
        
        layout18 = QHBoxLayout()
        layout18.addWidget(area)
        layout18.addWidget(self.areaEditBo)
        
        layout19 = QHBoxLayout()
        layout19.addWidget(motion)
        layout19.addWidget(self.motionEditBo)
                
        self.btnSave = QPushButton('Save')
        self.btnSave.clicked.connect(self.save_annotation)

        self.orivbox.addLayout(layout1)
        self.orivbox.addLayout(layout2)
        self.orivbox.addLayout(layout3)

        self.orivbox2.addLayout(layout4)
        self.orivbox2.addLayout(layout5)
        self.orivbox2.addLayout(layout6)
        self.orivbox2.addLayout(layout7)
        self.orivbox2.addLayout(layout8)

        self.orivbox3.addLayout(layout9)
        self.orivbox3.addLayout(layout10)
        self.orivbox3.addLayout(layout11)
        self.orivbox3.addLayout(layout12)
        self.orivbox3.addLayout(layout13)
        self.orivbox3.addLayout(layout14)

        self.orivbox4.addLayout(layout16)
        self.orivbox4.addLayout(layout17)
        self.orivbox4.addLayout(layout18)
        self.orivbox4.addLayout(layout19)

        self.groupBox.setLayout(self.orivbox)
        self.BalloonGroupBox.setLayout(self.orivbox2)
        self.FaceGroupBox.setLayout(self.orivbox3)
        self.BodyGroupBox.setLayout(self.orivbox4)
        
        self.grid.addWidget(self.groupBox)
        self.grid.addWidget(self.BalloonGroupBox)
        self.BalloonGroupBox.setHidden(True)
        self.grid.addWidget(self.FaceGroupBox)
        self.FaceGroupBox.setHidden(True)
        self.grid.addWidget(self.BodyGroupBox)
        self.BodyGroupBox.setHidden(True)
        self.grid.addWidget(self.btnSave)
                        
        self.groupBox2 = QGroupBox()
        box1 = QVBoxLayout()
        box1.addWidget(self.combo)
        box1.addLayout(self.grid)
        
        saved_item = QLabel('Saved Item')
        self.savedList = QTextEdit(self)
        box1.addWidget(saved_item)
        box1.addWidget(self.savedList)
        
        self.groupBox2.setLayout(box1)
        
        self.combo.currentIndexChanged.connect(self.detail_widget_change)
        
        hbox = QHBoxLayout()
        self.lbl = QLabel()
        hbox.addWidget(self.lbl)
        hbox.addWidget(self.groupBox2)
        
        self.btnExec = QPushButton('Output')
        self.btnExec.clicked.connect(self.output_annotation)
        self.btnExec.setEnabled(False)
        self.btnExec.setVisible(True)

        hb2 = QHBoxLayout()
        hb2.addWidget(self.btnExec)
        
        layout = QVBoxLayout()
        layout.addLayout(hb1)
        layout.addLayout(hbox)
        layout.addLayout(hb2)
        self.setLayout(layout)

        self.setWindowTitle('AnnotationTool by PyQt5')

    def show_image_dialog(self):
        # open dialog and set to image name
        file = QFileDialog.getOpenFileName(self, 'Open Image', os.path.expanduser('~'),"Image files (*.jpg *.png) ")
            
        if file:
            self.file = file[0]
            # テキストボックスにパスを代入
            self.txtFile.setText(self.file)
            # buttonを使用可能に
            self.btnExec.setEnabled(True)
            
            # 透過したい画像を読み込み
            orgin = Image.open(file[0])
            # 同じサイズの画像を作成
            trans = Image.new('RGBA', orgin.size, (0, 0, 0, 0))
            width = orgin.size[0]
            height = orgin.size[1]
            for x in range(width):
                for y in range(height):
                    pixel = orgin.getpixel((x, y))
                    # 白なら処理しない
                    if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
                        continue
                    # 白以外なら、用意した画像にピクセルを書き込み
                    trans.putpixel((x, y), pixel)
            trans.save('trans.png')
            orgin.close()
            # 画像の読み込み
            pixmap = QPixmap('trans.png')
            self.pixmap = pixmap.scaledToHeight(725)
            # ラベルを作ってその中に画像を置く
            self.lbl.setPixmap(self.pixmap)
            
    def detail_widget_change(self):
        if not self.groupBox.isHidden():        
            self.groupBox.setHidden(not self.groupBox.isHidden())
        elif not self.BalloonGroupBox.isHidden():
            self.BalloonGroupBox.setHidden(not self.BalloonGroupBox.isHidden())
        elif not self.FaceGroupBox.isHidden():
            self.FaceGroupBox.setHidden(not self.FaceGroupBox.isHidden())
        elif not self.BodyGroupBox.isHidden():
            self.BodyGroupBox.setHidden(not self.BodyGroupBox.isHidden())
        
        if self.combo.currentIndex() == 0:
            self.groupBox.setHidden(False)
        elif self.combo.currentIndex() == 1:
            self.BalloonGroupBox.setHidden(False)
        elif self.combo.currentIndex() == 2:
            self.FaceGroupBox.setHidden(False)
        elif self.combo.currentIndex() == 3:
            self.BodyGroupBox.setHidden(False)
        
    def mousePressEvent(self, event):
        self.points.append(event.pos())
        self.update()

    def paintEvent(self, event):
        if self.pixmap:
            pen = QPen(Qt.red, 4, Qt.SolidLine)
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setBrush(Qt.white)
            painter.drawRect(self.rect())
            painter.setPen(pen)
    
            # draw historical points
            for points in self.psets:
                painter.drawPolyline(*points)
    
            # draw current points
            # 画像始点(x=20, y=70),other:(x=530, y=70), (x=530, y=800), (x=20, y=800)
            if self.points:
                painter.drawPolyline(*self.points)
                #print(self.points)
                
            if len(self.points) == 5:
                grid = ''
                for p in self.points:
                    grid += '(' + str(p.x()) + ',' + str(p.y()) + ') '
                if self.combo.currentIndex() == 0:
                    self.areaEditFr.setText(grid)
                elif self.combo.currentIndex() == 1:
                    self.areaEditBa.setText(grid)
                elif self.combo.currentIndex() == 2:
                    self.areaEditFa.setText(grid)
                elif self.combo.currentIndex() == 3:
                    self.areaEditBo.setText(grid)   
                    
    def save_annotation(self):
        saved_title = ''
        if self.combo.currentIndex() == 0:
            frame_info ={}
            frame_info['frame_id'] = self.idEditFr.text()
            idFa = self.idEditFr.text()
            self.idEditFr.clear()
            frame_info['area'] = self.areaEditFr.text()
            self.areaEditFr.clear()
            self.points.clear()
            frame_info['framing'] = self.framingEditFr.text()
            self.framingEditFr.clear()
            self.frame_info_list.append(frame_info)
            saved_title += 'コマ' + idFa
        elif self.combo.currentIndex() == 1:
            balloon_info ={}
            balloon_info['frame_id'] = self.idEditBa.text()
            idBa = self.idEditBa.text()
            self.idEditBa.clear()
            balloon_info['area'] = self.areaEditBa.text()
            self.areaEditBa.clear()
            self.points.clear()
            balloon_info['content'] = self.contentEditBa.text()
            self.contentEditBa.clear()
            balloon_info['balloon'] = self.balloonEditBa.text()
            self.balloonEditBa.clear()
            balloon_info['speaker'] = self.speakerEditBa.text()
            self.speakerEditBa.clear()
            balloon_count = self.same_id_count(self.balloon_info_list,idBa)
            balloon_info['balloon_id'] = balloon_count
            self.balloon_info_list.append(balloon_info)
            saved_title += '台詞' + idBa + '-' + balloon_count
        elif self.combo.currentIndex() == 2:
            face_info ={}
            face_info['frame_id'] = self.idEditFa.text()
            idFa = self.idEditFa.text()
            self.idEditFa.clear()
            face_info['chara_id'] = self.charaidEditFa.text()
            self.charaidEditFa.clear()
            face_info['chara_no'] = self.charanoEditFa.text()
            self.charanoEditFa.clear()
            face_info['area'] = self.areaEditFa.text()
            self.areaEditFa.clear()
            self.points.clear()
            face_info['aspect'] = self.aspectEditFa.text()
            self.aspectEditFa.clear()
            face_info['direction'] = self.directionEditFa.text()
            self.directionEditFa.clear()
            self.face_info_list.append(face_info)
            saved_title += 'キャラ顔' + idFa + '-' + face_info['chara_id']
        elif self.combo.currentIndex() == 3:
            body_info ={}
            body_info['frame_id'] = self.idEditBo.text()
            idBo = self.idEditBo.text()
            self.idEditBo.clear()
            body_info['chara_id'] = self.charaidEditBo.text()
            self.charaidEditBo.clear()
            body_info['area'] = self.areaEditBo.text()
            self.areaEditBo.clear()
            self.points.clear()
            body_info['motion'] = self.motionEditBo.text()
            self.motionEditBo.clear()
            self.body_info_list.append(body_info)
            saved_title += 'キャラ全体' + idBo + '-' + body_info['chara_id']
            
        self.savedList.append(saved_title)
        
    def same_id_count(self, List, Id):
        count = 1
        for dic in List:
            if dic['frame_id'] == Id:
                count += 1
        return str(count)
        
    def output_annotation(self):
        top = Element('image')
        child_title = SubElement(top, 'title')
        child_title.text = self.file.split('/')[-1].split('.')[0]
        child_frames = SubElement(top, 'frames')
        
        sorted_balloon = sorted(self.balloon_info_list, key=lambda x:(x['frame_id'],x['balloon_id']))
        sorted_face = sorted(self.face_info_list, key=lambda x:(x['frame_id'],x['chara_id']))
        sorted_body = sorted(self.body_info_list, key=lambda x:(x['frame_id'],x['chara_id']))
        chara = []
        chara_id_list = []

        for face in sorted_face:
            for body in sorted_body:
                if face['chara_id'] == body['chara_id']:
                    face_body = [face['frame_id'], face['chara_id'], face['chara_no'], face['area'], face['aspect'], face['direction'], body['area'], body['motion']]
                    chara.append(face_body)
                    chara_id_list.append(face['chara_id'])
                elif body['chara_id'] > face['chara_id']:
                    break
        for face in sorted_face:
            if face['chara_id'] not in chara_id_list:
                face_list = [face['frame_id'], face['chara_id'], face['chara_no'], face['area'], face['aspect'], face['direction']]
                chara.append(face_list)
        for  body in sorted_body:
            if body['chara_id'] not in chara_id_list:
                body_list = [body['frame_id'], body['chara_id'], body['area'], body['motion']]
                chara.append(body_list)
                
        sorted_chara = sorted(chara, key=lambda x:(x[0],x[1]))
        
        for frame_dic in sorted(self.frame_info_list, key=lambda x:x['frame_id']):
            gchild_frame = SubElement(child_frames, 'frame')
            ggchild_id = SubElement(gchild_frame, 'ID')
            ggchild_id.text = frame_dic['frame_id']
            ggchild_area = SubElement(gchild_frame, 'Area')
            ggchild_area.text = frame_dic['area']
            ggchild_framing = SubElement(gchild_frame, 'Framing')
            ggchild_framing.text = frame_dic['framing']
            
            for balloon_dic in sorted_balloon:
                if balloon_dic['frame_id'] == frame_dic['frame_id']:
                    ggchild_balloon = SubElement(gchild_frame, 'Balloon')
                    gggchild_idBa = SubElement(ggchild_balloon, 'ID')
                    gggchild_idBa.text = balloon_dic['balloon_id']
                    gggchild_areaBa = SubElement(ggchild_balloon, 'Area')
                    gggchild_areaBa.text = balloon_dic['area']
                    gggchild_content = SubElement(ggchild_balloon, 'Content')
                    gggchild_content.text = balloon_dic['content']
                    gggchild_type = SubElement(ggchild_balloon, 'Type')
                    gggchild_type.text = balloon_dic['balloon']
                    gggchild_speaker = SubElement(ggchild_balloon, 'Speaker')
                    gggchild_speaker.text = balloon_dic['speaker']
                elif balloon_dic['frame_id'] > frame_dic['frame_id']:
                    break          
                
            for chara_list in sorted_chara:
                if chara_list[0] == frame_dic['frame_id'] and len(chara_list) == 8: # 顔と体両方のアノテーション
                    ggchild_chara = SubElement(gchild_frame, 'Character')
                    gggchild_idFa = SubElement(ggchild_chara, 'ID')
                    gggchild_idFa.text = chara_list[1]
                    gggchild_noFa = SubElement(ggchild_chara, 'Chara_No.')
                    gggchild_noFa.text = chara_list[2]
                    gggchild_areaFa = SubElement(ggchild_chara, 'FaceArea')
                    gggchild_areaFa.text = chara_list[3]
                    gggchild_aspect = SubElement(ggchild_chara, 'Aspect')
                    gggchild_aspect.text = chara_list[4]
                    gggchild_direction = SubElement(ggchild_chara, 'Direction')
                    gggchild_direction.text = chara_list[5]
                    gggchild_direction = SubElement(ggchild_chara, 'BodyArea')
                    gggchild_direction.text = chara_list[6]
                    gggchild_direction = SubElement(ggchild_chara, 'Motion')
                    gggchild_direction.text = chara_list[7]
                elif chara_list[0] == frame_dic['frame_id'] and len(chara_list) == 6: # 顔のみのアノテーション
                    ggchild_chara = SubElement(gchild_frame, 'Character')
                    gggchild_idFa = SubElement(ggchild_chara, 'ID')
                    gggchild_idFa.text = chara_list[1]
                    gggchild_noFa = SubElement(ggchild_chara, 'Chara_No.')
                    gggchild_noFa.text = chara_list[2]
                    gggchild_areaFa = SubElement(ggchild_chara, 'FaceArea')
                    gggchild_areaFa.text = chara_list[3]
                    gggchild_aspect = SubElement(ggchild_chara, 'Aspect')
                    gggchild_aspect.text = chara_list[4]
                    gggchild_direction = SubElement(ggchild_chara, 'Direction')
                    gggchild_direction.text = chara_list[5]
                    gggchild_direction = SubElement(ggchild_chara, 'BodyArea')
                    gggchild_direction = SubElement(ggchild_chara, 'Motion')
                elif chara_list[0] == frame_dic['frame_id'] and len(chara_list) == 4: # 体のみのアノテーション(不要？)
                    ggchild_chara = SubElement(gchild_frame, 'Character')
                    gggchild_idFa = SubElement(ggchild_chara, 'ID')
                    gggchild_idFa.text = chara_list[1]
                    gggchild_noFa = SubElement(ggchild_chara, 'Chara_No.')
                    gggchild_areaFa = SubElement(ggchild_chara, 'FaceArea')
                    gggchild_aspect = SubElement(ggchild_chara, 'Aspect')
                    gggchild_direction = SubElement(ggchild_chara, 'Direction')
                    gggchild_direction = SubElement(ggchild_chara, 'BodyArea')
                    gggchild_direction.text = chara_list[2]
                    gggchild_direction = SubElement(ggchild_chara, 'Motion')
                    gggchild_direction.text = chara_list[3]
                elif chara_list[0] > frame_dic['frame_id']:
                    break
                
        print(self.prettify(top))
        self.savedList.clear()
        
        file_name = self.file.split('/')[-1].split('.')[0] + '.xml'
        f = codecs.open(file_name, 'w', 'utf-8')
        f.write(self.prettify(top))
        f.close()
        
        self.frame_info_list = []
        self.balloon_info_list = []
        self.face_info_list = []
        self.body_info_list = []
        
    def prettify(self,elem):
        # Return a pretty-printed XML string for the Element.
        rough_string = tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")


def main(args):
    app = QApplication(args)
    dialog = MainWidget()
    dialog.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
