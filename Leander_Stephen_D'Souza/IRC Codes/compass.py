import cv2


def cardinal_directions(panaroma):
    height, width = panaroma.shape[:2]

    font_size = 0.3
    screen_offset = 320

    starting_angle = 130

    font_style = cv2.FONT_HERSHEY_SIMPLEX
    theta = starting_angle

    if theta % 45 == 0:
        panaroma = cv2.putText(panaroma, ' |', (screen_offset, 20), font_style, font_size * 1.5, (0, 0, 255), 2)

        if theta == 0:
            panaroma = cv2.putText(panaroma, ' N', (screen_offset, 40), font_style, font_size * 1.5,
                                   (0, 0, 255), 2)
        elif theta == 45:
            panaroma = cv2.putText(panaroma, 'NE', (screen_offset, 40), font_style, font_size * 1.5,
                                   (0, 0, 255), 2)
        elif theta == 90:
            panaroma = cv2.putText(panaroma, ' E', (screen_offset, 40), font_style, font_size * 1.5,
                                   (0, 0, 255), 2)
        elif theta == 135:
            panaroma = cv2.putText(panaroma, 'SE', (screen_offset, 40), font_style, font_size * 1.5,
                                   (0, 0, 255), 2)
        elif theta == 180:
            panaroma = cv2.putText(panaroma, ' S', (screen_offset, 40), font_style, font_size * 1.5,
                                   (0, 0, 255), 2)
        elif theta == 225:
            panaroma = cv2.putText(panaroma, 'SW', (screen_offset, 40), font_style, font_size * 1.5,
                                   (0, 0, 255), 2)
        elif theta == 270:
            panaroma = cv2.putText(panaroma, ' W', (screen_offset, 40), font_style, font_size * 1.5,
                                   (0, 0, 255), 2)
        elif theta == 315:
            panaroma = cv2.putText(panaroma, 'NW', (screen_offset, 40), font_style, font_size * 1.5,
                                   (0, 0, 255), 2)

    else:
        panaroma = cv2.putText(panaroma, '%s' % str(starting_angle), (screen_offset, 40),
                              font_style, font_size, (0, 0, 255), 2)

    curr_width = screen_offset
    flag =0
    double_flag =0
    next_angle =0
    prev_angle =0


    while curr_width < width+1:
        if flag ==0:
            flag =1
            next_angle = starting_angle + (15 - (starting_angle % 15))
            curr_width += (next_angle - starting_angle) * int(width / 360)+5
            next_angle %=360

            if next_angle ==starting_angle:
                continue

            if next_angle % 45 == 0:
                panaroma = cv2.putText(panaroma, ' |', (curr_width, 20), font_style, font_size * 1.5, (255, 255, 255), 2)

                if next_angle == 0:
                    panaroma = cv2.putText(panaroma, ' N', (curr_width, 40), font_style, font_size * 1.5,
                                           (255, 255, 255), 2)
                elif next_angle == 45:
                    panaroma = cv2.putText(panaroma, 'NE', (curr_width, 40), font_style, font_size * 1.5,
                                           (255, 255, 255), 2)
                elif next_angle == 90:
                    panaroma = cv2.putText(panaroma, ' E', (curr_width, 40), font_style, font_size * 1.5,
                                           (255, 255, 255), 2)
                elif next_angle == 135:
                    panaroma = cv2.putText(panaroma, 'SE', (curr_width, 40), font_style, font_size * 1.5,
                                           (255, 255, 255), 2)
                elif next_angle == 180:
                    panaroma = cv2.putText(panaroma, ' S', (curr_width, 40), font_style, font_size * 1.5,
                                           (255, 255, 255), 2)
                elif next_angle == 225:
                    panaroma = cv2.putText(panaroma, 'SW', (curr_width, 40), font_style, font_size * 1.5,
                                           (255, 255, 255), 2)
                elif next_angle == 270:
                    panaroma = cv2.putText(panaroma, ' W', (curr_width, 40), font_style, font_size * 1.5,
                                           (255, 255, 255), 2)
                elif next_angle == 315:
                    panaroma = cv2.putText(panaroma, 'NW', (curr_width, 40), font_style, font_size * 1.5,
                                           (255, 255, 255), 2)
                continue


            panaroma = cv2.putText(panaroma, ' %s' % str(next_angle), (curr_width, 38), font_style, font_size, (255, 255, 255), 2)
            continue

        next_angle = (next_angle+15)%360
        curr_width += int(width/23)

        if next_angle == starting_angle:
            continue

        if next_angle % 45 == 0:
            panaroma = cv2.putText(panaroma, ' |', (curr_width, 20), font_style, font_size * 1.5, (255, 255, 255), 2)

            if next_angle == 0:
                panaroma = cv2.putText(panaroma, ' N', (curr_width, 40), font_style, font_size * 1.5,
                                       (255, 255, 255), 2)
            elif next_angle == 45:
                panaroma = cv2.putText(panaroma, 'NE', (curr_width, 40), font_style, font_size * 1.5,
                                       (255, 255, 255), 2)
            elif next_angle == 90:
                panaroma = cv2.putText(panaroma, ' E', (curr_width, 40), font_style, font_size * 1.5,
                                       (255, 255, 255), 2)
            elif next_angle == 135:
                panaroma = cv2.putText(panaroma, 'SE', (curr_width, 40), font_style, font_size * 1.5,
                                       (255, 255, 255), 2)
            elif next_angle == 180:
                panaroma = cv2.putText(panaroma, ' S', (curr_width, 40), font_style, font_size * 1.5,
                                       (255, 255, 255), 2)
            elif next_angle == 225:
                panaroma = cv2.putText(panaroma, 'SW', (curr_width, 40), font_style, font_size * 1.5,
                                       (255, 255, 255), 2)
            elif next_angle == 270:
                panaroma = cv2.putText(panaroma, ' W', (curr_width, 40), font_style, font_size * 1.5,
                                       (255, 255, 255), 2)
            elif next_angle == 315:
                panaroma = cv2.putText(panaroma, 'NW', (curr_width, 40), font_style, font_size * 1.5,
                                       (255, 255, 255), 2)
            continue

        panaroma = cv2.putText(panaroma, ' %s' % str(next_angle), (curr_width, 38),
                               font_style, font_size, (255, 255, 255), 2)

    curr_width = screen_offset

    while curr_width >0:
        if double_flag ==0:
            double_flag =1
            prev_angle  = starting_angle - (starting_angle % 15)
            curr_width -= (starting_angle - prev_angle) * int(width / 360)
            prev_angle %=360

            if prev_angle ==starting_angle:
                continue

            if prev_angle % 45 == 0:
                panaroma = cv2.putText(panaroma, '|', (curr_width, 20), font_style, font_size * 1.5, (255, 255, 255), 2)

                if prev_angle == 0:
                    panaroma = cv2.putText(panaroma, 'N', (curr_width, 40), font_style, font_size * 1.5,
                                           (255, 255, 255), 2)
                elif prev_angle == 45:
                    panaroma = cv2.putText(panaroma, 'NE', (curr_width, 40), font_style, font_size * 1.5,
                                           (255, 255, 255), 2)
                elif prev_angle == 90:
                    panaroma = cv2.putText(panaroma, 'E', (curr_width, 40), font_style, font_size * 1.5,
                                           (255, 255, 255), 2)
                elif prev_angle == 135:
                    panaroma = cv2.putText(panaroma, 'SE', (curr_width, 40), font_style, font_size * 1.5,
                                           (255, 255, 255), 2)
                elif prev_angle == 180:
                    panaroma = cv2.putText(panaroma, 'S', (curr_width, 40), font_style, font_size * 1.5,
                                           (255, 255, 255), 2)
                elif prev_angle == 225:
                    panaroma = cv2.putText(panaroma, 'SW', (curr_width, 40), font_style, font_size * 1.5,
                                           (255, 255, 255), 2)
                elif prev_angle == 270:
                    panaroma = cv2.putText(panaroma, 'W', (curr_width, 40), font_style, font_size * 1.5,
                                           (255, 255, 255), 2)
                elif prev_angle == 315:
                    panaroma = cv2.putText(panaroma, 'NW', (curr_width, 40), font_style, font_size * 1.5,
                                           (255, 255, 255), 2)
                continue

            panaroma = cv2.putText(panaroma, '%s' % str(prev_angle), (curr_width, 38),
                                   font_style, font_size, (255, 255, 255), 2)
            continue

        prev_angle = (prev_angle - 15) % 360
        curr_width -=int(width/23)

        if prev_angle == starting_angle:
            continue

        if prev_angle % 45 == 0:
            panaroma = cv2.putText(panaroma, '|', (curr_width, 20), font_style, font_size * 1.5, (255, 255, 255), 2)

            if prev_angle == 0:
                panaroma = cv2.putText(panaroma, 'N', (curr_width, 40), font_style, font_size * 1.5,
                                       (255, 255, 255), 2)
            elif prev_angle == 45:
                panaroma = cv2.putText(panaroma, 'NE', (curr_width, 40), font_style, font_size * 1.5,
                                       (255, 255, 255), 2)
            elif prev_angle == 90:
                panaroma = cv2.putText(panaroma, 'E', (curr_width, 40), font_style, font_size * 1.5,
                                       (255, 255, 255), 2)
            elif prev_angle == 135:
                panaroma = cv2.putText(panaroma, 'SE', (curr_width, 40), font_style, font_size * 1.5,
                                       (255, 255, 255), 2)
            elif prev_angle == 180:
                panaroma = cv2.putText(panaroma, 'S', (curr_width, 40), font_style, font_size * 1.5,
                                       (255, 255, 255), 2)
            elif prev_angle == 225:
                panaroma = cv2.putText(panaroma, 'SW', (curr_width, 40), font_style, font_size * 1.5,
                                       (255, 255, 255), 2)
            elif prev_angle == 270:
                panaroma = cv2.putText(panaroma, 'W', (curr_width, 40), font_style, font_size * 1.5,
                                       (255, 255, 255), 2)
            elif prev_angle == 315:
                panaroma = cv2.putText(panaroma, 'NW', (curr_width, 40), font_style, font_size * 1.5,
                                       (255, 255, 255), 2)
            continue

        panaroma = cv2.putText(panaroma, '%s' % str(prev_angle), (curr_width, 38),
                               font_style, font_size, (255, 255, 255), 2)

    cv2.imshow("PANAROMA", panaroma)


panaroma = cv2.imread('1.jpg')
cardinal_directions(panaroma)

cv2.waitKey()
cv2.destroyAllWindows()








