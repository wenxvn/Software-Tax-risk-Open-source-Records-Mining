# Official Policy and Data Channels

检索顺序应优先使用以下官方来源。每次下载都要记录 URL、访问日期、原始文件、文本提取文件、文号、生效/失效日期和适用范围。

| 渠道 | URL | 可用于 | 备注 |
|---|---|---|---|
| 国家税务总局 | https://www.chinatax.gov.cn/ | 税收法律法规、公告、解读 | 最终税法依据优先 |
| 12366 纳税服务平台 | https://12366.chinatax.gov.cn/ | 口径和办税问答 | 需区分答复与正式规范性文件 |
| 财政部 | https://www.mof.gov.cn/ | 会计准则、税费政策 | 核对原文和生效日期 |
| 中国政府网 | https://www.gov.cn/ | 行政法规、国务院文件 | 保存原文 |
| 地方税务机关 | https://guangdong.chinatax.gov.cn/ | 地方执行口径、稽查公告 | 按案例所在地替换省份 |
| 国家统计局 | https://www.stats.gov.cn/ | 行业增加值、收入、成本等统计 | 不把单一指标当企业阈值 |
| 国家企业信用信息公示系统 | https://www.gsxt.gov.cn/ | 企业登记、年报、公示信息 | 需记录查询时间和主体 |
| 巨潮资讯 | https://www.cninfo.com.cn/ | 深市/部分跨市场上市公司公告、年报 | 公开上市公司主入口 |
| 上海证券交易所 | https://www.sse.com.cn/ | 沪市公司公告、年报和 XBRL | 以 PDF 报告为准 |
| 深圳证券交易所 | https://www.szse.cn/ | 深市公司公告、年报 | 以原始披露为准 |
| 全国股转系统 | https://www.neeq.com.cn/ | 新三板挂牌公司公告 | 备选样本来源 |
| 中国裁判文书网 | https://wenshu.court.gov.cn/ | 已公开裁判文书 | 仅作事实线索，核对文书原文 |

## 资料保存规则

政策和公告不可只保存 URL。原始 PDF/HTML 进入 `sources/policies/raw/` 或 `sources/curated/open_data/`，提取文本进入对应 `text/`，元数据进入索引。来源受限或无法下载时标记 `POLICY_UNVERIFIED`，不要用转载文章替代。

