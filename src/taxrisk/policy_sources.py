"""Official policy-source definitions used for the public-disclosure candidate only."""

from html.parser import HTMLParser


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        value = data.strip()
        if value:
            self.parts.append(value)


def html_to_text(html: str) -> str:
    parser = _TextExtractor()
    parser.feed(html)
    return "\n".join(parser.parts) + "\n"


POLICY_CANDIDATES = (
    {
        "policy_id": "POL-VAT-SOFTWARE-2011-100",
        "title": "财政部 国家税务总局关于软件产品增值税政策的通知",
        "document_number": "财税〔2011〕100号",
        "issuer": "财政部 国家税务总局",
        "publish_date": "2011-10-13",
        "effective_date": "2011-01-01",
        "expiry_date": "",
        "amendment_status": "OFFICIAL_SOURCE_CURRENT_STATUS_NOT_SEPARATELY_VERIFIED",
        "article": "第一、三、四、六至八条",
        "applicable_taxpayer": "销售自行开发生产的软件产品且满足资料、核算与管理条件的增值税一般纳税人（资格待核）",
        "applicable_business": "自行开发生产软件产品的销售；与其他货物或应税劳务并存时的进项税额分摊",
        "source_url": "https://fgk.chinatax.gov.cn/zcfgk/c102416/c5204304/content.html",
        "case_period_applicable": "",
        "notes": "已核验国家税务总局政策法规库原文及成文、生效日期；公开年报中的相关披露不能证明软件产品资格、备案、销售额拆分、进项税额分摊或实际退税额，均须以企业资料核验。",
        "status": "NEEDS_REVIEW",
    },
    {
        "policy_id": "POL-VAT-2016-36",
        "title": "财政部 国家税务总局关于全面推开营业税改征增值税试点的通知",
        "document_number": "财税〔2016〕36号",
        "issuer": "财政部 国家税务总局",
        "publish_date": "2016-03-23",
        "effective_date": "2016-05-01",
        "expiry_date": "",
        "amendment_status": "NEEDS_CASE_SPECIFIC_REVIEW",
        "article": "附件1：营业税改征增值税试点实施办法（须按具体业务进一步核验）",
        "applicable_taxpayer": "发生应税行为的纳税人（具体资格待核）",
        "applicable_business": "软件和信息技术服务相关应税行为（具体服务性质待核）",
        "source_url": "https://fgk.chinatax.gov.cn/zcfgk/c102416/c5203752/content.html",
        "case_period_applicable": "",
        "notes": "已核验官方来源、成文与起始日期；税率、计税方法及业务适用性须以合同、发票和纳税申报资料核验。",
        "status": "NEEDS_REVIEW",
    },
    {
        "policy_id": "POL-CIT-RD-2023-07",
        "title": "财政部 税务总局关于进一步完善研发费用税前加计扣除政策的公告",
        "document_number": "财政部 税务总局公告2023年第7号",
        "issuer": "财政部 税务总局",
        "publish_date": "2023-03-26",
        "effective_date": "2023-01-01",
        "expiry_date": "",
        "amendment_status": "CURRENT_FOR_CASE_PERIOD",
        "article": "第一至三条",
        "applicable_taxpayer": "开展符合条件研发活动的企业（资格待核）",
        "applicable_business": "研发活动及研发支出",
        "source_url": "https://www.mof.gov.cn/jrttts/202303/t20230328_3875460.htm",
        "case_period_applicable": "True",
        "notes": "时间适用性已核验；年报研发费用不等于可加计扣除研发费用，项目、辅助账和申报资料均为 TODO_MISSING_DATA。",
        "status": "VERIFIED",
    },
    {
        "policy_id": "POL-CIT-RD-2023-11",
        "title": "国家税务总局 财政部关于优化预缴申报享受研发费用加计扣除政策有关事项的公告",
        "document_number": "国家税务总局 财政部公告2023年第11号",
        "issuer": "国家税务总局 财政部",
        "publish_date": "2023-06-21",
        "effective_date": "2023-01-01",
        "expiry_date": "",
        "amendment_status": "CURRENT_FOR_CASE_PERIOD",
        "article": "第一至四条",
        "applicable_taxpayer": "能准确归集核算研发费用的企业（资格待核）",
        "applicable_business": "研发费用加计扣除预缴及留存备查",
        "source_url": "https://fgk.chinatax.gov.cn/zcfgk/c100012/c5209840/content.html",
        "case_period_applicable": "True",
        "notes": "时间适用性已核验；是否享受、具体申报和留存资料均为 TODO_MISSING_DATA。",
        "status": "VERIFIED",
    },
    {
        "policy_id": "POL-CIT-GOV-2011-70",
        "title": "财政部 国家税务总局关于专项用途财政性资金企业所得税处理问题的通知",
        "document_number": "财税〔2011〕70号",
        "issuer": "财政部 国家税务总局",
        "publish_date": "2011-09-07",
        "effective_date": "2011-01-01",
        "expiry_date": "",
        "amendment_status": "FULLY_EFFECTIVE_ON_OFFICIAL_SOURCE",
        "article": "第一至四条",
        "applicable_taxpayer": "取得专项用途财政性资金且满足全部条件的企业（资格待核）",
        "applicable_business": "财政性资金、专项用途、单独核算",
        "source_url": "https://guangdong.chinatax.gov.cn/gdsw/zjfg/2011-09/20/content_c466c018611d42a1ae91f65a9be88a3c.shtml",
        "case_period_applicable": "",
        "notes": "官方来源标注全文有效；年报政府补助不等于不征税收入，拨付文件、管理要求和单独核算均为 TODO_MISSING_DATA。",
        "status": "VERIFIED",
    },
    {
        "policy_id": "POL-STAMP-2022-14",
        "title": "国家税务总局关于实施《中华人民共和国印花税法》等有关事项的公告",
        "document_number": "国家税务总局公告2022年第14号",
        "issuer": "国家税务总局",
        "publish_date": "2022-06-28",
        "effective_date": "2022-07-01",
        "expiry_date": "",
        "amendment_status": "FULLY_EFFECTIVE_ON_OFFICIAL_SOURCE",
        "article": "第一条及印花税征收管理和纳税服务事项",
        "applicable_taxpayer": "书立印花税应税合同、产权转移书据或营业账簿的纳税人（事实待核）",
        "applicable_business": "应税凭证管理及申报",
        "source_url": "https://fgk.chinatax.gov.cn/zcfgk/c100012/c5196761/content.html",
        "case_period_applicable": "",
        "notes": "官方来源标注全文有效；年报不披露逐份合同及印花税申报，相关合同和申报资料均为 TODO_MISSING_DATA，不能据此推定印花税风险。",
        "status": "VERIFIED",
    },
)
