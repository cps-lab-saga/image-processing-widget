import cv2 as cv


def aruco_display(
    corners,
    ids,
    img,
    line_color=(0, 0, 255),
    line_thickness=2,
    font_color=(0, 0, 255),
    font_scale=1,
    font_thickness=2,
):
    if len(corners) > 0:
        new_img = img.copy()
        for c, m_id in zip(corners, ids.flatten()):
            top_left, top_right, bottom_right, bottom_left = c.reshape((4, 2)).astype(
                int
            )

            cv.line(new_img, top_left, top_right, line_color, line_thickness)
            cv.line(new_img, top_right, bottom_right, line_color, line_thickness)
            cv.line(new_img, bottom_right, bottom_left, line_color, line_thickness)
            cv.line(new_img, bottom_left, top_left, line_color, line_thickness)
            cv.putText(
                new_img,
                str(m_id),
                (top_right[0], top_right[1] + 15),
                cv.FONT_HERSHEY_SIMPLEX,
                font_scale,
                font_color,
                font_thickness,
            )
        return new_img
