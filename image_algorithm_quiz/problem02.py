# 문제 2. 컬러 이미지의 임계값 계산하고 흑백 이미지 만들기
#
# 과제 규칙상 AI에게 완성 정답 코드를 받지 않고,
# 아래 TODO를 하나씩 직접 채우면서 진행합니다.


def calc_brightness(r, g, b):
    """RGB 한 픽셀의 밝기를 계산합니다.

    TODO: (R + G + B) // 3의 의미를 이해한 뒤 직접 구현하기
    """
    pass


def calc_threshold(brightness_map, height, width):
    """전체 이미지의 평균 밝기를 임계값으로 계산합니다.

    TODO:
    1. 모든 밝기의 합 구하기
    2. 전체 픽셀 수 H * W 구하기
    3. 정수 나눗셈으로 평균 구하기
    """
    pass


def to_black_white(brightness_map, threshold):
    """밝기와 임계값을 비교하여 0/1 이미지로 바꿉니다.

    TODO: brightness >= threshold 이면 1, 아니면 0으로 처리하기
    """
    pass


def main():
    # TODO: H, W 입력받기
    # TODO: RGB 문자열을 분리해서 숫자로 바꾸기
    # TODO: 각 픽셀의 밝기 계산하기
    # TODO: threshold 계산하기
    # TODO: 흑백 이미지 출력하기
    pass


if __name__ == "__main__":
    main()
