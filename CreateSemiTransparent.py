from PySide6.QtGui import QPainter, QPixmap, QColor

#Function to create semitransparent image for pixmap
def create_semi_transparent_image(original_image_path, transparency): #funkcja służąca do zrobienia półprzeźroczystego obrazka
        pixmap = QPixmap(original_image_path)
        transparent_pixmap = QPixmap(pixmap.size())
        transparent_pixmap.fill(QColor(0, 0, 0, 0)) 
        painter = QPainter(transparent_pixmap)
        painter.setOpacity(transparency) 
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        return transparent_pixmap