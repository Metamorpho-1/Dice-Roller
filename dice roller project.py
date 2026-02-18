import sys
import random
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

def get_rarity(n, target_sum):
    """Calculates statistical rarity using NumPy vectorization."""
    sims = 100_000
    rolls = np.random.randint(1, 7, size=(sims, n))
    sums = np.sum(rolls, axis=1)
    return (np.sum(sums == target_sum) / sims) * 100

class DiceDashboard(QWidget):
    def __init__(self):
        super().__init__()
        # Every line is exactly 11 chars wide to ensure perfect horizontal zipping
        self.dice_art = {
            1: ["┌─────────┐", "│         │", "│    ●    │", "│         │", "└─────────┘"],
            2: ["┌─────────┐", "│  ●      │", "│         │", "│      ●  │", "└─────────┘"],
            3: ["┌─────────┐", "│  ●      │", "│    ●    │", "│      ●  │", "└─────────┘"],
            4: ["┌─────────┐", "│  ●   ●  │", "│         │", "│  ●   ●  │", "└─────────┘"],
            5: ["┌─────────┐", "│  ●   ●  │", "│    ●    │", "│  ●   ●  │", "└─────────┘"],
            6: ["┌─────────┐", "│  ●   ●  │", "│  ●   ●  │", "│  ●   ●  │", "└─────────┘"]
        }
        self.init_ui() # Calling the UI setup
        
        # Animation timer setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.roll_count = 0

    def init_ui(self):
        """Sets up the graphical components and styling."""
        self.setWindowTitle("Pro Probability Dice Engine")
        self.setFixedSize(650, 550) 
        self.setStyleSheet("background-color: #0F172A; color: #F8FAFC;")

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        title = QLabel("DICE PRO ANALYTICS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #10B981; font-family: 'Helvetica';")
        layout.addWidget(title)

        # Search/Input Bar
        input_row = QHBoxLayout()
        self.dice_input = QLineEdit()
        self.dice_input.setPlaceholderText("Count (1-5)")
        self.dice_input.setStyleSheet("padding: 12px; background: #1E293B; border: 1px solid #334155; border-radius: 8px;")
        
        self.roll_btn = QPushButton("CAST")
        self.roll_btn.clicked.connect(self.start_roll)
        self.roll_btn.setCursor(Qt.PointingHandCursor)
        self.roll_btn.setStyleSheet("background: #10B981; color: #0F172A; font-weight: bold; padding: 12px 25px; border-radius: 8px;")
        
        input_row.addWidget(self.dice_input)
        input_row.addWidget(self.roll_btn)
        layout.addLayout(input_row)

        # Dice Display - The critical alignment area
        self.dice_display = QLabel("READY")
        self.dice_display.setAlignment(Qt.AlignCenter)
        
        display_font = QFont("Monaco") 
        display_font.setStyleHint(QFont.Monospace)
        display_font.setFixedPitch(True)
        display_font.setPointSize(16)
        self.dice_display.setFont(display_font)
        
        # 'white-space: pre' and 'line-height: 1.0' ensure the ASCII characters don't drift
        self.dice_display.setStyleSheet("""
            QLabel {
                background: #1E293B; 
                border-radius: 12px; 
                padding: 40px; 
                color: #94A3B8;
                line-height: 1.0;
                white-space: pre;
            }
        """)
        layout.addWidget(self.dice_display)

        self.stats_label = QLabel("Waiting for cast...")
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setStyleSheet("color: #64748B; font-size: 14px;")
        layout.addWidget(self.stats_label)

        self.setLayout(layout)

    def start_roll(self):
        val = self.dice_input.text()
        if val.isdigit() and 0 < int(val) <= 5:
            self.n = int(val)
            self.roll_count = 0
            self.roll_btn.setEnabled(False)
            self.timer.start(70)
        else:
            self.stats_label.setText("Error: Enter 1 to 5 dice.")

    def animate(self):
        self.update_view([random.randint(1, 6) for _ in range(self.n)])
        self.roll_count += 1
        if self.roll_count > 12:
            self.timer.stop()
            self.finalize()

    def update_view(self, dice):
        # We build the horizontal string line-by-line to keep dice side-by-side
        output_lines = ["", "", "", "", ""]
        for val in dice:
            art = self.dice_art[val]
            for i in range(5):
                output_lines[i] += art[i] + "  " 
        
        self.dice_display.setText("\n".join(output_lines))

    def finalize(self):
        res = [random.randint(1, 6) for _ in range(self.n)]
        self.update_view(res)
        total = sum(res)
        rarity = get_rarity(self.n, total)
        self.stats_label.setText(f"TOTAL: {total}  |  RARITY: {rarity:.2f}%")
        self.roll_btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DiceDashboard()
    ex.show()
    sys.exit(app.exec_())