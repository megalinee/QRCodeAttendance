import cv2

window_x = 600
window_y = 340

# Color Settings
primary_color = "orange"
secondary_color = "black"

# Camera Text Overlay Settings
font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (20, 30)
fontScale = 1
fontColor = (255, 255, 255)
thickness = 3
lineType = 2

general_date = "Friday"

pathToJSON = "./data.json"
defaultJSON = "{\"members\":[],\"member-count\": 0}"
