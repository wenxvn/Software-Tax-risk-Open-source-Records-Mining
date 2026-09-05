from taxrisk.public_fields import extract_public_financial_fields, statement_window


def test_extract_public_financial_fields_from_statement_sections():
    text = """
合并资产负债表
应收账款 七、5 1,001 900
合同资产 七、6 1,002 901
合同负债 七、38 1,003 902
应交税费 七、40 1,004 903
母公司资产负债表
合并利润表
一、营业总收入  1,005 904
其中：营业成本 七、61 1,006 905
税金及附加 七、62 1,007 906
研发费用 七、65 1,008 907
减：所得税费用 七、76 -1,009 908
合并现金流量表
销售商品、提供劳务收到的
现金  1,010 909
支付的各项税费  1,011 910
3、 计入当期损益的政府补助
类型 本期发生额 上期发生额
合计 1,012 911
"""
    values = extract_public_financial_fields(text)
    assert values["operating_revenue"] == 1005
    assert values["income_tax_expense"] == -1009
    assert values["government_grants_recognized_in_profit"] == 1012
    assert len(values) == 12


def test_statement_window_stops_at_next_statement():
    text = "合并利润表\n一、营业总收入 1\n母公司利润表\n一、营业总收入 2"
    assert "收入 2" not in statement_window(text, "合并利润表")
