"""code check"""

from utils.quote_scales.quote_scales import QuotesScales

figi_list = ["RU000A106T36", "FUTASTR06250", "FUTASTR09250"]
scale_obj = QuotesScales(figi_list)
scale_obj.show_table()

# figi_list = ["BBG004730N88", "FUTSBRF06250", "FUTSBRF09250"]
# scale_obj = QuotesScales(figi_list)
# scale_obj.show_table()

figi_list = ["BBG004730ZJ9", "FUTVTBR06250", "FUTVTBR09250"]
scale_obj = QuotesScales(figi_list)
scale_obj.show_table()

figi_list = ["BBG00475KHX6", "FUTTRNF06250", "FUTTRNF09250"]
scale_obj = QuotesScales(figi_list)
scale_obj.show_table()
