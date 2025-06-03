"""main app"""

from bin.calculate_futures import show_futures_calculating

if __name__ == "__main__":
    ASTRA = ["RU000A106T36", "FUTASTR06250", "FUTASTR09250"]
    TRANSNEFT = ["BBG00475KHX6", "FUTTRNF06250", "FUTTRNF09250"]
    VTBR = ["BBG004730ZJ9", "FUTVTBR06250", "FUTVTBR09250"]

    show_futures_calculating(VTBR)
