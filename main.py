import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.uic.load_ui import loadUi
from PyQt6 import QtMultimedia
from pyarrow import json as pjson
import json
import pandas as pd
from elasticsearch import Elasticsearch , helpers
import subprocess

class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, df =pd.DataFrame(), parent =None):
        super().__init__(parent)
        self._df = df

    def rowCount(self, parent = QtCore.QModelIndex()):
        return self._df.shape[0]

    def columnCount(self, parent = QtCore.QModelIndex()):
        return self._df.shape[1]

    def data(self, index, role = QtCore.Qt.ItemDataRole.DisplayRole):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return QtCore.QVariant()
        if not index.isValid():
            return QtCore.QVariant()
        return QtCore.QVariant(str(self._df.iloc[index.row(),index.column()]))

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                return str(self._df.columns[section])
            if orientation == QtCore.Qt.Orientation.Vertical:
                return str(self._df.index[section])
    def click(self,):
        pass


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi("test2.ui", self)

        #elasticsearch object
        password = "0X=9*RicED0HZvTrYrxN"
        self.es = Elasticsearch(hosts ="https://localhost:9200",ca_certs="/Users/joel/Downloads/elasticsearch-8.6.1/config/certs/http_ca.crt",
        basic_auth=("elastic", password))

        #DataFrame
        table = pjson.read_json('database/testupdate_2k.jsonl')
        self.df = table.to_pandas()
        self.model = PandasModel(self.df)
        self.dataTable.setModel(self.model)
        

        #UI Settings
        self.playButton.setIcon(QtGui.QIcon("assets/play.png"))
        self.playButton.setText("Play")

        #Dynamic Functions
        self.videoPlayer()

        # self.retrieveData()
        self.buttonFunctions()
        self.sliderFunctions()
        self.dataTable.doubleClicked.connect(self.cell_clicked_to_play)
        

    def videoPlayer(self):
        self.mediaPlayer = QtMultimedia.QMediaPlayer(self)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.playbackStateChanged.connect(self.mediastate_changed)
        
        #self.mediaPlayer.setSource(QtCore.QUrl('videos/test3.mp4'))


        #TODO set video to play frame index relative to total frames in video
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def buttonFunctions(self):

        self.playButton.clicked.connect(self.play)
        self.stopButton.clicked.connect(self.mediaPlayer.stop)

        self.submitButton.clicked.connect(self.es_search)

    def play(self):
        if self.mediaPlayer.playbackState() == QtMultimedia.QMediaPlayer.PlaybackState.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    #TODO Put timestamps for sliders
    def sliderFunctions(self):
        self.videoSlider.setRange(0,0)
        self.videoSlider.sliderMoved.connect(self.set_position)
        
    def position_changed(self,position):
        self.videoSlider.setValue(position)

    def duration_changed(self,duration):
        self.videoSlider.setRange(0,duration)

    def set_position(self,position):
        self.mediaPlayer.setPosition(position)

    def mediastate_changed(self,state):
        if self.mediaPlayer.playbackState() == QtMultimedia.QMediaPlayer.PlaybackState.PlayingState:
            self.playButton.setIcon(QtGui.QIcon("assets/pause.png"))
            self.playButton.setText("Pause")
        else:
            self.playButton.setIcon(QtGui.QIcon("assets/play.png"))
            self.playButton.setText("Play")

    def es_search(self,text):
        text = self.searchBox.text()
        if not text:
            self.dataTable.setModel(self.model)
        else:
            result = self.es.search(index= 'testupdate_index1k', query= {
                "multi_match" : {"query" : text,
                "type" : "cross_fields",
                "analyzer" : "standard",
                "operator" : "and"}
            },size= 10000,)

            hits =result["hits"]["hits"]
            docs = [hit["_source"] for hit in hits]
            # print(docs)
            # print(result["hits"]["total"]["value"])
            result_df = pd.DataFrame(docs)
            if not result_df.empty:
                display_df = pd.merge(self.df,result_df)
                display_df = display_df.iloc[:,:-5]
                display_df = PandasModel(display_df)
                self.dataTable.setModel(display_df)
                
            else:
                #something went wrong (no matches / weird input)
                dlg = QtWidgets.QMessageBox(self)
                dlg.setWindowTitle("ERROR")
                dlg.setText("Something Went Wrong... ")
                dlg.exec()


            # print('this is result_df')
            # print(result_df)
            # common_cols = list(set(result_df.columns))
            # print(common_cols)

            #print('this is self.df')
            # print(self.df)
            
            
            # print(display_df)
    def cell_clicked_to_play(self,index):
        row = index.row()
        # column = index.column()
        #print(row,column)

        # Access current dataframe displayed to get video link from cell
        #print(self.df.iloc[row,column])
        self.mediaPlayer.setSource(QtCore.QUrl(self.df.iloc[row,0]))
        self.mediaPlayer.play()

    def shutdown(self,process):
        if process:
            process.kill()






        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    #Starts up elasticsearch server
    cmd = '/Users/joel/Downloads/elasticsearch-8.6.1/bin/elasticsearch'
    process = subprocess.Popen(cmd,shell= True)
    window = MainWindow()
    app.aboutToQuit.connect(lambda:window.shutdown(process))
    window.show()
    #suppose to shutdown elasticsearch server
    # process.terminate()
    app.exec()


#old useless code

    # def retrieveData(self):
    #     # Displaying the data as a dataframe from jsonl
    #     table = pjson.read_json('database/newdata10.jsonl')
    #     self.df = table.to_pandas()
    #     self.model = PandasModel(self.df)
    #     self.dataTable.setModel(self.model)


    #     #TODO remove combobox entirely when search is optmised
    #     self.dropdown.addItems(self.df.columns)
    
        # def retrieveVideos(self,text):
    #     if self.df is None:
    #         return
    #     col_index = self.df.columns.get_loc(self.dropdown.currentText())
        
    #     # text to be searched
    #     text = self.searchBox.text()
        

    #     # Makes the rows in the dataframe disappear
    #     for row_index in range(self.model.rowCount()):
    #         if text in self.model.index(row_index,col_index).data():
    #             self.dataTable.setRowHidden(row_index,False)
    #         else:
    #             self.dataTable.setRowHidden(row_index,True)
    