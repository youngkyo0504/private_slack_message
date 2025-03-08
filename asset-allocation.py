from google_sheets_manager import GoogleSheetsManager
from typing import List, Dict, Tuple, Any


def main():
    # 자산 데이터 가져오기
    asset_data = read_retirement_saving()

    # 전체 자산 금액 및 비율 계산
    total_amount, asset_weights = calculate_asset_allocation(asset_data)

    # 자산 클래스별 비중 계산
    class_weights = calculate_class_weights(asset_data)

    # 결과 출력
    print_results(total_amount, asset_weights, class_weights)

    return {
        "total_amount": total_amount,
        "asset_weights": asset_weights,
        "class_weights": class_weights,
    }


def read_retirement_saving():
    # 스프레드시트 상수 정의
    SPREADSHEET_ID = "1KwBg0x39gaaKjWFEt--tlQuX8mAb5pL6ZWtXMEI9VCs"
    RANGE_NAME = "retirement-saving!A2:G10"

    # GoogleSheetsManager 인스턴스 생성
    sheets_manager = GoogleSheetsManager()

    # 데이터 읽기 예제
    data = sheets_manager.read_range(SPREADSHEET_ID, RANGE_NAME)
    return data


def calculate_asset_allocation(
    asset_data: List[List[str]],
) -> Tuple[float, Dict[str, Dict[str, Any]]]:
    """
    전체 자산 금액과 각 자산별 실제 비중을 계산합니다.

    Args:
        asset_data: 스프레드시트에서 읽은 자산 데이터

    Returns:
        total_amount: 총 자산 금액
        asset_weights: 각 자산별 정보와 실제 비중을 담은 딕셔너리
    """
    total_amount = 0.0
    asset_weights = {}

    # 데이터 열 인덱스 정의 (가독성 향상)
    COL_NAME = 0
    COL_QUANTITY = 1
    COL_PRICE = 2
    COL_TICKER = 3
    COL_AMOUNT = 4
    COL_TARGET_WEIGHT = 5
    COL_ASSET_CLASS = 6

    # 총 금액 계산
    for row in asset_data:
        if len(row) > COL_AMOUNT:
            amount_str = row[COL_AMOUNT]
            if amount_str and amount_str.replace(".", "", 1).isdigit():
                total_amount += float(amount_str)

    # 각 자산별 비중 계산
    for row in asset_data:
        if len(row) > COL_ASSET_CLASS:  # 모든 필드가 있는지 확인
            name = row[COL_NAME]

            # 문자열을 숫자로 변환 (안전하게 처리)
            quantity_str = row[COL_QUANTITY]
            quantity = (
                float(quantity_str)
                if quantity_str and quantity_str.replace(".", "", 1).isdigit()
                else 0
            )

            price_str = row[COL_PRICE]
            price = (
                float(price_str)
                if price_str and price_str.replace(".", "", 1).isdigit()
                else 0
            )

            ticker = row[COL_TICKER]

            amount_str = row[COL_AMOUNT]
            amount = (
                float(amount_str)
                if amount_str and amount_str.replace(".", "", 1).isdigit()
                else 0
            )

            target_weight_str = row[COL_TARGET_WEIGHT]
            target_weight = (
                float(target_weight_str)
                if target_weight_str and target_weight_str.replace(".", "", 1).isdigit()
                else 0
            )

            asset_class = row[COL_ASSET_CLASS]

            # 실제 비중 계산 (%)
            actual_weight = (amount / total_amount * 100) if total_amount > 0 else 0

            # 목표 비중과 실제 비중 차이 계산
            weight_diff = actual_weight - target_weight

            asset_weights[name] = {
                "ticker": ticker,
                "quantity": quantity,
                "price": price,
                "amount": amount,
                "target_weight": target_weight,
                "actual_weight": actual_weight,
                "weight_diff": weight_diff,
                "asset_class": asset_class,
            }

    return total_amount, asset_weights


def calculate_class_weights(asset_data: List[List[str]]) -> Dict[str, Dict[str, float]]:
    """
    자산 클래스별 비중을 계산합니다.

    Args:
        asset_data: 스프레드시트에서 읽은 자산 데이터

    Returns:
        class_weights: 자산 클래스별 비중 정보
    """
    class_amounts = {}
    class_target_weights = {}
    total_amount = 0.0

    # 데이터 열 인덱스 정의 (가독성 향상)
    COL_AMOUNT = 4
    COL_TARGET_WEIGHT = 5
    COL_ASSET_CLASS = 6

    # 각 자산 클래스별 금액 합계 및 목표 비중 합계 계산
    for row in asset_data:
        if len(row) > COL_ASSET_CLASS:
            amount_str = row[COL_AMOUNT]
            amount = (
                float(amount_str)
                if amount_str and amount_str.replace(".", "", 1).isdigit()
                else 0
            )

            target_weight_str = row[COL_TARGET_WEIGHT]
            target_weight = (
                float(target_weight_str)
                if target_weight_str and target_weight_str.replace(".", "", 1).isdigit()
                else 0
            )

            asset_class = row[COL_ASSET_CLASS]

            total_amount += amount

            if asset_class not in class_amounts:
                class_amounts[asset_class] = 0
                class_target_weights[asset_class] = 0

            class_amounts[asset_class] += amount
            class_target_weights[asset_class] += target_weight

    # 각 자산 클래스별 실제 비중 계산
    class_weights = {}
    for asset_class, amount in class_amounts.items():
        actual_weight = (amount / total_amount * 100) if total_amount > 0 else 0
        target_weight = class_target_weights[asset_class]
        weight_diff = actual_weight - target_weight

        class_weights[asset_class] = {
            "amount": amount,
            "target_weight": target_weight,
            "actual_weight": actual_weight,
            "weight_diff": weight_diff,
        }

    return class_weights


def print_results(
    total_amount: float,
    asset_weights: Dict[str, Dict[str, Any]],
    class_weights: Dict[str, Dict[str, float]],
):
    """결과 정보를 콘솔에 출력합니다."""
    print(f"\n===== 포트폴리오 총액: {total_amount:,.0f}원 =====")

    print("\n===== 자산 클래스별 비중 =====")
    for asset_class, info in class_weights.items():
        print(
            f"{asset_class}: {info['actual_weight']:.2f}% (목표: {info['target_weight']:.2f}%, 차이: {info['weight_diff']:.2f}%)"
        )

    print("\n===== 개별 자산 비중 =====")
    for name, info in asset_weights.items():
        print(
            f"{name} ({info['ticker']}): {info['actual_weight']:.2f}% "
            f"(목표: {info['target_weight']:.2f}%, 차이: {info['weight_diff']:.2f}%)"
        )


if __name__ == "__main__":
    main()
