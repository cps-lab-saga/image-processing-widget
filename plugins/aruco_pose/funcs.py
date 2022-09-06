import cv2 as cv
import numpy as np


def aruco_detect_display(
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


def aruco_pose_display(
    corners,
    ids,
    img,
    K,
    D,
    font_color=(0, 0, 255),
    font_scale=1,
    font_thickness=2,
    show_axis=True,
    show_cube=False,
):
    if len(corners) > 0:
        new_img = img.copy()
        for c, m_id in zip(corners, ids.flatten()):
            top_left, top_right, bottom_right, bottom_left = c.reshape((4, 2)).astype(
                int
            )

            rvec, tvec, obj_points = cv.aruco.estimatePoseSingleMarkers(c, 1, K, D)
            if show_axis:
                cv.drawFrameAxes(new_img, K, D, rvec, tvec, 1)
            if show_cube:
                draw_cube(new_img, K, D, rvec, tvec)

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


def draw_cube(
    img,
    K,
    D,
    rvec,
    tvec,
    line_color=(23, 190, 207, 100),
    line_thickness=1,
):
    axis = np.float32(
        [
            [-0.5, -0.5, 0],
            [-0.5, 0.5, 0],
            [0.5, 0.5, 0],
            [0.5, -0.5, 0],
            [-0.5, -0.5, 1],
            [-0.5, 0.5, 1],
            [0.5, 0.5, 1],
            [0.5, -0.5, 1],
        ]
    )
    imgpts, jac = cv.projectPoints(axis, rvec, tvec, K, D)

    imgpts = np.int32(imgpts).reshape(-1, 2)

    # draw floor
    cv.drawContours(img, [imgpts[:4]], -1, line_color, line_thickness)

    # draw pillars
    for i, j in zip(range(4), range(4, 8)):
        cv.line(img, tuple(imgpts[i]), tuple(imgpts[j]), line_color, line_thickness)

    # draw roof
    cv.drawContours(img, [imgpts[4:]], -1, line_color, line_thickness)
