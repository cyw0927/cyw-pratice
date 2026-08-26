# 문제 2. 컬러 이미지의 임계값을 계산하고 흑백 이미지 만들기


def calc_brightness(r, g, b):
    """RGB 한 픽셀의 밝기를 정수 평균으로 계산한다."""
    return (r + g + b) // 3


def parse_pixel(pixel_text):
    """'255,0,0' 형태의 문자열을 (255, 0, 0) 정수 튜플로 바꾼다."""
    r, g, b = map(int, pixel_text.split(","))
    return r, g, b


def build_brightness_map(rgb_rows):
    """RGB 문자열 행들을 2차원 밝기 리스트로 변환한다.

    이 함수는 input()에 의존하지 않기 때문에 노트북이나 테스트 코드에서도
    같은 로직을 쉽게 확인할 수 있다.
    """
    brightness_map = []

    for pixels in rgb_rows:
        brightness_row = []

        for pixel in pixels:
            r, g, b = parse_pixel(pixel)
            brightness = calc_brightness(r, g, b)
            brightness_row.append(brightness)

        brightness_map.append(brightness_row)

    return brightness_map


def calc_threshold(brightness_map, height, width):
    """전체 픽셀의 평균 밝기를 threshold로 계산한다."""
    total = 0

    for row in brightness_map:
        for brightness in row:
            total += brightness

    pixel_count = height * width
    return total // pixel_count


def to_black_white(brightness_map, threshold):
    """threshold 이상은 1, 미만은 0으로 바꿔 행 문자열 리스트를 만든다."""
    result = []

    for row in brightness_map:
        result_row = ""

        for brightness in row:
            if brightness >= threshold:
                result_row += "1"
            else:
                result_row += "0"

        result.append(result_row)

    return result


def solve(height, width, rgb_rows):
    """문제 2의 전체 계산을 수행하고 (threshold, 결과행들)을 반환한다.

    main()과 계산 로직을 분리해 두면 VS Code, Jupyter Notebook,
    테스트 코드에서 동일한 함수를 직접 호출해 결과를 검증할 수 있다.
    """
    brightness_map = build_brightness_map(rgb_rows)
    threshold = calc_threshold(brightness_map, height, width)
    black_white_image = to_black_white(brightness_map, threshold)
    return threshold, black_white_image


def main():
    # 첫 줄: 이미지 높이 H, 너비 W
    height, width = map(int, input().split())

    # 각 행을 공백 기준으로 나눠 픽셀 문자열 리스트로 저장한다.
    rgb_rows = []

    for _ in range(height):
        pixels = input().split()
        rgb_rows.append(pixels)

    # 계산 로직 실행
    threshold, black_white_image = solve(height, width, rgb_rows)

    # 문제에서 요구한 출력 형식
    print(threshold)
    for row in black_white_image:
        print(row)


if __name__ == "__main__":
    main()
