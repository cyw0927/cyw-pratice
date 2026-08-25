# 문제 2. 컬러 이미지의 임계값을 계산하고 흑백 이미지 만들기


def calc_brightness(r, g, b):
    """RGB 한 픽셀의 밝기를 계산한다."""
    # 빨강, 초록, 파랑 값을 모두 더한 뒤 3으로 나눠 평균 밝기를 구한다.
    # //는 소수점 아래를 버리는 정수 나눗셈이다.
    return (r + g + b) // 3


def calc_threshold(brightness_map, height, width):
    """전체 이미지의 평균 밝기를 임계값으로 계산한다."""
    total = 0

    # 2차원 밝기 배열을 한 칸씩 돌면서 전체 밝기의 합을 구한다.
    for row in brightness_map:
        for brightness in row:
            total += brightness

    # 이미지의 전체 픽셀 수는 세로 칸 수 × 가로 칸 수이다.
    pixel_count = height * width

    # 전체 밝기의 평균을 threshold로 사용한다.
    return total // pixel_count


def to_black_white(brightness_map, threshold):
    """각 밝기를 threshold와 비교하여 0/1 이미지로 바꾼다."""
    result = []

    for row in brightness_map:
        result_row = ""

        for brightness in row:
            # threshold 이상이면 흰색(1), 미만이면 검은색(0)으로 처리한다.
            if brightness >= threshold:
                result_row += "1"
            else:
                result_row += "0"

        result.append(result_row)

    return result


def main():
    # 첫 줄에서 이미지의 높이(H)와 너비(W)를 입력받는다.
    height, width = map(int, input().split())

    brightness_map = []

    # 이미지의 높이만큼 한 줄씩 RGB 데이터를 입력받는다.
    for _ in range(height):
        pixels = input().split()
        brightness_row = []

        # 한 줄에 있는 각 RGB 문자열을 하나씩 처리한다.
        for pixel in pixels:
            # 예: "255,0,0" -> [255, 0, 0]
            r, g, b = map(int, pixel.split(","))

            # RGB를 하나의 밝기 값으로 바꾼 뒤 현재 행에 저장한다.
            brightness = calc_brightness(r, g, b)
            brightness_row.append(brightness)

        brightness_map.append(brightness_row)

    # 모든 픽셀의 평균 밝기를 기준값으로 계산한다.
    threshold = calc_threshold(brightness_map, height, width)

    # 계산한 threshold를 첫 줄에 출력한다.
    print(threshold)

    # 각 픽셀을 0 또는 1로 변환한다.
    black_white_image = to_black_white(brightness_map, threshold)

    # 원래 이미지와 같은 행 수로 결과를 출력한다.
    for row in black_white_image:
        print(row)


if __name__ == "__main__":
    main()
